# TrueFix

*The Mac browser-hijacker remover that actually fixes the problem.*

TrueFix is an open-source macOS app that finds and removes browser hijackers — Any Search Manager, Search Marquis, Trovi, and other adware-class search redirectors — without touching anything else on your Mac.

No accounts. No telemetry by default. No paid tier. No upsells. MIT-licensed.

> ⚠️ **Project status: pre-release.** Spec is written and the first detection rule is in place. We're looking for a Swift/macOS developer collaborator to build the app. See [CONTRIBUTING.md](CONTRIBUTING.md) if you'd like to help.

---

## Why TrueFix exists

If your Chrome's default search engine has been hijacked by something like `search.anysearchmanager.com` or `searchmarquis.com`, and the usual fixes haven't worked, you've probably tried:

- Removing the hijacker extension from `chrome://extensions` (blocked — it's marked "managed by your organization")
- Resetting Chrome settings (the hijacker comes back on restart)
- Deleting the Configuration Profile in System Settings (it was never there)
- Running Malwarebytes (it missed the actual persistence)
- Running AdwareCleaner (it "cleaned" by wiping all your cookies and extensions)

None of those actually fixed it. The actual problem is usually one or more of:

1. A **macOS Configuration Profile** that locks the setting (sometimes)
2. A **system-wide Chrome policy file** at `/Library/Preferences/com.google.Chrome.plist` with an `ExtensionInstallForcelist` entry that re-installs the hijacker on every launch (often missed by other tools)
3. A **root-owned extension folder** in `~/Library/Application Support/Google/Chrome/Profile 1/Extensions/` that you can't delete with normal permissions

TrueFix checks all three, plus several related persistence mechanisms, and removes only the bits that belong to known hijackers — with a preview of every action before it happens.

## Why not just use [other tool]?

| Tool | Why TrueFix is different |
|---|---|
| Malwarebytes for Mac | Better-known, but missed the system-wide plist mechanism in real-world testing. Requires download + account flow. |
| AdwareCleaner | "Cleans" by wiping all browser cookies and extensions — destroys your legitimate data alongside the hijacker. |
| CleanMyMac, MacKeeper, etc. | Bloated "do everything" tools with FUD-heavy marketing and unclear ethics. |
| The Configuration Profiles panel in System Settings | Apple's recommended path catches only one of several persistence mechanisms. |

TrueFix is **one knife, sharpened**.

## How it works

1. **Scan** — checks Chrome's active policies, Configuration Profiles, extension folders, LaunchAgents and LaunchDaemons against the open-source rule packs in `rules/`.
2. **Show** — every finding is displayed with a plain-language explanation of what it is and where it lives. Nothing is removed without your explicit OK.
3. **Fix it** — uses macOS's native admin-password dialog (via Authorization Services / XPC) to remove the specific bad keys and files. Logs everything.
4. **Verify** — re-scans automatically to confirm.

## What TrueFix will *never* do

- Send any data anywhere by default
- Modify settings outside its known-bad rules
- Wipe your cookies or your legitimate extensions
- Run in the background
- Ask you to create an account
- Try to sell you anything

## Installation *(once V1 ships)*

- **Direct download:** signed + notarized DMG from [Releases](../../releases)
- **Homebrew:** `brew install --cask truefix`

## How to contribute

Right now the project needs, in priority order:

1. **A Swift/macOS developer collaborator** — primary need. See [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue introducing yourself.
2. **New rule packs** — research a new hijacker family, document its extension IDs and persistence paths, submit a YAML rule pack PR. Format documented in [`rules/README.md`](rules/README.md).
3. **Hijacker references** — even just a link to a forum thread or blog post documenting a new hijacker family is useful. Open an issue.
4. **Translation** — V1 ships English-only; localization is on the V2 roadmap. Translators can subscribe to the issue queue.

## Roadmap

- **V1** *(in development)*: Chrome hijacker scanner + remover. Known families: Any Search Manager, Search Marquis, Trovi, Conduit, Safe Finder, Bing.vc redirector, Yahoo redirector variants.
- **V2**: Safari support, additional hijacker families, localization.
- **V3**: General macOS PUP scanner — still narrowly scoped.

## License

MIT. See [LICENSE](LICENSE).

## Maintainers

*(To be filled in once the team is assembled.)*

---

*TrueFix is not affiliated with Google, Apple, or any of the hijacker vendors it detects. Trademarks belong to their respective owners.*
