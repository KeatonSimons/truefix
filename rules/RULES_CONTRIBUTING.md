# Contributing Rule Packs to TrueFix

This document is the canonical contribution standard for new rule packs. The general [CONTRIBUTING.md](../CONTRIBUTING.md) covers everything else.

Rule packs are the project's unique value and they're security-critical. A false positive in a rule pack causes data loss for users. **The bar is intentionally high.**

---

## The short version

To add a new family or improve an existing rule pack:

1. **Bring real-world data.** A cleanup transcript, not a guess.
2. **Cite at least one independent reference.** Two is better.
3. **Use the schema in [`README.md`](README.md).** Each signal needs a plain-language `description`.
4. **Mark uncertainty.** TODOs are fine. Fake-but-plausible content is not.
5. **Open a PR using the [rule pack PR template](../.github/pull_request_template.md).**

---

## What "real-world data" means

The strictest test of a rule pack is: would it work on the next infected Mac without false-positive damage to legitimate files?

That requires data sourced from one of these:

1. **A documented cleanup transcript** — you cleaned a real Mac and recorded what was where. This is the gold standard. The TrueFix `rules/any-search-manager.yaml` rule pack is built from one (the 2026-05-23 transcript that motivated the project).

2. **A vendor write-up with specific paths and IDs** — Malwarebytes, Trend Micro, Kaspersky, MacSecurity, PCRisk often publish removal guides with concrete extension IDs, plist paths, and bundle identifiers. These are useful as corroboration but rarely sufficient on their own because vendor coverage lags real variants.

3. **A forum thread or blog post by a person who cleaned the family** — useful as a starting point, but treat with skepticism. People misidentify families, and the same family can present differently across variants.

**Not acceptable as sole evidence:**

- Generic "this hijacker exists" mentions in news articles
- Antivirus marketing pages
- A single Reddit post with no specific paths
- "I think I had this once"

---

## Schema requirements per signal

Every detection signal in a rule pack must have:

- A clear `kind`: `chrome-policy` | `filesystem` | `configuration-profile` | `launch-agent`
- A plain-language `description` (users will see this in the UI)
- A `match` block specific to the kind
- A `remove` block specifying the cleanup action, root requirement, and `surgical: true` if the action removes only part of a container (e.g. one ID from a list, not the whole list)

Optional but recommended:

- `precedence: first` for signals that must run before others (LaunchAgents that re-install other components)
- Per-family false-positive notes (see the Yahoo Redirector stub for an example of explicit FP warnings)

---

## What the review process looks like

Each rule pack PR is reviewed by at least two maintainers. The review will:

1. **Verify references are reachable** and confirm the claims you made
2. **Spot-check persistence paths** against public reports
3. **Look for false-positive risk** — does any path or pattern in the rule pack risk matching legitimate files?
4. **Test the rule pack** against a real or VM-staged infection if possible

A PR will be rejected if any of:

- A persistence path could match legitimate (non-hijacker) files
- An extension ID is shared with a known-good extension
- A description is unclear, misleading, or written in jargon
- References are dead links or self-citations (e.g. citing only your own forum post)
- The rule pack would change browser settings the user might legitimately want (see the Yahoo Redirector example: don't change Yahoo to another search engine, just remove the affiliate parameters)

A PR will be accepted with edits if:

- The schema is correct and the references are solid
- Some fields are TODO but the file is clearly marked as a stub
- The signal coverage is partial but the partial part is correct

---

## What to do if you have data but not skills

If you've cleaned a Mac of something we don't yet detect, but you don't want to write a rule pack yourself, **open a [Hijacker Family Report](../.github/ISSUE_TEMPLATE/hijacker_report.md)** with what you found. We will write the rule pack and credit you in `maintenance.curated_by` unless you tell us not to.

This is the most valuable contribution to TrueFix short of writing Swift code. Don't underestimate it.

---

## Stubs are explicitly welcome

Several rule packs in `rules/` are stubs — they document the family for contributors but aren't enabled in the production build until verified data fills in the TODOs. If you're contributing a stub, that's fine; please:

- Mark it clearly as `STUB` in the file header comment
- Set `maintenance.last_reviewed: null` (signal it's not ready to ship)
- Make every TODO explicit so the next contributor knows what to research

Search Marquis, Trovi, Safe Finder, Search Baron, Yahoo Redirector Variants, and Search Pulse are all currently stubs. Picking one up and turning it into a shipping rule pack is a high-impact contribution.

---

## Credit

Rule pack contributors are listed in:

- `maintenance.curated_by` in the rule pack YAML itself (with their GitHub handle)
- The eventual release notes
- The eventual contributors section of the README

Credit can be declined — set `curated_by: ["anonymous"]` or open the PR from a single-purpose throwaway account if you prefer.

---

*This document last revised: 2026-05-28. Open an issue if you think a standard here needs to change.*
