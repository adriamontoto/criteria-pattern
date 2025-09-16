"""
Test FilterOperator value object.
"""

from pytest import mark, raises as assert_raises

from criteria_pattern.errors import IntegrityError
from criteria_pattern.models.filter import FilterOperator, Operator
from criteria_pattern.models.testing.mothers.filter import FilterOperatorMother


@mark.unit_testing
def test_filter_operator_value_object_happy_path() -> None:
    """
    Test FilterOperator value object happy path.
    """
    field_operator = FilterOperatorMother.create().value
    field = FilterOperator(value=field_operator)

    assert type(field.value) is Operator
    assert field.value == field_operator


@mark.unit_testing
def test_filter_operator_value_object_invalid_type() -> None:
    """
    Test FilterOperator value object raises IntegrityError when invalid type is provided.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match=r'FilterOperator value <<<.*>>> must be from the enumeration <<<Operator>>>. Got <<<.*>>> type.',
    ):
        FilterOperator(value=FilterOperatorMother.invalid_type())
