# 🧱 Usage Guide

This guide explains the core Criteria Pattern models and how to compose them before converting to SQL or another query
representation.

## Core Models

`Criteria` is the central model. It groups filters, orders and optional pagination:

```python
from criteria_pattern import Criteria, Direction, Filter, Operator, Order


criteria = Criteria(
    filters=[
        Filter(field='status', operator=Operator.EQUAL, value='ACTIVE'),
        Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18),
    ],
    orders=[
        Order(field='created_at', direction=Direction.DESC),
    ],
    page_size=20,
    page_number=1,
)
```

`Filter` represents one field/operator/value condition. `Order` represents one field/direction sorting rule.

The field names are backend-neutral strings. They can be public API field names, internal domain fields or database
column names depending on where you create the criteria. Request converters and SQL converters can map those names before
validation or SQL rendering.

## Composition

Criteria can be composed with Python operators:

| Python expression | Criteria node | Meaning |
| --- | --- | --- |
| `left & right` | `AndCriteria` | Match both sides |
| `left | right` | `OrCriteria` | Match either side |
| `~criteria` | `NotCriteria` | Negate the wrapped criteria |

```python
from criteria_pattern import Criteria, Filter, Operator


is_active = Criteria(filters=[Filter(field='status', operator=Operator.EQUAL, value='ACTIVE')])
is_adult = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
has_company_email = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@acme.com')])

criteria = is_active & (is_adult | has_company_email)
```

Converters preserve the boolean structure when they render nested filters. Orders from composed criteria are exposed in
left-to-right order. Pagination prefers the left side when it exists, then falls back to the right side.

Named methods are also available:

```python
criteria = is_active.and_(criteria=is_adult)
criteria = criteria.or_(criteria=has_company_email)
criteria = criteria.not_()
```

## Operators

Criteria Pattern supports these filter operators:

| Operator | Value shape |
| --- | --- |
| `EQUAL`, `NOT_EQUAL` | scalar |
| `GREATER`, `GREATER_OR_EQUAL`, `LESS`, `LESS_OR_EQUAL` | scalar |
| `LIKE`, `NOT_LIKE` | scalar SQL-like pattern |
| `CONTAINS`, `NOT_CONTAINS` | scalar |
| `STARTS_WITH`, `NOT_STARTS_WITH` | scalar |
| `ENDS_WITH`, `NOT_ENDS_WITH` | scalar |
| `BETWEEN`, `NOT_BETWEEN` | exactly two values |
| `IS_NULL`, `IS_NOT_NULL` | value is ignored and treated as `None` by request converters |
| `IN`, `NOT_IN` | one or more values |

The base `Filter` object stores the value you provide. Request converters parse incoming raw strings or body values into
the expected shapes before constructing filters.

## Pagination

Pagination uses positive integer value objects:

- `page_size` means limit the number of returned rows.
- `page_number` is one-based and requires `page_size`.
- SQL converters calculate `OFFSET` as `page_size * (page_number - 1)`.

```python
criteria = Criteria(page_size=50, page_number=3)
```

`page_size` without `page_number` is valid and renders a `LIMIT` without an `OFFSET`.

```python
criteria = Criteria(page_size=50)
```

You can remove pagination from an existing criteria:

```python
criteria.clean_pagination()
```

`clean_pagination()` mutates the criteria and returns the same instance. On composed criteria it clears pagination from
the wrapped child criteria.

## Validation Behavior

Criteria Pattern uses value objects to validate model integrity:

- Filter and order fields must be non-empty, trimmed, printable strings.
- Operators must be valid `Operator` enum values.
- Directions must be valid `Direction` enum values.
- Order collections cannot contain duplicate fields.
- `page_number` cannot be supplied without `page_size`.

User-facing allowlist validation is handled by converters. See the [Security Guide](../security/README.md).

## Common Recipe

```python
from criteria_pattern import Criteria, Direction, Filter, Operator, Order


tenant_scope = Criteria(filters=[Filter(field='tenant_id', operator=Operator.EQUAL, value='tenant_123')])
active_scope = Criteria(filters=[Filter(field='is_active', operator=Operator.EQUAL, value=True)])
search_scope = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@acme.com')])
sort_scope = Criteria(orders=[Order(field='created_at', direction=Direction.DESC)])

criteria = tenant_scope & active_scope & search_scope & sort_scope
```

That criteria can later be passed to any SQL converter without changing the domain logic.
