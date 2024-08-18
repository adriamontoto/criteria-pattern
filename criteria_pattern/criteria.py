"""
This module contains the Criteria class.
"""

from __future__ import annotations

from typing import Any, override

from .filter import Filter
from .order import Order


class Criteria:
    """
    Criteria class.
    """

    _filters: list[Filter[Any]]
    _orders: list[Order]

    def __init__(self, filters: list[Filter[Any]], orders: list[Order] | None = None) -> None:
        """
        Criteria constructor.

        Args:
            filters (List[Filter[Any]]): List of filters.
            sort (List[Order], optional): List of orders. Defaults to [].
        """
        self._filters = filters
        self._orders = orders or []

    @override
    def __repr__(self) -> str:
        """
        Get string representation of Criteria.

        Returns:
            str: String representation of Criteria.
        """
        return f'<Criteria(filters={self._filters}, orders={self._orders})>'

    def __and__(self, criteria: Criteria) -> AndCriteria:
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

    def and_(self, criteria: Criteria) -> AndCriteria:
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

    def __or__(self, criteria: Criteria) -> OrCriteria:
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

    def or_(self, criteria: Criteria) -> OrCriteria:
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
    def filters(self) -> list[Filter[Any]]:
        """
        Get filters.

        Returns:
           list[Filter[Any]]: List of filters.
        """
        return self._filters

    @property
    def orders(self) -> list[Order]:
        """
        Get orders.

        Returns:
            list[Order]: List of orders.
        """
        return self._orders


class AndCriteria(Criteria):
    """
    AndCriteria class to handle AND logic.
    """

    _left: Criteria
    _right: Criteria

    def __init__(self, left: Criteria, right: Criteria) -> None:
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
    def filters(self) -> list[Filter[Any]]:
        """
        Get filters.

        Returns:
            list[Filter[Any]]: List of filters.
        """
        return self.left._filters + self.right._filters

    @property
    def orders(self) -> list[Order]:
        """
        Get orders, only left criteria orders are returned.

        Returns:
            list[Order]: List of orders.
        """
        return self.left._orders

    @property
    def left(self) -> Criteria:
        """
        Get left criteria.

        Returns:
            Criteria: Left criteria.
        """
        return self._left

    @property
    def right(self) -> Criteria:
        """
        Get right criteria.

        Returns:
            Criteria: Right criteria.
        """
        return self._right


class OrCriteria(Criteria):
    """
    OrCriteria class to handle OR logic.
    """

    _left: Criteria
    _right: Criteria

    def __init__(self, left: Criteria, right: Criteria) -> None:
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
    def filters(self) -> list[Filter[Any]]:
        """
        Get filters.

        Returns:
            list[Filter[Any]]: List of filters.
        """
        return self.left._filters + self.right._filters

    @property
    @override
    def orders(self) -> list[Order]:
        """
        Get orders, only left criteria orders are returned.

        Returns:
            list[Order]: List of orders.
        """
        return self.left._orders

    @property
    def left(self) -> Criteria:
        """
        Get left criteria.

        Returns:
            Criteria: Left criteria.
        """
        return self._left

    @property
    def right(self) -> Criteria:
        """
        Get right criteria.

        Returns:
            Criteria: Right criteria.
        """
        return self._right
