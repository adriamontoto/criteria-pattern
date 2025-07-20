"""
Test FilterField value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from criteria_pattern.models.filter import FilterField
from criteria_pattern.models.testing.mothers.filter import FilterFieldMother


@mark.unit_testing
def test_filter_field_value_object_happy_path() -> None:
    """
    Test FilterField value object happy path.
    """
    field_value = FilterFieldMother.create().value
    field = FilterField(value=field_value)

    assert type(field.value) is str
    assert field.value == field_value


@mark.unit_testing
def test_filter_field_value_object_invalid_type() -> None:
    """
    Test FilterField value object raises TypeError when invalid type is provided.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'FilterField value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        FilterField(value=StringMother.invalid_type())


@mark.unit_testing
def test_filter_field_value_object_invalid_empty_value() -> None:
    """
    Test FilterField value object raises ValueError when empty value is provided.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'FilterField value <<<>>> is an empty string. Only non-empty strings are allowed.',
    ):
        FilterField(value=StringMother.empty())


@mark.unit_testing
def test_filter_field_value_object_invalid_trimmed_value() -> None:
    """
    Test FilterField value object raises ValueError when trimmed value is provided.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'FilterField value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        FilterField(value=StringMother.not_trimmed())
