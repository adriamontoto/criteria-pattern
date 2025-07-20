"""
Orders module.
"""

from value_object_pattern import validation
from value_object_pattern.models.collections import ListValueObject

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

    def __init__(self, *, value: list[Order]) -> None:
        """
        Initialize a list of orders.

        Args:
            value (list[Order]): The list of orders.

        Example:
        ```python
        from criteria_pattern.models import Direction, Order
        from criteria_pattern.models.orders import Orders

        orders = Orders(value=[Order(field='name', direction=Direction.ASC)])
        print(orders)
        # >>> ['Order(direction=ASC, field=name)']
        ```
        """
        super().__init__(value=value)

    @validation(order=0)
    def _ensure_no_duplicate_fields(self, value: list[Order]) -> None:
        """
        Ensures that the provided list of orders has unique fields.

        Args:
            value (list[Order]): The provided list of orders.

        Raises:
            ValueError: If the list has duplicate fields.
        """
        order_fields = [order.field for order in value]
        if len(order_fields) != len(set(order_fields)):
            self._raise_value_has_duplicate_fields(value=value)

    def _raise_value_has_duplicate_fields(self, value: list[Order]) -> None:
        """
        Raises a ValueError if the provided list of orders has duplicate fields.

        Args:
            value (list[Order]): The provided list of orders.

        Raises:
            ValueError: If the list has duplicate fields.
        """
        raise ValueError(f'Orders values <<<{", ".join(order.field for order in value)}>>> must have unique fields.')
