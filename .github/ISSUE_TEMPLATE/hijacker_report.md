---
name: Hijacker family report
about: Tell us about a hijacker we don't yet detect — even if you only have partial info
title: "[Hijacker] "
labels: hijacker-research
assignees: ''
---

## Family identification

- **Common name(s) you've seen this called:**
- **What domain does it route searches to?**
- **What browser(s) was it affecting?** Chrome / Safari / Firefox / other

## What you observed

<!-- The symptoms. What did the user see that made you think "this is a hijacker"? -->

## What persistence mechanism did you find (if any)

<!-- Tick what you found, and add detail in the next section: -->

- [ ] Chrome `ExtensionInstallForcelist` policy (in a plist somewhere)
- [ ] Root-owned extension folder in `~/Library/Application Support/Google/Chrome/Profile */Extensions/`
- [ ] macOS Configuration Profile (in System Settings → Profiles)
- [ ] LaunchAgent under `~/Library/LaunchAgents/`
- [ ] LaunchAgent / LaunchDaemon under `/Library/LaunchAgents/` or `/Library/LaunchDaemons/`
- [ ] Helper application in `/Applications/` or `~/Applications/`
- [ ] Something else (describe below)
- [ ] Not sure — looking for help identifying

## Specifics (paths, IDs, etc.)

<!-- If you found any of the above, paste exact paths, extension IDs, plist contents, or bundle IDs. Even partial info is useful. -->

```
paste here
```

## How you cleaned it (or attempted to)

<!-- The actual commands you ran, or the steps you took. This is the most valuable section for us — a documented cleanup transcript is what lets us build a reliable rule pack. -->

## References

<!-- Links to vendor write-ups, forum threads, or other public sources documenting this family. -->

-

## What you'd like from us

- [ ] Help identifying the family
- [ ] A rule pack written for this family (we'll do it, you've given us the data)
- [ ] Just reporting — feel free to use as you see fit

---

Thank you. Hijacker reports are the most valuable contribution to TrueFix short of writing code. We'll credit you in the rule pack's `maintenance.curated_by` field unless you tell us not to.
