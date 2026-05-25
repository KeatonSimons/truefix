# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state: pre-code (rule packs + tooling only)

TrueFix is a planned open-source macOS app to surgically remove browser hijackers (Any Search Manager, Search Marquis, Trovi, etc.). **No Swift code exists yet** — `src/` is a placeholder README describing the intended layout. A Swift/macOS developer collaborator has not yet been recruited; that recruitment is the gating Week-1 task (`docs/NEXT-STEPS.md`, `recruiting/PITCHES.md`).

What does exist and is actively maintained:

- **`rules/*.yaml`** — detection rule packs (the project's unique value). One file per hijacker family. `any-search-manager.yaml` is the canonical, real-world-confirmed example; `search-marquis.yaml` is a stub.
- **`rules/schema.json`** — JSON Schema (draft 2020-12) the rule packs validate against.
- **`tools/lint_rules.py`** — Python linter (schema + security-critical custom checks) that runs in CI on every PR touching `rules/` or the linter itself.
- **`docs/`** — `V1-SPEC.md` (full product + technical spec), `KICKOFF.md` (project anchor doc, read first), `NEXT-STEPS.md` (checklist).
- **`recruiting/PITCHES.md`** — copy-paste pitches in different lengths for different channels.

Read `docs/KICKOFF.md` before doing substantive work — it has a "If you're Claude in a future session" section listing the most useful tasks in priority order.

## Commands

The only build/test/lint tooling that exists today is the rule-pack linter.

```sh
# Install (Python 3.12 in CI; should work on 3.10+)
pip install -r tools/requirements.txt

# Lint every rule pack
python tools/lint_rules.py rules/

# Lint a single file
python tools/lint_rules.py rules/any-search-manager.yaml
```

Exit codes: `0` clean, `1` lint errors, `2` invocation error. Warnings (cross-pack ID collisions, stale `last_reviewed` >365 days, orphan IDs declared but never referenced in a signal) print to stdout and do not fail the build. Errors print to stderr. CI is wired up at `.github/workflows/lint-rules.yml` and triggers on changes to `rules/**`, `tools/lint_rules.py`, or `tools/requirements.txt`. There is no Swift build, no test suite, no formatter.

## Working with the rule pack YAML

Rule packs are **security-critical**. A false positive deletes legitimate user data. The contribution bar is intentionally high — see `rules/README.md` for the full prose schema, `rules/schema.json` for the machine-readable version. Key rules when authoring or editing a rule pack:

- Never add patterns that could match legitimate files. The linter hard-rejects:
  - Forbidden path roots: `~/Downloads`, `~/Desktop`, `~/Documents`, `~/Movies`, `~/Music`, `~/Pictures`, `/Users/`, `/System`, `/usr`, `/bin`, `/sbin`, `/etc`.
  - Bare-extension final-segment globs: `*.zip`, `*.dmg`, `*.pkg`, `*.app`.
  - Open-ended trailing `/*` or `/**` unless either a specific 32-char extension ID appears as a path segment OR the `match` block has a content gate (`plist_contents_contains`, `file_contents_contains`, or `extension_ids`). See `check_path_safety` in `tools/lint_rules.py`.
- Every signal needs a plain-language `description` (≥20 chars per schema) — the UI shows it to end users at cleanup time.
- Chrome extension IDs are 32 lowercase `a-p` chars (validated by both schema and linter).
- Filename must equal `<family.id>.yaml`.
- Every new extension ID needs at least one independent reference (vendor write-up, security blog, public forum thread). Self-citations are not acceptable.
- One file per family even if two families share IDs; use `family.also_known_as` for aliases. Cross-pack ID collisions trigger a warning, not an error — fix by either consolidating or confirming via `also_known_as` that they're true aliases.
- New rule pack PRs are supposed to get two-maintainer review confirming persistence paths don't overlap legitimate files.

**Stubs.** A pack with top-level `status: stub` (see `rules/search-marquis.yaml`) is a placeholder that must not ship. The linter validates stubs against a relaxed schema (empty `signals`/`verification`/`extension_ids` allowed, `last_reviewed: null` allowed) and skips path-safety and reference checks. Don't graduate a stub to active without filling in every TODO and running the full lint.

If asked to research and seed a new rule pack, propose the YAML as a draft and explicitly flag every claim that still needs corroboration (TODO comments are fine — the stub `search-marquis.yaml` shows the pattern).

## Architecture (planned, for context when discussing code)

When the Swift code does land, the V1 spec (`docs/V1-SPEC.md` §5) commits to this shape:

- **Main app**: Swift 5.10+ / SwiftUI, minimum macOS 13, no third-party runtime dependencies (Apple frameworks only — keeps the binary small and the supply-chain attack surface near zero).
- **Privileged XPC helper** installed via `SMAppService` (the same pattern Little Snitch / Hand Mirror use). The helper does only the specific filesystem and `defaults` operations the user has approved in the UI. No shelling out to `sudo`.
- **Scan engine** loads YAML from `Resources/rules/` (bundled from this repo's `rules/`) into per-kind detectors — one detector per `signal.kind` value: `chrome-policy`, `filesystem`, `configuration-profile`, `launch-agent`. The set of `remove.action` values the helper must implement is fixed by the schema: `defaults-delete-key`, `remove-directory`, `remove-file`, `remove-profile`, `unload-and-remove-plist`.
- **Distribution**: signed + notarized DMG on GitHub Releases plus Homebrew Cask. **Not** Mac App Store — the sandbox prevents the required privilege escalation.

Suggestions that would violate these commitments (Electron, third-party deps, sandbox-incompatible patterns, shelling to `sudo` instead of XPC, supporting macOS < 13) should be flagged, not silently accommodated.

## Non-negotiable product constraints

These are anti-goals from the spec — flag any suggestion that crosses them:

- No telemetry without explicit opt-in (and even then: anonymized, aggregate, never file contents).
- No paid tier, no upsells, no accounts.
- No background daemon, no "real-time protection."
- Never wipe cookies or disable legitimate extensions to "clean" something. Surgical removal only, scoped to specific known-bad IDs/paths.
- Every action shown to the user before it happens, with plain-language explanation.

## Audience and tone

The project lead (Keaton) is non-technical. When proposing work or explaining tradeoffs, use plain language; when code is involved, write it for him and for the eventual developer collaborator to both review. Code-level pushback ("the spec says X but Y would be better because…") is welcome — rubber-stamping is not.

## Git workflow

The default branch is `main`. Feature branches follow `claude/<topic>-<suffix>`. Commits in history so far are short, imperative-mood, one-line ("Create V1-SPEC.md", "Add rule pack schema, linter, and CI workflow") — match that style.
