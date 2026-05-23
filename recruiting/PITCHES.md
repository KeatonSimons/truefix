# TrueFix — Recruiting a Developer

The single hardest and most important Week-1 action is finding **one Swift/macOS developer collaborator** who wants to ship a meaningful open-source side project.

Below are ready-to-post pitches in different lengths, tuned for different channels. Pick the one that matches where you're posting, copy it, lightly personalize it, and post.

---

## Short version — Twitter / X / Mastodon (280 chars)

> Building an open-source Mac app: a surgical browser-hijacker remover (Any Search Manager, Search Marquis, etc.). Spec is done, MIT-licensed, no business model — just a tool that should exist. Looking for one Swift/macOS dev collaborator. DM me.

---

## Reddit version — r/swift, r/macprogramming, r/MacOSBeta

> **Looking for a Swift/macOS collaborator for an open-source side project**
>
> Hey r/swift — I'm looking for one developer to partner with on a small, focused open-source Mac app called TrueFix. It detects and removes browser hijackers (Any Search Manager, Search Marquis, that whole adware-class search-redirect family) surgically — without the scorched-earth approach the existing tools take.
>
> The story: I just spent 90 minutes diagnosing one of these on my own Mac. The infection had been there for 2.5 years because the standard cleanup tools missed the system-wide Chrome plist persistence (`/Library/Preferences/com.google.Chrome.plist` with an `ExtensionInstallForcelist` entry, plus a root-owned extension folder). Existing consumer tools either missed it or used a sledgehammer (wipe all cookies + extensions). There's a real gap in the market for something open source, transparent, and trustworthy.
>
> **What's done:**
> - Full V1 spec (~12 pages) covering UX, architecture, distribution, trust strategy, roadmap
> - MIT license decided, no monetization, no telemetry by default
> - Apple Developer account budgeted ($99/yr personal)
>
> **What I'm looking for:**
> - Swift + SwiftUI, comfortable with XPC and the `SMAppService` privileged-helper pattern
> - Wants their name on a tightly-scoped, well-built open-source project
> - ~3-4 months of part-time work to V1
> - No equity, no money (it's free open source) — just impact, a clean GitHub project to point at, and the satisfaction of fixing a thing that actually annoys lots of people
>
> I'm not a developer myself — I'd be doing product, community, recruiting, comms, rule curation. You'd own the code architecture.
>
> If this sounds interesting, DM me or reply here. I can share the full spec.

---

## Hacker News version — "Ask HN: Who wants to be hired?" monthly thread

> **Location:** Remote
> **Looking for:** Open-source collaboration, not employment
> **Tech:** Swift, SwiftUI, macOS native, XPC privileged helpers
>
> I'm a non-technical project lead looking for one Swift/macOS developer to partner with me on **TrueFix**, an open-source Mac app that detects and removes browser hijackers (Any Search Manager / Search Marquis / Trovi family) surgically — without the scorched-earth approach existing tools take. MIT license, no monetization, no telemetry, no business model. Just a sharp tool that should exist.
>
> Full V1 spec is written. Project owns its own GitHub org and Apple Developer account. ~3–4 months part-time to ship V1. You'd own the architecture and the code; I'd handle product, community, recruiting, rule curation, comms.
>
> If you've ever wanted to ship a clean, narrowly-scoped open-source tool with your name on it that actually fixes a problem millions of Mac users have: hello.
>
> **Contact:** [your email]

---

## IndieHackers / Tiny Projects communities

> **Want to ship something genuinely useful on the side?**
>
> Open-source Mac app, MIT-licensed, no monetization. TrueFix: a surgical browser-hijacker remover that fills a real gap (existing tools either miss the persistence mechanisms or use a sledgehammer that wipes all your data).
>
> I'm the non-technical project lead — bringing the spec (~12 pages, done), the budget for the Apple Developer account, and the time for community + recruiting + comms. Need one Swift/SwiftUI dev who wants their name on a clean, focused open-source project.
>
> Worth your evenings? Reach out and I'll share the spec.

---

## Cold-email template (for specific named developers)

Use this when you've found a developer through their GitHub profile, their blog, or contributions to Mac security projects.

> Subject: Open-source Mac project — would love your eyes (or your help)
>
> Hi [Name],
>
> I came across your work on [specific project / blog post / talk] and thought you might be the right person to ask about a small open-source Mac project I'm trying to start.
>
> It's called TrueFix — a surgical browser-hijacker remover for macOS (the Any Search Manager / Search Marquis family). I just spent 90 minutes manually cleaning one out of my own Mac after the standard tools missed the system-wide Chrome plist persistence, and it crystallized for me how big the gap is for a properly-built open-source tool in this space.
>
> I have a full V1 spec written (~12 pages: UX, architecture, distribution, trust strategy, roadmap). MIT-licensed, no monetization, no telemetry. The project needs one Swift/macOS developer collaborator — that's the bottleneck.
>
> Two asks, either of which would be a help:
>
> 1. **Are you interested in being that collaborator?** ~3–4 months part-time. I'd handle product, community, recruiting, rule curation, comms; you'd own the code and architecture.
>
> 2. **If not, would you skim the spec and point out anything that's obviously wrong?** Even a 15-minute reality check from someone with your background would save me from going off the rails.
>
> Happy to send the spec or jump on a quick call. No pressure — I know cold emails are a lot.
>
> Thanks for your time,
> Keaton
>
> *(P.S. — I'm not a developer myself. I'm the project lead / community / non-technical owner. You'd be the technical lead, not my employee.)*

---

## A few specific Mac security developers to consider cold-emailing

These are public figures known for high-quality open-source macOS security work. They're long shots but worth trying:

- **Patrick Wardle** (Objective-See — KnockKnock, BlockBlock, LuLu). [https://objective-see.com/](https://objective-see.com/)
- **Csaba Fitzl** (security researcher, kandji)
- **Howard Oakley** (Eclectic Light Company; not a primary builder but well-networked)
- Active contributors to **Hand Mirror**, **Little Snitch**, **Lulu** on GitHub

Worst case they decline. Best case they introduce you to a junior or mid-level dev in their orbit who's looking for a project to put their name on.

---

## When you get responses

For each interested developer:

1. **Send the V1 spec** (`../docs/V1-SPEC.md`)
2. **Set up a 30-minute video call** to mutually vet fit
3. **Look for:** they read the spec before the call, they ask sharp questions about architecture, they care about *why* the project exists (not just "another side project")
4. **Red flags:** they want equity in a project that has no commercial component, they propose immediately rewriting the spec, they want to use Electron or React Native (the spec is opinionated about native Swift for a reason — see "trust strategy" in section 6)

You only need one, but talk to 3-5 candidates if you can — both to compare and to build relationships in the broader Mac dev community.
