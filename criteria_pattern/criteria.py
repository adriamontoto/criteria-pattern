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

    def __and__(self, criteria: Criteria[T]) -> Criteria[T]:
        """
        Combine two criteria with AND operator. It merges the filters from both criteria into a single Criteria object.

        Args:
            criteria (Criteria): Another criteria.

        Returns:
            Criteria: Combined criteria.

        Example:
        ```python
        criteria1 = Criteria(filters=[filter1])
        criteria2 = Criteria(filters=[filter2])

        # both are equivalent
        criteria3 = criteria1 & criteria2
        criteria3 = Criteria(filters=[filter1, filter2])
        ```
        """
        return Criteria(filters=self.__filters + criteria.filters)

    def add_(self, criteria: Criteria[T]) -> Criteria[T]:
        """
        Combine two criteria with AND operator.

        Args:
            criteria (Criteria): Another criteria.

        Returns:
            Criteria: Combined criteria.

        Example:
        ```python
        criteria1 = Criteria(filters=[filter1])
        criteria2 = Criteria(filters=[filter2])

        # both are equivalent
        criteria3 = criteria1.add_(criteria2)
        criteria3 = Criteria(filters=[filter1, filter2])
        ```
        """
        return self & criteria

    @property
    def filters(self) -> list[Filter[T]]:
        """
        Get filters.

        Returns:
            List[Filter]: List of filters.
        """
        return self.__filters
