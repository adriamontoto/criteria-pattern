"""
Test the AndCriteria class.
"""

from typing import Any

from pytest import mark, raises as assert_raises

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
def test_and_criteria_string_representation(filters: list[Filter[Any]], orders: list[Order]) -> None:
    """
    Test that the string representation of AndCriteria class is correct.

    Args:
        filters (list[Filter]): List of filters.
        orders (list[Order]): List of orders.
    """
    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = AndCriteria(left=left_criteria, right=right_criteria)

    assert repr(criteria) == f'<AndCriteria(left={criteria.left}, right={criteria.right})>'


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
def test_and_criteria_and_operator(filters: list[Filter[Any]], orders: list[Order]) -> None:
    """
    Test the AndCriteria class and operator.

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
def test_and_criteria_and_method(filters: list[Filter[Any]], orders: list[Order]) -> None:
    """
    Test the AndCriteria class and method.

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
def test_and_criteria_or_method(filters: list[Filter[Any]], orders: list[Order]) -> None:
    """
    Test the AndCriteria class or method.

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
def test_and_criteria_or_operator(filters: list[Filter[Any]], orders: list[Order]) -> None:
    """
    Test the AndCriteria class or operator.

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


def test_and_criteria_filters_type() -> None:
    """
    Test that the filters property of AndCriteria class is of type list[Filter].
    """
    filters = [Filter(field='field', operator=FilterOperator.EQUAL, value='value')]
    orders = [Order(field='field', direction=OrderDirection.ASC)]

    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = AndCriteria(left=left_criteria, right=right_criteria)

    assert isinstance(criteria.filters, list)
    for filter in criteria.filters:
        assert isinstance(filter, Filter)


def test_and_criteria_filters_cannot_be_hanged() -> None:
    """
    Test that the filters property of AndCriteria class cannot be changed.
    """
    filters = [Filter(field='field', operator=FilterOperator.EQUAL, value='value')]
    orders = [Order(field='field', direction=OrderDirection.ASC)]

    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = AndCriteria(left=left_criteria, right=right_criteria)

    with assert_raises(AttributeError, match="property 'filters' of 'AndCriteria' object has no setter"):
        criteria.filters = [Filter(field='new_field', operator=FilterOperator.EQUAL, value='new_value')]  # type: ignore


@mark.parametrize(
    'orders_left, orders_right',
    [
        ([Order(field='field', direction=OrderDirection.ASC)], []),
        ([Order(field='field', direction=OrderDirection.DESC)], []),
        ([], [Order(field='field', direction=OrderDirection.ASC)]),
        ([], [Order(field='field', direction=OrderDirection.DESC)]),
        ([Order(field='field', direction=OrderDirection.ASC)], [Order(field='field', direction=OrderDirection.DESC)]),
        ([Order(field='field', direction=OrderDirection.DESC)], [Order(field='field', direction=OrderDirection.ASC)]),
        ([Order(field='field', direction=OrderDirection.ASC)], [Order(field='field', direction=OrderDirection.ASC)]),
        ([Order(field='field', direction=OrderDirection.DESC)], [Order(field='field', direction=OrderDirection.DESC)]),
    ],
)
def test_and_criteria_orders(orders_left: list[Order], orders_right: list[Order]) -> None:
    """
    Test that the orders property of AndCriteria class is the same as the addition of the left and right criteria
    orders.

    Args:
        orders_left (list[Order]): List of orders for the left criteria.
        orders_right (list[Order]): List of orders for the right criteria.
    """
    filters = [Filter(field='field', operator=FilterOperator.EQUAL, value='value')]

    left_criteria = Criteria(filters=filters, orders=orders_left)
    right_criteria = Criteria(filters=filters, orders=orders_right)

    criteria = AndCriteria(left=left_criteria, right=right_criteria)

    assert criteria.orders == (orders_left + orders_right)


def test_and_criteria_orders_type() -> None:
    """
    Test that the orders property of AndCriteria class is of type list[Order].
    """
    filters = [Filter(field='field', operator=FilterOperator.EQUAL, value='value')]
    orders = [Order(field='field', direction=OrderDirection.ASC)]

    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = AndCriteria(left=left_criteria, right=right_criteria)

    assert isinstance(criteria.orders, list)
    for order in criteria.orders:
        assert isinstance(order, Order)


def test_and_criteria_orders_cannot_changed() -> None:
    """
    Test that the orders property of AndCriteria class cannot be changed.
    """
    filters = [Filter(field='field', operator=FilterOperator.EQUAL, value='value')]
    orders = [Order(field='field', direction=OrderDirection.ASC)]

    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = AndCriteria(left=left_criteria, right=right_criteria)

    with assert_raises(AttributeError, match="property 'orders' of 'AndCriteria' object has no setter"):
        criteria.orders = [Order(field='new_field', direction=OrderDirection.DESC)]  # type: ignore


def test_and_criteria_left_type() -> None:
    """
    Test that the left property of AndCriteria class is of type Criteria.
    """
    filters = [Filter(field='field', operator=FilterOperator.EQUAL, value='value')]
    orders = [Order(field='field', direction=OrderDirection.ASC)]

    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = AndCriteria(left=left_criteria, right=right_criteria)

    assert isinstance(criteria.left, Criteria)


def test_and_criteria_left_can_be_changed() -> None:
    """
    Test that the left property of AndCriteria class cannot be changed.
    """
    filters = [Filter(field='field', operator=FilterOperator.EQUAL, value='value')]
    orders = [Order(field='field', direction=OrderDirection.ASC)]

    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = AndCriteria(left=left_criteria, right=right_criteria)

    with assert_raises(AttributeError, match="property 'left' of 'AndCriteria' object has no setter"):
        criteria.left = Criteria(filters=filters, orders=orders)  # type: ignore


def test_and_criteria_right_type() -> None:
    """
    Test that the right property of AndCriteria class is of type Criteria.
    """
    filters = [Filter(field='field', operator=FilterOperator.EQUAL, value='value')]
    orders = [Order(field='field', direction=OrderDirection.ASC)]

    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = AndCriteria(left=left_criteria, right=right_criteria)

    assert isinstance(criteria.right, Criteria)


def test_and_criteria_right_cannot_be_changed() -> None:
    """
    Test that the right property of AndCriteria class cannot be changed.
    """
    filters = [Filter(field='field', operator=FilterOperator.EQUAL, value='value')]
    orders = [Order(field='field', direction=OrderDirection.ASC)]

    left_criteria = Criteria(filters=filters, orders=orders)
    right_criteria = Criteria(filters=filters, orders=orders)

    criteria = AndCriteria(left=left_criteria, right=right_criteria)

    with assert_raises(AttributeError, match="property 'right' of 'AndCriteria' object has no setter"):
        criteria.right = Criteria(filters=filters, orders=orders)  # type: ignore
