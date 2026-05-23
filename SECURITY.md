# Security Policy

TrueFix is a security tool that runs with elevated privileges on your Mac. We take vulnerabilities in it very seriously.

## Reporting a vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Instead, email the maintainer at **security@truefix.app** *(TODO: replace with real contact once domain is registered)* with:

1. A description of the vulnerability
2. Steps to reproduce
3. The version of TrueFix affected (commit hash if pre-release)
4. Your name / handle if you want credit; or specify if you'd prefer to remain anonymous

We'll acknowledge receipt within 48 hours and aim to have a fix or mitigation within two weeks for high-severity issues.

## What counts as a vulnerability

- TrueFix could be tricked into deleting or modifying files outside its rule pack scope
- A malicious rule pack PR could exfiltrate data or run code as root
- The privileged XPC helper could be invoked by another process bypassing user consent
- TrueFix incorrectly flags a legitimate extension or file as a hijacker, leading to data loss
- Code signing / notarization issues that would let an unsigned variant of TrueFix impersonate the real one

## What doesn't count

- TrueFix doesn't detect a hijacker family we haven't written a rule pack for yet (this is a feature request, not a vuln — open a regular issue)
- The macOS admin-password dialog appears more than once (this is by design)
- TrueFix can't run on older macOS versions than the spec supports

## Coordinated disclosure

For high-severity issues we'll work with the reporter on a coordinated disclosure timeline. Typical pattern: 90 days from report to public disclosure, with a fix shipped at least 30 days before disclosure if possible.

## Hall of fame

Researchers who responsibly disclose security issues will be credited here (with their permission).

*(Empty — be the first.)*
