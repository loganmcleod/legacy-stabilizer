# Remediation Master Plan

<!-- Decision and progress index. Not a scanner dump. Keep concise; push detailed
evidence into repositories/<repo-id>/ artifacts and link to them. -->

## Scope and Baseline
- Portfolio revision: ...
- Repositories: ...
- Assessment date: ...
- Mode: assessment-only | remediation-authorized (by whom, for what)
- Critical runtime paths: ...
- Evidence limitations: ...

## Architectural Health Baseline
- Presentation layer (AngularJS / Angular / React, MFE composition): ...
- Service/application layer (Spring Boot 2.7 / 3.5, Java 21, Maven): ...
- Persistence/database layer (Oracle 19c / AlloyDB): ...
- Search & cache layer (SOLR 9.x / Redis 7.2): ...
- Cross-repository coupling: ...
- Test and observability posture: ...

> **Companion artifact:** every assessment run also produces `SPEC_DRIVEN_BRIEF.md`
> — the same portfolio rewritten as a self-contained brief (stack, guardrails,
> epics/stories) for a spec-driven AI framework such as BMad or GitHub Spec Kit.
> This plan is for humans deciding; the brief is the input that generates the specs.

## Prioritized Remediation Portfolio
| Rank | ID | Finding | Runtime path | Impact | Confidence | Cost | Risk | Intervention | Owner | Status |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | STAB-XX-0001 | ... | ... | ... | ... | ... | ... | Lx | ... | Candidate |

## Findings

### [STAB-XX-0001] Defect or Anti-Pattern Name
- Status: Candidate / Confirmed / Planned / Verified / Deferred / Rejected
- Target Coordinates: repository, commit SHA, exact file+line range or runtime identifier
- Affected Runtime Path: user/system workflow
- Evidence and Confidence: observed facts, reproduction, metrics, confidence
- Debt Impact: High / Medium / Low — reliability / performance / testability / regression
- Current Code State: smallest exact relevant excerpt
- Root Cause: confirmed cause or explicitly labeled hypothesis
- Minimum Safe Remediation: intervention level and why lower levels are insufficient
- Proposed Modular Architecture: only if a boundary change is necessary; text/Mermaid
- Phased Remediation Snippet: example or pseudocode, clearly labeled; not "drop-in" until compiled/tested in context
- Verification Plan: tests and before/after measures
- Rollback Plan: feature flag, revert, compatibility mechanism, or DDL rollback
- Dependencies and Ownership: repos, teams, schema, release ordering
- Detailed Evidence: links to repo-local assessment artifacts
