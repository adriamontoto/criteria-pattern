"""
Filter operators supported by Criteria Pattern converters.
"""

from enum import StrEnum, unique


@unique
class Operator(StrEnum):
    """
    Enumerate all comparison operators supported by filters.

    SQL converters translate these values into the dialect-specific predicates and parameter bindings. Range operators
    expect two values, list operators expect one or more values, and null operators ignore the filter value.

    Example:
    ```python
    from criteria_pattern import Operator

    operator = Operator.EQUAL
    print(operator)
    # >>> EQUAL
    ```
    """

    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    GREATER = 'GREATER'
    GREATER_OR_EQUAL = 'GREATER_OR_EQUAL'
    LESS = 'LESS'
    LESS_OR_EQUAL = 'LESS_OR_EQUAL'
    LIKE = 'LIKE'
    NOT_LIKE = 'NOT_LIKE'
    CONTAINS = 'CONTAINS'  # LIKE '%value%'
    NOT_CONTAINS = 'NOT_CONTAINS'  # NOT LIKE '%value%'
    STARTS_WITH = 'STARTS_WITH'  # LIKE 'value%'
    NOT_STARTS_WITH = 'NOT_STARTS_WITH'  # NOT LIKE 'value%'
    ENDS_WITH = 'ENDS_WITH'  # LIKE '%value'
    NOT_ENDS_WITH = 'NOT_ENDS_WITH'  # NOT LIKE '%value'
    BETWEEN = 'BETWEEN'
    NOT_BETWEEN = 'NOT_BETWEEN'
    IS_NULL = 'IS_NULL'
    IS_NOT_NULL = 'IS_NOT_NULL'
    IN = 'IN'
    NOT_IN = 'NOT_IN'
