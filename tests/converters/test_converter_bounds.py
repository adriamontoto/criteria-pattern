"""
Test converter structural bounds and LIKE wildcard escaping.
"""

from pytest import mark, raises as assert_raises

from criteria_pattern import Criteria, Filter, Operator
from criteria_pattern.converters import (
    BodyToCriteriaConverter,
    CriteriaToMysqlConverter,
    CriteriaToPostgresqlConverter,
    SimpleUrlToCriteriaConverter,
    UrlToCriteriaConverter,
)
from criteria_pattern.errors import IntegrityError, PaginationBoundsError
from criteria_pattern.models.criteria import AndCriteria


@mark.unit_testing
def test_escape_like_pattern_value_escapes_wildcards() -> None:
    """
    Test LIKE pattern values escape SQL wildcard characters.
    """
    assert CriteriaToMysqlConverter._escape_like_pattern_value(value='100%_off') == '100\\%\\_off'


@mark.unit_testing
def test_body_to_criteria_converter_rejects_too_many_filters() -> None:
    """
    Test body converter rejects filter lists above the configured maximum.
    """
    body = {
        'filters': [
            {'field': f'field_{index}', 'operator': 'EQUAL', 'value': index}
            for index in range(BodyToCriteriaConverter.DEFAULT_MAX_FILTERS + 1)
        ],
    }

    with assert_raises(
        expected_exception=IntegrityError,
        match='BodyToCriteriaConverter filters exceeds maximum limit',
    ):
        BodyToCriteriaConverter.convert(body=body, max_filters=BodyToCriteriaConverter.DEFAULT_MAX_FILTERS)


@mark.unit_testing
def test_body_to_criteria_converter_rejects_large_in_list() -> None:
    """
    Test body converter rejects IN lists above the configured maximum.
    """
    body = {
        'filters': [
            {
                'field': 'status',
                'operator': 'IN',
                'value': list(range(BodyToCriteriaConverter.DEFAULT_MAX_IN_VALUES + 1)),
            },
        ],
    }

    with assert_raises(
        expected_exception=IntegrityError,
        match='IN values for filter',
    ):
        BodyToCriteriaConverter.convert(body=body)


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
        SimpleUrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_url_to_criteria_converter_rejects_large_in_list() -> None:
    """
    Test URL converter rejects IN lists above the configured maximum.
    """
    values = ','.join(str(index) for index in range(UrlToCriteriaConverter.DEFAULT_MAX_IN_VALUES + 1))
    url = f'https://api.example.com/users?filters[0][field]=status&filters[0][operator]=IN&filters[0][value]={values}'

    with assert_raises(
        expected_exception=IntegrityError,
        match='exceeds maximum limit',
    ):
        UrlToCriteriaConverter.convert(url=url)


@mark.unit_testing
def test_body_to_criteria_converter_rejects_large_operator_allowlist() -> None:
    """
    Test body converter rejects explicit operator allowlists above the configured maximum.
    """
    operators = [Operator.EQUAL] * (BodyToCriteriaConverter.DEFAULT_MAX_OPERATOR_ALLOWLIST + 1)

    with assert_raises(
        expected_exception=IntegrityError,
        match='valid_operators exceeds maximum limit',
    ):
        BodyToCriteriaConverter.convert(
            body={'filters': [{'field': 'name', 'operator': 'EQUAL', 'value': 'Doe'}]},
            valid_operators=operators,
        )


@mark.unit_testing
def test_postgresql_converter_rejects_deep_criteria_composition() -> None:
    """
    Test SQL converter rejects criteria trees deeper than the configured maximum.
    """
    nested = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')])
    for _ in range(CriteriaToPostgresqlConverter.DEFAULT_MAX_CRITERIA_COMPOSITION_DEPTH + 1):
        other = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')])
        nested = other & nested

    with assert_raises(
        expected_exception=IntegrityError,
        match='criteria composition depth',
    ):
        CriteriaToPostgresqlConverter.convert(
            criteria=nested,
            table='users',
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_mysql_converter_escapes_like_wildcards_in_contains_query() -> None:
    """
    Test MySQL converter escapes wildcard characters for CONTAINS filters.
    """
    criteria = Criteria(filters=[Filter(field='name', operator=Operator.CONTAINS, value='100%')])

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='users',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert CriteriaToMysqlConverter.SQL_LIKE_ESCAPE_CLAUSE in query
    assert parameters == ['100\\%']


@mark.unit_testing
def test_postgresql_converter_uses_lower_default_pagination_bounds() -> None:
    """
    Test PostgreSQL converter applies lower default pagination maxima.
    """
    criteria = Criteria(page_size=CriteriaToPostgresqlConverter.DEFAULT_MAX_PAGE_SIZE + 1, page_number=1)

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match=f'exceeds maximum allowed value <<<{CriteriaToPostgresqlConverter.DEFAULT_MAX_PAGE_SIZE}>>>',
    ):
        CriteriaToPostgresqlConverter.convert(criteria=criteria, table='users', valid_tables=['users'])


@mark.unit_testing
def test_and_criteria_depth_counts_boolean_nodes() -> None:
    """
    Test composed criteria depth is measured on boolean nodes only.
    """
    left = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')])
    right = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
    composed = left & right

    assert isinstance(composed, AndCriteria)
