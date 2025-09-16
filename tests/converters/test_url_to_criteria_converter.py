"""
Test UrlToCriteriaConverter class.
"""

from urllib.parse import quote_plus

from object_mother_pattern.mothers import IntegerMother, StringMother
from pytest import mark, raises as assert_raises

from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.converters import UrlToCriteriaConverter
from criteria_pattern.errors import (
    IntegrityError,
    InvalidColumnError,
    InvalidDirectionError,
    InvalidOperatorError,
    PaginationBoundsError,
)


@mark.unit_testing
def test_url_to_criteria_converter_with_empty_url() -> None:
    """
    Test UrlToCriteriaConverter class with an empty URL.
    """
    url = 'https://api.example.com/users'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected = Criteria(filters=None, orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_equal_filter() -> None:
    """
    Test UrlToCriteriaConverter class with an EQUAL filter.
    """
    field_name = StringMother.alphanumeric()
    field_value = StringMother.create()
    url = f'https://api.example.com/users?filters[0][field]={field_name}&filters[0][operator]=EQUAL&filters[0][value]={field_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field=field_name, operator=Operator.EQUAL, value=field_value)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_not_equal_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a NOT EQUAL filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=NOT_EQUAL&filters[0][value]=John Doe'  # noqa: E501  # fmt: skip
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.NOT_EQUAL, value='John Doe')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_greater_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a GREATER filter.
    """
    field_name = StringMother.alphanumeric()
    field_value = IntegerMother.positive()
    url = f'https://api.example.com/users?filters[0][field]={field_name}&filters[0][operator]=GREATER&filters[0][value]={field_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field=field_name, operator=Operator.GREATER, value=field_value)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_greater_or_equal_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a GREATER OR EQUAL filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=GREATER_OR_EQUAL&filters[0][value]=18'  # noqa: E501  # fmt: skip
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_less_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a LESS filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=LESS&filters[0][value]=18'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='age', operator=Operator.LESS, value=18)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_less_or_equal_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a LESS OR EQUAL filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=LESS_OR_EQUAL&filters[0][value]=18'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='age', operator=Operator.LESS_OR_EQUAL, value=18)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_like_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a LIKE filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=LIKE&filters[0][value]=John'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.LIKE, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_not_like_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a NOT LIKE filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=NOT_LIKE&filters[0][value]=John'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.NOT_LIKE, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_contains_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a CONTAINS filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=CONTAINS&filters[0][value]=John'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.CONTAINS, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_not_contains_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a NOT CONTAINS filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=NOT_CONTAINS&filters[0][value]=John'  # noqa: E501  # fmt: skip
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.NOT_CONTAINS, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_starts_with_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a STARTS WITH filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=STARTS_WITH&filters[0][value]=John'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.STARTS_WITH, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_not_starts_with_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a NOT STARTS WITH filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=NOT_STARTS_WITH&filters[0][value]=John'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.NOT_STARTS_WITH, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_ends_with_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a ENDS WITH filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=ENDS_WITH&filters[0][value]=Doe'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.ENDS_WITH, value='Doe')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_not_ends_with_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a NOT ENDS WITH filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=NOT_ENDS_WITH&filters[0][value]=Doe'  # noqa: E501  # fmt: skip
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.NOT_ENDS_WITH, value='Doe')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_between_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a BETWEEN filter.
    """
    field_name = StringMother.alphanumeric()
    min_value = IntegerMother.positive()
    max_value = IntegerMother.positive()
    url = f'https://api.example.com/users?filters[0][field]={field_name}&filters[0][operator]=BETWEEN&filters[0][value]={min_value},{max_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field=field_name, operator=Operator.BETWEEN, value=[min_value, max_value])
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_not_between_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a NOT BETWEEN filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=NOT_BETWEEN&filters[0][value]=18,30'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='age', operator=Operator.NOT_BETWEEN, value=[18, 30])
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_is_null_filter() -> None:
    """
    Test UrlToCriteriaConverter class with an IS NULL filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=email&filters[0][operator]=IS_NULL&filters[0][value]='
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='email', operator=Operator.IS_NULL, value=None)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_is_not_null_filter() -> None:
    """
    Test UrlToCriteriaConverter class with an IS NOT NULL filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=email&filters[0][operator]=IS_NOT_NULL&filters[0][value]='
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_in_filter() -> None:
    """
    Test UrlToCriteriaConverter class with an IN filter.
    """
    field_name = StringMother.alphanumeric()
    value1 = StringMother.alpha()
    value2 = StringMother.alpha()
    value3 = StringMother.alpha()
    url = f'https://api.example.com/users?filters[0][field]={field_name}&filters[0][operator]=IN&filters[0][value]={value1},{value2},{value3}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field=field_name, operator=Operator.IN, value=[value1, value2, value3])
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_not_in_filter() -> None:
    """
    Test UrlToCriteriaConverter class with a NOT IN filter.
    """
    url = 'https://api.example.com/users?filters[0][field]=status&filters[0][operator]=NOT_IN&filters[0][value]=deleted,banned'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='status', operator=Operator.NOT_IN, value=['deleted', 'banned'])
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_asc_order() -> None:
    """
    Test UrlToCriteriaConverter class with an ASC order.
    """
    field_name = StringMother.alphanumeric()
    url = f'https://api.example.com/users?orders[0][field]={field_name}&orders[0][direction]=ASC'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_order = Order(field=field_name, direction=Direction.ASC)
    expected = Criteria(filters=None, orders=[expected_order], page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_desc_order() -> None:
    """
    Test UrlToCriteriaConverter class with a DESC order.
    """
    url = 'https://api.example.com/users?orders[0][field]=name&orders[0][direction]=DESC'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_order = Order(field='name', direction=Direction.DESC)
    expected = Criteria(filters=None, orders=[expected_order], page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_multiple_orders() -> None:
    """
    Test UrlToCriteriaConverter class with multiple orders.
    """
    url = 'https://api.example.com/users?orders[0][field]=name&orders[0][direction]=ASC&orders[1][field]=email&orders[1][direction]=DESC'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_order1 = Order(field='name', direction=Direction.ASC)
    expected_order2 = Order(field='email', direction=Direction.DESC)
    expected = Criteria(filters=None, orders=[expected_order1, expected_order2], page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_filters_and_orders() -> None:
    """
    Test UrlToCriteriaConverter class with filters and orders.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=John Doe&filters[1][field]=email&filters[1][operator]=IS_NOT_NULL&filters[1][value]=&orders[0][field]=email&orders[0][direction]=DESC&orders[1][field]=name&orders[1][direction]=ASC'  # noqa: E501  # fmt: skip
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    expected_filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    expected_order1 = Order(field='email', direction=Direction.DESC)
    expected_order2 = Order(field='name', direction=Direction.ASC)
    expected = Criteria(
        filters=[expected_filter1, expected_filter2],
        orders=[expected_order1, expected_order2],
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_pagination() -> None:
    """
    Test UrlToCriteriaConverter class with pagination.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()
    url = f'https://api.example.com/users?page_size={page_size}&page_number={page_number}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected = Criteria(filters=None, orders=None, page_size=page_size, page_number=page_number)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_page_size_only() -> None:
    """
    Test UrlToCriteriaConverter class with only page_size.
    """
    url = 'https://api.example.com/users?page_size=10'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected = Criteria(filters=None, orders=None, page_size=10, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_filters_and_pagination() -> None:
    """
    Test UrlToCriteriaConverter class with filters and pagination.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=GREATER_OR_EQUAL&filters[0][value]=18&page_size=20&page_number=3'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=20, page_number=3)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_orders_and_pagination() -> None:
    """
    Test UrlToCriteriaConverter class with orders and pagination.
    """
    url = 'https://api.example.com/users?orders[0][field]=name&orders[0][direction]=ASC&page_size=20&page_number=3'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_order = Order(field='name', direction=Direction.ASC)
    expected = Criteria(filters=None, orders=[expected_order], page_size=20, page_number=3)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_filters_orders_and_pagination() -> None:
    """
    Test UrlToCriteriaConverter class with filters, orders, and pagination.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=GREATER_OR_EQUAL&filters[0][value]=18&orders[0][field]=name&orders[0][direction]=DESC&page_size=20&page_number=3'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    expected_order = Order(field='name', direction=Direction.DESC)
    expected = Criteria(filters=[expected_filter], orders=[expected_order], page_size=20, page_number=3)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_fields_mapping() -> None:
    """
    Test UrlToCriteriaConverter class with fields mapping.
    """
    url = 'https://api.example.com/users?filters[0][field]=full_name&filters[0][operator]=EQUAL&filters[0][value]=John Doe&orders[0][field]=full_name&orders[0][direction]=ASC'  # noqa: E501  # fmt: skip
    fields_mapping = {'full_name': 'name'}
    criteria = UrlToCriteriaConverter.convert(url=url, fields_mapping=fields_mapping)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    expected_order = Order(field='name', direction=Direction.ASC)
    expected = Criteria(filters=[expected_filter], orders=[expected_order], page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_url_encoded_values() -> None:
    """
    Test UrlToCriteriaConverter class with URL-encoded values.
    """
    encoded_value = quote_plus('John Doe Jr.')
    url = f'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]={encoded_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe Jr.')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_boolean_values() -> None:
    """
    Test UrlToCriteriaConverter class with boolean values.
    """
    url = 'https://api.example.com/users?filters[0][field]=active&filters[0][operator]=EQUAL&filters[0][value]=true&filters[1][field]=verified&filters[1][operator]=EQUAL&filters[1][value]=false'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter1 = Filter(field='active', operator=Operator.EQUAL, value=True)
    expected_filter2 = Filter(field='verified', operator=Operator.EQUAL, value=False)
    expected = Criteria(filters=[expected_filter1, expected_filter2], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_null_values() -> None:
    """
    Test UrlToCriteriaConverter class with null values.
    """
    url = 'https://api.example.com/users?filters[0][field]=middle_name&filters[0][operator]=EQUAL&filters[0][value]=null'  # noqa: E501  # fmt: skip
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='middle_name', operator=Operator.EQUAL, value=None)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_empty_string_value() -> None:
    """
    Test UrlToCriteriaConverter class with empty string value.
    """
    url = 'https://api.example.com/users?filters[0][field]=middle_name&filters[0][operator]=EQUAL&filters[0][value]='
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='middle_name', operator=Operator.EQUAL, value='')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_numeric_values() -> None:
    """
    Test UrlToCriteriaConverter class with numeric values.
    """
    field1_name = StringMother.alphanumeric()
    field2_name = StringMother.alphanumeric()
    integer_value = IntegerMother.positive()
    float_value = 50000.5
    url = f'https://api.example.com/users?filters[0][field]={field1_name}&filters[0][operator]=EQUAL&filters[0][value]={integer_value}&filters[1][field]={field2_name}&filters[1][operator]=EQUAL&filters[1][value]={float_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter1 = Filter(field=field1_name, operator=Operator.EQUAL, value=integer_value)
    expected_filter2 = Filter(field=field2_name, operator=Operator.EQUAL, value=float_value)
    expected = Criteria(filters=[expected_filter1, expected_filter2], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_field_injection_check_disabled() -> None:
    """
    Test UrlToCriteriaConverter class with field injection when check_field_injection is disabled.
    """
    url = 'https://api.example.com/users?filters[0][field]=id; DROP TABLE user;&filters[0][operator]=EQUAL&filters[0][value]=1'  # noqa: E501  # fmt: skip
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='id; DROP TABLE user;', operator=Operator.EQUAL, value=1)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_field_injection_check_enabled() -> None:
    """
    Test UrlToCriteriaConverter class with field injection when check_field_injection is enabled.
    """
    url = 'https://api.example.com/users?filters[0][field]=id; DROP TABLE user;&filters[0][operator]=EQUAL&filters[0][value]=1'  # noqa: E501  # fmt: skip
    valid_fields = ['id', 'name', 'email']

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name, email>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url, check_field_injection=True, valid_fields=valid_fields)


@mark.unit_testing
def test_url_to_criteria_converter_with_valid_fields() -> None:
    """
    Test UrlToCriteriaConverter class with valid fields.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=John Doe&orders[0][field]=email&orders[0][direction]=ASC'  # noqa: E501  # fmt: skip
    valid_fields = ['id', 'name', 'email']
    criteria = UrlToCriteriaConverter.convert(url=url, check_field_injection=True, valid_fields=valid_fields)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    expected_order = Order(field='email', direction=Direction.ASC)
    expected = Criteria(filters=[expected_filter], orders=[expected_order], page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_invalid_filter_field() -> None:
    """
    Test UrlToCriteriaConverter class with invalid filter field.
    """
    url = 'https://api.example.com/users?filters[0][field]=invalid_field&filters[0][operator]=EQUAL&filters[0][value]=test'
    valid_fields = ['id', 'name', 'email']

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<invalid_field>>>. Valid columns are <<<id, name, email>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url, check_field_injection=True, valid_fields=valid_fields)


@mark.unit_testing
def test_url_to_criteria_converter_with_invalid_order_field() -> None:
    """
    Test UrlToCriteriaConverter class with invalid order field.
    """
    url = 'https://api.example.com/users?orders[0][field]=invalid_field&orders[0][direction]=ASC'
    valid_fields = ['id', 'name', 'email']

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<invalid_field>>>. Valid columns are <<<id, name, email>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url, check_field_injection=True, valid_fields=valid_fields)


@mark.unit_testing
def test_url_to_criteria_converter_with_missing_filter_field() -> None:
    """
    Test UrlToCriteriaConverter class with missing filter field.
    """
    url = 'https://api.example.com/users?filters[0][operator]=EQUAL&filters[0][value]=test'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter filter <<<filters\\[0\\]>>> has missing field.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_missing_filter_operator() -> None:
    """
    Test UrlToCriteriaConverter class with missing filter operator.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][value]=test'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter filter <<<filters\\[0\\]>>> has missing operator.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_missing_filter_value() -> None:
    """
    Test UrlToCriteriaConverter class with missing filter value.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter filter <<<filters\\[0\\]>>> has missing value.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_invalid_operator() -> None:
    """
    Test UrlToCriteriaConverter class with invalid operator.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=INVALID_OP&filters[0][value]=test'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter filter <<<filters\\[0\\]>>> has unsupported operator <<<INVALID_OP>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_missing_order_field() -> None:
    """
    Test UrlToCriteriaConverter class with missing order field.
    """
    url = 'https://api.example.com/users?orders[0][direction]=ASC'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter order <<<orders\\[0\\]>>> has missing field.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_missing_order_direction() -> None:
    """
    Test UrlToCriteriaConverter class with missing order direction.
    """
    url = 'https://api.example.com/users?orders[0][field]=name'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter order <<<orders\\[0\\]>>> has missing direction.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_invalid_direction() -> None:
    """
    Test UrlToCriteriaConverter class with invalid direction.
    """
    url = 'https://api.example.com/users?orders[0][field]=name&orders[0][direction]=INVALID_DIR'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter order <<<orders\\[0\\]>>> has unsupported direction <<<INVALID_DIR>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_invalid_filter_index() -> None:
    """
    Test UrlToCriteriaConverter class with invalid filter index.
    """
    url = 'https://api.example.com/users?filters[abc][field]=name&filters[abc][operator]=EQUAL&filters[abc][value]=test'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter filter <<<filters\\[abc\\]>>> must be an integer.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_invalid_order_index() -> None:
    """
    Test UrlToCriteriaConverter class with invalid order index.
    """
    url = 'https://api.example.com/users?orders[xyz][field]=name&orders[xyz][direction]=ASC'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter order <<<orders\\[xyz\\]>>> must be an integer.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_between_insufficient_values() -> None:
    """
    Test UrlToCriteriaConverter class with BETWEEN filter having insufficient values.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=BETWEEN&filters[0][value]=18'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter filter <<<filters\\[0\\]>>> has invalid value <<<18>>> for operator <<<BETWEEN>>>.',  # noqa: E501
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_between_too_many_values() -> None:
    """
    Test UrlToCriteriaConverter class with BETWEEN filter having too many values.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=BETWEEN&filters[0][value]=18,25,30'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter filter <<<filters\\[0\\]>>> has invalid value <<<18,25,30>>> for operator <<<BETWEEN>>>.',  # noqa: E501
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_in_empty_values() -> None:
    """
    Test UrlToCriteriaConverter class with IN filter having empty values.
    """
    url = 'https://api.example.com/users?filters[0][field]=status&filters[0][operator]=IN&filters[0][value]=,,'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter filter <<<filters\\[0\\]>>> has invalid value <<<,,>>> for operator <<<IN>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_case_insensitive_operators() -> None:
    """
    Test UrlToCriteriaConverter class with case insensitive operators.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=equal&filters[0][value]=John&orders[0][field]=name&orders[0][direction]=asc'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='John')
    expected_order = Order(field='name', direction=Direction.ASC)
    expected = Criteria(filters=[expected_filter], orders=[expected_order], page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_mixed_case_operators() -> None:
    """
    Test UrlToCriteriaConverter class with mixed case operators.
    """
    field_name = StringMother.alphanumeric()
    threshold_value = IntegerMother.positive()
    url = f'https://api.example.com/users?filters[0][field]={field_name}&filters[0][operator]=Greater_Or_Equal&filters[0][value]={threshold_value}&orders[0][field]={field_name}&orders[0][direction]=Desc'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field=field_name, operator=Operator.GREATER_OR_EQUAL, value=threshold_value)
    expected_order = Order(field=field_name, direction=Direction.DESC)
    expected = Criteria(filters=[expected_filter], orders=[expected_order], page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_maximum_field_limit() -> None:
    """
    Test UrlToCriteriaConverter class with field index at maximum limit.
    """
    field_name = StringMother.alphanumeric()
    field_value = StringMother.create()
    url = f'https://api.example.com/users?filters[99][field]={field_name}&filters[99][operator]=EQUAL&filters[99][value]={field_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field=field_name, operator=Operator.EQUAL, value=field_value)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_field_limit_exceeded() -> None:
    """
    Test UrlToCriteriaConverter class with field index exceeding maximum limit.
    """
    field_name = StringMother.alphanumeric()
    field_value = StringMother.create()
    url = f'https://api.example.com/users?filters[100][field]={field_name}&filters[100][operator]=EQUAL&filters[100][value]={field_value}'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter filter <<<filters\\[100\\]>>> exceeds maximum limit of <<<100>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_order_limit_exceeded() -> None:
    """
    Test UrlToCriteriaConverter class with order index exceeding maximum limit.
    """
    field_name = StringMother.alphanumeric()
    url = f'https://api.example.com/users?orders[100][field]={field_name}&orders[100][direction]=ASC'

    with assert_raises(
        expected_exception=IntegrityError,
        match='UrlToCriteriaConverter order <<<orders\\[100\\]>>> exceeds maximum limit of <<<100>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_complex_combined_criteria() -> None:
    """
    Test UrlToCriteriaConverter class with complex combination of filters, orders and pagination.
    """
    name_field = StringMother.alphanumeric()
    email_field = StringMother.alphanumeric()
    age_field = StringMother.alphanumeric()
    name_value = StringMother.create()
    age_value = IntegerMother.positive()
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()
    url = f'https://api.example.com/users?filters[0][field]={name_field}&filters[0][operator]=EQUAL&filters[0][value]={name_value}&filters[1][field]={email_field}&filters[1][operator]=IS_NOT_NULL&filters[1][value]=&filters[2][field]={age_field}&filters[2][operator]=LESS&filters[2][value]={age_value}&orders[0][field]={email_field}&orders[0][direction]=DESC&orders[1][field]={name_field}&orders[1][direction]=ASC&page_size={page_size}&page_number={page_number}'  # noqa: E501  # fmt: skip
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter1 = Filter(field=name_field, operator=Operator.EQUAL, value=name_value)
    expected_filter2 = Filter(field=email_field, operator=Operator.IS_NOT_NULL, value=None)
    expected_filter3 = Filter(field=age_field, operator=Operator.LESS, value=age_value)
    expected_order1 = Order(field=email_field, direction=Direction.DESC)
    expected_order2 = Order(field=name_field, direction=Direction.ASC)
    expected = Criteria(
        filters=[expected_filter1, expected_filter2, expected_filter3],
        orders=[expected_order1, expected_order2],
        page_size=page_size,
        page_number=page_number,
    )

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_non_sequential_indexes() -> None:
    """
    Test UrlToCriteriaConverter class with non-sequential filter and order indexes.
    """
    name_field = StringMother.alphanumeric()
    age_field = StringMother.alphanumeric()
    name_value = StringMother.create()
    age_value = IntegerMother.positive()
    url = f'https://api.example.com/users?filters[2][field]={name_field}&filters[2][operator]=EQUAL&filters[2][value]={name_value}&filters[0][field]={age_field}&filters[0][operator]=GREATER&filters[0][value]={age_value}&orders[1][field]={name_field}&orders[1][direction]=ASC&orders[5][field]={age_field}&orders[5][direction]=DESC'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter1 = Filter(field=age_field, operator=Operator.GREATER, value=age_value)
    expected_filter2 = Filter(field=name_field, operator=Operator.EQUAL, value=name_value)
    expected_order1 = Order(field=name_field, direction=Direction.ASC)
    expected_order2 = Order(field=age_field, direction=Direction.DESC)

    expected = Criteria(
        filters=[expected_filter1, expected_filter2],
        orders=[expected_order1, expected_order2],
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_random_query_parameters() -> None:
    """
    Test UrlToCriteriaConverter class ignoring random unrelated query parameters.
    """
    field_name = StringMother.alphanumeric()
    field_value = StringMother.create()
    url = f'https://api.example.com/users?filters[0][field]={field_name}&filters[0][operator]=EQUAL&filters[0][value]={field_value}&randomParam=ignored&api_key=secret123&callback=jsonp&_timestamp=1234567890'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field=field_name, operator=Operator.EQUAL, value=field_value)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_special_characters_encoded() -> None:
    """
    Test UrlToCriteriaConverter class with various encoded special characters.
    """
    encoded_value = quote_plus('John & Jane = 100% "awesome"')
    url = f'https://api.example.com/users?filters[0][field]=description&filters[0][operator]=EQUAL&filters[0][value]={encoded_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='description', operator=Operator.EQUAL, value='John & Jane = 100% "awesome"')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_unicode_characters() -> None:
    """
    Test UrlToCriteriaConverter class with Unicode characters.
    """
    unicode_value = quote_plus('José María 🎉 测试')
    url = f'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]={unicode_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='José María 🎉 测试')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_html_entities() -> None:
    """
    Test UrlToCriteriaConverter class with HTML entities in values.
    """
    encoded_value = quote_plus('<script>alert("xss")</script>')
    url = f'https://api.example.com/users?filters[0][field]=comment&filters[0][operator]=EQUAL&filters[0][value]={encoded_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='comment', operator=Operator.EQUAL, value='<script>alert("xss")</script>')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_sql_injection_in_values() -> None:
    """
    Test UrlToCriteriaConverter class with SQL injection attempts in filter values.
    """
    sql_injection = quote_plus("'; DROP TABLE users; --")
    url = f'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]={sql_injection}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value="'; DROP TABLE users; --")
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_malformed_brackets() -> None:
    """
    Test UrlToCriteriaConverter class with malformed bracket syntax in query parameters.
    """
    url = 'https://api.example.com/users?filters[0[field]=name&filters0][operator]=EQUAL&filters[field]=ignored&orders][0][field]=name'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected = Criteria(filters=None, orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_empty_bracket_values() -> None:
    """
    Test UrlToCriteriaConverter class with empty bracket values.
    """
    url = 'https://api.example.com/users?filters[][field]=name&filters[][operator]=EQUAL&random=ignored'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected = Criteria(filters=None, orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_nested_brackets() -> None:
    """
    Test UrlToCriteriaConverter class with nested brackets in query parameters.
    """
    url = 'https://api.example.com/users?filters[0][nested[field]]=name&random=ignored'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected = Criteria(filters=None, orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_duplicate_parameters() -> None:
    """
    Test UrlToCriteriaConverter class with duplicate query parameters.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][field]=age&filters[0][operator]=EQUAL&filters[0][value]=John'
    criteria = UrlToCriteriaConverter.convert(url=url)
    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_very_long_values() -> None:
    """
    Test UrlToCriteriaConverter class with extremely long values.
    """
    field_name = StringMother.alphanumeric()
    long_value = StringMother.of_length(length=1000)  # 1000 character string
    encoded_value = quote_plus(long_value)
    url = f'https://api.example.com/users?filters[0][field]={field_name}&filters[0][operator]=EQUAL&filters[0][value]={encoded_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field=field_name, operator=Operator.EQUAL, value=long_value)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_plus_signs_in_values() -> None:
    """
    Test UrlToCriteriaConverter class with plus signs in values (URL encoding behavior).
    """
    url = 'https://api.example.com/users?filters[0][field]=phone&filters[0][operator]=EQUAL&filters[0][value]=%2B1-555-123-4567'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='phone', operator=Operator.EQUAL, value=' 1-555-123-4567')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_spaces_as_plus() -> None:
    """
    Test UrlToCriteriaConverter class with spaces encoded as plus signs.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=John+Doe'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_mixed_encoding_styles() -> None:
    """
    Test UrlToCriteriaConverter class with mixed URL encoding styles.
    """
    url = 'https://api.example.com/users?filters[0][field]=description&filters[0][operator]=CONTAINS&filters[0][value]=hello%20world+and%26more'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='description', operator=Operator.CONTAINS, value='hello world and&more')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_fragment_and_random_text() -> None:
    """
    Test UrlToCriteriaConverter class with URL fragments and random text after query.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=John#fragment-ignored'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_port_and_path() -> None:
    """
    Test UrlToCriteriaConverter class with different ports and paths.
    """
    url = 'https://api.example.com:8080/v1/admin/users/search?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=John'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_no_protocol() -> None:
    """
    Test UrlToCriteriaConverter class with URLs missing protocol.
    """
    url = 'api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=John'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_malformed_url() -> None:
    """
    Test UrlToCriteriaConverter class with malformed URL structure.
    """
    url = 'not-a-url?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=John'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='name', operator=Operator.EQUAL, value='John')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_percent_encoded_operators() -> None:
    """
    Test UrlToCriteriaConverter class with percent-encoded operators (should still work).
    """
    encoded_operator = quote_plus('GREATER_OR_EQUAL')
    url = f'https://api.example.com/users?filters[0][field]=age&filters[0][operator]={encoded_operator}&filters[0][value]=18'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_json_like_values() -> None:
    """
    Test UrlToCriteriaConverter class with JSON-like values that should be treated as strings.
    """
    json_value = quote_plus('{"key": "value", "number": 123}')
    url = f'https://api.example.com/users?filters[0][field]=metadata&filters[0][operator]=EQUAL&filters[0][value]={json_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='metadata', operator=Operator.EQUAL, value='{"key": "value", "number": 123}')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_array_like_values() -> None:
    """
    Test UrlToCriteriaConverter class with array-like values that should be treated as strings.
    """
    array_value = quote_plus('[1, 2, 3, "test"]')
    url = f'https://api.example.com/users?filters[0][field]=tags&filters[0][operator]=EQUAL&filters[0][value]={array_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='tags', operator=Operator.EQUAL, value='[1, 2, 3, "test"]')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_semicolon_separated_values() -> None:
    """
    Test UrlToCriteriaConverter class with semicolon-separated values (should be treated as single string for non-IN
    operators).
    """
    url = 'https://api.example.com/users?filters[0][field]=tags&filters[0][operator]=EQUAL&filters[0][value]=tag1;tag2;tag3'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='tags', operator=Operator.EQUAL, value='tag1;tag2;tag3')
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_mixed_case_boolean_values() -> None:
    """
    Test UrlToCriteriaConverter class with mixed case boolean values.
    """
    url = 'https://api.example.com/users?filters[0][field]=active&filters[0][operator]=EQUAL&filters[0][value]=True&filters[1][field]=verified&filters[1][operator]=EQUAL&filters[1][value]=FALSE'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter1 = Filter(field='active', operator=Operator.EQUAL, value=True)
    expected_filter2 = Filter(field='verified', operator=Operator.EQUAL, value=False)
    expected = Criteria(filters=[expected_filter1, expected_filter2], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_mixed_case_null_values() -> None:
    """
    Test UrlToCriteriaConverter class with mixed case null values.
    """
    url = 'https://api.example.com/users?filters[0][field]=middle_name&filters[0][operator]=EQUAL&filters[0][value]=NULL&filters[1][field]=suffix&filters[1][operator]=EQUAL&filters[1][value]=None'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter1 = Filter(field='middle_name', operator=Operator.EQUAL, value=None)
    expected_filter2 = Filter(field='suffix', operator=Operator.EQUAL, value=None)
    expected = Criteria(filters=[expected_filter1, expected_filter2], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_scientific_notation() -> None:
    """
    Test UrlToCriteriaConverter class with scientific notation numbers.
    """
    url = 'https://api.example.com/users?filters[0][field]=distance&filters[0][operator]=GREATER&filters[0][value]=1.5e10'  # noqa: E501  # fmt: skip
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='distance', operator=Operator.GREATER, value=1.5e10)
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_negative_numbers() -> None:
    """
    Test UrlToCriteriaConverter class with negative numbers.
    """
    field_name = StringMother.alphanumeric()
    negative_value = IntegerMother.negative()
    positive_value = IntegerMother.positive()
    url = f'https://api.example.com/users?filters[0][field]={field_name}&filters[0][operator]=BETWEEN&filters[0][value]={negative_value},{positive_value}'
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field=field_name, operator=Operator.BETWEEN, value=[negative_value, positive_value])
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_leading_trailing_spaces_in_values() -> None:
    """
    Test UrlToCriteriaConverter class with leading and trailing spaces in comma-separated values.
    """
    url = 'https://api.example.com/users?filters[0][field]=status&filters[0][operator]=IN&filters[0][value]= active , pending , inactive '  # noqa: E501  # fmt: skip
    criteria = UrlToCriteriaConverter.convert(url=url)

    expected_filter = Filter(field='status', operator=Operator.IN, value=['active', 'pending', 'inactive'])
    expected = Criteria(filters=[expected_filter], orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_url_to_criteria_converter_with_non_numeric_page_number() -> None:
    """
    Test UrlToCriteriaConverter class to trigger lines 351-352 - IntegrityError exception in _parse_page_number.
    """
    invalid_page_number = StringMother.alpha()
    url = f'https://api.example.com/users?page_number={invalid_page_number}'

    with assert_raises(
        expected_exception=IntegrityError,
        match=f'Criteria page_number <<<{invalid_page_number}>>> cannot be provided without page_size.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_non_numeric_page_size() -> None:
    """
    Test UrlToCriteriaConverter class to trigger lines 372-373 - IntegrityError exception in _parse_page_size.
    """
    invalid_page_size = StringMother.alpha()
    url = f'https://api.example.com/users?page_size={invalid_page_size}'

    with assert_raises(
        expected_exception=TypeError,
        match=f'Criteria page_size <<<{invalid_page_size}>>> must be an integer.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_both_non_numeric_pagination() -> None:
    """
    Test UrlToCriteriaConverter class with both non-numeric page_size and page_number.
    """
    invalid_page_size = StringMother.alpha()
    invalid_page_number = StringMother.alpha()
    url = f'https://api.example.com/users?page_size={invalid_page_size}&page_number={invalid_page_number}'

    with assert_raises(
        expected_exception=TypeError,
        match=f'Criteria page_size <<<{invalid_page_size}>>> must be an integer.',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_with_operator_injection_check_disabled() -> None:
    """
    Test UrlToCriteriaConverter class with operator injection when check_operator_injection is disabled.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=EQUAL&filters[0][value]=25'

    UrlToCriteriaConverter.convert(
        url=url,
        valid_operators=[Operator.GREATER, Operator.LESS],
    )


@mark.unit_testing
def test_url_to_criteria_converter_with_operator_injection() -> None:
    """
    Test UrlToCriteriaConverter class with operator injection.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=EQUAL&filters[0][value]=25'

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        UrlToCriteriaConverter.convert(
            url=url,
            check_operator_injection=True,
            valid_operators=[Operator.GREATER, Operator.LESS],
        )


@mark.unit_testing
def test_url_to_criteria_converter_with_valid_operator() -> None:
    """
    Test UrlToCriteriaConverter class with valid operator.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=GREATER&filters[0][value]=25'

    criteria = UrlToCriteriaConverter.convert(
        url=url,
        check_operator_injection=True,
        valid_operators=[Operator.GREATER, Operator.LESS],
    )

    assert len(criteria.filters) == 1
    assert criteria.filters[0].field == 'age'
    assert criteria.filters[0].operator == Operator.GREATER
    assert criteria.filters[0].value == 25


@mark.unit_testing
def test_url_to_criteria_converter_with_multiple_filters_operator_injection() -> None:
    """
    Test UrlToCriteriaConverter class with multiple filters where one has invalid operator.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=GREATER&filters[0][value]=25&filters[1][field]=name&filters[1][operator]=EQUAL&filters[1][value]=John'

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        UrlToCriteriaConverter.convert(
            url=url,
            check_operator_injection=True,
            valid_operators=[Operator.GREATER, Operator.LESS],
        )


@mark.unit_testing
def test_url_to_criteria_converter_with_complex_url_operator_injection() -> None:
    """
    Test UrlToCriteriaConverter class with complex URL containing invalid operator.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=GREATER&filters[0][value]=18&filters[1][field]=name&filters[1][operator]=LIKE&filters[1][value]=John&orders[0][field]=created_at&orders[0][direction]=DESC'

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<LIKE>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        UrlToCriteriaConverter.convert(
            url=url,
            check_operator_injection=True,
            valid_operators=[Operator.GREATER, Operator.LESS],
        )


@mark.unit_testing
def test_url_to_criteria_converter_with_direction_injection_check_disabled() -> None:
    """
    Test UrlToCriteriaConverter class with direction injection when check_direction_injection is disabled.
    """
    url = 'https://api.example.com/users?orders[0][field]=name&orders[0][direction]=DESC'

    UrlToCriteriaConverter.convert(
        url=url,
        valid_directions=[Direction.ASC],
    )


@mark.unit_testing
def test_url_to_criteria_converter_with_direction_injection() -> None:
    """
    Test UrlToCriteriaConverter class with direction injection.
    """
    url = 'https://api.example.com/users?orders[0][field]=name&orders[0][direction]=DESC'

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        UrlToCriteriaConverter.convert(
            url=url,
            check_direction_injection=True,
            valid_directions=[Direction.ASC],
        )


@mark.unit_testing
def test_url_to_criteria_converter_with_valid_direction() -> None:
    """
    Test UrlToCriteriaConverter class with valid direction.
    """
    url = 'https://api.example.com/users?orders[0][field]=name&orders[0][direction]=ASC'

    criteria = UrlToCriteriaConverter.convert(
        url=url,
        check_direction_injection=True,
        valid_directions=[Direction.ASC, Direction.DESC],
    )

    assert len(criteria.orders) == 1
    assert criteria.orders[0].field == 'name'
    assert criteria.orders[0].direction == Direction.ASC


@mark.unit_testing
def test_url_to_criteria_converter_with_multiple_orders_direction_injection() -> None:
    """
    Test UrlToCriteriaConverter class with multiple orders where one has invalid direction.
    """
    url = 'https://api.example.com/users?orders[0][field]=name&orders[0][direction]=ASC&orders[1][field]=age&orders[1][direction]=DESC'

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        UrlToCriteriaConverter.convert(
            url=url,
            check_direction_injection=True,
            valid_directions=[Direction.ASC],
        )


@mark.unit_testing
def test_url_to_criteria_converter_with_complex_url_direction_injection() -> None:
    """
    Test UrlToCriteriaConverter class with complex URL containing invalid direction.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=GREATER&filters[0][value]=18&orders[0][field]=name&orders[0][direction]=ASC&orders[1][field]=created_at&orders[1][direction]=DESC'

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        UrlToCriteriaConverter.convert(
            url=url,
            check_direction_injection=True,
            valid_directions=[Direction.ASC],
        )


@mark.unit_testing
def test_url_to_criteria_converter_with_pagination_bounds_check_disabled() -> None:
    """
    Test UrlToCriteriaConverter with pagination bounds check disabled (should not raise).
    """
    url = 'https://api.example.com/users?page_size=50000&page_number=2000000'

    criteria = UrlToCriteriaConverter.convert(url=url)

    assert criteria.page_size == 50000
    assert criteria.page_number == 2000000
    assert criteria.filters == []
    assert criteria.orders == []


@mark.unit_testing
def test_url_to_criteria_converter_with_page_size_bounds_exceeded() -> None:
    """
    Test UrlToCriteriaConverter raises PaginationBoundsError when page_size exceeds limit.
    """
    url = 'https://api.example.com/users?page_size=50000&page_number=1'

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_size>>> <<<50000>>> exceeds maximum allowed value <<<10000>>>.',
    ):
        UrlToCriteriaConverter.convert(
            url=url,
            check_pagination_bounds=True,
            max_page_size=10000,
        )


@mark.unit_testing
def test_url_to_criteria_converter_with_page_number_bounds_exceeded() -> None:
    """
    Test UrlToCriteriaConverter raises PaginationBoundsError when page_number exceeds limit.
    """
    url = 'https://api.example.com/users?page_size=100&page_number=2000000'

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_number>>> <<<2000000>>> exceeds maximum allowed value <<<1000000>>>.',
    ):
        UrlToCriteriaConverter.convert(
            url=url,
            check_pagination_bounds=True,
            max_page_number=1000000,
        )


@mark.unit_testing
def test_url_to_criteria_converter_with_valid_pagination_bounds() -> None:
    """
    Test UrlToCriteriaConverter with valid pagination parameters within bounds.
    """
    url = 'https://api.example.com/users?page_size=100&page_number=1000'

    criteria = UrlToCriteriaConverter.convert(
        url=url,
        check_pagination_bounds=True,
        max_page_size=10000,
        max_page_number=1000000,
    )

    assert criteria.page_size == 100
    assert criteria.page_number == 1000
    assert criteria.filters == []
    assert criteria.orders == []


@mark.unit_testing
def test_url_to_criteria_converter_with_custom_pagination_bounds() -> None:
    """
    Test UrlToCriteriaConverter with custom pagination bounds.
    """
    url = 'https://api.example.com/users?page_size=500&page_number=50000'

    criteria = UrlToCriteriaConverter.convert(
        url=url,
        check_pagination_bounds=True,
        max_page_size=1000,
        max_page_number=100000,
    )

    assert criteria.page_size == 500
    assert criteria.page_number == 50000
    assert criteria.filters == []
    assert criteria.orders == []


@mark.unit_testing
def test_url_to_criteria_converter_with_none_pagination_bounds_check() -> None:
    """
    Test UrlToCriteriaConverter with no pagination and bounds checking enabled.
    """
    url = 'https://api.example.com/users'

    criteria = UrlToCriteriaConverter.convert(
        url=url,
        check_pagination_bounds=True,
        max_page_size=10000,
        max_page_number=1000000,
    )

    assert criteria.page_size is None
    assert criteria.page_number is None
    assert criteria.filters == []
    assert criteria.orders == []


@mark.unit_testing
def test_url_to_criteria_converter_with_pagination_and_filters_bounds_check() -> None:
    """
    Test UrlToCriteriaConverter with pagination and filters together with bounds checking.
    """
    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=John&page_size=100&page_number=5'

    criteria = UrlToCriteriaConverter.convert(
        url=url,
        check_pagination_bounds=True,
        max_page_size=1000,
        max_page_number=100,
    )

    assert criteria.page_size == 100
    assert criteria.page_number == 5
    assert len(criteria.filters) == 1
    assert criteria.filters[0].field == 'name'
    assert criteria.filters[0].operator == Operator.EQUAL
    assert criteria.filters[0].value == 'John'


@mark.unit_testing
def test_url_to_criteria_converter_with_pagination_bounds_both_exceeded() -> None:
    """
    Test UrlToCriteriaConverter raises PaginationBoundsError for page_size when both exceed limits.
    """
    url = 'https://api.example.com/users?page_size=50000&page_number=2000000'

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_size>>> <<<50000>>> exceeds maximum allowed value <<<10000>>>.',
    ):
        UrlToCriteriaConverter.convert(
            url=url,
            check_pagination_bounds=True,
            max_page_size=10000,
            max_page_number=1000000,
        )
