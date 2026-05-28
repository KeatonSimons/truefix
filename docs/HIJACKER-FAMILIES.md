# Mac Browser Hijacker Families — Reference

This document is a public reference for the browser-hijacker families that affect macOS, the kind of project TrueFix is built to clean. It exists for two audiences:

1. **Users** trying to identify what they're infected with so they can find the right cleanup advice.
2. **Contributors** researching a new rule pack — this doc cross-references the rule packs in `../rules/` and links to primary sources.

> ⚠️ **Status: living document.** Each family below has been compiled from public sources (vendor write-ups, security forums, real-world cleanups). Where TrueFix has a corresponding rule pack, it's linked. Where data is sourced from a single vendor or write-up and hasn't been independently verified, that's marked. Pull requests adding new families or improving sources are welcome — see [RULES_CONTRIBUTING.md](../rules/RULES_CONTRIBUTING.md).

---

## How to use this document

If you're a user trying to identify your hijacker, the fastest path is to look at the **symptoms** column below. The hijacker that matches your symptoms is the family TrueFix will clean — assuming we have a rule pack for it yet. (We're working on coverage.)

If you're a contributor writing a new rule pack, find your target family below, follow the references, and use the schema in [`rules/README.md`](../rules/README.md).

---

## Family directory

### Any Search Manager / Search Marquis

**Aliases:** AnySearch, SearchMarquis. Two names commonly grouped as one family because variants are observed under both, and they share extension IDs and persistence patterns in some real-world cases.

**Symptoms:**
- Chrome's default search engine is forced to `search.anysearchmanager.com` or `searchmarquis.com`
- Chrome shows the banner "Your browser is managed by your organization"
- The hijacker extension cannot be removed from `chrome://extensions` (no Remove button visible)
- Resetting Chrome settings doesn't stick — the hijacker returns after restart
- Often also affects Safari with a similar marquis redirect

**Persistence:** System-wide Chrome policy plist at `/Library/Preferences/com.google.Chrome.plist` (an `ExtensionInstallForcelist` entry), and a root-owned extension folder at `~/Library/Application Support/Google/Chrome/Profile */Extensions/<extension_id>`. Some variants also drop a Configuration Profile or a LaunchAgent.

**Common install vector:** Fake media player, Flash update, codec installer, or PDF tool that asked for admin password during install.

**Rule pack:** [`rules/any-search-manager.yaml`](../rules/any-search-manager.yaml) (Search Marquis tracked as separate stub in [`rules/search-marquis.yaml`](../rules/search-marquis.yaml) pending its own research pass)

**References:**
- [Trend Micro: Remove Search Marquis browser hijacker on Mac](https://helpcenter.trendmicro.com/en-us/article/tmka-11049)
- [MacSecurity: Remove Search Marquis virus from Mac](https://macsecurity.net/view/289-search-marquis-com)
- [iBoysoft: What is Search Marquis in Google Chrome on Mac?](https://iboysoft.com/wiki/what-is-search-marquis.html)
- TrueFix internal: cleanup transcript 2026-05-23 (primary source — see `rules/any-search-manager.yaml`)

---

### Search Baron

**Symptoms:**
- Default search engine forcibly redirected through `search.baronsearch.com` (or similar baron-themed domain) to Bing
- New tab and homepage rerouted to associated domains
- Affects Safari, Chrome, and Firefox commonly
- Cleaning the browser fully does not stick — the hijacker reapplies on next launch

**Persistence:** Per vendor write-ups, Search Baron uses startup settings, background apps, or network-level changes to reinstall itself. Browser sync can restore it from the cloud if not disabled before cleanup. Specific extension IDs and exact filesystem paths are not consistently documented across sources and need a real-world cleanup transcript to nail down.

**Common install vector:** Freeware bundle or fake update prompt.

**Rule pack:** TODO — see issue tracker

**References:**
- [NordVPN: Remove the Search Baron virus from a Mac](https://nordvpn.com/blog/search-baron/)
- [MacSecurity: Remove Search Baron virus from Mac](https://macsecurity.net/view/279-remove-searchbaron-virus-from-mac)
- [Trend Micro: How to remove Search Baron browser hijacker on Mac](https://helpcenter.trendmicro.com/en-us/article/tmka-11050)

---

### Trovi

**Aliases:** Trovi Search, Search Protect (the Trovi-bundled component)

**Symptoms:**
- Homepage and default search engine forced to `trovi.com` or `search.trovi.com`
- Heavy ad injection and sponsored search results
- Mac performance noticeably degraded due to injected scripts
- Affects Chrome primarily but can hit Safari and Firefox

**Persistence:** Trovi typically installs as a browser extension plus an auxiliary helper application ("Search Protect") that monitors and re-applies the hijacker settings. The helper persists via a LaunchAgent and reinstalls the extension if removed by the browser UI alone. Detected by Malwarebytes as `PUP.Optional.Trovi`.

**Common install vector:** Bundled with free software installers — historically the "Conduit Search Protect" installer was the largest distributor.

**Rule pack:** TODO — see [`rules/trovi.yaml`](../rules/trovi.yaml) (stub)

**References:**
- [MalwareTips: Remove Trovi Browser Hijacker From Mac (Virus Removal Guide)](https://malwaretips.com/blogs/remove-trovi-mac-os-x/)
- [Tom's Guide: How to Remove Trovi Search](https://www.tomsguide.com/us/trovi-search-remove-how-to,news-19130.html)
- [2-Spyware: Remove Trovi (Removal Guide)](https://www.2-spyware.com/remove-trovi.html)

---

### Conduit

**Aliases:** Conduit Search, Conduit Toolbar, ClientConnect (corporate parent)

**Symptoms:**
- Default search engine and homepage forced to `conduit.com` or `search.conduit.com` (legacy)
- Browser shows installed Conduit Toolbar that cannot be removed via standard menu
- Conduit has historically been the parent/distributor of multiple hijacker families, including Trovi

**Persistence:** LaunchAgent plus a Chrome/Safari extension. Conduit's installer family has historically used `ExtensionInstallForcelist`-style mechanisms and dropped LaunchAgents under `~/Library/LaunchAgents/`. Specific naming has changed over the years as the brand has split.

**Status:** Largely historical as of 2025–2026. The original Conduit company sold its consumer business and the brand has faded, but Conduit-derived hijackers (especially Trovi-flavored ones) are still observed in older infections that were never cleaned up.

**Rule pack:** TODO (low priority — overlaps with Trovi rule pack)

**References:**
- See Trovi references above; most Conduit coverage is co-mingled with Trovi removal guides.

---

### Safe Finder / Genieo

**Aliases:** Genieo Innovation, Safe Finder Search, MyMacUpdater, ArchimedesLookup, SectionBrowser, SearchMainInfo, CreativeSearch (the broader Adload family that Genieo is part of)

**Symptoms:**
- Default search engine forced to `safefinder.com` or various AdLoad-family search portals
- Sponsored results and ads injected into legitimate-looking search pages
- Mac shows new "helper" applications in `/Applications/` with generic names like SearchMainInfo or ArchimedesLookup
- Affects Safari, Chrome, and Firefox simultaneously

**Persistence:** This is the most sophisticated family in macOS adware. Genieo/AdLoad uses:
- A **LaunchAgent** that runs at user login (typically at `~/Library/LaunchAgents/com.<random>.<random>.plist`)
- A **LaunchDaemon** at `/Library/LaunchDaemons/` for system-wide persistence in some variants
- Multiple **browser extensions** across all installed browsers
- **Configuration Profiles** in some variants
- **Helper apps** in `/Applications/` and `~/Applications/`
- Periodic re-installation if any single component is removed

Apple's XProtect ships specific signatures for Genieo (`XProtectRemediatorGenieo`), and Malwarebytes tracks the broader family as `OSX.Genieo` / `OSX.Adload`. This is the family that motivated Apple to build XProtect Remediator in the first place.

**Common install vector:** Fake Flash update, fake codec installer, or bundle with free software.

**Rule pack:** TODO — high priority. This is the most common family in real-world Mac infections.

**References:**
- [Malwarebytes Labs: OSX.Genieo](https://www.malwarebytes.com/blog/detections/osx-genieo)
- [PCRisk: Genieo Virus (Mac) — Removal steps](https://www.pcrisk.com/removal-guides/13772-genieo-virus-mac)
- [CoreLock: Genieo Mac Malware — How to Detect & Remove](https://corelock.net/threats/genieo)
- [MacSecurity: XProtectRemediatorGenieo Mac threat alert](https://macsecurity.net/view/568-xprotectremediatorgenieo-mac-alert)
- [Trend Micro: Remove Safe Finder Browser Hijacker on Mac](https://helpcenter.trendmicro.com/en-us/article/tmka-09594)

---

### Bing.vc Redirector

**Symptoms:**
- Default search engine forced to `bing.vc` (a redirector that bounces searches through `bing.vc` to bing.com)
- Distinct from the legitimate Bing search engine
- Often co-occurs with other hijackers — the `bing.vc` redirector is a payload module that other hijacker families drop

**Persistence:** Variable — `bing.vc` is more often a payload than a standalone family. It's typically dropped by AdLoad, Trovi, or Search Marquis variants that route through bing.vc as the actual ad-monetized endpoint.

**Rule pack:** TODO (likely folded into other families' rule packs once their persistence is mapped)

**References:** Primarily appears in combined-family writeups; no canonical standalone reference.

---

### Yahoo Redirector Variants

**Aliases:** "Yahoo Search" hijackers, `yahoo.com/?type=…` redirector chains

**Symptoms:**
- Default search engine appears to be Yahoo, but URLs include suspicious tracking parameters (e.g. `?type=hijacker_id`)
- Resetting search engine to Google or DuckDuckGo doesn't stick
- This is **not** Yahoo itself doing anything wrong — these are third-party hijackers that route through Yahoo's affiliate program to monetize

**Persistence:** Similar to other hijacker families — extension + LaunchAgent + optional Configuration Profile. The specific affiliate IDs in the URL parameters can identify the originating family.

**Rule pack:** TODO

**References:** Most Yahoo-redirector coverage is part of broader removal guides; specific Mac-targeted writeups are sparse.

---

### Search Pulse

**Symptoms:**
- Search engine forced to `searchpulse.net` or similar
- Often bundled with PDF-Maker-style fake utility apps

**Persistence:** Typical hijacker pattern — extension + LaunchAgent.

**Status:** Lower prevalence than the families above. Worth a rule pack stub.

**Rule pack:** TODO

**References:** See AdLoad family references; Search Pulse is generally classified under AdLoad.

---

## Family relationships at a glance

Many of these families are related — same distributor, shared extension IDs, or shared payload modules. Rough lineage:

```
Conduit (corporate parent, ~2010–2014)
  ├── Trovi (spun out, still active in old infections)
  └── Search Protect (helper component)

Genieo Innovation
  └── Genieo / Safe Finder / AdLoad family
        ├── SearchMainInfo, ArchimedesLookup, SectionBrowser, CreativeSearch (variant apps)
        ├── searchmarquis.com payload (in some variants)
        └── bing.vc / yahoo redirector payloads
```

The practical implication for TrueFix: writing a single, well-curated rule pack for the AdLoad family catches most modern macOS hijacker infections. The Conduit/Trovi lineage is still in the wild but largely on un-cleaned older Macs.

---

## Sources

This document is compiled from the following public references:

- [Malwarebytes Labs: OSX.Genieo](https://www.malwarebytes.com/blog/detections/osx-genieo)
- [PCRisk: Genieo Virus removal guide](https://www.pcrisk.com/removal-guides/13772-genieo-virus-mac)
- [NordVPN: Search Baron removal](https://nordvpn.com/blog/search-baron/)
- [MacSecurity: Search Marquis](https://macsecurity.net/view/289-search-marquis-com), [Search Baron](https://macsecurity.net/view/279-remove-searchbaron-virus-from-mac), [XProtectRemediatorGenieo](https://macsecurity.net/view/568-xprotectremediatorgenieo-mac-alert)
- [Trend Micro Help Center: Search Marquis](https://helpcenter.trendmicro.com/en-us/article/tmka-11049), [Safe Finder](https://helpcenter.trendmicro.com/en-us/article/tmka-09594), [Search Baron](https://helpcenter.trendmicro.com/en-us/article/tmka-11050)
- [MalwareTips: Trovi removal guide](https://malwaretips.com/blogs/remove-trovi-mac-os-x/)
- [Tom's Guide: Trovi Search removal](https://www.tomsguide.com/us/trovi-search-remove-how-to,news-19130.html)
- [iBoysoft: What is Search Marquis](https://iboysoft.com/wiki/what-is-search-marquis.html)
- TrueFix internal: cleanup transcript 2026-05-23 (primary source for the Any Search Manager rule pack)

---

*If you've encountered a hijacker family not listed here — or you have specific extension IDs / persistence paths for a family that has TODOs — please open an issue. See [CONTRIBUTING.md).*
