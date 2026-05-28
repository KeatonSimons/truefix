# TrueFix Roadmap

Living document. Updated as scope or sequencing changes.

For week-by-week milestones see [NEXT-STEPS.md](NEXT-STEPS.md). This document is the longer-horizon view.

---

## Phase 0 — Foundation *(current)*

**Status:** in progress

- [x] Project spec written
- [x] First rule pack written from a real-world cleanup (Any Search Manager / Search Marquis)
- [x] Public GitHub repo with full scaffold
- [x] Reference docs (hijacker families directory)
- [x] Issue and PR templates
- [ ] Domain registered (`truefix.app` or fallback)
- [ ] Single-page public website
- [ ] Maintainer contact email
- [ ] Swift/macOS developer collaborator recruited
- [ ] Apple Developer Program enrollment

## Phase 1 — CLI prototype

**Goal:** A pure Swift command-line tool that performs the scan and prints findings. Read-only — no cleanup actions yet. Used internally to validate detection logic on real infected machines.

- [ ] Swift project scaffold (SwiftPM)
- [ ] YAML rule pack loader
- [ ] Detectors:
  - [ ] `ChromePolicyDetector`
  - [ ] `ExtensionFolderDetector`
  - [ ] `ConfigProfileDetector`
  - [ ] `LaunchAgentDetector`
- [ ] Reporter (plain-text output to stdout)
- [ ] Tested against the Any Search Manager rule pack on a real infected Mac

## Phase 2 — Cleanup engine + privileged helper

**Goal:** Add the ability to actually fix what was detected. Privileged helper via `SMAppService`. Dry-run mode is the default for the first release.

- [ ] Privileged XPC helper tool (via `SMAppService`)
- [ ] Action handlers:
  - [ ] `DefaultsDeleteKey` (surgical plist key removal)
  - [ ] `RemoveDirectory` (with root if needed)
  - [ ] `RemoveProfile` (Configuration Profile)
  - [ ] `UnloadAndRemovePlist` (LaunchAgent / LaunchDaemon)
- [ ] Dry-run mode (default for first release)
- [ ] Full action logging + report export

## Phase 3 — SwiftUI app shell

**Goal:** Wrap the CLI engine in a native macOS app with the single-window scan/review/clean flow described in the spec.

- [ ] SwiftUI app shell
- [ ] Scan progress UI
- [ ] Results screen with per-item review
- [ ] Native macOS admin-password dialog (via Authorization Services)
- [ ] Verification re-scan + report-save UI
- [ ] Accessibility pass (VoiceOver, keyboard nav)
- [ ] Dark mode support

## Phase 4 — V1 launch

**Goal:** Public, signed, notarized release. Available via DMG download from GitHub Releases AND Homebrew Cask.

- [ ] Code signing + notarization
- [ ] DMG packaging
- [ ] Homebrew Cask formula submitted
- [ ] Release blog post / launch comms
- [ ] Outreach for coverage (Patrick Wardle, Howard Oakley, MacRumors)
- [ ] Public beta period (2 weeks minimum) before v1.0.0 tag

---

## V2 candidates (post-launch)

In rough priority order. None of these block V1.

- **Safari support.** Hijackers that target Safari's search-engine settings, Safari extensions, and Safari profiles. Safari is the most-used Mac browser; not covering it limits TrueFix's audience significantly.
- **AdLoad / Genieo / Safe Finder rule pack.** Highest-priority family in the rule pack queue — see [HIJACKER-FAMILIES.md](HIJACKER-FAMILIES.md). Likely V1.5 if a contributor brings a clean transcript.
- **Firefox and Edge support.** Lower priority — smaller affected populations on Mac.
- **Brave and Arc support.** Both are Chromium-based and may largely work with the existing Chrome rules; needs testing.
- **Localization.** English-only at V1; Spanish, French, German, Japanese, Chinese open up after launch.
- **Optional scheduled re-scan reminder.** User-initiated, not a background daemon. Explicitly not real-time protection.

## V3 candidates

Speculative, but the directional intent:

- **General macOS PUP (potentially unwanted program) scanner.** Still narrowly scoped — would target adware-class apps and bundled installers, not general anti-malware territory.
- **Browser-extension threat database integration.** Public lookup against the Chrome Web Store / Add-ons stats to surface "this extension you have was reported as malicious by N other users."

---

## Anti-roadmap

Things that look like they should be on the roadmap but deliberately aren't:

- **No real-time / background daemon.** TrueFix runs when launched and quits. This is a design commitment, not a phasing decision — see spec §3 Anti-goals.
- **No paid tier, ever.** Not on any roadmap.
- **No Windows / Linux port.** Out of scope. The whole positioning is Mac-native.
- **No AI-powered anything in the marketing.** The appeal of this tool is that it's small, focused, and transparent — AI buzzwords work against trust here.

---

*Roadmap last revised: 2026-05-28. Open an issue if you think something needs to move.*
