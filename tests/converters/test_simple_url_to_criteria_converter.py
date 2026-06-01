"""
Test SimpleUrlToCriteriaConverter class.
"""

from pytest import mark, raises as assert_raises

from criteria_pattern import Criteria, Filter, Operator
from criteria_pattern.converters import SimpleUrlToCriteriaConverter
from criteria_pattern.errors import IntegrityError, InvalidColumnError, InvalidOperatorError, PaginationBoundsError


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_empty_url() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with an empty URL.
    """
    url = 'https://api.example.com/users'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(filters=None, orders=None, page_size=None, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_bare_query_string() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with a bare query string.
    """
    url = 'name=Doe&age_ge=4'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[
            Filter(field='name', operator=Operator.EQUAL, value='Doe'),
            Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=4),
        ],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_explicit_equal_filter() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with an explicit EQUAL filter.
    """
    url = 'https://api.example.com/users?name_eq=Doe'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_comparison_filters() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with comparison filters.
    """
    url = 'https://api.example.com/products?price_gt=10&price_ge=11&price_gte=12&price_lt=100&price_le=99&price_lte=98'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[
            Filter(field='price', operator=Operator.GREATER, value=10),
            Filter(field='price', operator=Operator.GREATER_OR_EQUAL, value=11),
            Filter(field='price', operator=Operator.GREATER_OR_EQUAL, value=12),
            Filter(field='price', operator=Operator.LESS, value=100),
            Filter(field='price', operator=Operator.LESS_OR_EQUAL, value=99),
            Filter(field='price', operator=Operator.LESS_OR_EQUAL, value=98),
        ],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_string_and_negation_filters() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with string and negation filters.
    """
    url = (
        'https://api.example.com/users?'
        'name_ne=John&email_like=%40gmail.com&email_not_like=%40test.com&'
        'email_contains=gmail.com&email_not_contains=test.com&'
        'name_starts_with=Ad&name_not_starts_with=Jo&'
        'name_ends_with=Peris&name_not_ends_with=Doe'
    )
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[
            Filter(field='name', operator=Operator.NOT_EQUAL, value='John'),
            Filter(field='email', operator=Operator.LIKE, value='@gmail.com'),
            Filter(field='email', operator=Operator.NOT_LIKE, value='@test.com'),
            Filter(field='email', operator=Operator.CONTAINS, value='gmail.com'),
            Filter(field='email', operator=Operator.NOT_CONTAINS, value='test.com'),
            Filter(field='name', operator=Operator.STARTS_WITH, value='Ad'),
            Filter(field='name', operator=Operator.NOT_STARTS_WITH, value='Jo'),
            Filter(field='name', operator=Operator.ENDS_WITH, value='Peris'),
            Filter(field='name', operator=Operator.NOT_ENDS_WITH, value='Doe'),
        ],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_in_filters() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with IN and NOT IN filters.
    """
    url = (
        'https://api.example.com/users?'
        'status_in=ACTIVE,PENDING,BLOCKED&category_not_in=deprecated&category_not_in=archived'
    )
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[
            Filter(field='status', operator=Operator.IN, value=['ACTIVE', 'PENDING', 'BLOCKED']),
            Filter(field='category', operator=Operator.NOT_IN, value=['deprecated', 'archived']),
        ],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_between_filters() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with BETWEEN and NOT BETWEEN filters.
    """
    url = 'https://api.example.com/products?price_between=10,100&age_not_between=18&age_not_between=30'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[
            Filter(field='price', operator=Operator.BETWEEN, value=[10, 100]),
            Filter(field='age', operator=Operator.NOT_BETWEEN, value=[18, 30]),
        ],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_null_filters() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with IS NULL and IS NOT NULL filters.
    """
    url = 'https://api.example.com/users?deleted_at_is_null=true&archived_at_is_not_null=false'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

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
def test_simple_url_to_criteria_converter_with_filters_and_pagination() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with filters and pagination.
    """
    url = 'https://api.example.com/users?name=Doe&page_size=20&page_number=3'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')],
        orders=None,
        page_size=20,
        page_number=3,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_page_size_only() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with only page_size.
    """
    url = 'https://api.example.com/users?page_size=10'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(filters=None, orders=None, page_size=10, page_number=None)

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_fields_mapping() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with fields mapping.
    """
    url = 'https://api.example.com/users?full_name=Doe'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        fields_mapping={'full_name': 'name'},
        check_field_injection=True,
        valid_fields=['id', 'name', 'email'],
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_invalid_field() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with an invalid field.
    """
    url = 'https://api.example.com/users?invalid_field=Doe'

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<invalid_field>>>. Valid columns are <<<id, name, email>>>.',
    ):
        SimpleUrlToCriteriaConverter.convert(
            url=url,
            check_field_injection=True,
            valid_fields=['id', 'name', 'email'],
            check_operator_injection=False,
        )


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_invalid_operator() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with an invalid operator.
    """
    url = 'https://api.example.com/users?name=Doe'

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER>>>.',
    ):
        SimpleUrlToCriteriaConverter.convert(
            url=url,
            check_operator_injection=True,
            valid_operators=[Operator.GREATER],
            check_field_injection=False,
        )


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_valid_operator() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with a valid operator.
    """
    url = 'https://api.example.com/users?age_gt=18'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_operator_injection=True,
        valid_operators=[Operator.GREATER],
        check_field_injection=False,
    )

    expected = Criteria(
        filters=[Filter(field='age', operator=Operator.GREATER, value=18)],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_page_size_bounds_exceeded() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with page_size bounds exceeded.
    """
    url = 'https://api.example.com/users?page_size=50000&page_number=1'

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_size>>> <<<50000>>> exceeds maximum allowed value <<<10000>>>.',
    ):
        SimpleUrlToCriteriaConverter.convert(
            url=url,
            check_pagination_bounds=True,
            max_page_size=10000,
            check_field_injection=False,
            check_operator_injection=False,
        )


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_valid_pagination_bounds() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with valid pagination bounds.
    """
    url = 'https://api.example.com/users?page_size=50&page_number=2'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_pagination_bounds=True,
        max_page_size=100,
        max_page_number=10,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(filters=None, orders=None, page_size=50, page_number=2)

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_page_number_bounds_exceeded() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with page_number bounds exceeded.
    """
    url = 'https://api.example.com/users?page_size=10&page_number=2000000'

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_number>>> <<<2000000>>> exceeds maximum allowed value <<<1000000>>>.',
    ):
        SimpleUrlToCriteriaConverter.convert(
            url=url,
            check_pagination_bounds=True,
            max_page_number=1000000,
            check_field_injection=False,
            check_operator_injection=False,
        )


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_page_number_without_page_size() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with page_number but no page_size.
    """
    url = 'https://api.example.com/users?page_number=2'

    with assert_raises(
        expected_exception=IntegrityError,
        match='Criteria page_number <<<2>>> cannot be provided without page_size.',
    ):
        SimpleUrlToCriteriaConverter.convert(url=url, check_field_injection=False, check_operator_injection=False)


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_non_numeric_page_number() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with a non numeric page_number.
    """
    url = 'https://api.example.com/users?page_size=10&page_number=two'

    with assert_raises(
        expected_exception=IntegrityError,
        match='Criteria page_number <<<two>>> must be an integer.',
    ):
        SimpleUrlToCriteriaConverter.convert(url=url, check_field_injection=False, check_operator_injection=False)


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_non_numeric_page_size() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with a non numeric page_size.
    """
    url = 'https://api.example.com/users?page_size=big'

    with assert_raises(
        expected_exception=IntegrityError,
        match='Criteria page_size <<<big>>> must be an integer.',
    ):
        SimpleUrlToCriteriaConverter.convert(url=url, check_field_injection=False, check_operator_injection=False)


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_boolean_null_and_empty_values() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with boolean, null and empty string values.
    """
    url = 'https://api.example.com/users?active=true&verified=false&middle_name=null&suffix='
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[
            Filter(field='active', operator=Operator.EQUAL, value=True),
            Filter(field='verified', operator=Operator.EQUAL, value=False),
            Filter(field='middle_name', operator=Operator.EQUAL, value=None),
            Filter(field='suffix', operator=Operator.EQUAL, value=''),
        ],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_custom_suffix_mapping() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with custom suffix mapping.
    """
    url = 'https://api.example.com/users?created_at_after=2026-05-18'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        suffix_operator_mapping={'_After ': Operator.GREATER},
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[Filter(field='created_at', operator=Operator.GREATER, value='2026-05-18')],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_custom_suffix_override() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with custom suffix mapping override.
    """
    url = 'https://api.example.com/users?name_eq=Doe'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        suffix_operator_mapping={'eq': Operator.CONTAINS},
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[Filter(field='name', operator=Operator.CONTAINS, value='Doe')],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_unknown_suffix_like_field() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with an unknown suffix-like field.
    """
    url = 'https://api.example.com/users?name_unknown=Doe'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[Filter(field='name_unknown', operator=Operator.EQUAL, value='Doe')],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_keeps_plus_signs_after_url_decoding() -> None:
    """
    Test SimpleUrlToCriteriaConverter class without double-decoding plus signs.
    """
    url = 'https://api.example.com/users?phone=%2B1-555-123-4567&name=John+Doe'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        check_operator_injection=False,
    )

    expected = Criteria(
        filters=[
            Filter(field='phone', operator=Operator.EQUAL, value='+1-555-123-4567'),
            Filter(field='name', operator=Operator.EQUAL, value='John Doe'),
        ],
        orders=None,
        page_size=None,
        page_number=None,
    )

    assert criteria == expected


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_invalid_between_values() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with invalid BETWEEN values.
    """
    url = 'https://api.example.com/products?price_between=10'

    with assert_raises(
        expected_exception=IntegrityError,
        match='SimpleUrlToCriteriaConverter filter <<<price_between>>> has invalid value <<<10>>> '
        'for operator <<<BETWEEN>>>.',
    ):
        SimpleUrlToCriteriaConverter.convert(url=url, check_field_injection=False, check_operator_injection=False)


@mark.unit_testing
def test_simple_url_to_criteria_converter_with_empty_in_values() -> None:
    """
    Test SimpleUrlToCriteriaConverter class with empty IN values.
    """
    url = 'https://api.example.com/users?status_in=,,'

    with assert_raises(
        expected_exception=IntegrityError,
        match='SimpleUrlToCriteriaConverter filter <<<status_in>>> has invalid value <<<,,>>> for operator <<<IN>>>.',
    ):
        SimpleUrlToCriteriaConverter.convert(url=url, check_field_injection=False, check_operator_injection=False)


@mark.unit_testing
def test_simple_url_to_criteria_converter_rejects_too_many_filters() -> None:
    """
    Test simple URL converter rejects too many query-parameter filters.
    """
    query = '&'.join(f'field_{index}=value' for index in range(SimpleUrlToCriteriaConverter.DEFAULT_MAX_FILTERS + 1))
    url = f'https://api.example.com/users?{query}'

    with assert_raises(
        expected_exception=IntegrityError,
        match='SimpleUrlToCriteriaConverter filters exceeds maximum limit',
    ):
        SimpleUrlToCriteriaConverter.convert(
            url=url,
            check_field_injection=False,
            check_operator_injection=False,
        )


@mark.unit_testing
def test_simple_url_to_criteria_converter_rejects_large_in_list() -> None:
    """
    Test simple URL converter rejects IN lists above the configured maximum.
    """
    values = ','.join(str(index) for index in range(SimpleUrlToCriteriaConverter.DEFAULT_MAX_IN_VALUES + 1))
    url = f'https://api.example.com/users?status_in={values}'

    with assert_raises(
        expected_exception=IntegrityError,
        match='exceeds maximum limit',
    ):
        SimpleUrlToCriteriaConverter.convert(
            url=url,
            valid_fields=['status'],
            valid_operators=[Operator.IN],
        )


@mark.unit_testing
def test_simple_url_to_criteria_converter_rejects_large_operator_allowlist() -> None:
    """
    Test simple URL converter rejects explicit operator allowlists above the configured maximum.
    """
    operators = [Operator.EQUAL] * (SimpleUrlToCriteriaConverter.DEFAULT_MAX_OPERATOR_ALLOWLIST + 1)

    with assert_raises(
        expected_exception=IntegrityError,
        match='valid_operators exceeds maximum limit',
    ):
        SimpleUrlToCriteriaConverter.convert(
            url='https://api.example.com/users?name=Doe',
            valid_fields=['name'],
            valid_operators=operators,
        )
