# Security

Criteria Pattern is designed for safe dynamic filtering, but the caller must use allowlists correctly.

## Main Rule

SQL converters parameterize filter values. That protects values such as `'Doe'`, `18`, or `['ACTIVE', 'PENDING']`.

Database drivers do not parameterize identifiers. Table names, selected column names, filter fields, and order fields
must be controlled by application code or validated with allowlists.

## Validation Defaults

All converter validation flags default to `True`.

Request converters:

- `check_field_injection=True`
- `check_operator_injection=True`
- `check_direction_injection=True` where directions are supported
- `check_pagination_bounds=True`

SQL converters:

- `check_table_injection=True`
- `check_column_injection=True`
- `check_criteria_injection=True`
- `check_operator_injection=True`
- `check_direction_injection=True`
- `check_pagination_bounds=True`

Treat every `valid_*` allowlist as a complete enumeration. When a check is enabled and the allowlist is omitted or empty,
nothing is allowed for that dimension:

- Omitted or empty `valid_fields`: no request fields allowed.
- Omitted or empty `valid_columns`: no SQL columns or criteria fields allowed.
- Omitted or empty `valid_operators`: no operators allowed.
- Omitted or empty `valid_directions`: no directions allowed.
- Omitted `valid_tables`: SQL converters allow only the `table` argument.

Disable `check_*` flags only for trusted application-built criteria in internal code or focused tests.

## Structural Limits

Defaults in criteria-pattern 4.0.0:

| Limit | Default |
| --- | --- |
| Request `max_filters` | 100 |
| Request `max_orders` | 100 |
| Request `max_in_values` | 100 |
| Request `max_page_size` | 1000 |
| Request `max_page_number` | 10000 |
| SQL `max_criteria_depth` | 32 |
| SQL `max_in_values` | 100 |
| SQL `max_page_size` | 1000 |
| SQL `max_page_number` | 10000 |
| `max_operator_allowlist` | `len(Operator)` |

Use tighter page-size and page-number limits for public endpoints.

## LIKE Safety

SQL converters escape LIKE wildcard characters in bound values for:

- `LIKE`
- `NOT_LIKE`
- `CONTAINS`
- `NOT_CONTAINS`
- `STARTS_WITH`
- `NOT_STARTS_WITH`
- `ENDS_WITH`
- `NOT_ENDS_WITH`

Escaped characters include `%`, `_`, and backslash. Generated SQL includes `ESCAPE '\'`.

## Identifier Quoting

SQL converters quote identifiers:

- PostgreSQL and SQLite use double quotes and escape embedded double quotes.
- MySQL and MariaDB use backticks and escape embedded backticks.
- Qualified names such as `identity.user` are quoted part by part.

Quoting is not a substitute for allowlists. Keep allowlist checks enabled for user-facing paths.

## Safe Public API Flow

```python
from criteria_pattern import Direction, Operator
from criteria_pattern.converters import BodyToCriteriaConverter, CriteriaToPostgresqlConverter

fields_mapping = {'q': 'name', 'created': 'created_at'}
valid_fields = ['name', 'created_at']
valid_operators = [Operator.CONTAINS]
valid_directions = [Direction.DESC]

criteria = BodyToCriteriaConverter.convert(
    body=request_body,
    fields_mapping=fields_mapping,
    valid_fields=valid_fields,
    valid_operators=valid_operators,
    valid_directions=valid_directions,
    max_page_size=100,
    max_page_number=1000,
)

query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=criteria,
    table='users',
    columns=['id', 'name', 'created_at'],
    valid_tables=['users'],
    valid_columns=['id', 'name', 'created_at'],
    valid_operators=valid_operators,
    valid_directions=valid_directions,
    max_page_size=100,
    max_page_number=1000,
)
```

Pass `query` and `parameters` to the database driver without string-formatting values into SQL.

## Field Mapping Rule

Request converters apply `fields_mapping` before validating request fields. Therefore `valid_fields` should contain
mapped internal names.

SQL converters apply `columns_mapping` before validating criteria fields and order fields. Therefore `valid_columns`
must contain mapped SQL column names, not only public names.

For public APIs, prefer mapping public names in the request converter so the final `Criteria` contains internal field
names before SQL conversion.

## Operator Exposure

Expose only the operators each endpoint needs:

- Search boxes often need only `Operator.CONTAINS`.
- Numeric ranges often need `GREATER_OR_EQUAL` and `LESS_OR_EQUAL`.
- Admin-only screens may need `IS_NULL`, `IN`, or `BETWEEN`.
- Avoid broad wildcard-heavy operators unless the database and indexes can handle them.

## Errors To Expect

- `InvalidTableError`: table not allowed.
- `InvalidColumnError`: selected column, criteria field, or order field not allowed.
- `InvalidOperatorError`: operator not allowed.
- `InvalidDirectionError`: direction not allowed.
- `PaginationBoundsError`: page size or page number exceeds configured maximum.
- `IntegrityError`: malformed request/converter input or exceeded structural limits.
