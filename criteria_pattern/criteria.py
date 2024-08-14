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

    _filters: list[Filter[T]]

    def __init__(self, filters: list[Filter[T]]) -> None:
        """
        Criteria constructor.

        Args:
            filters (List[Filter]): List of filters.
        """
        self._filters = filters

    @override
    def __repr__(self) -> str:
        """
        Get string representation of Criteria.

        Returns:
            str: String representation of Criteria.
        """
        return f'<Criteria(filters={self._filters})>'

    def __and__(self, criteria: Criteria[T]) -> AndCriteria[T]:
        """
        Combine two criteria with AND operator. It merges the filters from both criteria into a single Criteria object.

        Args:
            criteria (Criteria): Another criteria.

        Returns:
            AndCriteria: Combined criteria.

        Example:
        ```python
        criteria1 = Criteria(filters=[filter1])
        criteria2 = Criteria(filters=[filter2])

        # both are equivalent
        criteria3 = criteria1 & criteria2
        criteria3 = Criteria(filters=[filter1, filter2])
        ```
        """
        return AndCriteria(left=self, right=criteria)

    def add_(self, criteria: Criteria[T]) -> AndCriteria[T]:
        """
        Combine two criteria with AND operator.

        Args:
            criteria (Criteria): Another criteria.

        Returns:
            AndCriteria: Combined criteria.

        Example:
        ```python
        criteria1 = Criteria(filters=[filter1])
        criteria2 = Criteria(filters=[filter2])

        # both are equivalent
        criteria3 = criteria1.add_(criteria=criteria2)
        criteria3 = Criteria(filters=[filter1, filter2])
        ```
        """
        return self & criteria

    def __or__(self, criteria: Criteria[T]) -> OrCriteria[T]:
        """
        Combine two criteria with OR operator. It merges the filters from both criteria into a single Criteria object.

        Args:
            criteria (Criteria): Another criteria.

        Returns:
            OrCriteria: Combined criteria.

        Example:
        ```python
        criteria1 = Criteria(filters=[filter1])
        criteria2 = Criteria(filters=[filter2])

        # both are equivalent
        criteria3 = criteria1 | criteria2
        criteria3 = criteria1.or_(criteria=criteria2)
        ```
        """
        return OrCriteria(left=self, right=criteria)

    def or_(self, criteria: Criteria[T]) -> OrCriteria[T]:
        """
        Combine two criteria with OR operator.

        Args:
            criteria (Criteria): Another criteria.

        Returns:
            OrCriteria: Combined criteria.

        Example:
        ```python
        criteria1 = Criteria(filters=[filter1])
        criteria2 = Criteria(filters=[filter2])

        # both are equivalent
        criteria3 = criteria1 | criteria2
        criteria3 = criteria1.or_(criteria=criteria2)
        ```
        """
        return self | criteria

    @property
    def filters(self) -> list[Filter[T]]:
        """
        Get filters.

        Returns:
            List[Filter]: List of filters.
        """
        return self._filters


class AndCriteria(Criteria[T]):
    """
    AndCriteria class to handle AND logic.
    """

    _left: Criteria[T]
    _right: Criteria[T]

    def __init__(self, left: Criteria[T], right: Criteria[T]) -> None:
        """
        AndCriteria constructor.

        Args:
            left (Criteria): Left criteria.
            right (Criteria): Right criteria.
        """
        self._left = left
        self._right = right

    @override
    def __repr__(self) -> str:
        """
        Get string representation of AndCriteria.

        Returns:
            str: String representation of AndCriteria.
        """
        return f'<AndCriteria(left={self._left}, right={self._right})>'

    @property
    @override
    def filters(self) -> list[Filter[T]]:
        """
        Get filters.

        Returns:
            List[Filter]: List of filters.
        """
        return self.left._filters + self.right._filters

    @property
    def left(self) -> Criteria[T]:
        """
        Get left criteria.

        Returns:
            Criteria: Left criteria.
        """
        return self._left

    @property
    def right(self) -> Criteria[T]:
        """
        Get right criteria.

        Returns:
            Criteria: Right criteria.
        """
        return self._right


class OrCriteria(Criteria[T]):
    """
    OrCriteria class to handle OR logic.
    """

    _left: Criteria[T]
    _right: Criteria[T]

    def __init__(self, left: Criteria[T], right: Criteria[T]) -> None:
        """
        OrCriteria constructor.

        Args:
            left (Criteria): Left criteria.
            right (Criteria): Right criteria.
        """
        self._left = left
        self._right = right

    @override
    def __repr__(self) -> str:
        """
        Get string representation of OrCriteria.

        Returns:
            str: String representation of OrCriteria.
        """
        return f'<OrCriteria(left={self._left}, right={self._right})>'

    @property
    @override
    def filters(self) -> list[Filter[T]]:
        """
        Get filters.

        Returns:
            List[Filter]: List of filters.
        """
        return self.left._filters + self.right._filters

    @property
    def left(self) -> Criteria[T]:
        """
        Get left criteria.

        Returns:
            Criteria: Left criteria.
        """
        return self._left

    @property
    def right(self) -> Criteria[T]:
        """
        Get right criteria.

        Returns:
            Criteria: Right criteria.
        """
        return self._right
