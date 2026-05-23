# TrueFix — V1 Project Spec

A focused, open-source macOS tool that detects and removes browser hijackers — surgically, transparently, and without wiping the user's legitimate data.

---

## 1. Why this exists

### The problem

Browser hijackers — Any Search Manager, Search Marquis, Trovi, Conduit, Bing Redirector, and dozens of variants — affect millions of Mac users. They're not technically "malware" in the criminal sense, but they:

- Hijack the default search engine to route searches through their own ad-monetized pages
- Inject sponsored results, redirects, and tracking
- Persist via macOS Configuration Profiles, system-wide Chrome policy files, and root-owned extension folders
- Cannot be removed from `chrome://extensions` because they use `ExtensionInstallForcelist` policy
- Often install during a "free download" of a fake media player, PDF tool, or codec, when the installer asks for admin password

The cleanup we just did on this Mac is illustrative. The infection had been there for **2.5 years**. The user knew something was wrong but the standard advice (remove the extension, delete the Configuration Profile) didn't apply because the persistence was system-wide, not user-level. The actual fix required:

1. Running `chrome://policy` to find the offending policy
2. Knowing that `Source: Platform` + empty user defaults + empty `/Library/Managed Preferences/` meant we had to check the system-wide plist at `/Library/Preferences/com.google.Chrome.plist`
3. Using `sudo grep` to locate the file
4. Using `sudo defaults delete` to surgically remove the bad key
5. Using `sudo rm -rf` to delete root-owned extension files
6. Restarting Chrome and verifying via `chrome://policy`

That is far beyond what a non-technical user can do, and far beyond what existing consumer tools handle correctly.

### Why existing tools fail

| Tool | Why it falls short |
|---|---|
| **Malwarebytes for Mac (free scanner)** | Solid product but missed the system-wide plist source in our test case; requires download, account flow, and brand trust we can underprice on simplicity. |
| **AdwareCleaner / similar PocketBits tools** | "Cleans" by wiping all cookies + all extensions — destroys legitimate data along with the hijacker. Plus shows upsell prompts for sibling products. |
| **CleanMyMac, MacKeeper, Disk Doctor, etc.** | Bloated "do everything" cleaners with histories of FUD-marketing and unclear ethics. Audience overlap with the *cause* of the problem. |
| **macOS Configuration Profiles UI** | The Apple-recommended cleanup path, but only catches the user-facing Profile mechanism — not the system-wide plist persistence we saw here. |
| **Removing the Chrome extension** | Blocked by the `ExtensionInstallForcelist` policy. UI doesn't even show a Remove button. |

The gap: nothing surgical, transparent, free, open-source, and trustworthy.

---

## 2. Vision

**TrueFix is the Linus's-knife of Mac browser cleanup.** One thing, done extremely well, with no upsells, no telemetry, no accounts, and code anyone can read.

Three design principles, in priority order:

1. **Transparency.** Every file TrueFix touches is shown to the user *before* it's touched, with plain-language explanation. Every action is logged. Every detection rule is open source and human-readable.
2. **Surgical precision.** Never wipe cookies, never disable legitimate extensions, never modify settings the user wouldn't recognize as malicious. When in doubt, don't act — ask.
3. **Trust through openness.** Source code on GitHub from day one. Reproducible builds. Signed releases. No tracking. No data leaving the user's Mac, ever.

---

## 3. V1 Scope

### In scope

- **Detection** of browser hijackers in Chrome, scoped to known families: Any Search Manager, Search Marquis, Search Pulse, Trovi, Conduit, Safe Finder, Bing.vc redirector, Yahoo redirector variants.
- **Cleanup** of:
  - Chrome `ExtensionInstallForcelist` policy entries that reference known hijacker extension IDs (both user and system scope)
  - Hijacker extension folders in `~/Library/Application Support/Google/Chrome/Profile */Extensions/`
  - macOS Configuration Profiles that target Chrome and inject known hijacker IDs
  - LaunchAgents / LaunchDaemons that reference known hijacker IDs
- **Verification step** after cleanup, automated re-scan to confirm.
- **Detailed report** the user can save (and that we collect anonymized aggregate stats from *only if user opts in*).

### Explicitly out of scope for V1

- Safari, Firefox, Edge, Brave, Arc support (V2)
- Real-time protection / background monitoring (might never be in scope — see "Anti-goals")
- General Mac cleanup (disk space, login items, "junk files," etc.) — that's a different product
- Anything for Windows or Linux
- Anything that requires a kernel extension or system extension
- Anything that needs to be a paid product

### Anti-goals

These are things we will deliberately **not** do, even if they'd technically work:

- **No "premium" tier or upsells.** The free version is the only version.
- **No telemetry without explicit opt-in.** And even opt-in data is anonymized, aggregate, and never includes file contents.
- **No background daemon.** TrueFix runs when the user launches it. Then it quits.
- **No "real-time protection" claims.** That's a misleading sales tactic from the bad cleaner ecosystem.
- **No CLI-tool-only release for V1.** A GUI is required because the non-technical users who need this most won't open a terminal.

---

## 4. User Experience

### First-launch flow

1. User downloads `TrueFix.dmg` from GitHub Releases or `truefix.app` website.
2. Drags to Applications. macOS Gatekeeper prompt: "This app is signed and notarized by [developer]. Open?" — user clicks Open.
3. App opens. Single-window, single-button UI: **"Scan my Mac"**.
4. Scan takes 5-15 seconds. Shows a progress indicator with the current step ("Checking Chrome policies… Checking Configuration Profiles… Checking extension folders…").

### Results screen

If clean:

> **No browser hijackers detected.**
> Last scan: just now. Chrome policy state: clean. Extension folders: clean. Configuration Profiles: clean.

If something found:

> **Found 3 issues. None of them have been touched yet — review before cleaning.**
>
> 1. **Forced extension policy** in `/Library/Preferences/com.google.Chrome.plist`
>    *Forces Chrome to install extension `gbinpomjmgglfdeadepbdmpcbjibgjea`, which belongs to the "Any Search Manager" hijacker family.*
>    → [Show me the exact policy] [Remove this key]
>
> 2. **Root-owned extension folder** at `~/Library/Application Support/Google/Chrome/Profile 1/Extensions/gbinpomjmgglfdeadepbdmpcbjibgjea`
>    *Created Dec 1, 2023. Owned by root, which means an installer was given admin password to drop these files. This is the extension's actual code.*
>    → [Show me what's in this folder] [Remove this folder]
>
> 3. **Configuration Profile** "AdminPrefs"
>    *Not present on your Mac. Skipping.*
>
> [Remove all 2 items above] [Remove items I selected] [Cancel]

For each action requiring `sudo`, TrueFix uses the Authorization Services framework to request admin password via a native macOS dialog (not a custom prompt, not the terminal). User sees Apple's standard "TrueFix wants to make changes" dialog. Password is never seen by the app.

After cleanup, automatic re-scan + verification screen:

> **Cleanup complete. Re-scan confirms: no remaining issues.**
> Chrome will need to be restarted to apply changes. [Quit & relaunch Chrome] [I'll do it myself]
>
> [Save report as PDF] [Done]

### What TrueFix never does without confirmation

- Delete anything in `~/Library` it doesn't have a specific rule for
- Modify any Chrome setting not in the rule pack
- Touch any extension not in the hijacker ID list
- Touch any LaunchAgent/Daemon not referencing a known hijacker
- Make a network request to anywhere other than the optional rule-pack update endpoint (and only if the user has opted into rule updates)

---

## 5. Technical Approach

### Language & framework

- **Swift 5.10+ / SwiftUI** for the app. Native macOS. Minimum macOS 13 (Ventura) — covers ~95% of active Macs and avoids legacy AppKit complications.
- **No third-party runtime dependencies.** Just Apple frameworks. Reduces supply-chain risk, simplifies signing/notarization, makes the binary small (~5MB).

### Architecture

```
TrueFix.app
├── UI layer (SwiftUI)
├── Scan engine
│   ├── Rule loader (reads rules/*.yaml)
│   ├── Detectors
│   │   ├── ChromePolicyDetector
│   │   ├── ExtensionFolderDetector
│   │   ├── ConfigProfileDetector
│   │   └── LaunchAgentDetector
│   └── Reporter
├── Cleanup engine
│   ├── PrivilegedHelper (XPC service, runs as root via SMJobBless / SMAppService)
│   └── Action handlers (delete plist key, remove folder, etc.)
└── Resources/
    └── rules/  (bundled YAML rule packs)
```

### Privilege escalation

Use Apple's recommended pattern: a **privileged helper tool** installed via `SMAppService` (macOS 13+). The main app communicates with the helper via XPC. The helper does only the specific filesystem and `defaults` operations the user has approved.

This is the same pattern used by legitimate apps like Little Snitch and Hand Mirror. It's more work than shell-ing out to `sudo`, but it's the right macOS-native approach and contributes to trust.

### Detection rules

Stored as YAML files in `Resources/rules/`, one file per hijacker family. Example:

```yaml
# rules/any-search-manager.yaml
family: any-search-manager
display_name: "Any Search Manager"
description: |
  Chrome hijacker that redirects searches to anysearchmanager.com.
  Typically installed via fake media player or PDF tool installers.
extension_ids:
  - gbinpomjmgglfdeadepbdmpcbjibgjea
  - "<other ids in family>"
url_patterns:
  - "search.anysearchmanager.com"
  - "anysearchmanager.com"
file_signatures:
  - path: "~/Library/Application Support/Google/Chrome/Profile *"
    extension_dir_glob: "Extensions/<extension_id>"
references:
  - https://www.malwarebytes.com/blog/detections/pup-optional-anysearchmanager
  - https://www.bleepingcomputer.com/...
```

Community contributors can submit pull requests adding new rule files. We curate and review.

### Distribution

- **Primary:** Signed + notarized DMG on GitHub Releases. Download from `truefix.app` or directly from GitHub.
- **Secondary:** Homebrew Cask formula (for the technical audience who lives in `brew`). One-line install: `brew install --cask truefix`.
- **Not on Mac App Store.** The sandboxed nature of App Store apps makes the required privilege escalation infeasible.

### Code signing & notarization

- Apple Developer Program enrollment: $99/year.
- All releases signed with the developer cert and submitted to Apple's notarization service. This is what makes the Gatekeeper "open" prompt show only once instead of warning users it can't be verified.

### License

**MIT License.** Most permissive, encourages adoption, doesn't scare off commercial users who might want to contribute or fork.

The rule packs are also MIT, but governed by a small `RULES_CONTRIBUTING.md` doc that explains the curation standards.

---

## 6. Trust Strategy

The hardest problem in this category. Here's how we build trust faster than the brand-name incumbents:

1. **Source open from day one.** Public GitHub repo before V1 ships. People who care can read the code. People who don't can know that people who do care, can.
2. **Reproducible builds.** Document the exact build environment and Swift toolchain version so anyone can verify the released binary matches the source.
3. **Sigstore / cosign release signatures.** In addition to Apple's notarization, sign release artifacts with sigstore so the chain of trust extends beyond just "we paid Apple $99."
4. **No accounts, no email collection, no telemetry by default.** "What does TrueFix send over the network?" → "Nothing, unless you check the box to receive rule updates, in which case it makes one HTTPS request to fetch the public rules.json from our CDN."
5. **Public maintainer identity.** A real person's name and face on the website and on commits. Anonymity is fine for some open-source projects but in security tooling it's a trust drag.
6. **Independent security review.** Once V1 is functional, get someone like Patrick Wardle (Objective-See) to look at the code. A blog post mentioning TrueFix from a trusted Mac-security figure is worth more than any marketing.
7. **In-app transparency.** Every action TrueFix takes is shown to the user first. The user can also export the full scan + action log as a text file.

---

## 7. Roadmap

### Phase 0: Foundation (Weeks 1–4)
- Pick a final name; register `<name>.app` domain and GitHub org
- Write README, CONTRIBUTING, CODE_OF_CONDUCT, LICENSE
- Find a Swift/macOS developer collaborator (see "Recruiting" below)
- Set up Apple Developer account
- Sketch wireframes for the UI

### Phase 1: CLI prototype (Weeks 4–8)
- Pure Swift command-line tool that performs the scan and prints findings
- Implement Any Search Manager + Search Marquis detection rules
- No cleanup actions yet — read-only
- Used internally to validate detection logic against known-infected machines

### Phase 2: Cleanup + privileged helper (Weeks 8–12)
- Add `PrivilegedHelper` XPC service for sudo operations
- Implement cleanup actions for the families V1 supports
- Dry-run mode (default for first release)
- Logging + report export

### Phase 3: SwiftUI app shell (Weeks 12–16)
- Wrap the CLI engine in a native app UI
- Polish, accessibility, dark mode, signed/notarized release
- Public beta on GitHub

### Phase 4: V1 launch (Week 16)
- Announce on Hacker News, r/MacOS, r/privacy, Mac-focused YouTube channels
- Reach out to Objective-See / The Eclectic Light Company / MacRumors for coverage
- Open issues for V2 feature requests

### V2 candidates (post-launch)
- Safari extension hijackers + Safari search-engine reset
- Firefox/Edge support
- Additional hijacker families (community-contributed rule packs)
- Localization (Spanish, French, German, Japanese, Chinese — large affected populations)
- Optional: scheduled re-scan reminder (user-initiated, not background daemon)

---

## 8. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| False positive deletes a legitimate file | Medium | Catastrophic | Conservative rule curation; dry-run-by-default; user confirmation per item; never delete based on heuristics, only on known IDs/paths |
| Bad actor submits a malicious rule pack PR | Medium | High | Two-maintainer review requirement; rule pack signing; community vetting of contributors |
| Apple developer account revoked | Low | High | Maintain backup signing identity; document unsigned-build install path as fallback |
| macOS update breaks privileged helper pattern | Medium | Medium | Use `SMAppService` (Apple's current recommended path); monitor each macOS beta; budget time for compatibility fixes |
| TrueFix mistaken for a scam by users skeptical of "Mac cleaners" | High | Medium | Open source from day 1; signed/notarized; identifiable maintainers; minimal UI; never ask for money; clear in-app transparency |
| Audience acquisition is hard | High | High (kills usefulness) | Partner with Objective-See, MacRumors, security-focused YouTubers for launch; SEO-targeted content ("how to remove Any Search Manager Mac" already has search volume); Homebrew listing reaches the technical audience |
| Project loses a sole maintainer | Medium | High | Build community early; document everything; aim for ≥2 active maintainers before V1 ship |

---

## 9. What it would take to ship V1

### People
- **You** (Keaton): project lead, product decisions, community building, comms.
- **1 Swift/macOS developer collaborator.** This is the critical hire/partner. See Recruiting below.
- **Optional**: a designer for the UI polish phase (commissionable on a one-off basis, $500-2000 for a clean V1 design).

### Money
- $99/year Apple Developer Program
- ~$15/year domain (`.app` is ~$15-20)
- ~$0 for GitHub (free for open source)
- ~$0 for Homebrew (free)
- ~$0 for hosting the rule-update endpoint (Cloudflare Pages free tier handles this easily)
- ~$0–500 for a designer if desired
- **Total**: under $200 to start, under $1000 even with a designer

### Time
- ~3-4 months part-time for the developer collaborator from spec → V1 launch
- ~5-10 hours/week from you on community, comms, rule curation, decisions

### Recruiting a developer
A few paths to find a collaborator:

1. **r/swift, r/macprogramming, r/MacOSBeta** — post the spec and a clear ask. Open-source security tools attract the right kind of dev.
2. **GitHub Issues on related projects** — find contributors to Objective-See's tools, Hand Mirror, Little Snitch ecosystem things, etc., and reach out personally.
3. **Hacker News "Who's hiring / Who wants to be hired" threads** — monthly threads, sometimes get high-quality applicants.
4. **Cold-email known Mac security devs** — Patrick Wardle, Csaba Fitzl, Howard Oakley. Worst case they decline; best case they introduce you to someone.
5. **Indie Hackers, IndieHackers slack, Tiny Project communities** — these have devs looking for meaningful side projects.

The pitch you'd give is: "I have a project spec for an open-source Mac browser-hijacker remover. Looking for a Swift/macOS dev who wants to ship something useful with their name on it. No equity, no money — but real impact and a clean GitHub project to point to."

---

## 10. Naming

The project is named **TrueFix**. (Lowercase `truefix` for filenames and the domain `truefix.app`.) The positioning is direct: every other tool in this category — CleanMyMac, MacKeeper, AdwareCleaner, the bundled "Mac cleaner" upsells — claims to fix browser hijackers, and either fails (misses the persistence mechanisms) or "succeeds" by wiping all your data. TrueFix is the one that actually does it.

**Domain:** `truefix.app` (to be registered).
**Backup name** if the domain or GitHub org is unavailable: **Truefix** (single-word variant of the same positioning).

The original brainstorm of alternatives is preserved here for reference: HijackRemover (too 2008), Plistwatch (too techy), Untether (too abstract), Cleanwise / OpenSweep / Janitor (all crowded or awkward). None held up against TrueFix's clean self-aware positioning.

---

## 11. Immediate Next Steps

If you want to actually start, here's the ordered list:

1. **This week**:
   - [ ] Decide if you want to move forward (no-pressure decision; could also just be "fun thought exercise, file it away")
   - [ ] If yes: pick a working name, register the domain, create the GitHub org
   - [ ] Open the new Cowork project and drop this spec in as the anchor doc

2. **Weeks 1-2**:
   - [ ] Write a one-paragraph "Looking for a collaborator" pitch
   - [ ] Post in r/swift and 1-2 other places
   - [ ] Reply to any interested devs; pick one to start working with
   - [ ] Set up Apple Developer account

3. **Weeks 3-4**:
   - [ ] You + dev: refine this spec into a kickoff doc you both agree on
   - [ ] Dev: scaffolds the Swift project, writes the first rule parser, picks ANY ONE hijacker family to implement detection for end-to-end
   - [ ] You: start collecting hijacker references / sources to seed the rule database

4. **Months 2-3**:
   - [ ] Build out the detection + cleanup engine
   - [ ] Build the GUI
   - [ ] Internal alpha testing on real infected machines

5. **Month 4**:
   - [ ] Public beta on GitHub
   - [ ] Outreach for coverage
   - [ ] V1 launch

---

## 12. Open questions to resolve later

These don't block starting, but should be decided before V1:

- Should TrueFix offer to install the **Malwarebytes Browser Guard** extension during cleanup, as a complementary preventive measure? (Pros: helps users; Cons: dependency on Malwarebytes ecosystem)
- Should the rule pack auto-update from the GitHub repo, or only update with new app releases? (Auto-update = faster reaction to new threats; new-release-only = less moving parts, less attack surface)
- Should we publish anonymized aggregate detection statistics ("TrueFix cleaned 14,302 Macs of Any Search Manager last month")? Could be powerful for awareness, but adds an opt-in telemetry path.
- Do we want a logo? When? Who designs it?

---

*End of V1 spec. Comments, questions, and edits welcome. The next document this needs is a kickoff doc once a developer collaborator is found.*
