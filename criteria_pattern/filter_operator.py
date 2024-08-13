"""
Filter operator module.
"""

from enum import StrEnum, unique


@unique
class FilterOperator(StrEnum):
    """
    FilterOperator enum class.
    """

    EQUAL = 'eq'
    NOT_EQUAL = 'neq'
    GREATER = 'gt'
    GREATER_OR_EQUAL = 'gte'
    LESS = 'lt'
    LESS_OR_EQUAL = 'lte'
    LIKE = 'like'
    IN = 'in'
    NOT_IN = 'nin'
    IS_NULL = 'is_null'
    IS_NOT_NULL = 'is_not_null'
    BETWEEN = 'between'
    NOT_BETWEEN = 'not_between'
    NOT_CONTAINS = 'not_contains'
    STARTS_WITH = 'starts_with'
    ENDS_WITH = 'ends_with'
    CONTAINS = 'contains'
