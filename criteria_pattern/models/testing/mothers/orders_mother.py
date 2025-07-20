"""
OrdersMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover


from object_mother_pattern.models import BaseMother
from object_mother_pattern.mothers import IntegerMother

from criteria_pattern.models import Order
from criteria_pattern.models.orders import Orders

from .order import OrderMother


class OrdersMother(BaseMother[Orders]):
    """
    OrdersMother class is responsible for generating random orders value.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers import OrdersMother

    orders = OrdersMother.create()
    print(orders)
    # >>> [Order(direction=OrderDirection(value=<Direction.DESC: 'DESC'>), field=OrderField(value='OxoKZnI5szu')), Order(direction=OrderDirection(value=<Direction.DESC: 'DESC'>), field=OrderField(value='GPaezpcjp5'))]
    ```
    """  # noqa: E501

    @classmethod
    @override
    def create(cls, *, value: list[Order] | None = None) -> Orders:
        """
        Create a random orders value. If a specific orders value is provided via `value`, it is returned after
        validation. Otherwise, a random orders value is generated.

        Args:
            value (list[Order] | None, optional): A specific orders value to return. If None, a random orders value is
            generated.

        Returns:
            Orders: A random orders value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import OrdersMother

        orders = OrdersMother.create()
        print(orders)
        # >>> [Order(direction=OrderDirection(value=<Direction.DESC: 'DESC'>), field=OrderField(value='OxoKZnI5szu')), Order(direction=OrderDirection(value=<Direction.DESC: 'DESC'>), field=OrderField(value='GPaezpcjp5'))]
        ```
        """  # noqa: E501
        if value is not None:
            return Orders(value=value)

        value = []
        for _ in range(IntegerMother.positive_or_zero(max=10)):
            value.append(OrderMother.create())

        return Orders(value=value)

    @classmethod
    def of_length(cls, *, length: int) -> Orders:
        """
        Create a random orders value of a specific length.

        Args:
            length (int): The length of the orders value to create.

        Returns:
            Orders: A random orders value of the specified length.
        """
        return cls.create(value=[OrderMother.create() for _ in range(length)])
