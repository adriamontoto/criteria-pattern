"""
Test PageSize value object.
"""

from object_mother_pattern import IntegerMother
from pytest import mark, raises as assert_raises

from criteria_pattern.errors import IntegrityError
from criteria_pattern.models import PageSize


@mark.unit_testing
def test_page_size_value_object_happy_path() -> None:
    """
    Test PageSize value object happy path.
    """
    page_size_value = IntegerMother.positive()
    page_size = PageSize(value=page_size_value)

    assert type(page_size.value) is int
    assert page_size.value == page_size_value


@mark.unit_testing
def test_page_size_value_object_invalid_type() -> None:
    """
    Test PageSize value object raises IntegrityError when invalid type is provided.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match=r'PageSize value <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        PageSize(value=IntegerMother.invalid_type())


@mark.unit_testing
def test_page_size_value_object_zero_value() -> None:
    """
    Test PageSize value object raises IntegrityError when zero is provided.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match=r'PageSize value <<<0>>> must be a positive integer.',
    ):
        PageSize(value=0)


@mark.unit_testing
def test_page_size_value_object_negative_value() -> None:
    """
    Test PageSize value object raises IntegrityError when negative integer is provided.
    """
    negative_integer = IntegerMother.negative_or_zero()

    with assert_raises(
        expected_exception=IntegrityError,
        match=rf'PageSize value <<<{negative_integer}>>> must be a positive integer.',
    ):
        PageSize(value=negative_integer)
