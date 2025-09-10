"""
Test Criteria model.
"""

from object_mother_pattern import IntegerMother
from object_mother_pattern.models import BaseMother
from pytest import mark, raises as assert_raises

from criteria_pattern import Criteria, Filter, Order, PageNumber, PageSize
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
    criteria = Criteria(
        filters=criteria_value.filters,
        orders=criteria_value.orders,
        page_size=criteria_value.page_size,
        page_number=criteria_value.page_number,
    )

    assert type(criteria.filters) is list
    for filter in criteria.filters:
        assert type(filter) is Filter

    assert type(criteria.orders) is list
    for order in criteria.orders:
        assert type(order) is Order

    assert type(criteria.page_size) is int
    assert type(criteria.page_number) is int

    assert criteria.filters == criteria_value.filters
    assert criteria.orders == criteria_value.orders
    assert criteria.page_size == criteria_value.page_size
    assert criteria.page_number == criteria_value.page_number


@mark.unit_testing
def test_criteria_model_repr_method_happy_path() -> None:
    """
    Test Criteria model repr method happy path.
    """
    criteria_value = CriteriaMother.create()
    criteria = Criteria(
        filters=criteria_value.filters,
        orders=criteria_value.orders,
        page_size=criteria_value.page_size,
        page_number=criteria_value.page_number,
    )

    assert repr(criteria) == f'Criteria(filters={Filters(value=criteria_value.filters)!r}, orders={Orders(value=criteria_value.orders)!r}, page_number={PageNumber(value=criteria_value.page_number)!r}, page_size={PageSize(value=criteria_value.page_size)!r})'  # type: ignore[arg-type]  # noqa: E501  # fmt: skip


@mark.unit_testing
def test_criteria_model_str_method_happy_path() -> None:
    """
    Test Criteria model str method happy path.
    """
    criteria_value = CriteriaMother.create()
    criteria = Criteria(
        filters=criteria_value.filters,
        orders=criteria_value.orders,
        page_size=criteria_value.page_size,
        page_number=criteria_value.page_number,
    )

    assert str(criteria) == f'Criteria(filters={criteria_value.filters!s}, orders={criteria_value.orders!s}, page_number={criteria_value.page_number!s}, page_size={criteria_value.page_size!s})'  # noqa: E501  # fmt: skip


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


@mark.unit_testing
def test_criteria_model_with_pagination() -> None:
    """
    Test Criteria model with pagination parameters.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    criteria = CriteriaMother.create(page_size=page_size, page_number=page_number)

    assert criteria.page_size == page_size
    assert criteria.page_number == page_number
    assert criteria.has_pagination()


@mark.unit_testing
def test_criteria_model_without_pagination() -> None:
    """
    Test Criteria model without pagination parameters.
    """
    criteria = CriteriaMother.without_pagination()

    assert criteria.page_size is None
    assert criteria.page_number is None
    assert not criteria.has_pagination()


@mark.unit_testing
def test_criteria_model_pagination_validation_page_number_without_page_size() -> None:
    """
    Test Criteria model raises ValueError when page_number is provided without page_size.
    """
    page_number = IntegerMother.positive()

    with assert_raises(
        expected_exception=ValueError,
        match=f'Criteria page_number <<<{page_number}>>> cannot be provided without page_size.',
    ):
        Criteria(page_number=page_number)


@mark.unit_testing
def test_criteria_model_pagination_with_page_size_only() -> None:
    """
    Test Criteria model allows page_size without page_number (LIMIT without OFFSET).
    """
    page_size = IntegerMother.positive()
    criteria = Criteria(page_size=page_size)

    assert criteria.page_size == page_size
    assert criteria.page_number is None
    assert criteria.has_page_size()
    assert not criteria.has_pagination()


@mark.unit_testing
def test_criteria_model_pagination_invalid_page_size_type() -> None:
    """
    Test Criteria model raises ValueError for invalid page_size type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Criteria page_size <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        Criteria(page_size=IntegerMother.invalid_type(), page_number=IntegerMother.positive())


@mark.unit_testing
def test_criteria_model_pagination_invalid_page_size() -> None:
    """
    Test Criteria model raises ValueError for invalid page_size.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Criteria page_size <<<0>>> must be a positive integer.',
    ):
        Criteria(page_size=0, page_number=IntegerMother.positive())


@mark.unit_testing
def test_criteria_model_pagination_invalid_page_size_random() -> None:
    """
    Test Criteria model raises ValueError for random invalid page_size.
    """
    page_size = IntegerMother.negative_or_zero()

    with assert_raises(
        expected_exception=ValueError,
        match=rf'Criteria page_size <<<{page_size}>>> must be a positive integer.',
    ):
        Criteria(page_size=page_size, page_number=IntegerMother.positive())


@mark.unit_testing
def test_criteria_model_pagination_invalid_page_number_type() -> None:
    """
    Test Criteria model raises ValueError for invalid page_number type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Criteria page_number <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        Criteria(page_size=IntegerMother.positive(), page_number=IntegerMother.invalid_type())


@mark.unit_testing
def test_criteria_model_pagination_invalid_page_number() -> None:
    """
    Test Criteria model raises ValueError for invalid page_number.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Criteria page_number <<<0>>> must be a positive integer.',
    ):
        Criteria(page_size=IntegerMother.positive(), page_number=0)


@mark.unit_testing
def test_criteria_model_pagination_invalid_page_number_random() -> None:
    """
    Test Criteria model raises ValueError for random invalid page_number.
    """
    page_number = IntegerMother.negative_or_zero()

    with assert_raises(
        expected_exception=ValueError,
        match=rf'Criteria page_number <<<{page_number}>>> must be a positive integer.',
    ):
        Criteria(page_size=IntegerMother.positive(), page_number=page_number)


@mark.unit_testing
def test_and_criteria_pagination_from_left() -> None:
    """
    Test AndCriteria takes pagination from left criteria.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    left_criteria = CriteriaMother.create(page_size=page_size, page_number=page_number)
    right_criteria = CriteriaMother.create()

    combined_criteria = left_criteria & right_criteria

    assert combined_criteria.page_size == page_size
    assert combined_criteria.page_number == page_number
    assert combined_criteria.has_pagination()


@mark.unit_testing
def test_or_criteria_pagination_from_left() -> None:
    """
    Test OrCriteria takes pagination from left criteria.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    left_criteria = CriteriaMother.create(page_size=page_size, page_number=page_number)
    right_criteria = CriteriaMother.create(page_number=33, page_size=99)

    combined_criteria = left_criteria | right_criteria

    assert combined_criteria.page_size == page_size
    assert combined_criteria.page_number == page_number
    assert combined_criteria.has_pagination()


@mark.unit_testing
def test_not_criteria_pagination_from_wrapped() -> None:
    """
    Test NotCriteria takes pagination from wrapped criteria.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    criteria = CriteriaMother.create(page_size=page_size, page_number=page_number)
    negated_criteria = ~criteria

    assert negated_criteria.page_size == page_size
    assert negated_criteria.page_number == page_number
    assert negated_criteria.has_pagination()
