"""
OrderMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from object_mother_pattern.models import BaseMother

from criteria_pattern.models.order import Order

from .order_direction_mother import OrderDirectionMother
from .order_field_mother import OrderFieldMother


class OrderMother(BaseMother[Order]):
    """
    OrderMother class is responsible for generating random order objects.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers import OrderMother

    order = OrderMother.create()
    print(order)
    # >>> <Order(field='oRe6OqcZ6zqXaZOYWRy', direction=ASC)>
    ```
    """

    @classmethod
    @override
    def create(cls, *, field: str | None = None, direction: str | None = None) -> Order:  # type: ignore[override]
        """
        Create a random order value. If specific order parameters are provided via `field` and `direction`,
        they are used to create the order after validation. Otherwise, a random order value is generated.

        Args:
            field (str | None, optional): The field to order. Defaults to None.
            direction (str | None, optional): The direction to use. Defaults to None.

        Raises:
            TypeError: If `field` is not a string.
            ValueError: If `field` is empty.
            ValueError: If `field` is not trimmed.
            ValueError: If `field` contains non-alphanumeric characters.
            TypeError: If `direction` is not an OrderDirection.

        Returns:
            Order: A random order value with the specified parameters.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import OrderMother

        order = OrderMother.create()
        print(order)
        # >>> <Order(field='oRe6OqcZ6zqXaZOYWRy', direction=ASC)>
        ```
        """
        return Order(
            field=OrderFieldMother.create(value=field).value,
            direction=OrderDirectionMother.create(value=direction).value,
        )
