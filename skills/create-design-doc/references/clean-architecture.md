<overview>
Clean Architecture organizes code into concentric layers where dependencies point INWARD only. The business logic (domain) sits at the center with zero external dependencies, making it testable, maintainable, and technology-agnostic.

## Contents
- The Dependency Rule — The only rule that matters
- Four Layers — Entities, Use Cases, Interface Adapters, Frameworks
- Layer Documentation — How to document each layer
- Crossing Boundaries — Dependency Inversion for outward control flow
- Interface Documentation — How to document interfaces
- Data Crossing Boundaries — DTOs at boundaries
- Common Violations — Signs and fixes
- Architecture Testing — How to verify correctness
- When Clean Architecture Fits — Decision guide
</overview>

<the_dependency_rule>

**The only rule that matters:**

> "Source code dependencies can only point inwards."

- Inner layers are completely ignorant of outer layers
- Nothing in an inner circle can know about an outer circle
- Not just classes—naming, data formats, framework artifacts cannot penetrate inward

**Visualization:**
```
┌─────────────────────────────────────────────────────────┐
│                 Frameworks & Drivers                     │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Interface Adapters                  │    │
│  │  ┌───────────────────────────────────────────┐  │    │
│  │  │              Use Cases                     │  │    │
│  │  │  ┌─────────────────────────────────────┐  │  │    │
│  │  │  │            Entities                  │  │  │    │
│  │  │  │      (Enterprise Business Rules)     │  │  │    │
│  │  │  └─────────────────────────────────────┘  │  │    │
│  │  └───────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘

              ←───── Dependencies point INWARD ─────→
```

</the_dependency_rule>

<four_layers>

**Layer 1: Entities (Domain)**
- Enterprise-wide business rules
- Pure business logic, no external dependencies
- Entities, value objects, domain services
- Changes only when business rules change

**Layer 2: Use Cases (Application)**
- Application-specific business rules
- Orchestrates data flow between entities
- Defines repository interfaces (ports)
- Changes when operational requirements change

**Layer 3: Interface Adapters**
- Converts data between use cases and external world
- Controllers, presenters, gateways
- Implements interfaces defined by use cases
- Changes when UI/API format changes

**Layer 4: Frameworks & Drivers**
- Database, web framework, external APIs
- The outermost, most volatile layer
- Pure implementation details
- Changes when technology choices change

</four_layers>

<layer_documentation>

**How to document each layer:**

```markdown
## Architecture Layers

### Domain Layer (Innermost)
**Contains:** Entities, Value Objects, Domain Services
**Dependencies:** None (pure business logic)
**Responsibilities:**
- Core business rules
- Domain validation
- Business calculations

### Application Layer
**Contains:** Use Cases, Repository Interfaces
**Dependencies:** Domain Layer only
**Responsibilities:**
- Orchestrate domain objects
- Define ports (interfaces) for adapters
- Application-specific validation

### Adapters Layer (Outermost)
**Contains:** Repository Implementations, API Controllers, UI
**Dependencies:** Application + Domain Layers
**Responsibilities:**
- Implement repository interfaces
- Handle HTTP/API concerns
- Database operations
```

</layer_documentation>

<crossing_boundaries>

**When control flow needs to go outward** (e.g., use case calls database), use Dependency Inversion:

1. **Inner layer defines interface (port):**
```python
# In application layer
class InfluencerRepository(Protocol):
    def find_by_id(self, id: UUID) -> Influencer | None: ...
    def save(self, influencer: Influencer) -> None: ...
```

2. **Use Case depends on interface:**
```python
# In application layer
class EnrichInfluencer:
    def __init__(self, repository: InfluencerRepository):
        self.repository = repository

    def execute(self, id: UUID, data: EnrichmentData) -> Influencer:
        influencer = self.repository.find_by_id(id)
        influencer.enrich(data)
        self.repository.save(influencer)
        return influencer
```

3. **Outer layer implements interface (adapter):**
```python
# In adapters layer
class PostgresInfluencerRepository:
    """Implements InfluencerRepository protocol"""

    def find_by_id(self, id: UUID) -> Influencer | None:
        # PostgreSQL-specific code here
        pass
```

**Dependencies still point inward** (adapter depends on interface in inner layer).

</crossing_boundaries>

<interface_documentation>

**How to document interfaces:**

```markdown
## Key Interfaces

### Repository Interfaces

**InfluencerRepository**
```python
class InfluencerRepository(Protocol):
    def find_by_id(self, id: UUID) -> Influencer | None: ...
    def search(self, criteria: SearchCriteria) -> list[Influencer]: ...
    def save(self, influencer: Influencer) -> None: ...
    def delete(self, id: UUID) -> None: ...
```

### Use Case Interfaces

**DiscoverInfluencers**
```python
@dataclass
class DiscoverInfluencersInput:
    platform: Platform
    niche: Niche
    min_followers: int

@dataclass
class DiscoverInfluencersOutput:
    influencers: list[InfluencerSummary]
    total_count: int
    has_more: bool
```
```

</interface_documentation>

<data_crossing_boundaries>

**Data structures at boundaries:**

Simple data structures (DTOs) pass across boundaries—not entities or database objects.

```python
# BAD: Returning ORM model from repository
def find_by_id(self, id: UUID) -> InfluencerModel:  # ORM model leaks
    return session.query(InfluencerModel).get(id)

# GOOD: Returning domain entity
def find_by_id(self, id: UUID) -> Influencer | None:  # Domain entity
    model = session.query(InfluencerModel).get(id)
    return self._to_domain(model) if model else None
```

</data_crossing_boundaries>

<common_violations>

**Signs you're violating Clean Architecture:**

| Violation | Symptom | Fix |
|-----------|---------|-----|
| Domain imports framework | `from sqlalchemy import Column` in domain/ | Use pure Python types |
| ORM models in domain | `class Influencer(Base)` | Separate ORM models from entities |
| Use case returns ORM | Repository returns database model | Map to domain entity |
| Adapter has business logic | Validation in controller | Move to domain/application |
| Circular dependencies | Domain imports application | Review layer boundaries |

</common_violations>

<architecture_testing>

**How to verify architecture is correct:**

1. **Domain tests run without mocks for DB/framework:**
```python
def test_influencer_engagement_rate():
    # No database, no HTTP, no external services
    influencer = Influencer(id=uuid4(), name="Test", platforms=[...])
    assert influencer.calculate_engagement_rate() == expected
```

2. **Use case tests mock only repository interface:**
```python
def test_enrich_influencer():
    mock_repo = Mock(spec=InfluencerRepository)
    mock_repo.find_by_id.return_value = test_influencer

    use_case = EnrichInfluencer(mock_repo)
    result = use_case.execute(id, data)

    mock_repo.save.assert_called_once()
```

3. **Lint rules catch imports:**
```python
# Domain layer: no imports from adapters, application, or frameworks
```

</architecture_testing>

<when_clean_architecture_fits>

| Scenario | Recommendation |
|----------|----------------|
| Complex domain logic | Use Clean Architecture |
| Multiple integrations | Use Clean Architecture |
| Long-lived system | Use Clean Architecture |
| Team needs guardrails | Use Clean Architecture |
| Simple CRUD app | Skip it—use simple layers |
| MVP/Prototype | Skip it—speed first |
| < 5 endpoints | Overkill—add structure later |

</when_clean_architecture_fits>
