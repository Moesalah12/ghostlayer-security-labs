# GhostLayer Security Labs

**Reproducible defensive investigations using synthetic evidence.**

This initial lab connects three small tools built for Mohammad Salah’s cybersecurity engineering portfolio and GhostLayer Defense. It contains no customer evidence, real intrusion claims, or third-party targets.

## Lab 01: Authentication triage and control review

### Scenario and scope

A fictional administrator reports unusual sign-in activity. You have a normalized export of nine authentication events, two synthetic HTTP header captures, and a local static site fixture. Determine what the evidence supports and identify follow-up work.

### Prerequisites

Python 3.11+. Place these repositories next to this one:

| Directory | Role |
| --- | --- |
| ghostlayer-authwatch | Event correlation |
| ghostlayer-integrity | Local file comparison |
| ghostlayer-headercheck | Offline browser-control review |
| ghostlayer-security-labs | Reproduction runner and report |

No external network requests are needed. From this repository:

```sh
python reproduce.py
```

The runner invokes the actual command-line tools against fixtures, checks expected results, modifies a temporary copy of the site, and verifies that the change is detected. It does not change the original examples. A successful run prints `Lab passed: 9 events, 3 alerts, 5 weak-header findings, 0 hardened-header findings, 1 integrity modification.`

### Evidence and interpretation

1. At 12:00:04 UTC, `192.0.2.10` reaches five failures for `training-admin`.
2. At 12:00:06 UTC, the same account and source records a success, yielding an escalation signal. This does **not** prove unauthorized access.
3. At 12:01:02 UTC, `198.51.100.20` reaches three distinct failed accounts. This is consistent with several possibilities, including account probing or a shared system with misconfigured credentials.
4. The weak header capture lacks five controls recognized by HeaderCheck. The hardened fixture addresses those heuristics. Neither capture establishes the exploitability or overall security of an application.
5. A known change to a temporary site file is detected as one modification. This proves content comparison for the fixture, not malware detection or resistance to baseline tampering.

### Triage and remediation exercise

| Observation | Follow-up evidence | Proportionate action |
| --- | --- | --- |
| Success after failures | User confirmation, MFA details, device/session records | If unauthorized access is confirmed, revoke affected sessions and follow account recovery procedures |
| Several accounts targeted | Source attribution, SSO/NAT context, longer timeline | Tune rate limits and alert thresholds to normal behavior |
| Missing browser controls | Actual app routes, CSP report-only telemetry | Test an application-specific CSP; deploy HTTPS controls with a rollback plan |
| File content change | Deployment records, trusted baseline provenance | Determine whether the change was approved before restoring anything |

### Investigation boundaries

No geolocation, attribution, malware analysis, customer exposure, or credential theft is established. Reports should distinguish observations from hypotheses. The sample accounts are fictional and IPs come from documentation ranges.

### Extend the lab

- Change a failure to another account and explain why the success correlation changes.
- Move an event outside the 300-second window and compare output.
- Add/delete a file in the temporary site and inspect the added/removed lists.
- Design a normalized adapter for a log format you understand, with timezone and malformed-input tests.

## Provenance

This is a worked educational scenario, not a claim that a real incident was investigated. Tool repositories contain their implementation details, licenses, and test suites.
