"""
Test Criteria model.
"""

from object_mother_pattern.models import BaseMother
from pytest import mark

from criteria_pattern import Criteria, Filter, Order
from criteria_pattern.models.criteria import AndCriteria, NotCriteria, OrCriteria
from criteria_pattern.models.filters import Filters
from criteria_pattern.models.orders import Orders
from criteria_pattern.models.testing.mothers import CriteriaMother


@mark.unit_testing
def test_criteria_model_happy_path() -> None:
    """
    Test Criteria model happy path.
    """
    criteria_value = CriteriaMother.create()
    criteria = Criteria(filters=criteria_value.filters, orders=criteria_value.orders)

    assert type(criteria.filters) is list
    for filter in criteria.filters:
        assert type(filter) is Filter

    assert type(criteria.orders) is list
    for order in criteria.orders:
        assert type(order) is Order

    assert criteria.filters == criteria_value.filters
    assert criteria.orders == criteria_value.orders


@mark.unit_testing
def test_criteria_model_repr_method_happy_path() -> None:
    """
    Test Criteria model repr method happy path.
    """
    criteria_value = CriteriaMother.create()
    criteria = Criteria(filters=criteria_value.filters, orders=criteria_value.orders)

    assert repr(criteria) == f'Criteria(filters={Filters(value=criteria_value.filters)!r}, orders={Orders(value=criteria_value.orders)!r})'  # noqa: E501  # fmt: skip


@mark.unit_testing
def test_criteria_model_str_method_happy_path() -> None:
    """
    Test Criteria model str method happy path.
    """
    criteria_value = CriteriaMother.create()
    criteria = Criteria(filters=criteria_value.filters, orders=criteria_value.orders)

    assert str(criteria) == f'Criteria(filters={criteria_value.filters!s}, orders={criteria_value.orders!s})'


@mark.unit_testing
def test_criteria_model_eq_method_returns_true_if_the_two_criteria_are_equal() -> None:
    """
    Test Criteria model eq method returns True if the two criteria are equal.
    """
    criteria_value = CriteriaMother.create()
    criteria1 = Criteria(filters=criteria_value.filters, orders=criteria_value.orders)
    criteria2 = Criteria(filters=criteria_value.filters, orders=criteria_value.orders)

    assert criteria1 == criteria2


@mark.unit_testing
def test_criteria_model_eq_method_returns_false_if_the_two_criteria_are_not_equal() -> None:
    """
    Test Criteria model eq method returns False if the two criteria are not equal.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    assert criteria1 != criteria2


@mark.unit_testing
def test_criteria_model_eq_method_returns_false_if_the_compared_object_is_not_a_criteria() -> None:
    """
    Test Criteria model eq method returns False if the compared object is not a Criteria.
    """
    criteria = CriteriaMother.create()
    not_a_criteria = BaseMother.invalid_type()

    assert criteria != not_a_criteria


@mark.unit_testing
def test_criteria_model_filters_method_returns_filters() -> None:
    """
    Test Criteria model filters method returns filters.
    """
    criteria = CriteriaMother.with_filters()

    assert criteria.filters == criteria.filters


@mark.unit_testing
def test_criteria_model_orders_method_returns_orders() -> None:
    """
    Test Criteria model orders method returns orders.
    """
    criteria = CriteriaMother.with_orders()

    assert criteria.orders == criteria.orders


@mark.unit_testing
def test_criteria_model_has_filters_method_returns_true_if_criteria_has_filters() -> None:
    """
    Test Criteria model has_filters method returns True if criteria has filters.
    """
    criteria = CriteriaMother.with_filters()

    assert criteria.has_filters()


@mark.unit_testing
def test_criteria_model_has_filters_method_returns_false_if_criteria_does_not_have_filters() -> None:
    """
    Test Criteria model has_filters method returns False if criteria does not have filters.
    """
    criteria = CriteriaMother.empty()

    assert not criteria.has_filters()


@mark.unit_testing
def test_criteria_model_has_orders_method_returns_true_if_criteria_has_orders() -> None:
    """
    Test Criteria model has_orders method returns True if criteria has orders.
    """
    criteria = CriteriaMother.with_orders()

    assert criteria.has_orders()


@mark.unit_testing
def test_criteria_model_has_orders_method_returns_false_if_criteria_does_not_have_orders() -> None:
    """
    Test Criteria model has_orders method returns False if criteria does not have orders.
    """
    criteria = CriteriaMother.empty()

    assert not criteria.has_orders()


@mark.unit_testing
def test_and_criteria_model_repr_method() -> None:
    """
    Test AndCriteria model repr method.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1 & criteria2

    assert repr(combined_criteria) == f'AndCriteria(left={criteria1!r}, right={criteria2!r})'


@mark.unit_testing
def test_and_criteria_model_str_method() -> None:
    """
    Test AndCriteria model str method.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1 & criteria2

    assert str(combined_criteria) == f'AndCriteria(left={criteria1!s}, right={criteria2!s})'


@mark.unit_testing
def test_and_criteria_model_right_method_returns_criteria() -> None:
    """
    Test AndCriteria model right method returns criteria.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1 & criteria2

    assert type(combined_criteria.right) is Criteria


@mark.unit_testing
def test_and_criteria_model_left_method_returns_criteria() -> None:
    """
    Test AndCriteria model left method returns criteria.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1 & criteria2

    assert type(combined_criteria.left) is Criteria


@mark.unit_testing
def test_criteria_model_and_operator_returns_new_criteria_with_combined_filters_and_orders() -> None:
    """
    Test Criteria model and operator returns new criteria with combined filters and orders.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1 & criteria2

    assert type(combined_criteria) is AndCriteria
    assert combined_criteria.filters == criteria1.filters + criteria2.filters
    assert combined_criteria.orders == criteria1.orders + criteria2.orders


@mark.unit_testing
def test_criteria_model_and_method_returns_new_criteria_with_combined_filters_and_orders() -> None:
    """
    Test Criteria model and method returns new criteria with combined filters and orders.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1.and_(criteria=criteria2)

    assert type(combined_criteria) is AndCriteria
    assert combined_criteria.filters == criteria1.filters + criteria2.filters
    assert combined_criteria.orders == criteria1.orders + criteria2.orders


@mark.unit_testing
def test_or_criteria_model_repr_method() -> None:
    """
    Test OrCriteria model repr method.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1 | criteria2

    assert repr(combined_criteria) == f'OrCriteria(left={criteria1!r}, right={criteria2!r})'


@mark.unit_testing
def test_or_criteria_model_str_method() -> None:
    """
    Test OrCriteria model str method.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1 | criteria2

    assert str(combined_criteria) == f'OrCriteria(left={criteria1!s}, right={criteria2!s})'


@mark.unit_testing
def test_or_criteria_model_right_method_returns_criteria() -> None:
    """
    Test OrCriteria model right method returns criteria.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1 | criteria2

    assert type(combined_criteria.right) is Criteria


@mark.unit_testing
def test_or_criteria_model_left_method_returns_criteria() -> None:
    """
    Test OrCriteria model left method returns criteria.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1 | criteria2

    assert type(combined_criteria.left) is Criteria


@mark.unit_testing
def test_criteria_model_or_operator_returns_new_criteria_with_combined_filters_and_orders() -> None:
    """
    Test Criteria model or operator returns new criteria with combined filters and orders.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1 | criteria2

    assert type(combined_criteria) is OrCriteria
    assert combined_criteria.filters == criteria1.filters + criteria2.filters
    assert combined_criteria.orders == criteria1.orders + criteria2.orders


@mark.unit_testing
def test_criteria_model_or_method_returns_new_criteria_with_combined_filters_and_orders() -> None:
    """
    Test Criteria model or method returns new criteria with combined filters and orders.
    """
    criteria1 = CriteriaMother.create()
    criteria2 = CriteriaMother.create()

    combined_criteria = criteria1.or_(criteria=criteria2)

    assert type(combined_criteria) is OrCriteria
    assert combined_criteria.filters == criteria1.filters + criteria2.filters
    assert combined_criteria.orders == criteria1.orders + criteria2.orders


@mark.unit_testing
def test_not_criteria_model_repr_method() -> None:
    """
    Test NotCriteria model repr method.
    """
    criteria = CriteriaMother.create()
    negated_criteria = ~criteria

    assert repr(negated_criteria) == f'NotCriteria(criteria={criteria!r})'


@mark.unit_testing
def test_not_criteria_model_str_method() -> None:
    """
    Test NotCriteria model str method.
    """
    criteria = CriteriaMother.create()
    negated_criteria = ~criteria

    assert str(negated_criteria) == f'NotCriteria(criteria={criteria!s})'


@mark.unit_testing
def test_not_criteria_model_criteria_method_returns_criteria() -> None:
    """
    Test Criteria model criteria method returns criteria.
    """
    criteria = CriteriaMother.create()

    negated_criteria = ~criteria

    assert type(negated_criteria.criteria) is Criteria


@mark.unit_testing
def test_criteria_model_not_operator_returns_new_criteria_with_negated_filters_and_orders() -> None:
    """
    Test Criteria model not operator returns new criteria with negated filters and orders.
    """
    criteria = CriteriaMother.create()

    negated_criteria = ~criteria

    assert type(negated_criteria) is NotCriteria
    assert negated_criteria.filters == criteria.filters
    assert negated_criteria.orders == criteria.orders


@mark.unit_testing
def test_criteria_model_not_method_returns_new_criteria_with_negated_filters_and_orders() -> None:
    """
    Test Criteria model not method returns new criteria with negated filters and orders.
    """
    criteria = CriteriaMother.create()

    negated_criteria = criteria.not_()

    assert type(negated_criteria) is NotCriteria
    assert negated_criteria.filters == criteria.filters
    assert negated_criteria.orders == criteria.orders
