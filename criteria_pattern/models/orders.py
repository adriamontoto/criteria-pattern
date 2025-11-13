"""
Orders module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import Any, NoReturn

from value_object_pattern import validation
from value_object_pattern.models.collections import ListValueObject

from criteria_pattern.errors import IntegrityError

from .order import Order


class Orders(ListValueObject[Order]):
    """
    Orders class.

    Example:
    ```python
    from criteria_pattern.models import Direction, Order
    from criteria_pattern.models.orders import Orders

    orders = Orders(value=[Order(field='name', direction=Direction.ASC)])
    print(orders)
    # >>> ['Order(direction=ASC, field=name)']
    ```
    """

    def __init__(self, *, value: list[Order], title: str | None = None, parameter: str | None = None) -> None:
        """
        Initialize a list of orders.

        Args:
            value (list[Order]): The list of orders.
            title (str | None, optional): The title of the orders. Default is None.
            parameter (str | None, optional): The parameter name of the orders. Default is None.

        Example:
        ```python
        from criteria_pattern.models import Direction, Order
        from criteria_pattern.models.orders import Orders

        orders = Orders(value=[Order(field='name', direction=Direction.ASC)])
        print(orders)
        # >>> ['Order(direction=ASC, field=name)']
        ```
        """
        super().__init__(value=value, title=title, parameter=parameter)

    @validation(order=0)
    def _ensure_no_duplicate_fields(self, value: list[Order]) -> None:
        """
        Ensures that the provided list of orders has unique fields.

        Args:
            value (list[Order]): The provided list of orders.

        Raises:
            IntegrityError: If the list has duplicate fields.
        """
        order_fields = [order.field for order in value]
        if len(order_fields) != len(set(order_fields)):
            self._raise_value_has_duplicate_fields(value=value)

    def _raise_value_has_duplicate_fields(self, value: list[Order]) -> None:
        """
        Raises a IntegrityError if the provided list of orders has duplicate fields.

        Args:
            value (list[Order]): The provided list of orders.

        Raises:
            IntegrityError: If the list has duplicate fields.
        """
        raise IntegrityError(message=f'Orders values <<<{", ".join(order.field for order in value)}>>> must have unique fields.')  # noqa: E501  # fmt: skip

    @override
    def _raise_value_is_not_list(self, value: Any) -> NoReturn:
        """
        Raises a IntegrityError if the value object `value` is not a list.

        Args:
            value (Any): The provided value.

        Raises:
            IntegrityError: If the `value` is not a list.
        """
        raise IntegrityError(message=f'ListValueObject value <<<{value}>>> must be a list. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip # pragma: no cover

    @override
    def _raise_value_is_not_of_type(self, value: Any) -> NoReturn:
        """
        Raises a IntegrityError if the value object `value` is not of type `T`.

        Args:
            value (Any): The provided value.

        Raises:
            IntegrityError: If the `value` is not of type `T`.
        """
        raise IntegrityError(message=f'ListValueObject value <<<{value}>>> must be of type <<<{self._type.__name__}>>> type. Got <<<{type(value).__name__}>>> type.')  # type: ignore[attr-defined]  # noqa: E501  # fmt: skip
