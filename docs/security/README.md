# 🔐 Security Guide

This guide explains how to use Criteria Pattern safely when criteria comes from user-facing inputs such as URLs, JSON
bodies, forms, dashboards or admin tools.

## Secure Defaults

All converters enable validation by default:

- SQL converters: `check_table_injection`, `check_column_injection`, `check_criteria_injection`, `check_operator_injection`, `check_direction_injection`, and `check_pagination_bounds` default to `True`.
- Request converters: `check_field_injection`, `check_operator_injection`, `check_direction_injection`, and `check_pagination_bounds` default to `True`.

For user-controlled input, pass explicit `valid_*` allowlists. Set individual `check_*` flags to `False` only for trusted, application-built criteria in tests or internal tooling.

## Main Rule

Criteria Pattern parameterizes **filter values** in SQL converters. That protects predicate values such as `'Doe'`, `18`
or `['ACTIVE', 'PENDING']`.

SQL identifiers are different. Database drivers do not parameterize table names, selected column names, filter field
names or order field names. Those values must be controlled by application code or validated with allowlists.

## Risk Matrix

| Input kind | Example | Risk | Protection |
| --- | --- | --- | --- |
| Filter value | `value='Doe'` | SQL value injection | Converter parameter binding |
| Table name | `table='users'` | SQL identifier injection | `valid_tables` allowlist (enabled by default) |
| Selected column | `columns=['name']` | SQL identifier injection | `valid_columns` allowlist (enabled by default) |
| Filter field | `field='name'` | SQL identifier injection | request field validation + SQL criteria validation (enabled by default) |
| Order field | `field='created_at'` | SQL identifier injection | request field validation + SQL criteria validation (enabled by default) |
| Operator | `operator='CONTAINS'` | Query behavior abuse | `valid_operators` allowlist (enabled by default) |
| Direction | `direction='DESC'` | Query behavior abuse | `valid_directions` allowlist (enabled by default) |
| Page size / number | `page_size=1000000` | Expensive query or overflow | strict `max_page_size` / `max_page_number` (enabled by default) |

## Recommended Production Flow

1. Keep allowlists in code or configuration controlled by your application.
2. Parse request data with a request converter.
3. Map public field names to internal names with `fields_mapping`.
4. Validate parsed fields, operators, directions and pagination bounds in the request converter.
5. Convert to SQL with table, column, criteria, operator, direction and pagination validation enabled.
6. Pass the returned query and parameters to your database driver without string-formatting values into the query.

```python
from criteria_pattern import Direction, Operator
from criteria_pattern.converters import BodyToCriteriaConverter, CriteriaToPostgresqlConverter


body = {
    'filters': [{'field': 'q', 'operator': 'contains', 'value': 'Doe'}],
    'orders': [{'field': 'created', 'direction': 'DESC'}],
    'page_size': 20,
    'page_number': 1,
}

fields_mapping = {'q': 'name', 'created': 'created_at'}
valid_fields = ['name', 'created_at']
valid_operators = [Operator.CONTAINS]
valid_directions = [Direction.DESC]

criteria = BodyToCriteriaConverter.convert(
    body=body,
    fields_mapping=fields_mapping,
    check_field_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
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
    check_table_injection=True,
    check_column_injection=True,
    check_criteria_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
    valid_tables=['users'],
    valid_columns=['id', 'name', 'created_at'],
    valid_operators=valid_operators,
    valid_directions=valid_directions,
    max_page_size=100,
    max_page_number=1000,
)
```

## Request Converter Validation

Enable request converter checks when the client controls fields, operators, directions or pagination.

```python
criteria = BodyToCriteriaConverter.convert(
    body=body,
    fields_mapping={'q': 'name', 'created': 'created_at'},
    check_field_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
    valid_fields=['name', 'created_at'],
    valid_operators=[Operator.CONTAINS],
    valid_directions=[Direction.DESC],
    max_page_size=100,
    max_page_number=1000,
)
```

Request converters validate after applying `fields_mapping`, so `valid_fields` should contain the mapped internal names.

## SQL Converter Validation

Enable SQL converter checks when table names, selected columns or criteria fields might be affected by request data.

```python
query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=criteria,
    table='users',
    columns=['id', 'name', 'created_at'],
    check_table_injection=True,
    check_column_injection=True,
    check_criteria_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
    valid_tables=['users'],
    valid_columns=['id', 'name', 'created_at'],
    valid_operators=[Operator.CONTAINS],
    valid_directions=[Direction.DESC],
    max_page_size=100,
    max_page_number=1000,
)
```

SQL converters validate criteria fields before applying `columns_mapping`. The safest pattern is to map public field
names in the request converter, then pass internal criteria fields to the SQL converter.

If you use SQL `columns_mapping` directly with public criteria fields, include both the public criteria field and the
mapped SQL column in `valid_columns`.

## Operator Allowlisting

Do not expose every operator by default. Operators change query cost and behavior.

Examples:

- Public search boxes often need only `CONTAINS`.
- Numeric filters may need `GREATER_OR_EQUAL` and `LESS_OR_EQUAL`.
- Admin-only filters may allow `IS_NULL`, `IN` or `BETWEEN`.
- Avoid exposing expensive wildcard-heavy patterns unless the database and indexes are prepared for them.

```python
valid_operators = [Operator.CONTAINS]
```

## Pagination Bounds

Always set maximums for user-facing pagination. Defaults are intentionally broad because libraries cannot know your
application limits.

```python
check_pagination_bounds=True
max_page_size=100
max_page_number=1000
```

Choose values based on your database size, indexes, latency budget and UI needs.

## Unsafe Pattern To Avoid

Avoid taking user-provided identifiers and passing them directly to SQL conversion without validation:

```python
# Avoid this for user-facing input.
query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=user_controlled_criteria,
    table=user_controlled_table,
    columns=user_controlled_columns,
)
```

Use explicit allowlists instead.

## Reporting Security Issues

Security vulnerabilities should be reported through the repository security process, not public issues. See the root
[`README.md`](../../README.md) and the repository security policy for current reporting links.
