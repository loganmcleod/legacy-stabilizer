# Changelog

All notable changes to legacy-stabilizer are recorded here. Versions follow
[semantic versioning](https://semver.org/); each release is tagged in git and
published on the [GitHub releases page](https://github.com/loganmcleod/legacy-stabilizer/releases).

## [0.3.0] — 2026-09-05

Expanded the target stack, added a spec-driven hand-off deliverable, and completed
true/false-positive fixture coverage for every detector.

### Added

- **Expanded target stack.** New candidate detectors for the technologies that
  appear in modern polyrepos, each held to the same candidate-until-evidence
  discipline:
  - React 19 and Webpack 5 Module Federation — `references/detectors-react-mfe.md`
    (effect-cleanup leaks, unstable refs/re-render, fetch cancellation; MFE
    singleton version skew, unshared heavy deps, remote-load failure, contract
    drift).
  - AlloyDB / PostgreSQL — `references/detectors-alloydb.md` (N+1, non-sargable
    predicates, missing indexes, `EXPLAIN (ANALYZE, BUFFERS)`, `pg_stat_statements`,
    columnar engine, read-pool lag).
  - SOLR 9.x and Redis 7.2 (GCP) — `references/detectors-search-cache.md` (slow
    queries, deep paging vs `cursorMark`, commit strategy, caches; cache stampede,
    TTL, blocking O(N) commands, pooling, invalidation).
  - Spring Boot 3.5 / Maven 3.8+ additions to `references/detectors-spring.md`
    (`jakarta.*` vs `javax.*`, Hibernate 6.x, virtual threads).
- **`SPEC_DRIVEN_BRIEF.md` deliverable.** Every assessment run now also produces a
  machine/agent-facing brief designed to be handed whole to spec-driven AI
  frameworks (BMad, GitHub Spec Kit, Amazon Kiro) to generate PRDs/epics/stories —
  `templates/SPEC_DRIVEN_BRIEF.md`. It never fabricates; unknowns are marked
  `unknown`.
- **Setup skill** and clearer onboarding docs.
- **Full detector fixture coverage.** True/false-positive pairs with an
  `EXPECTED.md` for each detector, each keeping a finding at `Candidate` until the
  named runtime evidence is attached:
  `react-effect-leak`, `module-federation-skew`, `alloydb-nonsargable`,
  `solr-deep-paging`, `redis-stampede`, `angular-rxjs-leak`, `nx-boundary-violation`
  (added alongside the existing `nplus1-java`, `angularjs-listener-leak`,
  `oracle-fullscan`).

### Changed

- Workspace inventory recognizes the new stacks: Webpack / Module Federation build
  markers, `.jsx`/`.tsx` counting, and `presentation-react` / `search-solr` /
  `cache-redis` layer hints. The `persistence-oracle` layer key was renamed to
  `persistence-sql` to cover Oracle and AlloyDB.
- Phase workflow, artifact schemas, templates, the design brief, the playbook, and
  the README were updated to reflect the expanded stack and the spec-driven brief.
- Helper self-checks grew to 13 (`scripts/test_scripts.py`).

## [0.2.0]

Fixtures, dedupe/merge, CI, and the plan-scan note.

## [0.1.0]

Initial `legacy-stabilizer` skill and plugin.
