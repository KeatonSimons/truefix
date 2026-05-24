# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state: pre-code

TrueFix is a planned open-source macOS app to surgically remove browser hijackers (Any Search Manager, Search Marquis, Trovi, etc.). **No Swift code exists yet** — `src/` is a placeholder README describing the intended layout. There is nothing to build, lint, test, or run. A Swift/macOS developer collaborator has not yet been recruited; that recruitment is the gating Week-1 task (`docs/NEXT-STEPS.md`, `recruiting/PITCHES.md`).

What does exist and is actively maintained:

- **`rules/*.yaml`** — detection rule packs (the project's unique value). One file per hijacker family. `any-search-manager.yaml` is the canonical, real-world-confirmed example; `search-marquis.yaml` is a stub.
- **`docs/`** — `V1-SPEC.md` (full product + technical spec), `KICKOFF.md` (project anchor doc, read first), `NEXT-STEPS.md` (checklist).
- **`recruiting/PITCHES.md`** — copy-paste pitches in different lengths for different channels.

Read `docs/KICKOFF.md` before doing substantive work — it has a "If you're Claude in a future session" section listing the most useful tasks in priority order.

## Working with the rule pack YAML

Rule packs are **security-critical**. A false positive deletes legitimate user data. The contribution bar is intentionally high — see `rules/README.md` for the full schema and standards. Key rules when authoring or editing a rule pack:

- Never add patterns that could match legitimate files (no `*.zip`, no `~/Downloads/*`). Only specific known-bad extension IDs and paths.
- Every signal needs a plain-language `description` — the UI shows it to end users at cleanup time.
- Every new extension ID needs at least one independent reference (vendor write-up, security blog, public forum thread). Self-citations are not acceptable.
- One file per family, even if two families share IDs. Use `also_known_as` for aliases.
- A new rule pack PR is supposed to get two-maintainer review and confirmation that persistence paths don't overlap legitimate files.

If asked to research and seed a new rule pack, propose the YAML as a draft and explicitly flag every claim that still needs corroboration (TODO comments are fine — the stub `search-marquis.yaml` shows the pattern).

## Architecture (planned, for context when discussing code)

When the Swift code does land, the V1 spec (`docs/V1-SPEC.md` §5) commits to this shape:

- **Main app**: Swift 5.10+ / SwiftUI, minimum macOS 13, no third-party runtime dependencies (Apple frameworks only — keeps the binary small and the supply-chain attack surface near zero).
- **Privileged XPC helper** installed via `SMAppService` (the same pattern Little Snitch / Hand Mirror use). The helper does only the specific filesystem and `defaults` operations the user has approved in the UI. No shelling out to `sudo`.
- **Scan engine** loads YAML from `Resources/rules/` (bundled from this repo's `rules/`) into per-kind detectors: chrome-policy, filesystem, configuration-profile, launch-agent.
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

The default branch is `main`. Feature branches follow `claude/<topic>-<suffix>`. Commits in history so far are short, imperative-mood, one-line ("Create V1-SPEC.md", "Add GitHub handle for any-search-manager curator") — match that style. No CI is configured yet.
