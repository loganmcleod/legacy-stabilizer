# Stabilization Charter

<!-- The keystone artifact. Phase 0 produces this before any other work. The
remediation authorization gate reads this file: no code changes happen unless the
Authorization section below explicitly permits them for the named finding/repo. -->

## Scope
- Assessment date: ...
- Portfolio revision / snapshot: ...
- Repositories in scope: ...
- Explicit exclusions: ...
- Business-critical user journeys: ...
- Current production symptoms: ...
- Target environments: ...

## Mode

Set exactly one. This governs what the workflow is allowed to do.

- [ ] **Assessment-only** — read-only. Phases 0–6 and plan generation. No code,
      DDL, dependency, contract, or deployment changes.
- [ ] **Remediation-authorized** — assessment plus authorized implementation. Fill
      the Authorization table; leave it empty and the workflow stays read-only.

## Authorization

Remediation is permitted ONLY for the rows listed here. Each row names who
authorized it, what it covers, and when. No row = no code change.

| Finding ID | Repo(s) | Authorized by | Date | Notes / limits |
|---|---|---|---|---|
|  |  |  |  |  |

## Change Boundaries (hold unless a row above overrides them)
- No production code changes during discovery.
- No database DDL, dependency upgrade, data migration, public-contract change, or
  deployment without a matching Authorization row.
- No load testing against production.
- Redact credentials, personal data, customer data, and secrets from every artifact.
- Pin every finding to a repository and commit SHA.
- No mixing of unrelated fixes, formatting, renames, or upgrades into one batch.

## Evidence Limitations
- Production telemetry available: yes / no / partial
- Known inaccessible sources: ...
- Assumptions that must be confirmed: ...
