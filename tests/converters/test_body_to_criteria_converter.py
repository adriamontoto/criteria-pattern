"""
Test BodyToCriteriaConverter class.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.converters import BodyToCriteriaConverter
from criteria_pattern.errors import (
    IntegrityError,
    InvalidColumnError,
    InvalidDirectionError,
    InvalidOperatorError,
    PaginationBoundsError,
)


@mark.unit_testing
def test_body_to_criteria_converter_with_empty_body() -> None:
    """
    Test BodyToCriteriaConverter class with an empty body.
    """
    criteria = BodyToCriteriaConverter.convert(body={})

    expected = Criteria(filters=None, orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_body_to_criteria_converter_with_filters() -> None:
    """
    Test BodyToCriteriaConverter class with filters.
    """
    body = {
        'filters': [
            {'field': 'test', 'operator': 'EQUAL', 'value': 'a'},
            {'field': 'price', 'operator': 'GREATER_THAN', 'value': 10},
            {'field': 'age', 'operator': Operator.LESS, 'value': 18},
        ],
    }
    criteria = BodyToCriteriaConverter.convert(body=body)

    expected = Criteria(
        filters=[
            Filter(field='test', operator=Operator.EQUAL, value='a'),
            Filter(field='price', operator=Operator.GREATER, value=10),
            Filter(field='age', operator=Operator.LESS, value=18),
        ],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_body_to_criteria_converter_with_full_body() -> None:
    """
    Test BodyToCriteriaConverter class with filters, orders and pagination.
    """
    body = {
        'filters': [{'field': 'full_name', 'operator': 'contains', 'value': 'Doe'}],
        'orders': [
            {'field': 'created_at', 'direction': 'desc'},
            {'field': 'full_name', 'direction': Direction.ASC},
        ],
        'page_size': 20,
        'page_number': 2,
    }
    criteria = BodyToCriteriaConverter.convert(body=body, fields_mapping={'full_name': 'name'})

    expected = Criteria(
        filters=[Filter(field='name', operator=Operator.CONTAINS, value='Doe')],
        orders=[
            Order(field='created_at', direction=Direction.DESC),
            Order(field='name', direction=Direction.ASC),
        ],
        page_size=20,
        page_number=2,
    )

    assert criteria == expected


@mark.unit_testing
def test_body_to_criteria_converter_with_null_filters() -> None:
    """
    Test BodyToCriteriaConverter class with null filters.
    """
    body = {
        'filters': [
            {'field': 'deleted_at', 'operator': 'IS_NULL'},
            {'field': 'archived_at', 'operator': 'IS_NOT_NULL', 'value': True},
        ],
    }
    criteria = BodyToCriteriaConverter.convert(body=body)

    expected = Criteria(
        filters=[
            Filter(field='deleted_at', operator=Operator.IS_NULL, value=None),
            Filter(field='archived_at', operator=Operator.IS_NOT_NULL, value=None),
        ],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_body_to_criteria_converter_with_list_filters() -> None:
    """
    Test BodyToCriteriaConverter class with list-valued filters.
    """
    body = {
        'filters': [
            {'field': 'status', 'operator': 'IN', 'value': ['ACTIVE', 'PENDING']},
            {'field': 'category', 'operator': 'NOT_IN', 'value': ('archived', 'deleted')},
            {'field': 'price', 'operator': 'BETWEEN', 'value': [10, 100]},
            {'field': 'age', 'operator': 'NOT_BETWEEN', 'value': (18, 30)},
        ],
    }
    criteria = BodyToCriteriaConverter.convert(body=body)

    expected = Criteria(
        filters=[
            Filter(field='status', operator=Operator.IN, value=['ACTIVE', 'PENDING']),
            Filter(field='category', operator=Operator.NOT_IN, value=['archived', 'deleted']),
            Filter(field='price', operator=Operator.BETWEEN, value=[10, 100]),
            Filter(field='age', operator=Operator.NOT_BETWEEN, value=[18, 30]),
        ],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_body_to_criteria_converter_with_custom_operator_mapping() -> None:
    """
    Test BodyToCriteriaConverter class with custom operator mapping.
    """
    body = {'filters': [{'field': 'created_at', 'operator': 'after', 'value': '2026-05-18'}]}
    criteria = BodyToCriteriaConverter.convert(body=body, operator_mapping={'after': Operator.GREATER})

    expected = Criteria(
        filters=[Filter(field='created_at', operator=Operator.GREATER, value='2026-05-18')],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_body_to_criteria_converter_with_custom_operator_override() -> None:
    """
    Test BodyToCriteriaConverter class with a custom operator override.
    """
    body = {'filters': [{'field': 'name', 'operator': 'equal', 'value': 'Doe'}]}
    criteria = BodyToCriteriaConverter.convert(body=body, operator_mapping={'EQUAL': Operator.CONTAINS})

    expected = Criteria(
        filters=[Filter(field='name', operator=Operator.CONTAINS, value='Doe')],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_body_to_criteria_converter_with_valid_field_operator_direction_and_pagination_checks() -> None:
    """
    Test BodyToCriteriaConverter class with all validation checks enabled.
    """
    body = {
        'filters': [{'field': 'name', 'operator': 'EQUAL', 'value': 'Doe'}],
        'orders': [{'field': 'name', 'direction': 'ASC'}],
        'page_size': 20,
        'page_number': 1,
    }
    criteria = BodyToCriteriaConverter.convert(
        body=body,
        check_field_injection=True,
        check_operator_injection=True,
        check_direction_injection=True,
        check_pagination_bounds=True,
        valid_fields=['name'],
        valid_operators=[Operator.EQUAL],
        valid_directions=[Direction.ASC],
        max_page_size=100,
        max_page_number=10,
    )

    expected = Criteria(
        filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')],
        orders=[Order(field='name', direction=Direction.ASC)],
        page_size=20,
        page_number=1,
    )

    assert criteria == expected


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_body_type() -> None:
    """
    Test BodyToCriteriaConverter class with an invalid body type.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter body <<<\\[\\]>>> must be a mapping. Got <<<list>>> type.',
    ):
        BodyToCriteriaConverter.convert(body=[])  # type: ignore[arg-type]


@mark.unit_testing
def test_body_to_criteria_converter_with_non_string_body_key() -> None:
    """
    Test BodyToCriteriaConverter class with a non-string body key.
    """
    body: dict[Any, Any] = {1: []}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter body keys <<<1>>> must be strings.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_unknown_body_key() -> None:
    """
    Test BodyToCriteriaConverter class with an unknown body key.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter body has unsupported keys <<<limit>>>.',
    ):
        BodyToCriteriaConverter.convert(body={'limit': 10})


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_filters_type() -> None:
    """
    Test BodyToCriteriaConverter class with invalid filters type.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filters <<<invalid>>> must be a list. Got <<<str>>> type.',
    ):
        BodyToCriteriaConverter.convert(body={'filters': 'invalid'})


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_filter_item_type() -> None:
    """
    Test BodyToCriteriaConverter class with an invalid filter item type.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filters\\[0\\] <<<invalid>>> must be a mapping. Got <<<str>>> type.',
    ):
        BodyToCriteriaConverter.convert(body={'filters': ['invalid']})


@mark.unit_testing
def test_body_to_criteria_converter_with_non_string_filter_key() -> None:
    """
    Test BodyToCriteriaConverter class with a non-string filter key.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filters\\[0\\] keys <<<1>>> must be strings.',
    ):
        BodyToCriteriaConverter.convert(body={'filters': [{1: 'name'}]})


@mark.unit_testing
def test_body_to_criteria_converter_with_missing_filter_field() -> None:
    """
    Test BodyToCriteriaConverter class with missing filter field.
    """
    body = {'filters': [{'operator': 'EQUAL', 'value': 'Doe'}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filters\\[0\\] has missing keys <<<field>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_extra_filter_key() -> None:
    """
    Test BodyToCriteriaConverter class with an extra filter key.
    """
    body = {'filters': [{'field': 'name', 'operator': 'EQUAL', 'value': 'Doe', 'extra': True}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filters\\[0\\] has unsupported keys <<<extra>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_unsupported_filter_operator() -> None:
    """
    Test BodyToCriteriaConverter class with unsupported filter operator.
    """
    body = {'filters': [{'field': 'name', 'operator': 'UNKNOWN', 'value': 'Doe'}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filter <<<filters\\[0\\]>>> has unsupported operator <<<UNKNOWN>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_filter_operator_type() -> None:
    """
    Test BodyToCriteriaConverter class with invalid filter operator type.
    """
    body = {'filters': [{'field': 'name', 'operator': 1, 'value': 'Doe'}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filter <<<filters\\[0\\]>>> has unsupported operator <<<1>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_missing_filter_value() -> None:
    """
    Test BodyToCriteriaConverter class with missing filter value.
    """
    body = {'filters': [{'field': 'name', 'operator': 'EQUAL'}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filter <<<filters\\[0\\]>>> has missing value.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_between_type() -> None:
    """
    Test BodyToCriteriaConverter class with invalid BETWEEN value type.
    """
    body = {'filters': [{'field': 'price', 'operator': 'BETWEEN', 'value': '10,100'}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filter <<<filters\\[0\\]>>> expects exactly two values for BETWEEN operators.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_between_length() -> None:
    """
    Test BodyToCriteriaConverter class with invalid BETWEEN value length.
    """
    body = {'filters': [{'field': 'price', 'operator': 'BETWEEN', 'value': [10]}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filter <<<filters\\[0\\]>>> expects exactly two values for BETWEEN operators.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_in_type() -> None:
    """
    Test BodyToCriteriaConverter class with invalid IN value type.
    """
    body = {'filters': [{'field': 'status', 'operator': 'IN', 'value': 'ACTIVE'}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filter <<<filters\\[0\\]>>> expects at least one value for IN operators.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_empty_in_value() -> None:
    """
    Test BodyToCriteriaConverter class with empty IN value.
    """
    body = {'filters': [{'field': 'status', 'operator': 'IN', 'value': []}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filter <<<filters\\[0\\]>>> expects at least one value for IN operators.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_orders_type() -> None:
    """
    Test BodyToCriteriaConverter class with invalid orders type.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter orders <<<invalid>>> must be a list. Got <<<str>>> type.',
    ):
        BodyToCriteriaConverter.convert(body={'orders': 'invalid'})


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_order_item_type() -> None:
    """
    Test BodyToCriteriaConverter class with an invalid order item type.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter orders\\[0\\] <<<invalid>>> must be a mapping. Got <<<str>>> type.',
    ):
        BodyToCriteriaConverter.convert(body={'orders': ['invalid']})


@mark.unit_testing
def test_body_to_criteria_converter_with_missing_order_field() -> None:
    """
    Test BodyToCriteriaConverter class with missing order field.
    """
    body = {'orders': [{'direction': 'ASC'}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter orders\\[0\\] has missing keys <<<field>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_extra_order_key() -> None:
    """
    Test BodyToCriteriaConverter class with extra order key.
    """
    body = {'orders': [{'field': 'name', 'direction': 'ASC', 'extra': True}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter orders\\[0\\] has unsupported keys <<<extra>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_unsupported_order_direction() -> None:
    """
    Test BodyToCriteriaConverter class with unsupported order direction.
    """
    body = {'orders': [{'field': 'name', 'direction': 'UNKNOWN'}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter order <<<orders\\[0\\]>>> has unsupported direction <<<UNKNOWN>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_order_direction_type() -> None:
    """
    Test BodyToCriteriaConverter class with invalid order direction type.
    """
    body = {'orders': [{'field': 'name', 'direction': 1}]}

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter order <<<orders\\[0\\]>>> has unsupported direction <<<1>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_field() -> None:
    """
    Test BodyToCriteriaConverter class with invalid field validation.
    """
    body = {'filters': [{'field': 'invalid', 'operator': 'EQUAL', 'value': 'Doe'}]}

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<invalid>>>. Valid columns are <<<name>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body, check_field_injection=True, valid_fields=['name'])


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_order_field() -> None:
    """
    Test BodyToCriteriaConverter class with invalid order field validation.
    """
    body = {'orders': [{'field': 'invalid', 'direction': 'ASC'}]}

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<invalid>>>. Valid columns are <<<name>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body, check_field_injection=True, valid_fields=['name'])


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_operator_validation() -> None:
    """
    Test BodyToCriteriaConverter class with invalid operator validation.
    """
    body = {'filters': [{'field': 'name', 'operator': 'EQUAL', 'value': 'Doe'}]}

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER>>>.',
    ):
        BodyToCriteriaConverter.convert(
            body=body,
            check_operator_injection=True,
            valid_operators=[Operator.GREATER],
        )


@mark.unit_testing
def test_body_to_criteria_converter_with_invalid_direction_validation() -> None:
    """
    Test BodyToCriteriaConverter class with invalid direction validation.
    """
    body = {'orders': [{'field': 'name', 'direction': 'DESC'}]}

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        BodyToCriteriaConverter.convert(
            body=body,
            check_direction_injection=True,
            valid_directions=[Direction.ASC],
        )


@mark.unit_testing
def test_body_to_criteria_converter_with_page_size_bounds_exceeded() -> None:
    """
    Test BodyToCriteriaConverter class with page_size bounds exceeded.
    """
    body = {'page_size': 50000, 'page_number': 1}

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_size>>> <<<50000>>> exceeds maximum allowed value <<<10000>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body, check_pagination_bounds=True, max_page_size=10000)


@mark.unit_testing
def test_body_to_criteria_converter_with_page_number_bounds_exceeded() -> None:
    """
    Test BodyToCriteriaConverter class with page_number bounds exceeded.
    """
    body = {'page_size': 10, 'page_number': 2000000}

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_number>>> <<<2000000>>> exceeds maximum allowed value <<<1000000>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body, check_pagination_bounds=True, max_page_number=1000000)


@mark.unit_testing
def test_body_to_criteria_converter_with_page_number_without_page_size() -> None:
    """
    Test BodyToCriteriaConverter class with page_number but no page_size.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match='Criteria page_number <<<2>>> cannot be provided without page_size.',
    ):
        BodyToCriteriaConverter.convert(body={'page_number': 2})


@mark.unit_testing
def test_body_to_criteria_converter_with_non_integer_page_size() -> None:
    """
    Test BodyToCriteriaConverter class with a non-integer page_size.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match='Criteria page_size <<<20>>> must be an integer.',
    ):
        BodyToCriteriaConverter.convert(body={'page_size': '20'})


@mark.unit_testing
def test_body_to_criteria_converter_export() -> None:
    """
    Test BodyToCriteriaConverter class export.
    """
    from criteria_pattern.converters import BodyToCriteriaConverter as ExportedBodyToCriteriaConverter

    assert ExportedBodyToCriteriaConverter is BodyToCriteriaConverter
