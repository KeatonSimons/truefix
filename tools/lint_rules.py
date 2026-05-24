#!/usr/bin/env python3
"""Validate TrueFix rule packs.

Runs JSON Schema validation against rules/schema.json and then a set of
security-critical custom checks that JSON Schema can't easily express:

  - Filename matches family.id
  - Chrome extension IDs are 32 lowercase a-p chars
  - No `match.paths` entry uses a dangerously broad glob without a content gate
  - No extension ID is shared across rule pack files without an explicit alias
  - Every ID listed in `extension_ids` shows up somewhere in a signal
  - `maintenance.last_reviewed` is not absurdly old (warning only)

Stubs (top-level `status: stub`) are validated against a relaxed schema and
skipped for most custom checks — but their `status` keeps them out of any
"shippable" tally.

Usage:
    python tools/lint_rules.py rules/
    python tools/lint_rules.py rules/any-search-manager.yaml

Exit codes:
    0  all packs valid
    1  one or more errors
    2  invocation error
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator

EXTENSION_ID_RE = re.compile(r"^[a-p]{32}$")
STALE_REVIEW_DAYS = 365

FORBIDDEN_PATH_PREFIXES: tuple[str, ...] = (
    "~/Downloads",
    "~/Desktop",
    "~/Documents",
    "~/Movies",
    "~/Music",
    "~/Pictures",
    "/Users/",
    "/System",
    "/usr",
    "/bin",
    "/sbin",
    "/etc",
)

FORBIDDEN_BARE_GLOBS: tuple[str, ...] = (
    "*.zip",
    "*.dmg",
    "*.pkg",
    "*.app",
)


class LintError(Exception):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise LintError(f"{path}: top-level YAML must be a mapping")
    return data


def coerce_dates_to_strings(value: Any) -> Any:
    """JSON Schema sees ISO dates as strings, but PyYAML decodes them as
    datetime.date. Walk the structure and stringify dates so the schema check
    behaves the same as a YAML written with quoted dates."""
    if isinstance(value, dict):
        return {k: coerce_dates_to_strings(v) for k, v in value.items()}
    if isinstance(value, list):
        return [coerce_dates_to_strings(v) for v in value]
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    return value


def load_schema(schema_path: Path) -> dict[str, Any]:
    with schema_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def relax_schema_for_stub(schema: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of the schema with stub-friendly relaxations.

    Stubs are placeholders that explicitly must not ship. We still want them
    to parse and have the right shape, but empty arrays and short descriptions
    and null review dates are acceptable.
    """
    relaxed = json.loads(json.dumps(schema))
    props = relaxed["properties"]
    props["signals"]["minItems"] = 0
    props["verification"]["minItems"] = 0
    props["extension_ids"]["minItems"] = 0
    relaxed["required"] = [
        r for r in relaxed["required"] if r != "verification"
    ]
    defs = relaxed["$defs"]
    defs["family"]["properties"]["description"]["minLength"] = 1
    defs["family"]["properties"]["references"]["minItems"] = 0
    defs["family"]["properties"]["references"]["items"]["properties"]["url"]["minLength"] = 0
    defs["signal"]["properties"]["description"]["minLength"] = 1
    defs["signal"]["properties"]["match"]["minProperties"] = 0
    defs["signal"]["properties"]["remove"]["required"] = ["action"]
    defs["maintenance"]["required"] = ["curated_by"]
    defs["maintenance"]["properties"]["curated_by"]["minItems"] = 0
    defs["maintenance"]["properties"]["last_reviewed"] = {
        "oneOf": [{"$ref": "#/$defs/iso_date"}, {"type": "null"}]
    }
    return relaxed


def iter_path_strings(match_block: Any) -> Iterable[str]:
    if not isinstance(match_block, dict):
        return
    for key in ("paths", "path"):
        value = match_block.get(key)
        if isinstance(value, str):
            yield value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    yield item


def has_content_gate(match_block: dict[str, Any]) -> bool:
    """True if a `match` block restricts a broad path glob by content."""
    if not isinstance(match_block, dict):
        return False
    content_keys = (
        "plist_contents_contains",
        "file_contents_contains",
        "extension_ids",
    )
    for key in content_keys:
        value = match_block.get(key)
        if isinstance(value, list) and value:
            return True
        if isinstance(value, str) and value:
            return True
    return False


def is_specific_extension_id_in_path(path: str) -> bool:
    """A path is considered specific enough if any segment is a 32-char ext ID."""
    for segment in re.split(r"[/\\]", path):
        if EXTENSION_ID_RE.match(segment):
            return True
    return False


def check_path_safety(
    rule_path: Path, signal_id: str, match_block: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    paths = list(iter_path_strings(match_block))
    if not paths:
        return errors

    gated = has_content_gate(match_block)
    for p in paths:
        # Forbidden roots — these match too much legitimate data.
        for bad_prefix in FORBIDDEN_PATH_PREFIXES:
            if p == bad_prefix or p.startswith(bad_prefix + "/"):
                errors.append(
                    f"{rule_path}: signal '{signal_id}' uses forbidden path root "
                    f"'{bad_prefix}' in '{p}'. See rules/README.md 'Don'ts'."
                )

        final = p.rsplit("/", 1)[-1]
        if final in FORBIDDEN_BARE_GLOBS:
            errors.append(
                f"{rule_path}: signal '{signal_id}' uses a bare-glob final "
                f"component '{final}' in '{p}'. Extension-only globs match "
                "legitimate files."
            )

        # Trailing '*' / '**' is OK iff a content gate (e.g.
        # plist_contents_contains) is also present, OR a specific extension ID
        # appears earlier in the path, OR a more-specific glob ('Profile *')
        # is used mid-path.
        if (
            (p.endswith("/*") or p.endswith("/**"))
            and not gated
            and not is_specific_extension_id_in_path(p)
        ):
            errors.append(
                f"{rule_path}: signal '{signal_id}' has open-ended glob '{p}' "
                "without a content gate (plist_contents_contains / "
                "file_contents_contains) or a specific extension ID. This "
                "would match legitimate files."
            )
    return errors


def check_extension_id_format(
    rule_path: Path, pack: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    for entry in pack.get("extension_ids", []) or []:
        ext_id = entry.get("id") if isinstance(entry, dict) else None
        if isinstance(ext_id, str) and not EXTENSION_ID_RE.match(ext_id):
            errors.append(
                f"{rule_path}: extension_ids contains '{ext_id}' which is not "
                "a valid Chrome extension ID (32 chars, lowercase a-p)."
            )
    for signal in pack.get("signals", []) or []:
        match = signal.get("match", {}) if isinstance(signal, dict) else {}
        ids = match.get("extension_ids") if isinstance(match, dict) else None
        if isinstance(ids, list):
            for ext_id in ids:
                if isinstance(ext_id, str) and not EXTENSION_ID_RE.match(ext_id):
                    errors.append(
                        f"{rule_path}: signal '{signal.get('id')}' references "
                        f"invalid extension ID '{ext_id}'."
                    )
    return errors


def check_filename_matches_family_id(
    rule_path: Path, pack: dict[str, Any]
) -> list[str]:
    family_id = (pack.get("family") or {}).get("id")
    if not isinstance(family_id, str):
        return []
    expected = f"{family_id}.yaml"
    if rule_path.name != expected:
        return [
            f"{rule_path}: filename does not match family.id "
            f"(expected '{expected}', got '{rule_path.name}')."
        ]
    return []


def check_extension_ids_referenced(
    rule_path: Path, pack: dict[str, Any]
) -> list[str]:
    """Every declared extension ID should appear in at least one signal."""
    declared: set[str] = set()
    for entry in pack.get("extension_ids", []) or []:
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            declared.add(entry["id"])

    if not declared:
        return []

    referenced: set[str] = set()
    for signal in pack.get("signals", []) or []:
        if not isinstance(signal, dict):
            continue
        match = signal.get("match", {})
        if isinstance(match, dict):
            ids = match.get("extension_ids")
            if isinstance(ids, list):
                for v in ids:
                    if isinstance(v, str):
                        referenced.add(v)
            for p in iter_path_strings(match):
                for seg in re.split(r"[/\\]", p):
                    if EXTENSION_ID_RE.match(seg):
                        referenced.add(seg)

    orphans = declared - referenced
    if orphans:
        return [
            f"{rule_path}: extension_ids declared but not referenced in any "
            f"signal: {sorted(orphans)}"
        ]
    return []


def check_last_reviewed_freshness(
    rule_path: Path, pack: dict[str, Any]
) -> list[str]:
    """Warning, not error — return a string prefixed 'warn:'."""
    maint = pack.get("maintenance") or {}
    reviewed = maint.get("last_reviewed")
    if isinstance(reviewed, dt.date):
        last = reviewed
    elif isinstance(reviewed, str):
        try:
            last = dt.date.fromisoformat(reviewed)
        except ValueError:
            return []
    else:
        return []
    age = (dt.date.today() - last).days
    if age > STALE_REVIEW_DAYS:
        return [
            f"warn: {rule_path}: maintenance.last_reviewed is {age} days old "
            f"(>{STALE_REVIEW_DAYS}). Re-confirm signals against current sources."
        ]
    return []


def check_cross_pack_id_collisions(
    packs: list[tuple[Path, dict[str, Any]]],
) -> list[str]:
    """Same extension ID listed in multiple packs without an alias relationship."""
    owners: dict[str, list[Path]] = defaultdict(list)
    for path, pack in packs:
        for entry in pack.get("extension_ids", []) or []:
            if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                owners[entry["id"]].append(path)

    aka: dict[str, set[str]] = {}
    for path, pack in packs:
        fam = pack.get("family") or {}
        fam_id = fam.get("id")
        also = fam.get("also_known_as") or []
        if isinstance(fam_id, str):
            aka.setdefault(fam_id, set()).update(
                a for a in also if isinstance(a, str)
            )

    errors: list[str] = []
    for ext_id, paths in owners.items():
        if len(paths) > 1:
            errors.append(
                f"warn: extension ID '{ext_id}' is declared in multiple "
                f"rule packs: {[str(p) for p in paths]}. Confirm these are "
                "true aliases (use family.also_known_as) and not a "
                "mis-attribution."
            )
    return errors


def lint_file(
    path: Path,
    schema: dict[str, Any],
    relaxed: dict[str, Any],
) -> tuple[list[str], list[str], dict[str, Any] | None]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        pack = load_yaml(path)
    except (yaml.YAMLError, LintError) as e:
        return [f"{path}: failed to parse YAML: {e}"], [], None

    status = pack.get("status", "active")
    chosen_schema = relaxed if status == "stub" else schema
    validator = Draft202012Validator(chosen_schema)
    for err in sorted(validator.iter_errors(coerce_dates_to_strings(pack)), key=lambda e: e.path):
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        errors.append(f"{path}: schema [{loc}]: {err.message}")

    errors.extend(check_filename_matches_family_id(path, pack))
    errors.extend(check_extension_id_format(path, pack))

    if status != "stub":
        for signal in pack.get("signals", []) or []:
            if not isinstance(signal, dict):
                continue
            sig_id = signal.get("id", "<unknown>")
            errors.extend(check_path_safety(path, sig_id, signal.get("match", {})))
        warnings.extend(check_extension_ids_referenced(path, pack))
        warnings.extend(check_last_reviewed_freshness(path, pack))

    return errors, warnings, pack


def collect_targets(args: list[str]) -> list[Path]:
    targets: list[Path] = []
    for raw in args:
        p = Path(raw)
        if p.is_dir():
            targets.extend(sorted(p.glob("*.yaml")))
        elif p.is_file():
            targets.append(p)
        else:
            raise LintError(f"not a file or directory: {raw}")
    return targets


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="+",
        help="Rule pack YAML files or directories containing them",
    )
    parser.add_argument(
        "--schema",
        default=str(Path(__file__).resolve().parent.parent / "rules" / "schema.json"),
        help="Path to schema.json (default: rules/schema.json)",
    )
    ns = parser.parse_args(argv)

    schema = load_schema(Path(ns.schema))
    relaxed = relax_schema_for_stub(schema)

    try:
        targets = collect_targets(ns.paths)
    except LintError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    all_warnings: list[str] = []
    packs: list[tuple[Path, dict[str, Any]]] = []

    for path in targets:
        if path.name == "schema.json":
            continue
        errors, warnings, pack = lint_file(path, schema, relaxed)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
        if pack is not None and pack.get("status") != "stub":
            packs.append((path, pack))

    all_warnings.extend(check_cross_pack_id_collisions(packs))

    for w in all_warnings:
        print(w)
    for e in all_errors:
        print(f"error: {e}", file=sys.stderr)

    if all_errors:
        print(
            f"\n{len(all_errors)} error(s), {len(all_warnings)} warning(s) "
            f"across {len(targets)} file(s).",
            file=sys.stderr,
        )
        return 1
    print(
        f"OK: {len(targets)} file(s) validated, {len(all_warnings)} warning(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
