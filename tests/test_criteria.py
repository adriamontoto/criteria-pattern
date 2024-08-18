"""
Test the Criteria class.
"""

from typing import Any

from pytest import mark, raises as pytest_raises

from criteria_pattern import Criteria, Filter, FilterOperator, Order, OrderDirection
from criteria_pattern.criteria import AndCriteria, OrCriteria


@mark.parametrize(
    'filters, orders',
    [
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [Order(field='field', direction=OrderDirection.ASC)],
        ),
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [Order(field='field', direction=OrderDirection.DESC)],
        ),
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [],
        ),
        (
            [],
            [Order(field='field', direction=OrderDirection.ASC)],
        ),
        (
            [],
            [Order(field='field', direction=OrderDirection.DESC)],
        ),
        (
            [],
            [],
        ),
    ],
)
def test_criteria_string_representation(filters: list[Filter[Any]], orders: list[Order]) -> None:
    """
    Test that the string representation of Criteria class is correct.

    Args:
        filters (list[Filter]): List of filters.
        orders (list[Order]): List of orders.
    """
    criteria = Criteria(filters=filters, orders=orders)

    assert repr(criteria) == f'<Criteria(filters={filters}, orders={orders})>'


@mark.parametrize(
    'filters, orders',
    [
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [Order(field='field', direction=OrderDirection.ASC)],
        ),
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [Order(field='field', direction=OrderDirection.DESC)],
        ),
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [],
        ),
        (
            [],
            [Order(field='field', direction=OrderDirection.ASC)],
        ),
        (
            [],
            [Order(field='field', direction=OrderDirection.DESC)],
        ),
        (
            [],
            [],
        ),
    ],
)
def test_criteria_and_operator(filters: list[Filter[Any]], orders: list[Order]) -> None:
    """
    Test the Criteria class and operator.

    Args:
        filters (list[Filter]): List of filters.
        orders (list[Order]): List of orders.
    """
    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = left_criteria & right_criteria

    assert isinstance(criteria, AndCriteria)
    assert criteria.left == left_criteria
    assert criteria.right == right_criteria


@mark.parametrize(
    'filters, orders',
    [
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [Order(field='field', direction=OrderDirection.ASC)],
        ),
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [Order(field='field', direction=OrderDirection.DESC)],
        ),
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [],
        ),
        (
            [],
            [Order(field='field', direction=OrderDirection.ASC)],
        ),
        (
            [],
            [Order(field='field', direction=OrderDirection.DESC)],
        ),
        (
            [],
            [],
        ),
    ],
)
def test_criteria_and_method(filters: list[Filter[Any]], orders: list[Order]) -> None:
    """
    Test the Criteria class and method.

    Args:
        filters (list[Filter]): List of filters.
        orders (list[Order]): List of orders.
    """
    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = left_criteria.and_(right_criteria)

    assert isinstance(criteria, AndCriteria)
    assert criteria.left == left_criteria
    assert criteria.right == right_criteria


@mark.parametrize(
    'filters, orders',
    [
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [Order(field='field', direction=OrderDirection.ASC)],
        ),
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [Order(field='field', direction=OrderDirection.DESC)],
        ),
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [],
        ),
        (
            [],
            [Order(field='field', direction=OrderDirection.ASC)],
        ),
        (
            [],
            [Order(field='field', direction=OrderDirection.DESC)],
        ),
        (
            [],
            [],
        ),
    ],
)
def test_criteria_or_method(filters: list[Filter[Any]], orders: list[Order]) -> None:
    """
    Test the Criteria class or method.

    Args:
        filters (list[Filter]): List of filters.
        orders (list[Order]): List of orders.
    """
    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    or_criteria = left_criteria.or_(right_criteria)

    assert isinstance(or_criteria, OrCriteria)
    assert or_criteria.left == left_criteria
    assert or_criteria.right == right_criteria


@mark.parametrize(
    'filters, orders',
    [
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [Order(field='field', direction=OrderDirection.ASC)],
        ),
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [Order(field='field', direction=OrderDirection.DESC)],
        ),
        (
            [Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
            [],
        ),
        (
            [],
            [Order(field='field', direction=OrderDirection.ASC)],
        ),
        (
            [],
            [Order(field='field', direction=OrderDirection.DESC)],
        ),
        (
            [],
            [],
        ),
    ],
)
def test_criteria_or_operator(filters: list[Filter[Any]], orders: list[Order]) -> None:
    """
    Test the Criteria class or operator.

    Args:
        filters (list[Filter]): List of filters.
        orders (list[Order]): List of orders.
    """
    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    or_criteria = left_criteria | right_criteria

    assert isinstance(or_criteria, OrCriteria)
    assert or_criteria.left == left_criteria
    assert or_criteria.right == right_criteria


def test_criteria_filters_type() -> None:
    """
    Test that the filters property of Criteria class is of type list[Filter].
    """
    criteria = Criteria(filters=[Filter(field='field', operator=FilterOperator.EQUAL, value='value')])

    assert isinstance(criteria.filters, list)
    for filter in criteria.filters:
        assert isinstance(filter, Filter)


def test_criteria_filters_cannot_changed() -> None:
    """
    Test that the filters property of Criteria class cannot be changed.
    """
    criteria = Criteria(filters=[Filter(field='field', operator=FilterOperator.EQUAL, value='value')])

    with pytest_raises(AttributeError, match="property 'filters' of 'Criteria' object has no setter"):
        criteria.filters = [Filter(field='new_field', operator=FilterOperator.EQUAL, value='new_value')]  # type: ignore


def test_criteria_orders_type() -> None:
    """
    Test that the orders property of Criteria class is of type list[Order].
    """
    criteria = Criteria(
        filters=[Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
        orders=[Order(field='field', direction=OrderDirection.ASC)],
    )

    assert isinstance(criteria.orders, list)
    for order in criteria.orders:
        assert isinstance(order, Order)


def test_criteria_orders_cannot_changed() -> None:
    """
    Test that the orders property of Criteria class cannot be changed.
    """
    criteria = Criteria(
        filters=[Filter(field='field', operator=FilterOperator.EQUAL, value='value')],
        orders=[Order(field='field', direction=OrderDirection.ASC)],
    )

    with pytest_raises(AttributeError, match="property 'orders' of 'Criteria' object has no setter"):
        criteria.orders = [Order(field='new_field', direction=OrderDirection.DESC)]  # type: ignore
