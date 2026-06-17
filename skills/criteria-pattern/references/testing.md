# Testing

Criteria Pattern includes object mother helpers for downstream tests.

## Imports

High-level helpers:

```python
from criteria_pattern.models.testing.mothers import (
    CriteriaMother,
    FilterMother,
    FiltersMother,
    OrderMother,
    OrdersMother,
    PageNumberMother,
    PageSizeMother,
)
```

More specific helpers live under:

```python
from criteria_pattern.models.testing.mothers.filter import (
    FilterFieldMother,
    FilterMother,
    FilterOperatorMother,
    FilterValueMother,
    OperatorMother,
)
from criteria_pattern.models.testing.mothers.order import (
    DirectionMother,
    OrderDirectionMother,
    OrderFieldMother,
    OrderMother,
)
```

## Deterministic Converter Tests

Use explicit values when asserting exact SQL, parameters, dictionaries, primitive output, or ordering. Random object
mothers are useful for construction and validation tests, but can make exact-output tests flaky.

```python
from criteria_pattern import Criteria, Filter, Operator
from criteria_pattern.converters import CriteriaToPostgresqlConverter

criteria = Criteria(filters=[Filter(field='name', operator=Operator.CONTAINS, value='Doe')])

query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=criteria,
    table='users',
    valid_tables=['users'],
    valid_columns=['name'],
    valid_operators=[Operator.CONTAINS],
    check_direction_injection=False,
)

assert query == 'SELECT * FROM "users" WHERE "name" LIKE \'%%\' || %(parameter_0)s || \'%%\' ESCAPE \'\\\';'
assert parameters == {'parameter_0': 'Doe'}
```

If a criteria has no orders, either pass `valid_directions=[Direction.ASC, Direction.DESC]` or disable direction checks in
focused tests. For public-path integration tests, prefer passing the explicit allowlist.

## Security Regression Tests

For user-facing paths, test both accepted and rejected inputs.

```python
from pytest import raises

from criteria_pattern import Operator
from criteria_pattern.converters import BodyToCriteriaConverter
from criteria_pattern.errors import InvalidColumnError

with raises(InvalidColumnError):
    BodyToCriteriaConverter.convert(
        body={'filters': [{'field': 'unknown', 'operator': 'CONTAINS', 'value': 'Doe'}]},
        valid_fields=['name'],
        valid_operators=[Operator.CONTAINS],
    )
```

Useful cases:

- Unknown field is rejected.
- Unknown selected SQL column is rejected.
- Unknown table is rejected.
- Operator outside endpoint allowlist is rejected.
- Direction outside endpoint allowlist is rejected.
- Oversized page size or page number raises `PaginationBoundsError`.
- Oversized `IN` lists raise `IntegrityError`.
- LIKE values containing `%` or `_` are escaped in generated SQL and parameters.

## Package Maintenance Tests

When changing package behavior, update skill evals too:

- Operator changes should update operator docs and at least one eval that asks for the operator list.
- Converter default/signature changes should update converter docs and at least one secure conversion eval.
- Security changes should update security docs and at least one rejected-input eval.

Run normal project verification for package code changes:

```bash
make format
make lint
make test
make coverage
```

For documentation-only skill updates, validate the skill and run the skill eval loop instead.
