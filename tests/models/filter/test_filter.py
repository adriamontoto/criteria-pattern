"""
Test Filter model.
"""

from typing import Any

from object_mother_pattern import StringMother
from object_mother_pattern.models import BaseMother
from pytest import mark, raises as assert_raises

from criteria_pattern.errors import IntegrityError
from criteria_pattern.models.filter import Filter, FilterField, FilterOperator, FilterValue
from criteria_pattern.models.testing.mothers import FilterMother
from criteria_pattern.models.testing.mothers.filter import FilterFieldMother, FilterOperatorMother, FilterValueMother


@mark.unit_testing
def test_filter_model_happy_path() -> None:
    """
    Test Filter model happy path.
    """
    filter_value: Filter[Any] = FilterMother.create()
    filter = Filter(field=filter_value.field, operator=filter_value.operator, value=filter_value.value)

    assert type(filter.field) is str
    assert type(filter.operator) is str
    assert filter.field == filter_value.field
    assert filter.operator == filter_value.operator
    assert filter.value == filter_value.value


@mark.unit_testing
def test_filter_model_repr_method_happy_path() -> None:
    """
    Test Filter model repr method happy path.
    """
    filter_value: Filter[Any] = FilterMother.create()
    filter = Filter(field=filter_value.field, operator=filter_value.operator, value=filter_value.value)

    assert repr(filter) == f'Filter(field={FilterField(value=filter_value.field)!r}, operator={FilterOperator(value=filter_value.operator)!r}, value={FilterValue(value=filter_value.value)!r})'  # noqa: E501  # fmt: skip


@mark.unit_testing
def test_filter_model_str_method_happy_path() -> None:
    """
    Test Filter model str method happy path.
    """
    filter_value: Filter[Any] = FilterMother.create()
    filter = Filter(field=filter_value.field, operator=filter_value.operator, value=filter_value.value)

    assert str(filter) == f'Filter(field={filter_value.field}, operator={filter_value.operator}, value={filter_value.value})'  # noqa: E501  # fmt: skip


@mark.unit_testing
def test_filter_model_eq_method_returns_true_if_the_two_filters_are_equal() -> None:
    """
    Test Filter model eq method returns True if the two filters are equal.
    """
    filter_value: Filter[Any] = FilterMother.create()
    filter1 = Filter(field=filter_value.field, operator=filter_value.operator, value=filter_value.value)
    filter2 = Filter(field=filter_value.field, operator=filter_value.operator, value=filter_value.value)

    assert filter1 == filter2


@mark.unit_testing
def test_filter_model_eq_method_returns_false_if_the_two_filters_are_not_equal() -> None:
    """
    Test Filter model eq method returns False if the two filters are not equal.
    """
    filter1: Filter[Any] = FilterMother.create()
    filter2: Filter[Any] = FilterMother.create()

    assert filter1 != filter2


@mark.unit_testing
def test_filter_model_eq_method_returns_false_if_the_compared_object_is_not_a_filter() -> None:
    """
    Test Filter model eq method returns False if the compared object is not a Filter.
    """
    filter: Filter[Any] = FilterMother.create()
    not_a_filter = BaseMother.invalid_type()

    assert filter != not_a_filter


@mark.unit_testing
def test_filter_model_from_primitives_method_happy_path() -> None:
    """
    Test Filter model from primitives method happy path.
    """
    filter_value: Filter[Any] = FilterMother.create()
    filter: Filter[Any] = Filter.from_primitives(
        primitives={
            'field': filter_value.field,
            'operator': filter_value.operator,
            'value': filter_value.value,
        }
    )

    assert filter == filter_value


@mark.unit_testing
def test_filter_model_to_primitives_method_happy_path() -> None:
    """
    Test Filter model to primitives method happy path.
    """
    filter: Filter[Any] = FilterMother.create()
    primitives = {
        'field': filter.field,
        'operator': filter.operator,
        'value': filter.value,
    }

    assert filter.to_primitives() == primitives


@mark.unit_testing
def test_filter_model_field_invalid_type() -> None:
    """
    Test Filter model raises IntegrityError when field is not a string.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match=r'Filter field <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        Filter(
            field=StringMother.invalid_type(),
            operator=FilterOperatorMother.create().value.value,
            value=FilterValueMother.create().value,
        )


@mark.unit_testing
def test_filter_model_field_empty_value() -> None:
    """
    Test Filter model raises IntegrityError when field is empty.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match=r'Filter field <<<>>> is an empty string. Only non-empty strings are allowed.',
    ):
        Filter(
            field=StringMother.empty(),
            operator=FilterOperatorMother.create().value.value,
            value=FilterValueMother.create().value,
        )


@mark.unit_testing
def test_filter_model_field_not_trimmed() -> None:
    """
    Test Filter model raises IntegrityError when field has leading/trailing whitespace.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match=r'Filter field <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',
    ):
        Filter(
            field=StringMother.not_trimmed(),
            operator=FilterOperatorMother.create().value.value,
            value=FilterValueMother.create().value,
        )


@mark.unit_testing
def test_filter_model_field_non_printable() -> None:
    """
    Test Filter model raises IntegrityError when field contains non-printable characters.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match=r'Filter field <<<.*>>> contains invalid characters. Only printable characters are allowed.',
    ):
        Filter(
            field=StringMother.invalid_value(),
            operator=FilterOperatorMother.create().value.value,
            value=FilterValueMother.create().value,
        )


@mark.unit_testing
def test_filter_model_operator_invalid_type() -> None:
    """
    Test Filter model raises IntegrityError when operator is not a valid type.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match=r'Filter operator <<<.*>>> must be from the enumeration <<<Operator>>>. Got <<<.*>>> type.',
    ):
        Filter(
            field=FilterFieldMother.create().value,
            operator=StringMother.invalid_type(),
            value=FilterValueMother.create().value,
        )
