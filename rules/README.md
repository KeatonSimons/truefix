# TrueFix Rule Packs

Each YAML file in this folder describes one **hijacker family** that TrueFix can detect and clean. Rule packs are the project's unique value — they're what makes TrueFix surgical instead of scorched-earth.

This document explains the schema and the contribution standards.

---

## File naming

One file per family, kebab-case, lowercase:

```
rules/any-search-manager.yaml
rules/search-marquis.yaml
rules/trovi.yaml
```

If a family has well-known aliases, list them in `also_known_as` inside the file rather than creating duplicate files.

## Schema (version 1)

A rule pack has five top-level sections:

1. `family` — metadata about the hijacker family (display name, description, references)
2. `signals` — independent detection rules; each one can match and trigger cleanup
3. `verification` — checks run after cleanup to confirm the fix
4. `extension_ids` — full list of known Chrome extension IDs in this family
5. `maintenance` — curator info and review date

See [`any-search-manager.yaml`](any-search-manager.yaml) as the canonical example.

### `signals` — the heart of a rule pack

A signal has four parts:

```yaml
- id: short-kebab-case-id
  kind: one-of: chrome-policy | filesystem | configuration-profile | launch-agent
  description: >
    Plain-language explanation. The UI will show this to the user when this
    signal matches — make it readable.
  match:
    # Kind-specific fields describing what to look for.
  remove:
    action: defaults-delete-key | remove-directory | remove-profile | unload-and-remove-plist
    surgical: true   # if true, remove only matching entries within a container
    requires_root: true | false
    precedence: first   # optional; some signals must run before others
```

Signal kinds:

| Kind | What it matches | Typical `remove` action |
|---|---|---|
| `chrome-policy` | A key in a Chrome plist (system or user) referencing a hijacker extension ID | `defaults-delete-key` |
| `filesystem` | One or more file paths existing (glob-supported) | `remove-directory` or `remove-file` |
| `configuration-profile` | A macOS Configuration Profile with a hijacker-targeting payload | `remove-profile` |
| `launch-agent` | A LaunchAgent or LaunchDaemon referencing a hijacker | `unload-and-remove-plist` |

### `verification`

Each check has a `description` (shown to the user) and a `check` type. TrueFix runs all verification checks automatically after cleanup. If any check fails, the user is shown what's still wrong and offered options.

---

## Contribution standards

Rule packs are security-critical. A false positive in a rule pack causes data loss for users. **The bar is intentionally high.**

### Required for every new rule pack

1. **At least one independent reference.** A vendor write-up, a security blog post, a public forum thread, or a documented real-world cleanup. Self-published claims with no corroboration are not acceptable.
2. **Real-world confirmation of each persistence path.** Don't list a path you "think" the hijacker uses — list the ones you've actually observed.
3. **Confirmation date for each extension ID.** When was this ID last observed in the wild? Older confirmations should be re-verified periodically.
4. **A `description` field on every signal** written in plain language. Not jargon. Real users read these when TrueFix shows them what it found.

### Recommended

- Multiple references when possible — two or more independent sources is much more trustworthy than one
- Notes on whether the family has known *non-hijacker* uses of the same extension IDs (extremely rare for adware, but worth flagging if so)
- A `last_reviewed` date in `maintenance` so contributors can see when the rule pack was last verified

### How review works

Each rule pack PR is reviewed by at least two maintainers. Reviewers will:

1. Check that references are reachable and confirm the claims
2. Spot-check the persistence paths against public reports
3. Reject the PR if any of:
   - A persistence path could match legitimate (non-hijacker) files
   - An extension ID is shared with a known-good extension
   - The description is unclear or misleading
   - References are dead links or self-citations

### Don'ts

- ❌ Don't add patterns like `*.zip` or `~/Downloads/*` — anything that could match legitimate files. TrueFix only removes things that match a *specific* known-bad ID or path.
- ❌ Don't add a rule pack for a family you've only read about secondhand without checking primary sources.
- ❌ Don't combine multiple families into one file because they "feel similar." One file per family, even if two families share extension IDs.

---

## TODO: schema features not yet implemented

These are planned for schema v2 but not in v1:

- Time-based signal weighting (a recently-observed extension ID is more trustworthy than one not seen in 3+ years)
- Cross-family precedence (some hijackers can re-install each other; the engine should know to clean them in a specific order)
- Localization of `description` fields
- Auto-update endpoint for rule packs (community-contributed YAML pulled from `main` after a release tag)

If you want to help design the v2 schema, open an issue.
