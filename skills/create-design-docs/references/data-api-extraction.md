<overview>
When users provide pre-existing data models (database schemas, ER diagrams, ORM definitions) or API specifications (OpenAPI, GraphQL, gRPC, REST docs) as input files, these artifacts contain structural information that accelerates domain model extraction and interface documentation. This reference covers how to identify, parse, and map these artifacts into architecture elements.

## Contents
- Detecting Input Types — Recognizing data model and API spec formats
- Data Model Extraction — Mapping schemas to domain model elements
- API Specification Extraction — Mapping API contracts to interfaces and boundaries
- Cross-Mapping to Architecture — How extracted artifacts feed into architecture phases
- Reconciliation — Resolving conflicts between data models and requirements
- Validation Questions — Checklist to verify extraction completeness
</overview>

<detecting_input_types>

**Data Model Formats:**

| Format | Detection Pattern | Common Extensions |
|--------|-------------------|-------------------|
| SQL DDL | `CREATE TABLE`, `ALTER TABLE`, `FOREIGN KEY` | `.sql` |
| Prisma Schema | `model`, `@@map`, `@relation` | `schema.prisma` |
| TypeORM / Sequelize | `@Entity()`, `@Column()`, `Model.init()` | `.ts`, `.js` |
| Django Models | `class X(models.Model):`, `models.CharField` | `models.py` |
| SQLAlchemy | `class X(Base):`, `Column(`, `relationship(` | `.py` |
| Drizzle Schema | `pgTable(`, `sqliteTable(`, `mysqlTable(` | `.ts` |
| JSON Schema | `"$schema"`, `"type": "object"`, `"properties"` | `.json`, `.yaml` |
| ER Diagram (Mermaid) | `erDiagram`, `}o--\|\|` | `.md`, `.mmd` |

**API Specification Formats:**

| Format | Detection Pattern | Common Extensions |
|--------|-------------------|-------------------|
| OpenAPI / Swagger | `openapi:`, `swagger:`, `paths:` | `.yaml`, `.json` |
| GraphQL Schema | `type Query`, `type Mutation`, `schema {` | `.graphql`, `.gql` |
| gRPC / Protobuf | `syntax = "proto3"`, `service`, `rpc` | `.proto` |
| tRPC Router | `router({`, `publicProcedure`, `protectedProcedure` | `.ts` |
| REST Docs (informal) | Endpoint tables, curl examples, route listings | `.md` |

**When you encounter these patterns in input files, apply the corresponding extraction techniques below.**

</detecting_input_types>

<data_model_extraction>

**Data models describe STORAGE STRUCTURE. Domain models describe BUSINESS STRUCTURE.**

They overlap but are NOT the same. A database table is not automatically a domain entity — and a domain entity may span multiple tables or have no table at all.

**Extraction Patterns:**

| Data Model Element | Maps To | Confidence | Notes |
|--------------------|---------|------------|-------|
| Table / model class | Entity candidate | High | Verify it has identity and lifecycle |
| Column with constraints | Value Object candidate | Medium | Validated types suggest VOs |
| Foreign key / relation | Aggregate boundary signal | Medium | References may cross aggregates |
| Composite unique constraint | Value Object identity | High | Multiple columns forming a key |
| Enum column / type | Value Object or strategy | High | Closed set of domain concepts |
| Join table (many-to-many) | Domain relationship | Medium | May indicate a hidden entity |
| Timestamps (created_at, updated_at) | Entity lifecycle | High | Confirms entity status |
| Soft delete (deleted_at, is_active) | Entity lifecycle rule | High | Business rule for deletion |
| JSON / JSONB column | Embedded Value Object | Medium | Structured data within entity |
| Computed / virtual column | Derived attribute | Low | May be presentation, not domain |

**Worked Example — SQL DDL:**

```sql
CREATE TABLE hooks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_url TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    lifecycle_event TEXT NOT NULL,
    stars INTEGER DEFAULT 0,
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE hook_tags (
    hook_id UUID REFERENCES hooks(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (hook_id, tag_id)
);
```

**Extraction result:**

| Element | Type | Reasoning |
|---------|------|-----------|
| Hook | Entity | Has UUID identity, timestamps, changes over time |
| Tag | Entity or Value Object | Has identity (serial PK), but may be a VO if tags are just labels |
| RepoUrl | Value Object | `UNIQUE` + `NOT NULL` = validated identity-less concept |
| Category | Value Object (enum) | Closed set: "security", "formatting", "testing" |
| LifecycleEvent | Value Object (enum) | Closed set: "PreToolUse", "PostToolUse", etc. |
| StarCount | Value Object | Numeric with implied validation (>= 0) |
| hook_tags | Relationship | Many-to-many — Hook aggregate may contain tags |

**Worked Example — Prisma Schema:**

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
}
```

**Extraction result:**

| Element | Type | Reasoning |
|---------|------|-----------|
| User | Entity (Aggregate Root) | Has identity, owns Posts and Profile |
| Post | Entity | Has identity, lifecycle (published state) |
| Profile | Entity or VO | Depends on whether it has independent lifecycle |
| Email | Value Object | `@unique` validated string, no independent identity |
| User Aggregate | Aggregate | User → Posts, User → Profile (cascade boundary) |

**Key principle:** Foreign keys pointing FROM child TO parent suggest the parent is an aggregate root. The `@relation` in Prisma and `REFERENCES` in SQL are aggregate boundary signals.

</data_model_extraction>

<api_spec_extraction>

**API specifications describe EXTERNAL CONTRACTS. Architecture interfaces describe INTERNAL BOUNDARIES.**

API specs inform adapter-layer interfaces, while use case interfaces are derived from requirements. They serve different purposes.

**OpenAPI / Swagger Extraction:**

| OpenAPI Element | Maps To | Architecture Layer |
|-----------------|---------|-------------------|
| Path (`/users/{id}`) | API Controller endpoint | Adapters |
| Request body schema | Use Case Input candidate | Application |
| Response schema | Use Case Output candidate | Application |
| Path parameters + query params | Search/filter criteria | Application |
| Security schemes (`bearerAuth`) | Cross-cutting concern | Architecture decision |
| Tags / groupings | Bounded context signal | Domain |
| Error responses (4xx, 5xx) | Error handling strategy | Cross-cutting |
| Rate limiting headers | Quality attribute (performance) | NFR mapping |

**Worked Example — OpenAPI:**

```yaml
paths:
  /hooks:
    get:
      summary: List hooks with filtering
      parameters:
        - name: category
          in: query
          schema:
            type: string
            enum: [security, formatting, testing, workflow]
        - name: lifecycle_event
          in: query
          schema:
            type: string
        - name: min_stars
          in: query
          schema:
            type: integer
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                properties:
                  hooks:
                    type: array
                    items:
                      $ref: '#/components/schemas/Hook'
                  total:
                    type: integer
```

**Extraction result:**

| Element | Architecture Artifact | Location |
|---------|----------------------|----------|
| GET /hooks | ListHooks use case | Application layer |
| query params (category, lifecycle_event, min_stars) | SearchCriteria value object | Domain layer |
| enum [security, formatting, ...] | Category value object | Domain layer |
| response schema (hooks + total) | ListHooksOutput | Application layer |
| $ref Hook schema | Hook entity attributes | Domain layer |

**GraphQL Schema Extraction:**

| GraphQL Element | Maps To | Architecture Layer |
|-----------------|---------|-------------------|
| `type` (non-Query/Mutation) | Entity or VO candidate | Domain |
| `type Query` fields | Read use cases | Application |
| `type Mutation` fields | Write use cases | Application |
| Input types | Use Case Input | Application |
| Enum types | Value Object (enum) | Domain |
| `@auth` / `@deprecated` directives | Cross-cutting / lifecycle | Architecture decision |
| Nested resolvers | Aggregate structure signal | Domain |

**gRPC / Protobuf Extraction:**

| Protobuf Element | Maps To | Architecture Layer |
|------------------|---------|-------------------|
| `service` | Bounded context / adapter | Adapters |
| `rpc` methods | Use case candidates | Application |
| `message` (request) | Use Case Input | Application |
| `message` (response) | Use Case Output | Application |
| `enum` | Value Object | Domain |
| `repeated` fields | Collection relationship | Domain |
| `oneof` | Polymorphic behavior | Domain |

**tRPC Router Extraction:**

| tRPC Element | Maps To | Architecture Layer |
|--------------|---------|-------------------|
| `router({})` groupings | Bounded context signal | Domain |
| `.query()` procedures | Read use cases | Application |
| `.mutation()` procedures | Write use cases | Application |
| Input validation (Zod schemas) | Value Object validation rules | Domain |
| Middleware chains | Cross-cutting concerns | Architecture decision |

</api_spec_extraction>

<cross_mapping>

**How extracted artifacts feed into architecture phases:**

| Architecture Phase | Data Model Contribution | API Spec Contribution |
|--------------------|-------------------------|-----------------------|
| **Domain Model (Entities)** | Tables/models with identity → entities; columns → attributes | Response schemas confirm entity shape |
| **Domain Model (Value Objects)** | Enums, validated columns, composite keys → VOs | Input parameter enums, query constraints → VOs |
| **Domain Model (Aggregates)** | Foreign key clusters, cascade rules → aggregate boundaries | Nested response objects → aggregate structure |
| **Domain Model (Services)** | Join tables with extra columns → potential services | Endpoints spanning multiple resources → service candidates |
| **Architecture Layers** | ORM/schema location → adapter layer structure | API route groupings → adapter organization |
| **Key Interfaces (Repository)** | Table structure → repository method signatures | — (repos are internal) |
| **Key Interfaces (Use Cases)** | — (use cases come from requirements) | Request/response schemas → use case I/O |
| **C4 Container Diagram** | Database type → container | API type (REST/GraphQL/gRPC) → container boundary |
| **Quality Attributes** | Indexes, constraints → performance decisions | Rate limits, auth schemes → security/performance NFRs |
| **Constraints** | DB engine choice → technical constraint | API versioning strategy → compatibility constraint |

**Priority rule:** When data models and requirements conflict, **requirements take precedence**. The data model may reflect implementation history or legacy decisions. The architecture should serve the requirements, not the schema.

</cross_mapping>

<reconciliation>

**Common conflicts between data models, API specs, and requirements:**

| Conflict | Resolution |
|----------|------------|
| Table exists but no requirement references it | Flag as potential technical debt or legacy; exclude from domain model unless business relevance confirmed |
| Requirement describes entity not in data model | Add to domain model; data model is incomplete or entity is new |
| API endpoint has no matching requirement | Flag as undocumented capability; ask stakeholder if in scope |
| Data model has denormalized fields (e.g., cached counts) | Document as implementation optimization in ADR, not in domain model |
| FK relationship contradicts aggregate boundary from requirements | Requirements define the domain truth; FK may be for query convenience |
| API returns fields not in data model (computed/derived) | Document as derived attribute; clarify if domain logic or presentation |

**Reconciliation process:**

1. **Extract from requirements first** (user stories, SRS, business case) — this is the source of domain truth
2. **Overlay data model extraction** — validates and enriches the domain model with structural details
3. **Overlay API spec extraction** — validates interfaces and adds contract details
4. **Flag discrepancies** — document conflicts in a reconciliation table in the architecture doc
5. **Resolve with stakeholder** — if conflicts affect scope, raise as an open question

</reconciliation>

<validation_questions>

After extracting from data models and API specs, verify:

1. **Every entity in the domain model has a source.** Can you trace it to a requirement, a table, or an API schema?
2. **No "ghost entities" from data alone.** Every table promoted to an entity has a business justification from requirements.
3. **API contracts align with use cases.** Each documented endpoint maps to a use case derived from requirements.
4. **Aggregate boundaries match both FK clusters AND business rules.** If they disagree, business rules win.
5. **Value objects extracted from enums/constraints are domain-meaningful.** A database enum for internal status codes is NOT a domain value object.
6. **Derived/computed fields are not mistaken for entity attributes.** Cache columns and view fields belong in the adapter layer, not the domain model.

</validation_questions>
