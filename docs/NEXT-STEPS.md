# TrueFix — Next Steps Checklist

Concrete actions, ordered. Check things off as you do them. When something stalls, move to the next item — don't let perfect block forward motion.

---

## This week (Week 1)

The goal of Week 1 is to commit and to start outreach. Nothing else.

- [ ] **Make the go/no-go decision.** Do you actually want to do this? (Acceptable answer: "not now" — file the kit away. Acceptable answer: "yes." Not acceptable: indecision for two weeks.)
- [ ] **Pick a working name.** "TrueFix" is the current placeholder. Try saying 3-4 alternatives out loud. Pick the one that doesn't make you cringe. You can change it once before V1 ships without it being a problem.
- [ ] **Check `.app` domain availability** for your top 2-3 names at any registrar (Namecheap, Cloudflare Registrar). Register the one that's available and feels right. (~$15-20/year.)
- [ ] **Create the GitHub organization** under that name. Free.
- [ ] **Open the new Cowork project** in the Claude app. Drop all six files from this kit into it.
- [ ] **Read `../recruiting/PITCHES.md`.** Pick which channel you want to start with. (Recommendation: r/swift — biggest pool of right-fit devs, easy to post.)
- [ ] **Post the recruiting pitch** in one channel. Just one. See what response you get before fanning out.

---

## Weeks 2-4

Goal: find your developer collaborator.

- [ ] **Reply to every response** within 48 hours. Even rejections — keep the door open.
- [ ] **Schedule 30-minute video calls** with 3-5 strong candidates if you can. Don't just go with the first person who says yes.
- [ ] **Send each candidate the V1 spec** before the call. The ones who actually read it before the meeting are the ones to talk seriously with.
- [ ] **In each call:** explain the project, listen for their take on the architecture, ask what they'd change. The right collaborator pushes back constructively. The wrong one rubber-stamps everything OR wants to rewrite everything.
- [ ] **If first channel doesn't produce a candidate after 2 weeks:** post in a second channel (IndieHackers, Hacker News "who wants to be hired" thread, or 2-3 cold emails from the named-developer list).
- [ ] **Pick one collaborator.** Send them a "let's do this" message. Open a private Discord/Slack/Signal channel for ongoing project comms.
- [ ] **Sign up for the Apple Developer Program.** $99/year. The collaborator can technically use their own, but the project is cleaner if you own the developer ID.

---

## Month 2

Goal: V1 scaffolding + first detection rule implemented end-to-end.

- [ ] **Kickoff meeting with the developer.** Both of you read the V1 spec end-to-end and align on it. Document any changes in a `KICKOFF.md` in the GitHub repo.
- [ ] **Developer scaffolds the Swift project.** Empty SwiftUI app, Authorization Services pattern, YAML rule loader.
- [ ] **Pick one hijacker family to implement end-to-end** (recommendation: Any Search Manager — well-documented, easy to test on).
- [ ] **You: start curating the rule pack.** Research known hijacker extension IDs. Sources: Malwarebytes' threat database, Bleeping Computer, MacRumors threads, Reddit r/macsysadmin threads. Compile into the YAML format the spec describes.
- [ ] **Internal testing.** Get the scanner working on a known-infected Mac (real, or a VM you can deliberately infect for testing).

---

## Month 3

Goal: GUI + cleanup actions.

- [ ] **Developer implements cleanup actions** for the V1 family list, plus the privileged XPC helper.
- [ ] **Developer builds the SwiftUI shell** around the engine. Single window, scan/review/clean flow as described in the spec.
- [ ] **You: write release notes, draft the launch blog post, prepare social media posts.**
- [ ] **Set up the public website** at `<name>.app`. Static site (Cloudflare Pages free tier). One page is enough: what it does, how to install, link to GitHub.
- [ ] **Internal alpha.** Test on 3-5 real Macs with various states (clean, infected, partially-cleaned). Capture every bug.

---

## Month 4

Goal: launch V1.

- [ ] **Code signing + notarization** of the release build. Apple submission, ~24 hour turnaround.
- [ ] **Publish v1.0.0 on GitHub Releases** — DMG + checksum + signed.
- [ ] **Submit Homebrew Cask** PR. (Approval can take a few days to a couple weeks.)
- [ ] **Post launch announcement** on:
  - Hacker News (best time: Tuesday-Thursday, 8-10am Eastern)
  - r/MacOS, r/privacy, r/swift
  - Mastodon (#macOS, #infosec)
  - LinkedIn (if you use it)
- [ ] **Reach out for coverage:** email Patrick Wardle, MacRumors, Daring Fireball, The Eclectic Light Company, 9to5Mac with a brief intro and the GitHub link. (Don't expect responses; one yes makes the launch.)
- [ ] **Watch the issue queue.** Respond to every issue within 24 hours for the first month. Set expectations early about what you'll fix and what you won't.

---

## After V1

- [ ] Collect user feedback and triage feature requests
- [ ] Recruit a second maintainer (single-maintainer projects die when the maintainer burns out)
- [ ] Decide what V2 looks like — most likely Safari support, more hijacker families
- [ ] Independent security review (ask Patrick Wardle / Csaba Fitzl)
- [ ] Localization sprint if there's translator interest

---

## Things that are tempting but not on this list

These are real things you might be drawn to do that would slow you down or pull you off course:

- ❌ Designing a logo before V1 ships (do it later, or pay a designer $200 once you have an audience)
- ❌ Building a fancy website before there's a product to download
- ❌ Setting up Patreon, Open Collective, Buy Me a Coffee, etc. (do it later if at all)
- ❌ Worrying about the name being perfect (good enough is good enough; you can rename once)
- ❌ Trying to do anything Windows or Linux related (out of scope; stay focused)
- ❌ Adding "AI-powered" anything (the appeal of this tool is that it's small, focused, and transparent — AI buzzwords work against trust here)

---

## When to give up and go home

You don't have to do this. Real reasons to set it down:

- After 4 weeks of outreach you've found zero developer candidates worth talking to a second time. (Means the pitch needs work, or the project genuinely doesn't have a hook for the right people.)
- You realize the work of running an open-source security project — bug triage, false-positive complaints, contributor management — isn't something you actually want to do.
- A bigger fish enters the market and does it better than you could. (Unlikely but possible.)

Setting it down is fine. The spec lives on GitHub regardless and anyone can pick it up.
