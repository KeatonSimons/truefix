# TrueFix — Cowork Project Kickoff

**This document orients a Claude session on what TrueFix is and where things stand. If you're a fresh session and you've been pointed here, read this first.**

---

## What TrueFix is

An open-source macOS app that detects and removes browser hijackers (Any Search Manager, Search Marquis, Trovi, and related families) — surgically, transparently, and without wiping the user's legitimate data. MIT-licensed, no telemetry, no paid tier.

**One-liner:** *"The Mac browser-hijacker remover that respects you."*

The full V1 spec is in `V1-SPEC.md`. Read that for the deep details.

## Why it exists

On May 23, 2026, Keaton (the project lead) discovered his Chrome had been hijacked by Any Search Manager. We spent ~90 minutes diagnosing and removing it. The infection had been there for 2.5 years because:

- The standard cleanup advice (delete the Configuration Profile) didn't apply — the persistence was in a *system-wide* Chrome plist instead
- The hijacker extension folder was owned by root, so normal `rm` failed
- Existing consumer tools either missed it (Malwarebytes for Mac scanner) or used scorched-earth methods (AdwareCleaner wipes all cookies + extensions)

The cleanup process was:
1. `chrome://policy` revealed the offending `ExtensionInstallForcelist` policy
2. `sudo grep` located `/Library/Preferences/com.google.Chrome.plist` as the source
3. `sudo defaults delete /Library/Preferences/com.google.Chrome ExtensionInstallForcelist` removed the policy key
4. `sudo rm -rf` removed the root-owned extension folder

That whole workflow is automatable. That's TrueFix.

## Project lead

**Keaton** — non-technical, project vision/lead/community. Will recruit a Swift/macOS developer collaborator (not yet found at the time this doc was written).

## Current status

**Phase 0: Foundation, Week 0.** Spec written. No code yet. No name finalized ("TrueFix" is a working title). No developer recruited yet. No GitHub org. No domain.

## Decisions already made

- **License:** MIT
- **Distribution:** Open source on GitHub. Signed + notarized DMG on GitHub Releases. Also Homebrew Cask. **Not** Mac App Store (sandbox restrictions prevent the needed privilege escalation).
- **Language/framework:** Swift + SwiftUI, native macOS, min macOS 13
- **Architecture:** Main app + privileged XPC helper (via `SMAppService`), YAML-based detection rule packs
- **Anti-goals:** No telemetry by default, no upsells, no paid tier, no background daemon, no real-time protection
- **Trust strategy:** Source open from day 1, reproducible builds, identifiable maintainers, in-app transparency for every action

## Decisions still pending

- Final name and domain
- Who the developer collaborator will be
- Designer for UI polish (later phase)
- Whether the rule pack auto-updates or only updates with app releases
- Whether to publish anonymized aggregate detection stats

## What the immediate next action is

**Recruit one Swift/macOS developer.** Everything else builds on that. The pitch text is in `../recruiting/PITCHES.md`. Channels to post in: r/swift, IndieHackers, Hacker News "Who wants to be hired" monthly thread, GitHub Issues on related open-source projects, cold email to known Mac-security developers.

## If you're Claude in a future session

Useful things to do for Keaton, in rough order of likely value:

1. **Help refine the recruiting pitch** based on which channel he's posting to
2. **Research candidate developers** — look at recent contributors to Objective-See, Hand Mirror, Little Snitch ecosystem, etc.
3. **Workshop the name** — search domain availability, suggest alternatives, narrow it down
4. **Draft outreach emails** to specific named devs Keaton wants to contact
5. **When a developer is recruited**, help write the kickoff doc that aligns both of them on the spec
6. **Maintain the next-steps checklist** in `NEXT-STEPS.md` — mark items done, add new ones as they emerge
7. **Curate the initial hijacker rule pack** — research known hijacker extension IDs from MalwareBazaar, security blogs, Reddit threads. Compile into the YAML format the spec describes.

Keaton is non-technical, so when you propose work, propose it in plain language. When code is involved, write it for him (and the eventual dev collaborator).

Be a steady executive function for this project. Keaton has the vision and drive; you provide structure, follow-through, and depth.

## Files in this project

- `../START-HERE.md` — orientation for new Cowork sessions
- `KICKOFF.md` — **(this file)** anchor doc
- `V1-SPEC.md` — the full V1 product spec
- `../README.md` — draft GitHub README
- `../recruiting/PITCHES.md` — copy-paste text for finding a developer
- `NEXT-STEPS.md` — actionable checklist
