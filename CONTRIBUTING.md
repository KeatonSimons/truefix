# Contributing to TrueFix

Thanks for considering it. TrueFix only exists if people contribute — there's no funding behind it, no company. Here's how to help.

---

## The biggest current need: a Swift/macOS developer collaborator

The spec is written. The first detection rule is in place. What's missing is the Swift code that ties it all together.

**If you've ever wanted to ship a clean, narrowly-scoped open-source Mac tool with your name on it — one that actually fixes a problem millions of users have — this is that project.**

You'd own:
- The Swift / SwiftUI app shell
- The privileged XPC helper (the `SMAppService` pattern, like Little Snitch / Hand Mirror)
- The detection engine that consumes the YAML rule packs in `rules/`

The non-technical project lead handles:
- Product direction, scope, decisions
- Recruiting, community, comms
- Rule pack curation and PR review
- Launch and outreach

Time commitment: ~3–4 months part-time to V1. No equity, no money — it's MIT-licensed open source. But: a clean public project to point at, ownership of a piece of macOS security tooling that gets actually used, and a low-drama collaborator on the non-code side.

**To start the conversation:** open an issue titled "Interested in collaborating — [your name]" with a few lines about your background and any questions on the spec. Or email the project lead directly (see the [README](README.md) — TODO: add maintainer contact once filled in).

We'll send you the full V1 spec, set up a 30-minute call, and go from there. Bring sharp questions about the architecture.

---

## Other ways to help (no Swift required)

### Submit a new rule pack

Rule packs are YAML files in `rules/` that describe a hijacker family — its extension IDs, the URLs it redirects to, the files it drops, where it persists. Each rule pack is independent. Adding a new one teaches TrueFix to detect a new family.

See [`rules/README.md`](rules/README.md) for the schema and contribution standards. The bar is high — rule packs are what make TrueFix trustworthy. False positives in a security tool are catastrophic, so each new rule pack needs:

- At least one independent reference (security blog post, vendor write-up, public forum thread)
- A real-world example of the file paths and IDs (not just "I think it does this")
- A clear family description in plain language

### Report a hijacker we don't cover yet

If you've cleaned a Mac of something TrueFix doesn't detect — even just manually, before TrueFix shipped — open an issue with what you found. Don't worry about formatting. The maintainers will help turn it into a rule pack.

### Test on real-world infected Macs

Once V1 ships, the most useful thing you can do is run TrueFix on Macs you know are infected and report what it catches and what it misses. We need a community of contributors who can confirm detection across hijacker variants in the wild.

### Translation

V1 is English-only. Localization opens up for V2. If you're a native speaker of Spanish, French, German, Japanese, Chinese, or another widely-spoken language, watch the issue queue — there'll be a localization sprint after V1 launch.

---

## Code of Conduct

By participating you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Be kind, assume good faith, and check your tone before posting.

## Security

If you find a vulnerability — not a bug, a *vulnerability* (e.g. TrueFix could be tricked into running arbitrary code as root, or a rule pack could exfiltrate data) — please follow the disclosure process in [SECURITY.md](SECURITY.md) instead of opening a public issue.
