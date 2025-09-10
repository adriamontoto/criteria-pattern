"""
OrdersMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import Any

from object_mother_pattern import IntegerMother
from object_mother_pattern.models import BaseMother

from criteria_pattern import Criteria, Filter, Order

from .filter import FilterMother
from .filters_mother import FiltersMother
from .order import OrderMother
from .orders_mother import OrdersMother
from .page_number_mother import PageNumberMother
from .page_size_mother import PageSizeMother


class CriteriaMother(BaseMother[Criteria]):
    """
    CriteriaMother class is responsible for generating random criteria value.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers import CriteriaMother

    criteria = CriteriaMother.create()
    print(criteria)
    # >>> Criteria(filters=[Filter(field=FilterField(value='ThlumotY'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value=6273))], orders=[Order(direction=OrderDirection(value=<Direction.ASC: 'ASC'>), field=OrderField(value='OQnCs6O8JZE'))], page_size=10, page_number=1)
    ```
    """  # noqa: E501

    @classmethod
    @override
    def create(
        cls,
        *,
        value: Criteria | None = None,
        filters: list[Filter[Any]] | None = None,
        orders: list[Order] | None = None,
        page_size: int | None = None,
        page_number: int | None = None,
    ) -> Criteria:
        """
        Create a random criteria value. If a specific criteria value is provided via `value`, it is returned after
        validation. Otherwise, a random criteria value is generated.

        Args:
            value (Criteria | None, optional): A specific criteria value to return. If None, a random criteria value is
            generated.
            filters (list[Filter[Any]] | None, optional): A list of filters to include in the criteria. If None, random
            filters are generated.
            orders (list[Order] | None, optional): A list of orders to include in the criteria. If None, random orders
            are generated.
            page_size (int | None, optional): The page size to include in the criteria. If None, a random page size is
            generated.
            page_number (int | None, optional): The page number to include in the criteria. If None, a random page number
            is generated.

        Returns:
            Criteria: A random criteria value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import CriteriaMother

        criteria = CriteriaMother.create()
        print(criteria)
        # >>> Criteria(filters=[Filter(field=FilterField(value='ThlumotY'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value=6273))], orders=[Order(direction=OrderDirection(value=<Direction.ASC: 'ASC'>), field=OrderField(value='OQnCs6O8JZE'))], page_size=10, page_number=1)
        ```
        """  # noqa: E501
        if value is not None:
            return value

        return Criteria(
            filters=FiltersMother.create(value=filters).value,
            orders=OrdersMother.create(value=orders).value,
            page_size=PageSizeMother.create(value=page_size).value,
            page_number=PageNumberMother.create(value=page_number).value,
        )

    @classmethod
    def empty(cls) -> Criteria:
        """
        Create an empty Criteria object.

        Returns:
            Criteria: An empty Criteria object.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import CriteriaMother

        criteria = CriteriaMother.empty()
        print(criteria)
        # >>> Criteria(filters=[], orders=[], page_size=None, page_number=None)
        ```
        """  # noqa: E501
        return Criteria()

    @classmethod
    def with_filters(cls, *, filters: list[Filter[Any]] | None = None) -> Criteria:
        """
        Create a Criteria object with specific filters.

        Args:
            filters (list[Filter[Any]] | None, optional): The filters to include in the Criteria object.

        Returns:
            Criteria: A Criteria object with the specified filters.

        Example:
        ```python
        from criteria_pattern import Filter, Operator
        from criteria_pattern.models.testing.mothers import CriteriaMother

        criteria = CriteriaMother.with_filters(filters=[Filter(field='name', operator=Operator.EQUAL, value='John')])
        print(criteria)
        # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='John'))], orders=[], page_size=None, page_number=None)
        ```
        """  # noqa: E501
        if filters is None:
            filters = []
            for _ in range(IntegerMother.positive(max=10)):
                filters.append(FilterMother.create())

        return Criteria(filters=filters, orders=[])

    @classmethod
    def with_orders(cls, *, orders: list[Order] | None = None) -> Criteria:
        """
        Create a Criteria object with specific orders.

        Args:
            orders (list[Order] | None, optional): The orders to include in the Criteria object.

        Returns:
            Criteria: A Criteria object with the specified orders.

        Example:
        ```python
        from criteria_pattern import Direction, Order
        from criteria_pattern.models.testing.mothers import CriteriaMother

        criteria = CriteriaMother.with_orders(orders=[Order(direction=Direction.ASC, field='name')])
        print(criteria)
        # >>> Criteria(filters=[], orders=[Order(direction=OrderDirection(value=<Direction.ASC: 'ASC'>), field=OrderField(value='name'))], page_size=None, page_number=None)
        ```
        """  # noqa: E501
        if orders is None:
            orders = []
            for _ in range(IntegerMother.positive(max=10)):
                orders.append(OrderMother.create())

        return Criteria(orders=orders)

    @classmethod
    def with_pagination(cls, *, page_size: int | None = None, page_number: int | None = None) -> Criteria:
        """
        Create a Criteria object with specific pagination.

        Args:
            page_size (int | None, optional): The page size to include in the Criteria object.
            page_number (int | None, optional): The page number to include in the Criteria object.

        Returns:
            Criteria: A Criteria object with the specified pagination.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import CriteriaMother

        criteria = CriteriaMother.with_pagination(page_size=10, page_number=1)
        print(criteria)
        # >>> Criteria(filters=[], orders=[], page_size=10, page_number=1)
        ```
        """
        return Criteria(
            page_size=PageSizeMother.create(value=page_size).value,
            page_number=PageNumberMother.create(value=page_number).value,
        )

    @classmethod
    def without_pagination(cls) -> Criteria:
        """
        Create a Criteria object without pagination (i.e., page_size and page_number are None).

        Returns:
            Criteria: A Criteria object without pagination.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import CriteriaMother

        criteria = CriteriaMother.without_pagination()
        print(criteria)
        # >>> Criteria(filters=[], orders=[], page_size=None, page_number=None)
        ```
        """
        return Criteria(filters=FiltersMother.create().value, orders=OrdersMother.create().value)
