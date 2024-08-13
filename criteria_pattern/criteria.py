"""
This module contains the Criteria class.
"""

from __future__ import annotations

from typing import Generic, TypeVar
from typing_extensions import override

from .filter import Filter

T = TypeVar('T')


class Criteria(Generic[T]):
    """
    Criteria class.
    """

    __filters: list[Filter[T]]

    def __init__(self, filters: list[Filter[T]]) -> None:
        """
        Criteria constructor.

        Args:
            filters (List[Filter]): List of filters.
        """
        self.__filters = filters

    @override
    def __repr__(self) -> str:
        """
        Get string representation of Criteria.

        Returns:
            str: String representation of Criteria.
        """
        return f'<Criteria(filters={self.__filters})>'

    @property
    def filters(self) -> list[Filter[T]]:
        """
        Get filters.

        Returns:
            List[Filter]: List of filters.
        """
        return self.__filters
