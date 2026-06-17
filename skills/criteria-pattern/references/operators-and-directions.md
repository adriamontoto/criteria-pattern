# Operators And Directions

Import operators and directions from the root package:

```python
from criteria_pattern import Direction, Operator
```

## Operators

`Operator` is a `StrEnum` with exactly 20 values in criteria-pattern 4.0.0.

| Operator | Value shape | SQL meaning |
| --- | --- | --- |
| `Operator.EQUAL` | scalar | `=` |
| `Operator.NOT_EQUAL` | scalar | `!=` |
| `Operator.GREATER` | scalar | `>` |
| `Operator.GREATER_OR_EQUAL` | scalar | `>=` |
| `Operator.LESS` | scalar | `<` |
| `Operator.LESS_OR_EQUAL` | scalar | `<=` |
| `Operator.LIKE` | scalar pattern | `LIKE value ESCAPE '\'` |
| `Operator.NOT_LIKE` | scalar pattern | `NOT LIKE value ESCAPE '\'` |
| `Operator.CONTAINS` | scalar | `LIKE '%value%' ESCAPE '\'` |
| `Operator.NOT_CONTAINS` | scalar | `NOT LIKE '%value%' ESCAPE '\'` |
| `Operator.STARTS_WITH` | scalar | `LIKE 'value%' ESCAPE '\'` |
| `Operator.NOT_STARTS_WITH` | scalar | `NOT LIKE 'value%' ESCAPE '\'` |
| `Operator.ENDS_WITH` | scalar | `LIKE '%value' ESCAPE '\'` |
| `Operator.NOT_ENDS_WITH` | scalar | `NOT LIKE '%value' ESCAPE '\'` |
| `Operator.BETWEEN` | exactly two values | `BETWEEN start AND end` |
| `Operator.NOT_BETWEEN` | exactly two values | `NOT BETWEEN start AND end` |
| `Operator.IS_NULL` | ignored; use `None` | `IS NULL` |
| `Operator.IS_NOT_NULL` | ignored; use `None` | `IS NOT NULL` |
| `Operator.IN` | one or more values | `IN (...)` |
| `Operator.NOT_IN` | one or more values | `NOT IN (...)` |

The base `Filter` model stores the value as supplied. Request converters normalize value shapes for range, list, null,
boolean, numeric, and null-like strings.

## Direction

`Direction` is a `StrEnum` with:

| Direction | Meaning |
| --- | --- |
| `Direction.ASC` | Ascending order |
| `Direction.DESC` | Descending order |

## Request Converter Aliases

`BodyToCriteriaConverter` accepts case-insensitive aliases such as:

| Input alias | Parsed operator |
| --- | --- |
| `EQUAL`, `EQ` | `Operator.EQUAL` |
| `NOT_EQUAL`, `NE` | `Operator.NOT_EQUAL` |
| `GREATER`, `GREATER_THAN`, `GT` | `Operator.GREATER` |
| `GREATER_OR_EQUAL`, `GREATER_THAN_OR_EQUAL`, `GREATER_THAN_OR_EQUALS`, `GREATER_EQUAL`, `GTE`, `GE` | `Operator.GREATER_OR_EQUAL` |
| `LESS`, `LESS_THAN`, `LT` | `Operator.LESS` |
| `LESS_OR_EQUAL`, `LESS_THAN_OR_EQUAL`, `LESS_THAN_OR_EQUALS`, `LESS_EQUAL`, `LTE`, `LE` | `Operator.LESS_OR_EQUAL` |
| `LIKE`, `NOT_LIKE` | LIKE operators |
| `CONTAINS`, `NOT_CONTAINS` | Contains operators |
| `STARTS_WITH`, `NOT_STARTS_WITH` | Prefix operators |
| `ENDS_WITH`, `NOT_ENDS_WITH` | Suffix operators |
| `BETWEEN`, `NOT_BETWEEN` | Range operators |
| `IS_NULL`, `IS_NOT_NULL` | Null operators |
| `IN`, `NOT_IN` | List operators |

Directions accept `ASC` and `DESC`, case-insensitively.

`BodyToCriteriaConverter.convert(..., operator_mapping={...})` can add aliases or override existing aliases before
validation. Use this when an API wants public words such as `after` mapped to `Operator.GREATER`.

## Simple URL Suffixes

`SimpleUrlToCriteriaConverter` maps query parameter suffixes:

| Suffix | Operator |
| --- | --- |
| no suffix, `_eq` | `Operator.EQUAL` |
| `_ne` | `Operator.NOT_EQUAL` |
| `_gt` | `Operator.GREATER` |
| `_ge`, `_gte` | `Operator.GREATER_OR_EQUAL` |
| `_lt` | `Operator.LESS` |
| `_le`, `_lte` | `Operator.LESS_OR_EQUAL` |
| `_like`, `_not_like` | LIKE operators |
| `_contains`, `_not_contains` | Contains operators |
| `_starts_with`, `_not_starts_with` | Prefix operators |
| `_ends_with`, `_not_ends_with` | Suffix operators |
| `_between`, `_not_between` | Range operators |
| `_is_null`, `_is_not_null` | Null operators |
| `_in`, `_not_in` | List operators |

`suffix_operator_mapping` can add or override suffix behavior.
