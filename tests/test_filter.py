"""
Test the Filter class.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from criteria_pattern import Filter, FilterOperator


@mark.parametrize(
    'field, operator, value',
    [
        ('field', FilterOperator.EQUAL, 'value'),
        ('field', FilterOperator.NOT_EQUAL, 'value'),
        ('field', FilterOperator.GREATER, 1),
        ('field', FilterOperator.GREATER_OR_EQUAL, 6),
        ('field', FilterOperator.LESS, 3),
        ('field', FilterOperator.LESS_OR_EQUAL, 5),
        ('field', FilterOperator.LIKE, 'value'),
        ('field', FilterOperator.BETWEEN, ['value', 'value']),
        ('field', FilterOperator.IS_NULL, None),
        ('field', FilterOperator.NOT_BETWEEN, ['value', 'value']),
        ('field', FilterOperator.NOT_CONTAINS, 'value'),
        ('field', FilterOperator.IS_NOT_NULL, None),
        ('field', FilterOperator.CONTAINS, 'value'),
        ('field', FilterOperator.ENDS_WITH, 'value'),
        ('field', FilterOperator.STARTS_WITH, 'value'),
    ],
)
def test_filter_constructor(field: str, operator: FilterOperator, value: Any) -> None:
    """
    Test that the Filter class constructor is correct.
    """
    filter = Filter(field=field, operator=operator, value=value)

    assert filter.field == field
    assert filter.operator == operator
    assert filter.value == value


@mark.parametrize(
    'operator, value',
    [
        (FilterOperator.EQUAL, 'value'),
        (FilterOperator.NOT_EQUAL, 'value'),
        (FilterOperator.GREATER, 'value'),
        (FilterOperator.GREATER_OR_EQUAL, 'value'),
        (FilterOperator.LESS, 'value'),
        (FilterOperator.LESS_OR_EQUAL, 'value'),
        (FilterOperator.LIKE, 'value'),
        (FilterOperator.IS_NULL, None),
        (FilterOperator.IS_NOT_NULL, None),
        (FilterOperator.BETWEEN, ['value', 'value']),
        (FilterOperator.NOT_BETWEEN, ['value', 'value']),
        (FilterOperator.NOT_CONTAINS, 'value'),
        (FilterOperator.STARTS_WITH, 'value'),
        (FilterOperator.ENDS_WITH, 'value'),
        (FilterOperator.CONTAINS, 'value'),
    ],
)
def test_filter_string_representation(operator: FilterOperator, value: Any) -> None:
    """
    Test that the string representation of Filter class is correct.

    Args:
        operator (FilterOperator): Filter operator.
        value (Any): Filter value.
    """
    filter = Filter(field='field', operator=operator, value=value)

    assert repr(filter) == f"'field' {operator} {value!r}"


def test_filter_field_type() -> None:
    """
    Test that the field property of Filter class is of type str.
    """
    filter = Filter(field='field', operator=FilterOperator.EQUAL, value='value')

    assert isinstance(filter.field, str)


def test_filter_field_cannot_be_changed() -> None:
    """
    Test that the field property of Filter class cannot be changed.
    """
    filter = Filter(field='field', operator=FilterOperator.EQUAL, value='value')

    with assert_raises(AttributeError, match="property 'field' of 'Filter' object has no setter"):
        filter.field = 'new_field'  # type: ignore


def test_filter_operator_type() -> None:
    """
    Test that the operator property of Filter class is of type FilterOperator.
    """
    filter = Filter(field='field', operator=FilterOperator.EQUAL, value='value')

    assert isinstance(filter.operator, FilterOperator)


def test_filter_operator_cannot_be_changed() -> None:
    """
    Test that the operator property of Filter class cannot be changed.
    """
    filter = Filter(field='field', operator=FilterOperator.EQUAL, value='value')

    with assert_raises(AttributeError, match="property 'operator' of 'Filter' object has no setter"):
        filter.operator = FilterOperator.BETWEEN  # type: ignore


@mark.parametrize(
    'value',
    [
        ('value'),
        (['value']),
        (3,),
        15,
        None,
    ],
)
def test_filter_value_type(value: Any) -> None:
    """
    Test that the value property of Filter class is of type Any.

    Args:
        value (Any): Filter value.
    """
    filter = Filter(field='field', operator=FilterOperator.EQUAL, value=value)

    assert isinstance(filter.value, type(value))


def test_filter_value_cannot_be_changed() -> None:
    """
    Test that the value property of Filter class cannot be changed.
    """
    filter = Filter(field='field', operator=FilterOperator.EQUAL, value='value')

    with assert_raises(AttributeError, match="property 'value' of 'Filter' object has no setter"):
        filter.value = 'new_value'  # type: ignore
