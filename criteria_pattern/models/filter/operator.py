"""
Filter operator module.
"""

from enum import StrEnum, unique


@unique
class Operator(StrEnum):
    """
    Operator enum class.

    Example:
    ```python
    from criteria_pattern import Operator

    operator = Operator.EQUAL
    print(operator)
    # >>> EQUAL
    ```
    """

    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT EQUAL'
    GREATER = 'GREATER'
    GREATER_OR_EQUAL = 'GREATER OR EQUAL'
    LESS = 'LESS'
    LESS_OR_EQUAL = 'LESS OR EQUAL'
    LIKE = 'LIKE'
    NOT_LIKE = 'NOT LIKE'
    CONTAINS = 'CONTAINS'  # LIKE '%value%'
    NOT_CONTAINS = 'NOT CONTAINS'  # NOT LIKE '%value%'
    STARTS_WITH = 'STARTS WITH'  # LIKE 'value%'
    NOT_STARTS_WITH = 'NOT STARTS WITH'  # NOT LIKE 'value%'
    ENDS_WITH = 'ENDS WITH'  # LIKE '%value'
    NOT_ENDS_WITH = 'NOT ENDS WITH'  # NOT LIKE '%value'
    BETWEEN = 'BETWEEN'
    NOT_BETWEEN = 'NOT BETWEEN'
    IS_NULL = 'IS NULL'
    IS_NOT_NULL = 'IS NOT NULL'
    IN = 'IN'
    NOT_IN = 'NOT IN'
