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

from value_object_pattern.models import BaseModel

from .filter import Filter
from .filters import Filters
from .order import Order
from .orders import Orders


class Criteria(BaseModel):
    """
    Criteria class.

    Example:
    ```python
    from criteria_pattern import Criteria, Filter, Operator

    criteria = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='John')])
    print(criteria)
    # >>> Criteria(filters=[Filter(field='name', operator=EQUAL, value='John')], orders=[])
    ```
    """

    _filters: Filters
    _orders: Orders

    def __init__(self, *, filters: list[Filter[Any]], orders: list[Order] | None = None) -> None:
        """
        Criteria constructor.

        Args:
            filters (list[Filter[Any]]): List of filters.
            orders (list[Order], optional): List of orders. Defaults to [].

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator

        criteria = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='John')])
        print(criteria)
        # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='John'))], orders=[])
        ```
        """  # noqa: E501
        self._filters = Filters(value=filters)
        self._orders = Orders(value=orders if orders is not None else [])

    def __and__(self, criteria: Criteria) -> AndCriteria:
        """
        Combine two criteria with AND operator. It merges the filters from both criteria into a single Criteria object.

        Args:
            criteria (Criteria): Another criteria.

        Returns:
            AndCriteria: Combined criteria.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator

        filter1 = Filter(field='name', operator=Operator.EQUAL, value='John')
        filter2 = Filter(field='age', operator=Operator.GREATER, value=18)

        criteria1 = Criteria(filters=[filter1])
        criteria2 = Criteria(filters=[filter2])

        # both are equivalent
        criteria3 = criteria1 & criteria2
        criteria3 = criteria1.and_(criteria=criteria2)
        print(criteria3)
        # >>> AndCriteria(left=Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='John'))], orders=[]), right=Criteria(filters=[Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER: 'GREATER'>), value=FilterValue(value=18))], orders=[]))
        ```
        """  # noqa: E501
        return AndCriteria(left=self, right=criteria)

    def and_(self, *, criteria: Criteria) -> AndCriteria:
        """
        Combine two criteria with AND operator.

        Args:
            criteria (Criteria): Another criteria.

        Returns:
            AndCriteria: Combined criteria.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator

        filter1 = Filter(field='name', operator=Operator.EQUAL, value='John')
        filter2 = Filter(field='age', operator=Operator.GREATER, value=18)

        criteria1 = Criteria(filters=[filter1])
        criteria2 = Criteria(filters=[filter2])

        # both are equivalent
        criteria3 = criteria1 & criteria2
        criteria3 = criteria1.and_(criteria=criteria2)
        print(criteria3)
        # >>> AndCriteria(left=Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='John'))], orders=[]), right=Criteria(filters=[Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER: 'GREATER'>), value=FilterValue(value=18))], orders=[]))
        ```
        """  # noqa: E501
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
        from criteria_pattern import Criteria, Filter, Operator

        filter1 = Filter(field='name', operator=Operator.EQUAL, value='John')
        filter2 = Filter(field='age', operator=Operator.GREATER, value=18)

        criteria1 = Criteria(filters=[filter1])
        criteria2 = Criteria(filters=[filter2])

        # both are equivalent
        criteria3 = criteria1 | criteria2
        criteria3 = criteria1.or_(criteria=criteria2)
        print(criteria3)
        # >>> OrCriteria(left=Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='John'))], orders=[]), right=Criteria(filters=[Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER: 'GREATER'>), value=FilterValue(value=18))], orders=[]))
        ```
        """  # noqa: E501
        return OrCriteria(left=self, right=criteria)

    def or_(self, *, criteria: Criteria) -> OrCriteria:
        """
        Combine two criteria with OR operator.

        Args:
            criteria (Criteria): Another criteria.

        Returns:
            OrCriteria: Combined criteria.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator

        filter1 = Filter(field='name', operator=Operator.EQUAL, value='John')
        filter2 = Filter(field='age', operator=Operator.GREATER, value=18)

        criteria1 = Criteria(filters=[filter1])
        criteria2 = Criteria(filters=[filter2])

        # both are equivalent
        criteria3 = criteria1 | criteria2
        criteria3 = criteria1.or_(criteria=criteria2)
        print(criteria3)
        # >>> OrCriteria(left=Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='John'))], orders=[]), right=Criteria(filters=[Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER: 'GREATER'>), value=FilterValue(value=18))], orders=[]))
        ```
        """  # noqa: E501
        return self | criteria

    def __invert__(self) -> NotCriteria:
        """
        Negate the criteria.

        Returns:
            NotCriteria: Negated criteria.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator

        filter = Filter(field='name', operator=Operator.EQUAL, value='John')
        criteria = Criteria(filters=[filter])

        # both are equivalent
        not_criteria = ~criteria
        not_criteria = criteria.not_()
        print(not_criteria)
        # >>> NotCriteria(criteria=Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='John'))], orders=[]))
        ```
        """  # noqa: E501
        return NotCriteria(criteria=self)

    def not_(self) -> NotCriteria:
        """
        Negate the criteria.

        Returns:
            NotCriteria: Negated criteria.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator

        filter = Filter(field='name', operator=Operator.EQUAL, value='John')
        criteria = Criteria(filters=[filter])

        # both are equivalent
        not_criteria = ~criteria
        not_criteria = criteria.not_()
        print(not_criteria)
        # >>> NotCriteria(criteria=Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='John'))], orders=[]))
        ```
        """  # noqa: E501
        return ~self

    @property
    def filters(self) -> list[Filter[Any]]:
        """
        Get criteria filters.

        Returns:
           list[Filter[Any]]: List of filters.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator

        criteria = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='John')])
        print(criteria.filters)
        # >>> [Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='John'))]
        ```
        """  # noqa: E501
        return self._filters.value

    @property
    def orders(self) -> list[Order]:
        """
        Get criteria orders.

        Returns:
            list[Order]: List of orders.

        Example:
        ```python
        from criteria_pattern import Criteria, Direction, Filter, Operator, Order

        criteria = Criteria(
            filters=[Filter(field='name', operator=Operator.EQUAL, value='John')],
            orders=[Order(field='name', direction=Direction.ASC)],
        )
        print(criteria.orders)
        # >>> [Order(direction=OrderDirection(value=<Direction.ASC: 'ASC'>), field=OrderField(value='name'))]
        ```
        """
        return self._orders.value

    def has_filters(self) -> bool:
        """
        Check if criteria has filters.

        Returns:
            bool: True if criteria has filters, False otherwise.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator

        criteria = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='John')])
        print(criteria.has_filters())
        # >>> True
        ```
        """
        return bool(self.filters)

    def has_orders(self) -> bool:
        """
        Check if criteria has orders.

        Returns:
            bool: True if criteria has orders, False otherwise.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator

        criteria = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='John')])
        print(criteria.has_orders())
        # >>> False
        ```
        """
        return bool(self.orders)


class AndCriteria(Criteria):
    """
    AndCriteria class to handle AND logic.

    ***This class is not intended to be used directly. Use the `&` operator on Criteria objects instead.***
    """

    _left: Criteria
    _right: Criteria

    def __init__(self, *, left: Criteria, right: Criteria) -> None:
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
        return f'{self.__class__.__name__}(left={self._left!r}, right={self._right!r})'

    @override
    def __str__(self) -> str:
        """
        Get string representation of AndCriteria.

        Returns:
            str: String representation of AndCriteria.
        """
        return f'{self.__class__.__name__}(left={self._left}, right={self._right})'

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
        return self.left.orders + self.right.orders

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

    ***This class is not intended to be used directly. Use the `|` operator on Criteria objects instead.***
    """

    _left: Criteria
    _right: Criteria

    def __init__(self, *, left: Criteria, right: Criteria) -> None:
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
        return f'{self.__class__.__name__}(left={self._left!r}, right={self._right!r})'

    @override
    def __str__(self) -> str:
        """
        Get string representation of OrCriteria.

        Returns:
            str: String representation of OrCriteria.
        """
        return f'{self.__class__.__name__}(left={self._left}, right={self._right})'

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
        return self.left.orders + self.right.orders

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

    ***This class is not intended to be used directly. Use the `~` operator on Criteria objects instead.***
    """

    _criteria: Criteria

    def __init__(self, *, criteria: Criteria) -> None:
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
        return f'{self.__class__.__name__}(criteria={self._criteria!r})'

    @override
    def __str__(self) -> str:
        """
        Get string representation of NotCriteria.

        Returns:
            str: String representation of NotCriteria.
        """
        return f'{self.__class__.__name__}(criteria={self._criteria})'

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
        Get filters.

        Returns:
            list[Filter[Any]]: List of filters.
        """
        return self.criteria.filters

    @property
    @override
    def orders(self) -> list[Order]:
        """
        Get orders.

        Returns:
            list[Order]: List of orders.
        """
        return self.criteria.orders
