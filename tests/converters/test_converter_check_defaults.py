"""
Test default security check flags on converters.
"""

import inspect
from collections.abc import Callable
from typing import Any

from pytest import mark, param, raises as assert_raises

from criteria_pattern import Criteria, Direction, Filter, Operator
from criteria_pattern.converters import (
    BodyToCriteriaConverter,
    CriteriaToMariadbConverter,
    CriteriaToMysqlConverter,
    CriteriaToPostgresqlConverter,
    CriteriaToSqliteConverter,
    SimpleUrlToCriteriaConverter,
    UrlToCriteriaConverter,
)
from criteria_pattern.errors import (
    InvalidColumnError,
    InvalidDirectionError,
    InvalidOperatorError,
    InvalidTableError,
    PaginationBoundsError,
)
from criteria_pattern.models.testing.mothers import CriteriaMother, FilterMother, OrderMother

_SQL_CONVERTERS: tuple[type, ...] = (
    CriteriaToPostgresqlConverter,
    CriteriaToMysqlConverter,
    CriteriaToMariadbConverter,
    CriteriaToSqliteConverter,
)


def _assert_check_parameter_defaults(*, convert: Callable[..., Any], check_parameters: tuple[str, ...]) -> None:
    signature = inspect.signature(convert)
    for name in check_parameters:
        parameter = signature.parameters[name]
        assert parameter.default is True, f'{convert.__qualname__}.{name} must default to True'


_REQUEST_CHECK_PARAMETERS: tuple[str, ...] = (
    'check_field_injection',
    'check_operator_injection',
    'check_direction_injection',
    'check_pagination_bounds',
)

_SIMPLE_URL_CHECK_PARAMETERS: tuple[str, ...] = (
    'check_field_injection',
    'check_operator_injection',
    'check_pagination_bounds',
)

_SQL_CHECK_PARAMETERS: tuple[str, ...] = (
    'check_criteria_injection',
    'check_table_injection',
    'check_column_injection',
    'check_operator_injection',
    'check_direction_injection',
    'check_pagination_bounds',
)


@mark.unit_testing
@mark.parametrize(
    ('convert', 'check_parameters'),
    [
        param(BodyToCriteriaConverter.convert, _REQUEST_CHECK_PARAMETERS, id='body'),
        param(UrlToCriteriaConverter.convert, _REQUEST_CHECK_PARAMETERS, id='url'),
        param(SimpleUrlToCriteriaConverter.convert, _SIMPLE_URL_CHECK_PARAMETERS, id='simple_url'),
        param(CriteriaToPostgresqlConverter.convert, _SQL_CHECK_PARAMETERS, id='postgresql'),
        param(CriteriaToMysqlConverter.convert, _SQL_CHECK_PARAMETERS, id='mysql'),
        param(CriteriaToMariadbConverter.convert, _SQL_CHECK_PARAMETERS, id='mariadb'),
        param(CriteriaToSqliteConverter.convert, _SQL_CHECK_PARAMETERS, id='sqlite'),
    ],
)
def test_converter_check_flags_default_to_true(
    *,
    convert: Callable[..., Any],
    check_parameters: tuple[str, ...],
) -> None:
    """
    Security-related check flags must default to enabled on converter entry points.
    """
    _assert_check_parameter_defaults(convert=convert, check_parameters=check_parameters)


@mark.unit_testing
def test_body_to_criteria_converter_validates_fields_by_default() -> None:
    """
    Field allowlist validation runs when check_field_injection is omitted.
    """
    body = {'filters': [{'field': 'invalid', 'operator': 'EQUAL', 'value': 'Doe'}]}

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<invalid>>>. Valid columns are <<<name>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body, valid_fields=['name'])


@mark.unit_testing
def test_body_to_criteria_converter_validates_pagination_by_default() -> None:
    """
    Pagination bounds validation runs when check_pagination_bounds is omitted.
    """
    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_size>>> <<<50000>>> exceeds maximum allowed value <<<10000>>>.',
    ):
        BodyToCriteriaConverter.convert(body={'page_size': 50000}, max_page_size=10000)


@mark.unit_testing
def test_body_to_criteria_converter_validates_operators_by_default() -> None:
    """
    Operator allowlist validation runs when check_operator_injection is omitted.
    """
    body = {'filters': [{'field': 'name', 'operator': 'EQUAL', 'value': 'Doe'}]}

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body, valid_operators=[Operator.GREATER])


@mark.unit_testing
def test_body_to_criteria_converter_validates_directions_by_default() -> None:
    """
    Direction allowlist validation runs when check_direction_injection is omitted.
    """
    body = {'orders': [{'field': 'name', 'direction': 'DESC'}]}

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body, valid_directions=[Direction.ASC])


@mark.unit_testing
def test_url_to_criteria_converter_validates_fields_by_default() -> None:
    """
    Field allowlist validation runs when check_field_injection is omitted.
    """
    url = 'https://api.example.com/users?filters[0][field]=id; DROP TABLE user;&filters[0][operator]=EQUAL&filters[0][value]=1'  # noqa: E501  # fmt: skip
    valid_fields = ['id', 'name', 'email']

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name, email>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url, valid_fields=valid_fields)


@mark.unit_testing
def test_url_to_criteria_converter_validates_operators_by_default() -> None:
    """
    Operator allowlist validation runs when check_operator_injection is omitted.
    """
    url = 'https://api.example.com/users?filters[0][field]=age&filters[0][operator]=EQUAL&filters[0][value]=25'

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url, valid_operators=[Operator.GREATER, Operator.LESS])


@mark.unit_testing
def test_url_to_criteria_converter_validates_directions_by_default() -> None:
    """
    Direction allowlist validation runs when check_direction_injection is omitted.
    """
    url = 'https://api.example.com/users?orders[0][field]=name&orders[0][direction]=DESC'

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url, valid_directions=[Direction.ASC])


@mark.unit_testing
def test_url_to_criteria_converter_validates_pagination_by_default() -> None:
    """
    Pagination bounds validation runs when check_pagination_bounds is omitted.
    """
    url = 'https://api.example.com/users?page_size=50000&page_number=1'

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_size>>> <<<50000>>> exceeds maximum allowed value <<<10000>>>.',
    ):
        UrlToCriteriaConverter.convert(url=url, max_page_size=10000)


@mark.unit_testing
def test_simple_url_to_criteria_converter_validates_fields_by_default() -> None:
    """
    Field allowlist validation runs when check_field_injection is omitted.
    """
    url = 'https://api.example.com/users?invalid_field=Doe'

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<invalid_field>>>. Valid columns are <<<id, name, email>>>.',
    ):
        SimpleUrlToCriteriaConverter.convert(url=url, valid_fields=['id', 'name', 'email'])


@mark.unit_testing
def test_simple_url_to_criteria_converter_validates_operators_by_default() -> None:
    """
    Operator allowlist validation runs when check_operator_injection is omitted.
    """
    url = 'https://api.example.com/users?name=Doe'

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER>>>.',
    ):
        SimpleUrlToCriteriaConverter.convert(url=url, valid_operators=[Operator.GREATER])


@mark.unit_testing
def test_simple_url_to_criteria_converter_validates_pagination_by_default() -> None:
    """
    Pagination bounds validation runs when check_pagination_bounds is omitted.
    """
    url = 'https://api.example.com/users?page_size=50000&page_number=1'

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_size>>> <<<50000>>> exceeds maximum allowed value <<<10000>>>.',
    ):
        SimpleUrlToCriteriaConverter.convert(url=url, max_page_size=10000)


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_validates_table_by_default(*, converter: type) -> None:
    """
    Table allowlist validation runs when check_table_injection is omitted.
    """
    with assert_raises(
        expected_exception=InvalidTableError,
        match='Invalid table specified <<<user; DROP TABLE user;>>>. Valid tables are <<<user>>>.',
    ):
        converter.convert(
            criteria=CriteriaMother.create(),
            table='user; DROP TABLE user;',
            valid_tables=['user'],
        )


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_validates_columns_by_default(*, converter: type) -> None:
    """
    Column allowlist validation runs when check_column_injection is omitted.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        converter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            columns=['id; DROP TABLE user;', 'name'],
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_validates_criteria_fields_by_default(*, converter: type) -> None:
    """
    Criteria field allowlist validation runs when check_criteria_injection is omitted.
    """
    filter = FilterMother.create(field='id; DROP TABLE user;')

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        converter.convert(
            criteria=CriteriaMother.with_filters(filters=[filter]),
            table='user',
            columns=['id', 'name'],
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_validates_operators_by_default(*, converter: type) -> None:
    """
    Operator allowlist validation runs when check_operator_injection is omitted.
    """
    filter = FilterMother.create(operator=Operator.EQUAL)

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        converter.convert(
            criteria=CriteriaMother.with_filters(filters=[filter]),
            table='user',
            columns=['id', 'name'],
            valid_operators=[Operator.GREATER, Operator.LESS],
        )


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_validates_directions_by_default(*, converter: type) -> None:
    """
    Direction allowlist validation runs when check_direction_injection is omitted.
    """
    order = OrderMother.create(direction=Direction.DESC)

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        converter.convert(
            criteria=CriteriaMother.with_orders(orders=[order]),
            table='user',
            columns=['id', 'name'],
            valid_directions=[Direction.ASC],
        )


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_validates_pagination_by_default(*, converter: type) -> None:
    """
    Pagination bounds validation runs when check_pagination_bounds is omitted.
    """
    criteria = Criteria(page_size=50000, page_number=1)

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_size>>> <<<50000>>> exceeds maximum allowed value <<<10000>>>.',
    ):
        converter.convert(criteria=criteria, table='user', max_page_size=10000)
