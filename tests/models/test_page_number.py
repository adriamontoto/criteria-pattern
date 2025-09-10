"""
Test PageNumber value object.
"""

from object_mother_pattern import IntegerMother
from pytest import mark, raises as assert_raises

from criteria_pattern.models import PageNumber


@mark.unit_testing
def test_page_number_value_object_happy_path() -> None:
    """
    Test PageNumber value object happy path.
    """
    page_number_value = IntegerMother.positive()
    page_number = PageNumber(value=page_number_value)

    assert type(page_number.value) is int
    assert page_number.value == page_number_value


@mark.unit_testing
def test_page_number_value_object_with_positive_integer() -> None:
    """
    Test PageNumber value object accepts positive integers.
    """
    page_number = PageNumber(value=1)
    assert page_number.value == 1


@mark.unit_testing
def test_page_number_value_object_invalid_type() -> None:
    """
    Test PageNumber value object raises TypeError when invalid type is provided.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'PageNumber value <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        PageNumber(value=IntegerMother.invalid_type())


@mark.unit_testing
def test_page_number_value_object_zero_value() -> None:
    """
    Test PageNumber value object raises ValueError when zero is provided.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PageNumber value <<<0>>> must be a positive integer.',
    ):
        PageNumber(value=0)


@mark.unit_testing
def test_page_number_value_object_negative_value() -> None:
    """
    Test PageNumber value object raises ValueError when negative integer is provided.
    """
    negative_integer = IntegerMother.negative_or_zero()

    with assert_raises(
        expected_exception=ValueError,
        match=rf'PageNumber value <<<{negative_integer}>>> must be a positive integer.',
    ):
        PageNumber(value=negative_integer)
