# Changelog

All notable changes to TrueFix are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html) once releases begin.

---

## [Unreleased]

### Added
- Reference doc `docs/HIJACKER-FAMILIES.md` covering Any Search Manager / Search Marquis, Search Baron, Trovi, Conduit, Safe Finder / Genieo / AdLoad, Bing.vc redirector, Yahoo redirector variants, and Search Pulse with sourced references.
- Stub rule packs for Trovi, Safe Finder / Genieo / AdLoad, Search Baron, Yahoo Redirector Variants, and Search Pulse — clearly marked as stubs pending verified data.
- Issue templates: bug report, feature request, hijacker family report.
- Pull request template with separate checklists for rule pack PRs and Swift code PRs.
- `docs/ROADMAP.md` — phase-by-phase plan from current state through V1, V2, V3 candidates.
- `docs/CHANGELOG.md` — this file.
- `rules/RULES_CONTRIBUTING.md` — dedicated contribution standards for rule packs (separate from general CONTRIBUTING.md).
- Single-page website draft in `website/` for eventual deployment to `truefix.app`.
- Targeted cold-email drafts for named Mac security developers (Patrick Wardle, Csaba Fitzl, Howard Oakley) in `recruiting/cold-emails/`.

### Changed
- (Nothing yet.)

### Pending
- Apple Developer Program enrollment
- Domain registration for `truefix.app`
- Maintainer contact email in `SECURITY.md` and `README.md`
- Swift / macOS developer collaborator recruitment

---

## [0.0.1] — 2026-05-28

Initial public scaffold.

### Added
- `README.md` with positioning, install plan, and contribution guide
- `LICENSE` (MIT)
- `CONTRIBUTING.md` leading with the Swift developer ask
- `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1, with a project-specific note about not making affected users feel stupid)
- `SECURITY.md` with vulnerability disclosure process
- `.gitignore` (Swift / Xcode / macOS standard)
- `docs/V1-SPEC.md` — full project spec, ~20KB
- `docs/KICKOFF.md` — orientation doc for fresh Cowork sessions
- `docs/NEXT-STEPS.md` — week-by-week checklist
- `recruiting/PITCHES.md` — copy-paste recruiting pitches for r/swift, Hacker News, IndieHackers, cold email
- `rules/README.md` — rule pack schema documentation and contribution standards
- `rules/any-search-manager.yaml` — first rule pack, sourced from a real-world Any Search Manager cleanup performed 2026-05-23
- `rules/search-marquis.yaml` — stub
- `src/README.md` — placeholder showing the planned Swift project layout

---

*Format note: this CHANGELOG starts at 0.0.1 (the scaffold release), with versioning following SemVer once code releases begin. Rule pack changes that don't touch app code are tracked here in the `[Unreleased]` section and rolled into the next code release's version notes.*
