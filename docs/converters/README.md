# 🔄 Converter Guide

Converters move between `Criteria` objects and external representations: SQL, decoded request bodies and URL query
strings.

## Choosing A Converter

| Need | Converter |
| --- | --- |
| PostgreSQL `SELECT` query | `CriteriaToPostgresqlConverter` |
| MySQL `SELECT` query | `CriteriaToMysqlConverter` |
| MariaDB `SELECT` query | `CriteriaToMariadbConverter` |
| SQLite `SELECT` query | `CriteriaToSqliteConverter` |
| JSON-like decoded body to criteria | `BodyToCriteriaConverter` |
| Explicit bracketed URL query to criteria | `UrlToCriteriaConverter` |
| Compact suffix-based URL query to criteria | `SimpleUrlToCriteriaConverter` |

## SQL Converters

SQL converters return a `(query, parameters)` tuple.

| Converter | Placeholder style | Parameters type | Identifier style |
| --- | --- | --- | --- |
| `CriteriaToPostgresqlConverter` | `%(parameter_0)s` | `dict[str, object]` | quotes table and column identifiers |
| `CriteriaToMysqlConverter` | `%s` | `list[object]` | renders identifiers as provided |
| `CriteriaToMariadbConverter` | `%s` | `list[object]` | inherits MySQL behavior |
| `CriteriaToSqliteConverter` | `:parameter_0` | `dict[str, object]` | quotes table and column identifiers |

```python
from criteria_pattern import Criteria, Filter, Operator
from criteria_pattern.converters import CriteriaToPostgresqlConverter


criteria = Criteria(filters=[Filter(field='name', operator=Operator.CONTAINS, value='Doe')])
query, parameters = CriteriaToPostgresqlConverter.convert(criteria=criteria, table='users')

print(query)
print(parameters)
# >>> SELECT * FROM "users" WHERE "name" LIKE '%%' || %(parameter_0)s || '%%';
# >>> {'parameter_0': 'Doe'}
```

Common SQL converter arguments:

| Argument | Purpose |
| --- | --- |
| `criteria` | Criteria to render |
| `table` | Table name to select from |
| `columns` | Columns to select, defaults to `['*']` |
| `columns_mapping` | Maps criteria field names to SQL column names |
| `valid_tables` | Allowed table names when table validation is enabled |
| `valid_columns` | Allowed column and criteria field names when column/criteria validation is enabled |
| `valid_operators` | Allowed filter operators |
| `valid_directions` | Allowed order directions |
| `max_page_size` | Upper bound for page size when pagination bounds validation is enabled |
| `max_page_number` | Upper bound for page number when pagination bounds validation is enabled |

Validation flags are disabled by default. Enable them for user-facing inputs:

```python
query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=criteria,
    table='users',
    check_table_injection=True,
    check_column_injection=True,
    check_criteria_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
    valid_tables=['users'],
    valid_columns=['id', 'name', 'created_at'],
    valid_operators=[Operator.CONTAINS],
    max_page_size=100,
    max_page_number=1000,
)
```

See the [Security Guide](../security/README.md) for the recommended production flow.

## BodyToCriteriaConverter

Use `BodyToCriteriaConverter` for decoded dictionaries, usually from JSON request bodies.

Accepted top-level keys:

- `filters`
- `orders`
- `page_size`
- `page_number`

```python
from criteria_pattern.converters import BodyToCriteriaConverter


criteria = BodyToCriteriaConverter.convert(
    body={
        'filters': [
            {'field': 'full_name', 'operator': 'contains', 'value': 'Doe'},
            {'field': 'status', 'operator': 'IN', 'value': ['ACTIVE', 'PENDING']},
        ],
        'orders': [{'field': 'created_at', 'direction': 'DESC'}],
        'page_size': 20,
        'page_number': 1,
    },
    fields_mapping={'full_name': 'name'},
)
```

Body operator aliases are intentionally forgiving. Examples include:

| Body operator | Parsed operator |
| --- | --- |
| `EQUAL`, `EQ` | `Operator.EQUAL` |
| `NOT_EQUAL`, `NE` | `Operator.NOT_EQUAL` |
| `GREATER`, `GREATER_THAN`, `GT` | `Operator.GREATER` |
| `GREATER_OR_EQUAL`, `GTE`, `GE` | `Operator.GREATER_OR_EQUAL` |
| `LESS`, `LESS_THAN`, `LT` | `Operator.LESS` |
| `LESS_OR_EQUAL`, `LTE`, `LE` | `Operator.LESS_OR_EQUAL` |
| `CONTAINS`, `STARTS_WITH`, `ENDS_WITH` | Matching string operators |
| `BETWEEN`, `NOT_BETWEEN` | Range operators |
| `IN`, `NOT_IN` | List operators |
| `IS_NULL`, `IS_NOT_NULL` | Null operators |

You can add or override aliases:

```python
from criteria_pattern import Operator
from criteria_pattern.converters import BodyToCriteriaConverter


criteria = BodyToCriteriaConverter.convert(
    body={'filters': [{'field': 'created_at', 'operator': 'after', 'value': '2026-05-18'}]},
    operator_mapping={'after': Operator.GREATER},
)
```

## UrlToCriteriaConverter

Use `UrlToCriteriaConverter` for explicit bracketed query parameters.

```python
from criteria_pattern.converters import UrlToCriteriaConverter


url = (
    'https://api.example.com/users?'
    'filters[0][field]=name&filters[0][operator]=CONTAINS&filters[0][value]=Doe&'
    'orders[0][field]=created_at&orders[0][direction]=DESC&'
    'page_size=20&page_number=1'
)

criteria = UrlToCriteriaConverter.convert(url=url)
```

Supported parameter groups:

- `filters[index][field]`
- `filters[index][operator]`
- `filters[index][value]`
- `orders[index][field]`
- `orders[index][direction]`
- `page_size`
- `page_number`

Values are converted to Python primitives where possible: booleans, `null` / `none`, integers and floats.

## SimpleUrlToCriteriaConverter

Use `SimpleUrlToCriteriaConverter` for compact public query formats where each non-pagination parameter becomes one
filter. It accepts a full URL or a bare query string.

```python
from criteria_pattern.converters import SimpleUrlToCriteriaConverter


criteria = SimpleUrlToCriteriaConverter.convert(url='name=Doe&age_gte=18&page_size=20&page_number=1')
```

Common suffixes:

| Suffix | Operator |
| --- | --- |
| no suffix, `_eq` | `Operator.EQUAL` |
| `_ne` | `Operator.NOT_EQUAL` |
| `_gt`, `_ge`, `_gte`, `_lt`, `_le`, `_lte` | Comparison operators |
| `_like`, `_not_like` | Pattern operators |
| `_contains`, `_not_contains` | Contains operators |
| `_starts_with`, `_not_starts_with` | Prefix operators |
| `_ends_with`, `_not_ends_with` | Suffix operators |
| `_between`, `_not_between` | Range operators |
| `_in`, `_not_in` | List operators |
| `_is_null`, `_is_not_null` | Null operators |

List and range operators can use comma-separated values or repeated query parameters:

```python
criteria = SimpleUrlToCriteriaConverter.convert(url='status_in=ACTIVE,PENDING&price_between=10,100')
```

`SimpleUrlToCriteriaConverter` does not parse orders. Use `UrlToCriteriaConverter` or `BodyToCriteriaConverter` when the
client needs to choose ordering.

## Field Mapping

Request converters use `fields_mapping` to translate public field names into internal names before criteria validation:

```python
criteria = BodyToCriteriaConverter.convert(
    body={'filters': [{'field': 'full_name', 'operator': 'contains', 'value': 'Doe'}]},
    fields_mapping={'full_name': 'name'},
    check_field_injection=True,
    valid_fields=['name'],
)
```

SQL converters use `columns_mapping` to translate criteria fields into SQL column names during rendering:

```python
query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=criteria,
    table='users',
    columns_mapping={'name': 'user_name'},
)
```

For user-facing APIs, prefer mapping in the request converter so the final criteria contains internal field names before
SQL conversion.
