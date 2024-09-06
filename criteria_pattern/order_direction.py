"""
Order direction module.
"""

from enum import StrEnum, unique


@unique
class OrderDirection(StrEnum):
    """
    OrderDirection enum class.
    """

    ASC = 'ASC'
    DESC = 'DESC'
