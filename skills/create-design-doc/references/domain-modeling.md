<overview>
Domain modeling extracts the core business concepts from requirements. This reference covers entities, value objects, aggregates, and domain services following Domain-Driven Design (DDD) tactical patterns.
</overview>

<extraction_from_requirements>

**User stories describe BEHAVIOR. Domain model describes STRUCTURE.**

**Extraction patterns:**

| Source | Extract | Examples |
|--------|---------|----------|
| Nouns in stories | Entity candidates | "Influencer", "Campaign", "Brand" |
| "As a [role]" | Actor candidates | "Team member", "Admin", "Client" |
| "I want to [action]" | Use case candidates | "discover", "filter", "export" |
| Acceptance criteria | Business rules | "Must have at least 1000 followers" |
| NFRs | Quality attributes | "Response time < 500ms" |

**Example extraction:**

Story: "As a team member, I want to discover influencers by niche so that I can match them to brand requests."

- **Entity:** Influencer (has identity, changes over time)
- **Entity:** Brand (has identity, requests)
- **Value Object:** Niche (defined by attributes, no identity)
- **Actor:** Team member
- **Use Case:** DiscoverInfluencers

</extraction_from_requirements>

<entities>

**Definition:** Objects with identity and lifecycle. Two entities with the same attributes are still different if they have different IDs.

**Characteristics:**
- Have a unique identifier (ID)
- Change state over time
- Encapsulate business logic
- Are the "nouns" of your domain

**Example:**
```python
@dataclass
class Influencer:
    id: UUID
    name: str
    platforms: list[PlatformPresence]
    niches: list[Niche]
    created_at: datetime

    def calculate_engagement_rate(self) -> Decimal:
        """Business logic lives with the entity"""
        total_engagement = sum(p.engagement for p in self.platforms)
        total_followers = sum(p.followers for p in self.platforms)
        return Decimal(total_engagement / total_followers) if total_followers > 0 else Decimal(0)
```

**Anti-pattern:** Anemic entities (just data, no behavior). Put business logic IN the entity.

</entities>

<value_objects>

**Definition:** Immutable objects defined by their attributes. Two VOs with the same attributes ARE the same.

**Characteristics:**
- No identity (no ID field)
- Immutable (can't change after creation)
- Encapsulate validation
- Replace primitives with meaningful types

**Example:**
```python
@dataclass(frozen=True)  # frozen = immutable
class FollowerCount:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Follower count cannot be negative")

    @property
    def tier(self) -> str:
        if self.value >= 1_000_000:
            return "mega"
        elif self.value >= 100_000:
            return "macro"
        elif self.value >= 10_000:
            return "micro"
        else:
            return "nano"
```

**Common value objects:**
- Email, PhoneNumber (validated strings)
- Money, FollowerCount (validated numbers)
- DateRange, TimeSlot (validated date/time)
- Address (composite values)

</value_objects>

<aggregates>

**Definition:** Cluster of entities and value objects with a consistency boundary. All access goes through the **aggregate root**.

**Rules:**
1. One entity is the root (only entity referenceable from outside)
2. External objects can only hold references to the root
3. Transactions don't span aggregates
4. Deleting root deletes entire aggregate

**Identifying aggregates:**
- What needs to be consistent together?
- What is the unit of change?
- What can be loaded/saved as a unit?

**Example:**
```
Influencer Aggregate
├── Influencer (root)     ← Only this has a repository
├── PlatformPresence      ← Part of aggregate
├── EngagementMetrics     ← Value object
└── ContactInfo           ← Value object

Campaign Aggregate (separate)
├── Campaign (root)
├── Requirement
└── Submission
```

**Anti-pattern:** One giant aggregate with everything. Keep aggregates small—transactional boundaries.

</aggregates>

<domain_services>

**Definition:** Operations that don't naturally belong to a single entity. They operate on multiple entities or require external information.

**When to use:**
- Logic spans multiple aggregates
- Orchestration of complex domain rules
- Calculations requiring multiple entities

**Example:**
```python
class MatchingService:
    """Matches influencers to brand requirements"""

    def find_matches(
        self,
        requirement: BrandRequirement,
        influencers: list[Influencer]
    ) -> list[InfluencerMatch]:
        """Domain service - spans Influencer and Brand aggregates"""
        return [
            InfluencerMatch(influencer, self._calculate_score(influencer, requirement))
            for influencer in influencers
            if self._meets_criteria(influencer, requirement)
        ]
```

**Anti-pattern:** Putting all logic in services (anemic domain model). Domain logic should live in entities first.

</domain_services>

<domain_model_documentation>

**Format for documenting domain model:**

```markdown
## Domain Model

### Entities
| Entity | Description | Key Attributes | Aggregate |
|--------|-------------|----------------|-----------|
| Influencer | Content creator | id, name, platforms | Influencer |
| Campaign | Brand campaign | id, brand, requirements | Campaign |

### Value Objects
| Value Object | Encapsulates | Validation |
|--------------|--------------|------------|
| FollowerCount | Follower numbers | Must be >= 0 |
| EngagementRate | Engagement % | 0.0 - 100.0 |

### Aggregates
| Aggregate | Root | Contains |
|-----------|------|----------|
| Influencer | Influencer | PlatformPresence, ContactInfo |
| Campaign | Campaign | Requirement, Submission |

### Domain Services
| Service | Purpose | Entities Involved |
|---------|---------|-------------------|
| MatchingService | Match influencers to requirements | Influencer, Campaign |
```

</domain_model_documentation>

<validation_questions>

Ask these to validate your domain model:

1. **Does each entity have a clear identity?** Can you distinguish two entities with identical attributes?
2. **Are value objects truly immutable?** No setters, no state changes?
3. **Are aggregates small enough?** Can they be loaded in one query?
4. **Is the aggregate root clear?** Only one entity referenced from outside?
5. **Is business logic in entities?** Or scattered in services (anemic)?
6. **Do entities have meaningful behavior?** Or just getters/setters?

</validation_questions>
