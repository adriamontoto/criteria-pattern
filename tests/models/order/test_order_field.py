"""
Test OrderField value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from criteria_pattern.models.order import OrderField
from criteria_pattern.models.testing.mothers.order import OrderFieldMother


@mark.unit_testing
def test_order_field_value_object_happy_path() -> None:
    """
    Test OrderField value object happy path.
    """
    order_value = OrderFieldMother.create().value
    order = OrderField(value=order_value)

    assert type(order.value) is str
    assert order.value == order_value


@mark.unit_testing
def test_order_field_value_object_invalid_type() -> None:
    """
    Test OrderField value object raises TypeError when invalid type is provided.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'OrderField value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        OrderField(value=StringMother.invalid_type())


@mark.unit_testing
def test_order_field_value_object_invalid_empty_value() -> None:
    """
    Test OrderField value object raises ValueError when empty value is provided.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'OrderField value <<<>>> is an empty string. Only non-empty strings are allowed.',
    ):
        OrderField(value=StringMother.empty())


@mark.unit_testing
def test_order_field_value_object_invalid_trimmed_value() -> None:
    """
    Test OrderField value object raises ValueError when trimmed value is provided.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'OrderField value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        OrderField(value=StringMother.not_trimmed())
