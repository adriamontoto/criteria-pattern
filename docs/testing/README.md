# 🧪 Testing Guide

Criteria Pattern includes object mother helpers for downstream tests. They help you create valid criteria objects without
duplicating construction boilerplate.

## Main Helpers

Import high-level helpers from `criteria_pattern.models.testing.mothers`:

```python
from criteria_pattern.models.testing.mothers import CriteriaMother, FilterMother, OrderMother
```

Available high-level helpers:

- `CriteriaMother`
- `FilterMother`
- `FiltersMother`
- `OrderMother`
- `OrdersMother`
- `PageSizeMother`
- `PageNumberMother`

More specific helpers are available under:

- `criteria_pattern.models.testing.mothers.filter`
- `criteria_pattern.models.testing.mothers.order`

## Explicit Values For Deterministic Tests

Prefer explicit values when your test asserts exact strings, dictionaries, SQL or parameter order:

```python
from criteria_pattern import Filter, Operator
from criteria_pattern.models.testing.mothers import CriteriaMother


criteria = CriteriaMother.with_filters(
    filters=[
        Filter(field='name', operator=Operator.CONTAINS, value='Doe'),
    ]
)
```

Random mothers are useful for validation and broad object-construction tests, but exact converter output should use fixed
inputs.

## Creating Filters And Orders

```python
from criteria_pattern import Direction, Operator
from criteria_pattern.models.testing.mothers import FilterMother, OrderMother


filter = FilterMother.create(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
order = OrderMother.create(field='created_at', direction=Direction.DESC)
```

## Criteria Recipes

```python
from criteria_pattern import Filter, Operator
from criteria_pattern.models.testing.mothers import CriteriaMother


empty_criteria = CriteriaMother.empty()
filtered_criteria = CriteriaMother.with_filters(
    filters=[Filter(field='status', operator=Operator.EQUAL, value='ACTIVE')]
)
random_criteria = CriteriaMother.create()
```

## Testing Converters

When testing SQL or URL converter behavior:

- Use explicit fields, operators, values, orders and pagination.
- Assert the returned SQL and parameters together.
- Keep input order deterministic.
- Avoid random object mothers for exact output assertions.
- Use allowlist validation in tests that represent user-facing paths.

```python
from criteria_pattern import Criteria, Filter, Operator
from criteria_pattern.converters import CriteriaToPostgresqlConverter


criteria = Criteria(filters=[Filter(field='name', operator=Operator.CONTAINS, value='Doe')])
query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=criteria,
    table='users',
    valid_columns=['name'],
    valid_operators=[Operator.CONTAINS],
)

assert query == 'SELECT * FROM "users" WHERE "name" LIKE \'%%\' || %(parameter_0)s || \'%%\';'
assert parameters == {'parameter_0': 'Doe'}
```

## Testing Security Rules

For user-facing paths, include tests for rejected fields, operators, directions and pagination bounds:

```python
from pytest import raises

from criteria_pattern import Operator
from criteria_pattern.converters import BodyToCriteriaConverter
from criteria_pattern.errors import InvalidColumnError


with raises(InvalidColumnError):
    BodyToCriteriaConverter.convert(
        body={'filters': [{'field': 'unknown', 'operator': 'CONTAINS', 'value': 'Doe'}]},
        check_field_injection=True,
        valid_fields=['name'],
        valid_operators=[Operator.CONTAINS],
    )
```

This keeps security assumptions executable and close to the code that exposes criteria input.
