# Models

Criteria Pattern exposes public model imports from `criteria_pattern`:

```python
from criteria_pattern import Criteria, Direction, Filter, Operator, Order, PageNumber, PageSize
```

The package is typed (`criteria_pattern/py.typed`) and supports Python `>=3.11`.

## Criteria

Construct a criteria with filters, orders, and optional pagination:

```python
criteria = Criteria(
    filters=[
        Filter(field='status', operator=Operator.EQUAL, value='ACTIVE'),
        Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18),
    ],
    orders=[Order(field='created_at', direction=Direction.DESC)],
    page_size=20,
    page_number=1,
)
```

Constructor arguments:

| Argument | Type | Notes |
| --- | --- | --- |
| `filters` | `list[Filter[Any]] | None` | Defaults to an empty list. |
| `orders` | `list[Order] | None` | Defaults to an empty list. Duplicate order fields are rejected. |
| `page_size` | `int | None` | Positive integer; renders `LIMIT` in SQL converters. |
| `page_number` | `int | None` | Positive one-based integer; requires `page_size`. |

Useful properties and methods:

| Member | Behavior |
| --- | --- |
| `criteria.filters` | List of `Filter` objects in declaration order. |
| `criteria.orders` | List of `Order` objects in declaration order. |
| `criteria.page_size` | `int` or `None`. |
| `criteria.page_number` | `int` or `None`. |
| `criteria.has_filters()` | True when at least one filter exists. |
| `criteria.has_orders()` | True when at least one order exists. |
| `criteria.has_page_size()` | True when a page size exists. |
| `criteria.has_pagination()` | True when page size and page number both exist. |
| `criteria.clean_pagination()` | Mutates the criteria, clears pagination, and returns the same instance. |
| `criteria.to_primitives()` | Inherited value-object serializer. Use tests to confirm exact enum representation. |
| `Criteria.from_primitives(...)` | Inherited constructor helper used by tests and downstream code. |

`page_size` without `page_number` is valid. `page_number` without `page_size` raises `IntegrityError`.

## Boolean Composition

Criteria compose with Python operators:

```python
is_active = Criteria(filters=[Filter(field='status', operator=Operator.EQUAL, value='ACTIVE')])
is_adult = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
has_company_email = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@acme.com')])

criteria = is_active & (is_adult | has_company_email)
not_archived = ~Criteria(filters=[Filter(field='archived_at', operator=Operator.IS_NOT_NULL, value=None)])
```

Equivalent named methods:

```python
criteria = is_active.and_(criteria=is_adult)
criteria = criteria.or_(criteria=has_company_email)
criteria = criteria.not_()
```

Composition nodes are `AndCriteria`, `OrCriteria`, and `NotCriteria` in `criteria_pattern.models.criteria`. They are
not usually constructed directly. SQL converters preserve the boolean tree with parentheses and `NOT`.

For `AndCriteria` and `OrCriteria`, filters and orders are exposed as left followed by right. Pagination prefers the
left side when set and falls back to the right side. `clean_pagination()` propagates to children. `NotCriteria` exposes
the wrapped criteria through `.criteria` and propagates pagination cleanup to it.

## Filter

```python
filter = Filter(field='name', operator=Operator.CONTAINS, value='Doe')
```

Arguments:

| Argument | Notes |
| --- | --- |
| `field` | Non-empty, trimmed, printable string. Represents a public field, internal field, or SQL column depending on layer. |
| `operator` | `Operator` value or valid operator string. |
| `value` | Generic value passed through to converters; shape depends on operator. |

Properties:

| Property | Behavior |
| --- | --- |
| `field` | Returns a string. |
| `operator` | Returns the operator value as a string such as `'EQUAL'`. |
| `value` | Returns the original value after value-object storage. |

## Order

```python
order = Order(field='created_at', direction=Direction.DESC)
```

Arguments:

| Argument | Notes |
| --- | --- |
| `field` | Non-empty, trimmed, printable string. |
| `direction` | `Direction` value or valid direction string. |

Properties:

| Property | Behavior |
| --- | --- |
| `field` | Returns a string. |
| `direction` | Returns `'ASC'` or `'DESC'`. |

`Orders` rejects duplicate order fields so `ORDER BY` output stays deterministic.

## Pagination Value Objects

`PageSize(value=...)` and `PageNumber(value=...)` wrap positive integers and raise `IntegrityError` for non-integers,
zero, or negative values. Most users pass integers directly to `Criteria` instead of constructing these wrappers.

## Errors

Public package-specific errors:

```python
from criteria_pattern.errors import (
    IntegrityError,
    InvalidColumnError,
    InvalidDirectionError,
    InvalidOperatorError,
    InvalidTableError,
    PaginationBoundsError,
)
```

Use `IntegrityError` for model-shape and parser-shape problems. Use the specific validation errors when converter
allowlists reject tables, columns/fields, operators, directions, or pagination bounds.
