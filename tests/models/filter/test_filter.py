"""
Test Filter model.
"""

from typing import Any

from object_mother_pattern.models import BaseMother
from pytest import mark

from criteria_pattern.models.filter import Filter, FilterField, FilterOperator, FilterValue
from criteria_pattern.models.testing.mothers import FilterMother


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
