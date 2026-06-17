---
name: criteria-pattern
description: >-
  Use this skill whenever working with the criteria-pattern Python package or designing criteria-based filtering in
  Python: Criteria, Filter, Operator, Order, Direction, pagination, SQL converters for PostgreSQL, MySQL, MariaDB, and
  SQLite, URL/body converters, allowlist security, injection checks, testing mothers, or package maintenance. Trigger
  even when the user only mentions filters, operators, directions, criteria, query conversion, user-facing search APIs,
  or secure dynamic SQL in a Criteria Pattern project.
compatibility: Codex/Claude-style agent skills. Covers criteria-pattern 4.0.0 on Python 3.11 and newer.
---

# Criteria Pattern

Use this skill to help users build, review, debug, or maintain code that uses the `criteria-pattern` Python package.
Criteria Pattern represents filters, sorting, pagination, and boolean query composition as typed Python objects before
converting them to SQL or request formats.

## Start Here

1. Identify the user's task:
   - Core model usage: read `references/models.md`.
   - Operators or directions: read `references/operators-and-directions.md`.
   - SQL/body/URL conversion: read `references/converters.md`.
   - User-facing input, SQL safety, allowlists, or security review: read `references/security.md`.
   - Tests, examples, fixtures, or object mothers: read `references/testing.md`.
2. Prefer local source and tests when working inside the Criteria Pattern repository. If installed-package behavior is
   uncertain, run `python skills/criteria-pattern/scripts/inspect_criteria_pattern.py` from the repository root or from
   the consuming project.
3. Use public imports first:

```python
from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.converters import CriteriaToPostgresqlConverter
```

4. Keep security checks enabled for any user-controlled request data. Pass explicit `valid_*` allowlists instead of
   disabling checks.

## High-Level API

- `Criteria(filters=None, orders=None, page_size=None, page_number=None)` groups filters, orders, and optional
  pagination.
- `Filter(field, operator, value)` represents one field/operator/value predicate.
- `Order(field, direction)` represents one ordering rule.
- `Operator` has 20 values for equality, comparison, LIKE-style string matching, ranges, null checks, and membership.
- `Direction` has `ASC` and `DESC`.
- Compose criteria with `&`, `|`, and `~`, or named methods `and_()`, `or_()`, and `not_()`.
- `page_size` may be used alone. `page_number` requires `page_size`.

## Converter Choice

Use the converter that matches the user's boundary:

| Need                                   | Converter                       |
| -------------------------------------- | ------------------------------- |
| PostgreSQL SELECT SQL                  | `CriteriaToPostgresqlConverter` |
| MySQL SELECT SQL                       | `CriteriaToMysqlConverter`      |
| MariaDB SELECT SQL                     | `CriteriaToMariadbConverter`    |
| SQLite SELECT SQL                      | `CriteriaToSqliteConverter`     |
| Decoded JSON-like body to `Criteria`   | `BodyToCriteriaConverter`       |
| Bracketed URL query to `Criteria`      | `UrlToCriteriaConverter`        |
| Compact suffix URL query to `Criteria` | `SimpleUrlToCriteriaConverter`  |

SQL converters return `(query, parameters)`. PostgreSQL and SQLite return named-parameter dictionaries; MySQL and
MariaDB return positional parameter lists.

## Secure Production Recipe

For public APIs:

1. Parse request data with `BodyToCriteriaConverter`, `UrlToCriteriaConverter`, or `SimpleUrlToCriteriaConverter`.
2. Map public names to internal names with `fields_mapping`.
3. Validate fields, operators, directions, and pagination bounds with explicit allowlists.
4. Convert to SQL with table, column, criteria, operator, direction, and pagination validation still enabled.
5. Pass the returned SQL and parameters to the database driver. Do not interpolate filter values into SQL strings.

```python
from criteria_pattern import Direction, Operator
from criteria_pattern.converters import BodyToCriteriaConverter, CriteriaToPostgresqlConverter

criteria = BodyToCriteriaConverter.convert(
    body={
        'filters': [{'field': 'q', 'operator': 'contains', 'value': 'Doe'}],
        'orders': [{'field': 'created', 'direction': 'DESC'}],
        'page_size': 20,
        'page_number': 1,
    },
    fields_mapping={'q': 'name', 'created': 'created_at'},
    valid_fields=['name', 'created_at'],
    valid_operators=[Operator.CONTAINS],
    valid_directions=[Direction.DESC],
    max_page_size=100,
    max_page_number=1000,
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

## Important Defaults

- Converter validation flags default to `True`.
- Omitted or empty `valid_fields`, `valid_columns`, `valid_operators`, and `valid_directions` deny everything for that
  dimension when the corresponding check is enabled.
- SQL `valid_tables` defaults to `[table]` when omitted.
- Request converters default to maximum 100 filters, 100 orders, 100 `IN` values, page size 1000, and page number 10000.
- SQL converters default to boolean composition depth 32, 100 `IN` values, page size 1000, page number 10000, and
  operator allowlist size `len(Operator)`.
- LIKE-style values escape `%`, `_`, and backslash and generated SQL includes `ESCAPE '\'`.
