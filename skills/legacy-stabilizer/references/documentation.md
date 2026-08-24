# Required Architectural Documentation

Produce documentation proportionate to the system, using lightweight C4-style
views and targeted runtime diagrams. Prefer Mermaid text so diagrams review in
version control. Generate from confirmed evidence where possible; **label inferred
elements explicitly**.

## The six views

1. **System context** — users, external systems, and the polyrepo application
   boundary.
2. **Container / deployable view** — AngularJS 1.x and Angular 17 (NX) apps,
   Spring Boot services/jobs, integration components, Oracle schemas.
3. **Component hot-spot view** — only for high-risk / high-change areas.
4. **Critical runtime sequences** — the most important user and batch workflows.
5. **Data ownership map** — authoritative sources, shared tables/schemas,
   cross-service database access.
6. **Deployment coupling map** — release ordering, compatibility windows, rollback
   dependencies.

## Mermaid patterns

Container view:

```mermaid
flowchart LR
  UI[Angular 17 SPA / AngularJS SPA] -->|HTTPS/JSON| API[Spring Boot: orders-api]
  API -->|JDBC| ORA[(Oracle: ORDERS schema)]
  API -->|HTTP| PAY[payments-service]
  JOB[Spring batch: nightly-recon] --> ORA
```

Critical runtime sequence:

```mermaid
sequenceDiagram
  participant UI as AngularJS
  participant API as Spring endpoint
  participant SVC as OrderService
  participant DAO as OrderDao
  participant DB as Oracle
  UI->>API: POST /orders
  API->>SVC: placeOrder(cmd)
  SVC->>DAO: findLines(orderId)
  loop N+1 (confirmed: 101 selects)
    DAO->>DB: SELECT line WHERE ...
  end
  DAO-->>SVC: lines
  SVC-->>API: OrderView
  API-->>UI: 201 Created
```

Mark any element not backed by evidence with `%% inferred` or a note node, so a
reviewer can tell confirmed topology from hypothesis.
