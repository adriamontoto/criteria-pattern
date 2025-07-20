"""
Test OrderDirection value object.
"""

from pytest import mark, raises as assert_raises

from criteria_pattern.models.order import Direction, OrderDirection
from criteria_pattern.models.testing.mothers.order import OrderDirectionMother


@mark.unit_testing
def test_order_direction_value_object_happy_path() -> None:
    """
    Test OrderDirection value object happy path.
    """
    order_direction = OrderDirectionMother.create().value
    field = OrderDirection(value=order_direction)

    assert type(field.value) is Direction
    assert field.value == order_direction


@mark.unit_testing
def test_order_direction_value_object_invalid_type() -> None:
    """
    Test OrderDirection value object raises TypeError when invalid type is provided.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'OrderDirection value <<<.*>>> must be from the enumeration <<<Direction>>>. Got <<<.*>>> type.',
    ):
        OrderDirection(value=OrderDirectionMother.invalid_type())
