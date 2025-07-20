"""
Test Orders model.
"""

from object_mother_pattern.models import BaseMother
from pytest import mark, raises as assert_raises

from criteria_pattern.models.order import Order
from criteria_pattern.models.orders import Orders
from criteria_pattern.models.testing.mothers import OrderMother, OrdersMother


@mark.unit_testing
def test_orders_model_happy_path() -> None:
    """
    Test Orders model happy path.
    """
    orders_value = OrdersMother.create()
    orders = Orders(value=orders_value.value)

    assert type(orders.value) is list
    for order in orders.value:
        assert type(order) is Order


@mark.unit_testing
def test_orders_model_empty() -> None:
    """
    Test Orders model with empty value.
    """
    orders = Orders(value=[])

    assert type(orders.value) is list
    assert len(orders.value) == 0


@mark.unit_testing
def test_orders_model_invalid_type_raises_type_error() -> None:
    """
    Test Orders model with invalid type raises TypeError.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Orders value <<<.*>>> must be of type <<<Order>>> type. Got <<<.*>>> type.',
    ):
        Orders(value=[BaseMother.invalid_type()])


@mark.unit_testing
def test_orders_model_duplicate_orders_raises_value_error() -> None:
    """
    Test Orders model with duplicate orders raises ValueError.
    """
    order = OrderMother.create()

    with assert_raises(
        expected_exception=ValueError,
        match=r'Orders values <<<.*>>> must have unique fields.',
    ):
        Orders(value=[order, order])
