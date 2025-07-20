"""
Test Order model.
"""

from object_mother_pattern.models import BaseMother
from pytest import mark

from criteria_pattern.models.order import Order, OrderDirection, OrderField
from criteria_pattern.models.testing.mothers import OrderMother


@mark.unit_testing
def test_order_model_happy_path() -> None:
    """
    Test Order model happy path.
    """
    order_value = OrderMother.create()
    order = Order(field=order_value.field, direction=order_value.direction)

    assert type(order.field) is str
    assert type(order.direction) is str
    assert order.field == order_value.field
    assert order.direction == order_value.direction


@mark.unit_testing
def test_order_model_repr_method_happy_path() -> None:
    """
    Test Order model repr method happy path.
    """
    order_value: Order = OrderMother.create()
    order = Order(field=order_value.field, direction=order_value.direction)

    assert repr(order) == f'Order(direction={OrderDirection(value=order_value.direction)!r}, field={OrderField(value=order_value.field)!r})'  # noqa: E501  # fmt: skip


@mark.unit_testing
def test_order_model_str_method_happy_path() -> None:
    """
    Test Order model str method happy path.
    """
    order_value = OrderMother.create()
    order = Order(field=order_value.field, direction=order_value.direction)

    assert str(order) == f'Order(direction={order_value.direction}, field={order_value.field})'  # noqa: E501  # fmt: skip


@mark.unit_testing
def test_order_model_eq_method_returns_true_if_the_two_orders_are_equal() -> None:
    """
    Test Order model eq method returns True if the two orders are equal.
    """
    order_value = OrderMother.create()
    order1 = Order(field=order_value.field, direction=order_value.direction)
    order2 = Order(field=order_value.field, direction=order_value.direction)

    assert order1 == order2


@mark.unit_testing
def test_order_model_eq_method_returns_false_if_the_two_orders_are_not_equal() -> None:
    """
    Test Order model eq method returns False if the two orders are not equal.
    """
    order1 = OrderMother.create()
    order2 = OrderMother.create()

    assert order1 != order2


@mark.unit_testing
def test_order_model_eq_method_returns_false_if_the_compared_object_is_not_a_order() -> None:
    """
    Test Order model eq method returns False if the compared object is not a Order.
    """
    order = OrderMother.create()
    not_a_order = BaseMother.invalid_type()

    assert order != not_a_order


@mark.unit_testing
def test_order_model_from_primitives_method_happy_path() -> None:
    """
    Test Order model from primitives method happy path.
    """
    order_value = OrderMother.create()
    order = Order.from_primitives(
        primitives={
            'field': order_value.field,
            'direction': order_value.direction,
        }
    )

    assert order == order_value


@mark.unit_testing
def test_order_model_to_primitives_method_happy_path() -> None:
    """
    Test Order model to primitives method happy path.
    """
    order = OrderMother.create()
    primitives = {
        'field': order.field,
        'direction': order.direction,
    }

    assert order.to_primitives() == primitives
