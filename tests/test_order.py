"""
Test the Order class.
"""

from pytest import mark, raises as pytest_raises

from criteria_pattern import Order, OrderDirection


@mark.parametrize(
    'field, direction',
    [
        ('field', OrderDirection.ASC),
        ('field', OrderDirection.DESC),
    ],
)
def test_order_constructor(field: str, direction: OrderDirection) -> None:
    """
    Test that the Order class constructor is correct.

    Args:
        field (str): Field name.
        direction (OrderDirection): Order direction.
    """
    order = Order(field=field, direction=direction)

    assert order.field == field
    assert order.direction == direction


@mark.parametrize(
    'direction',
    [
        (OrderDirection.ASC),
        (OrderDirection.DESC),
    ],
)
def test_order_string_representation(direction: OrderDirection) -> None:
    """
    Test that the string representation of Order class is correct.

    Args:
        direction (OrderDirection): Order direction.
    """
    order = Order(field='field', direction=direction)

    assert repr(order) == f"'field' {direction}"


def test_order_field_type() -> None:
    """
    Test that the field property of Order class is of type str.
    """
    order = Order(field='field', direction=OrderDirection.ASC)

    assert isinstance(order.field, str)


def test_order_field_cannot_be_changed() -> None:
    """
    Test that the field property of Order class cannot be changed.
    """
    order = Order(field='field', direction=OrderDirection.ASC)

    with pytest_raises(AttributeError, match="property 'field' of 'Order' object has no setter"):
        order.field = 'new_field'  # type: ignore


def test_order_direction_type() -> None:
    """
    Test that the direction property of Order class is of type OrderDirection.
    """
    order = Order(field='field', direction=OrderDirection.ASC)

    assert isinstance(order.direction, OrderDirection)


def test_order_direction_cannot_be_changed() -> None:
    """
    Test that the direction property of Order class cannot be changed.
    """
    order = Order(field='field', direction=OrderDirection.ASC)

    with pytest_raises(AttributeError, match="property 'direction' of 'Order' object has no setter"):
        order.direction = OrderDirection.DESC  # type: ignore
