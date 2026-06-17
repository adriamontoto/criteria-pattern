# Converters

Converters live under `criteria_pattern.converters`:

```python
from criteria_pattern.converters import (
    BodyToCriteriaConverter,
    CriteriaToMariadbConverter,
    CriteriaToMysqlConverter,
    CriteriaToPostgresqlConverter,
    CriteriaToSqliteConverter,
    SimpleUrlToCriteriaConverter,
    UrlToCriteriaConverter,
)
```

## SQL Converters

All SQL converters produce `SELECT` statements and preserve `AND`, `OR`, and `NOT` criteria composition.

| Converter | Placeholder style | Parameters | Identifier quoting |
| --- | --- | --- | --- |
| `CriteriaToPostgresqlConverter` | `%(parameter_0)s` | `dict[str, Any]` | double quotes for table/column identifiers |
| `CriteriaToMysqlConverter` | `%s` | `list[Any]` | backticks for table/column identifiers |
| `CriteriaToMariadbConverter` | `%s` | `list[Any]` | inherits MySQL behavior |
| `CriteriaToSqliteConverter` | `:parameter_0` | `dict[str, Any]` | double quotes for table/column identifiers |

SQL converter signature shape:

```python
query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=criteria,
    table='users',
    columns=None,
    columns_mapping=None,
    check_table_injection=True,
    check_column_injection=True,
    check_criteria_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
    valid_tables=None,
    valid_columns=None,
    valid_operators=None,
    valid_directions=None,
    max_page_size=1000,
    max_page_number=10000,
    max_criteria_depth=32,
    max_in_values=100,
    max_operator_allowlist=len(Operator),
)
```

`columns` defaults to `['*']`. `'*'` skips selected-column allowlist validation, but criteria fields and order fields
still need `valid_columns` when criteria validation is enabled.

`columns_mapping` maps criteria field names to SQL column names during SQL rendering. Criteria validation checks fields
after applying `columns_mapping`, so `valid_columns` must contain the SQL column names that will appear in the query.

### SQL Example

```python
from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.converters import CriteriaToPostgresqlConverter

criteria = Criteria(
    filters=[Filter(field='name', operator=Operator.CONTAINS, value='Doe')],
    orders=[Order(field='created_at', direction=Direction.DESC)],
    page_size=20,
    page_number=1,
)

query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=criteria,
    table='users',
    columns=['id', 'name', 'created_at'],
    valid_tables=['users'],
    valid_columns=['id', 'name', 'created_at'],
    valid_operators=[Operator.CONTAINS],
    valid_directions=[Direction.DESC],
    max_page_size=100,
    max_page_number=1000,
)
```

## BodyToCriteriaConverter

Use `BodyToCriteriaConverter` for decoded mappings, usually JSON request bodies.

Accepted top-level keys:

- `filters`
- `orders`
- `page_size`
- `page_number`

Signature shape:

```python
criteria = BodyToCriteriaConverter.convert(
    body=body,
    fields_mapping=None,
    operator_mapping=None,
    check_field_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
    valid_fields=None,
    valid_operators=None,
    valid_directions=None,
    max_page_size=1000,
    max_page_number=10000,
    max_filters=100,
    max_orders=100,
    max_in_values=100,
    max_operator_allowlist=len(Operator),
)
```

Example body:

```python
body = {
    'filters': [
        {'field': 'full_name', 'operator': 'contains', 'value': 'Doe'},
        {'field': 'status', 'operator': 'IN', 'value': ['ACTIVE', 'PENDING']},
    ],
    'orders': [{'field': 'created_at', 'direction': 'DESC'}],
    'page_size': 20,
    'page_number': 1,
}
```

`fields_mapping` is applied before validation, so `valid_fields` should contain mapped internal names.

## UrlToCriteriaConverter

Use `UrlToCriteriaConverter` for explicit bracketed URL query parameters:

```text
filters[0][field]=name
filters[0][operator]=CONTAINS
filters[0][value]=Doe
orders[0][field]=created_at
orders[0][direction]=DESC
page_size=20
page_number=1
```

Signature shape is like the body converter except there is no `operator_mapping`:

```python
criteria = UrlToCriteriaConverter.convert(
    url=url,
    fields_mapping=None,
    check_field_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
    valid_fields=None,
    valid_operators=None,
    valid_directions=None,
    max_page_size=1000,
    max_page_number=10000,
    max_filters=100,
    max_orders=100,
    max_in_values=100,
    max_operator_allowlist=len(Operator),
)
```

Values are parsed into Python primitives where possible: booleans, `null`/`none`, integers, and floats. `BETWEEN` and
`NOT_BETWEEN` expect exactly two comma-separated values. `IN` and `NOT_IN` expect at least one value.

## SimpleUrlToCriteriaConverter

Use `SimpleUrlToCriteriaConverter` for compact public query formats where each non-pagination parameter becomes a
filter. It accepts a full URL or bare query string.

```python
criteria = SimpleUrlToCriteriaConverter.convert(
    url='name=Doe&age_gte=18&page_size=20&page_number=1',
    valid_fields=['name', 'age'],
    valid_operators=[Operator.EQUAL, Operator.GREATER_OR_EQUAL],
)
```

Signature shape:

```python
criteria = SimpleUrlToCriteriaConverter.convert(
    url=url,
    fields_mapping=None,
    suffix_operator_mapping=None,
    check_field_injection=True,
    check_operator_injection=True,
    check_pagination_bounds=True,
    valid_fields=None,
    valid_operators=None,
    max_page_size=1000,
    max_page_number=10000,
    max_filters=100,
    max_in_values=100,
    max_operator_allowlist=len(Operator),
)
```

This converter does not parse orders. Use `UrlToCriteriaConverter` or `BodyToCriteriaConverter` when clients must choose
ordering.

Repeated parameters and comma-separated values can both produce list/range values:

```text
status_in=ACTIVE,PENDING
category_not_in=deprecated&category_not_in=archived
price_between=10,100
```

## Pagination Output

SQL converters render:

- `LIMIT` when `criteria.has_page_size()` is true.
- `OFFSET` when `criteria.has_pagination()` is true.
- `OFFSET` value as `page_size * (page_number - 1)`.

PostgreSQL and SQLite add limit/offset as named parameters. MySQL and MariaDB append them to the positional parameter
list.
