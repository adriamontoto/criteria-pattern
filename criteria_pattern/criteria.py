"""
This module contains the Criteria class.
"""

from __future__ import annotations

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import Any

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

    def __invert__(self) -> NotCriteria:
        """
        Negate the criteria.

        Returns:
            NotCriteria: Negated criteria.

        Example:
        ```python
        criteria = Criteria(filters=[filter1])

        # both are equivalent
        not_criteria = ~criteria
        not_criteria = criteria.not_()
        ```
        """
        return NotCriteria(criteria=self)

    def not_(self) -> NotCriteria:
        """
        Negate the criteria.

        Returns:
            NotCriteria: Negated criteria.

        Example:
        ```python
        criteria = Criteria(filters=[filter1])

        # both are equivalent
        not_criteria = criteria.not_()
        not_criteria = ~criteria
        ```
        """
        return ~self

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

    def has_filters(self) -> bool:
        """
        Check if criteria has filters.

        Returns:
            bool: True if criteria has filters, False otherwise.
        """
        return bool(self.filters)

    def has_orders(self) -> bool:
        """
        Check if criteria has orders.

        Returns:
            bool: True if criteria has orders, False otherwise.
        """
        return bool(self.orders)


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
        return self.left.filters + self.right.filters

    @property
    @override
    def orders(self) -> list[Order]:
        """
        Get orders, only left criteria orders are returned.

        Returns:
            list[Order]: List of orders.
        """
        return self.left.orders

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
        return self.left.filters + self.right.filters

    @property
    @override
    def orders(self) -> list[Order]:
        """
        Get orders, only left criteria orders are returned.

        Returns:
            list[Order]: List of orders.
        """
        return self.left.orders

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


class NotCriteria(Criteria):
    """
    NotCriteria class to handle NOT logic.
    """

    _criteria: Criteria

    def __init__(self, criteria: Criteria) -> None:
        """
        NotCriteria constructor.

        Args:
            criteria (Criteria): Criteria to negate.
        """
        self._criteria = criteria

    @override
    def __repr__(self) -> str:
        """
        Get string representation of NotCriteria.

        Returns:
            str: String representation of NotCriteria.
        """
        return f'<NotCriteria(criteria={self._criteria})>'

    @property
    def criteria(self) -> Criteria:
        """
        Get criteria.

        Returns:
            Criteria: Criteria to negate.
        """
        return self._criteria

    @property
    @override
    def filters(self) -> list[Filter[Any]]:
        """
        Get negated filters.

        Returns:
            list[Filter[Any]]: List of negated filters.
        """
        return self._criteria.filters

    @property
    @override
    def orders(self) -> list[Order]:
        """
        Get orders.

        Returns:
            list[Order]: List of orders.
        """
        return self._criteria.orders
