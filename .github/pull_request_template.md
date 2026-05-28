<!--
Thanks for contributing. Fill in what's relevant; delete what's not.

For rule pack PRs, please ensure your YAML follows the schema in rules/README.md
and meets the contribution standards in rules/RULES_CONTRIBUTING.md. PRs that
don't meet the rule pack bar will be sent back for revision — false positives
in a security tool cause data loss, so we're deliberately strict.
-->

## What this PR does

<!-- One paragraph. What changed and why. -->

## Type of change

- [ ] New rule pack (new hijacker family detection)
- [ ] Rule pack update (added IDs, paths, or references to an existing family)
- [ ] Bug fix (Swift code, app behavior)
- [ ] New feature (Swift code, app behavior)
- [ ] Documentation
- [ ] Build / CI / tooling
- [ ] Other (explain below)

## Checklist for rule pack PRs

<!-- Only fill in if this is a rule pack PR -->

- [ ] The YAML validates against the schema in `rules/README.md`
- [ ] At least one independent reference is cited (vendor write-up, security blog, forum thread, or documented cleanup)
- [ ] Persistence paths are from real-world observation, not speculation
- [ ] Each `description` field is plain language (users will read these in the UI)
- [ ] False-positive risk has been considered — the rule pack only matches on known-bad IDs or specific paths, never on heuristics
- [ ] Extension IDs include a `confirmed:` date and `source:` note in `extension_ids`
- [ ] The `maintenance.last_reviewed` date has been set
- [ ] If this is a STUB (incomplete), the file is clearly marked and not enabled in production builds

## Checklist for code PRs

<!-- Only fill in if this is a Swift code PR -->

- [ ] Build succeeds with no new warnings
- [ ] Unit tests added / updated where appropriate
- [ ] Integration test exists for new detection or cleanup behavior
- [ ] No new third-party dependencies added (see V1 spec §5)
- [ ] Privileged helper changes (if any) are minimal and reviewed for least-privilege

## Reviewer notes

<!-- Anything reviewers should know — known limitations, follow-ups, related issues. -->

## Linked issues

<!-- Closes #123, Refs #456, etc. -->
