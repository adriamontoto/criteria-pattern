"""
Filter operator module.
"""

from enum import StrEnum


class FilterOperator(StrEnum):
    """
    FilterOperator enum class.
    """

    EQUAL = '='
    NOT_EQUAL = '!='
    GREATER = '>'
    GREATER_OR_EQUAL = '>='
    LESS = '<'
    LESS_OR_EQUAL = '<='
    LIKE = 'LIKE'
    NOT_LIKE = 'NOT LIKE'
    IN = 'IN'
    NOT_IN = 'NOT IN'
    IS_NULL = 'IS NULL'
    IS_NOT_NULL = 'IS NOT NULL'
    BETWEEN = 'BETWEEN'
    NOT_BETWEEN = 'NOT BETWEEN'
    CONTAINS = 'LIKE'
    NOT_CONTAINS = 'NOT LIKE'
    STARTS_WITH = 'LIKE'
    ENDS_WITH = 'LIKE'
