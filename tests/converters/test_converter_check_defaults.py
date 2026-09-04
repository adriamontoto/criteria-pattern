"""
Test default security check flags on converters.
"""

import inspect
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from pytest import mark, param, raises as assert_raises

from criteria_pattern import Criteria, Direction, Filter, Operator, Order
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

SqlConverterClass = (
    type[CriteriaToMysqlConverter] | type[CriteriaToPostgresqlConverter] | type[CriteriaToSqliteConverter]
)


def _sql_allowlist_kwargs(
    *,
    criteria: Criteria,
    table: str,
    columns: Sequence[str] | None = None,
    columns_mapping: Mapping[str, str] | None = None,
    tables: Sequence[str] | None = None,
    operators: Sequence[Operator] | None = None,
    directions: Sequence[Direction] | None = None,
) -> dict[str, Any]:
    selected_columns = list(columns or ['*'])
    mapping = columns_mapping or {}
    allowlisted_columns = {column for column in selected_columns if column != '*'}
    allowlisted_columns.update(mapping.values())
    for filter in criteria.filters:
        allowlisted_columns.add(mapping.get(filter.field, filter.field))
    for order in criteria.orders:
        allowlisted_columns.add(mapping.get(order.field, order.field))
    if not allowlisted_columns and any(column == '*' for column in selected_columns):
        allowlisted_columns.add('*')
    resolved_operators = (
        list(operators)
        if operators is not None
        else sorted(
            {Operator(value=filter.operator) for filter in criteria.filters}, key=lambda operator: operator.value
        )
        or list(Operator)
    )
    resolved_directions = (
        list(directions)
        if directions is not None
        else sorted(
            {Direction(value=order.direction) for order in criteria.orders}, key=lambda direction: direction.value
        )
        or [Direction.ASC, Direction.DESC]
    )
    return {
        'valid_tables': list(tables) if tables is not None else [table],
        'valid_columns': sorted(allowlisted_columns),
        'valid_operators': resolved_operators,
        'valid_directions': resolved_directions,
    }


def _assert_check_parameter_defaults(*, convert: Callable[..., Any], check_parameters: tuple[str, ...]) -> None:
    signature = inspect.signature(convert)
    for name in check_parameters:
        parameter = signature.parameters[name]
        assert parameter.default is True, f'{convert.__qualname__}.{name} must default to True'  # type: ignore[ty:unresolved-attribute]


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
        BodyToCriteriaConverter.convert(body=body, valid_fields=['name'], valid_operators=[Operator.GREATER])


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
        BodyToCriteriaConverter.convert(body=body, valid_fields=['name'], valid_directions=[Direction.ASC])


@mark.unit_testing
def test_body_to_criteria_converter_skips_field_validation_when_disabled() -> None:
    """
    Field allowlist validation is skipped when check_field_injection is False.
    """
    body = {'filters': [{'field': 'invalid', 'operator': 'EQUAL', 'value': 'Doe'}]}

    criteria = BodyToCriteriaConverter.convert(
        body=body,
        check_field_injection=False,
        valid_operators=[Operator.EQUAL],
    )

    assert criteria.filters is not None
    assert criteria.filters[0].field == 'invalid'


@mark.unit_testing
def test_body_to_criteria_converter_skips_operator_validation_when_disabled() -> None:
    """
    Operator allowlist validation is skipped when check_operator_injection is False.
    """
    body = {'filters': [{'field': 'name', 'operator': 'EQUAL', 'value': 'Doe'}]}

    criteria = BodyToCriteriaConverter.convert(
        body=body,
        check_operator_injection=False,
        valid_fields=['name'],
    )

    assert criteria.filters is not None
    assert criteria.filters[0].operator == Operator.EQUAL


@mark.unit_testing
def test_body_to_criteria_converter_skips_direction_validation_when_disabled() -> None:
    """
    Direction allowlist validation is skipped when check_direction_injection is False.
    """
    body = {'orders': [{'field': 'name', 'direction': 'DESC'}]}

    criteria = BodyToCriteriaConverter.convert(
        body=body,
        check_direction_injection=False,
        valid_fields=['name'],
    )

    assert criteria.orders is not None
    assert criteria.orders[0].direction == Direction.DESC


@mark.unit_testing
def test_body_to_criteria_converter_skips_pagination_validation_when_disabled() -> None:
    """
    Pagination bounds validation is skipped when check_pagination_bounds is False.
    """
    criteria = BodyToCriteriaConverter.convert(
        body={'page_size': 50000},
        check_pagination_bounds=False,
        max_page_size=100,
    )

    assert criteria.page_size == 50000


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
        UrlToCriteriaConverter.convert(
            url=url,
            valid_fields=['age'],
            valid_operators=[Operator.GREATER, Operator.LESS],
        )


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
        UrlToCriteriaConverter.convert(url=url, valid_fields=['name'], valid_directions=[Direction.ASC])


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
        SimpleUrlToCriteriaConverter.convert(url=url, valid_fields=['name'], valid_operators=[Operator.GREATER])


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
def test_simple_url_to_criteria_converter_skips_field_validation_when_disabled() -> None:
    """
    Field allowlist validation is skipped when check_field_injection is False.
    """
    url = 'https://api.example.com/users?invalid_field=Doe'

    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_field_injection=False,
        valid_operators=[Operator.EQUAL],
    )

    assert criteria.filters is not None
    assert criteria.filters[0].field == 'invalid_field'


@mark.unit_testing
def test_simple_url_to_criteria_converter_skips_operator_validation_when_disabled() -> None:
    """
    Operator allowlist validation is skipped when check_operator_injection is False.
    """
    url = 'https://api.example.com/users?age=18'

    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_operator_injection=False,
        valid_fields=['age'],
    )

    assert criteria.filters is not None
    assert criteria.filters[0].operator == Operator.EQUAL


@mark.unit_testing
def test_simple_url_to_criteria_converter_skips_pagination_validation_when_disabled() -> None:
    """
    Pagination bounds validation is skipped when check_pagination_bounds is False.
    """
    url = 'https://api.example.com/users?page_size=50000&page_number=1'

    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        check_pagination_bounds=False,
        max_page_size=100,
    )

    assert criteria.page_size == 50000


@mark.unit_testing
def test_simple_url_to_criteria_converter_validate_criteria_accepts_allowlisted_order_field() -> None:
    """
    Criteria validation accepts order fields that are in the allowlist.
    """
    criteria = Criteria(orders=[Order(field='name', direction=Direction.ASC)])

    SimpleUrlToCriteriaConverter._validate_criteria(
        criteria=criteria,
        columns_mapping={},
        valid_columns=['name'],
    )


@mark.unit_testing
def test_simple_url_to_criteria_converter_validate_criteria_rejects_invalid_order_field() -> None:
    """
    Criteria validation rejects order fields that are not in the allowlist.
    """
    criteria = Criteria(orders=[Order(field='invalid', direction=Direction.ASC)])

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<invalid>>>. Valid columns are <<<name>>>.',
    ):
        SimpleUrlToCriteriaConverter._validate_criteria(
            criteria=criteria,
            columns_mapping={},
            valid_columns=['name'],
        )


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_validates_table_by_default(*, converter: SqlConverterClass) -> None:
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
def test_sql_converter_validates_columns_by_default(*, converter: SqlConverterClass) -> None:
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
def test_sql_converter_validates_criteria_fields_by_default(*, converter: SqlConverterClass) -> None:
    """
    Criteria field allowlist validation runs when check_criteria_injection is omitted.
    """
    criteria_filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;')

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        converter.convert(
            criteria=CriteriaMother.with_filters(filters=[criteria_filter]),
            table='user',
            columns=['id', 'name'],
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_validates_operators_by_default(*, converter: SqlConverterClass) -> None:
    """
    Operator allowlist validation runs when check_operator_injection is omitted.
    """
    criteria_filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        criteria = CriteriaMother.with_filters(filters=[criteria_filter])
        allowlists = _sql_allowlist_kwargs(criteria=criteria, table='user', columns=['id', 'name'])
        allowlists['valid_operators'] = [Operator.GREATER, Operator.LESS]
        converter.convert(
            criteria=criteria,
            table='user',
            columns=['id', 'name'],
            **allowlists,
        )


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_validates_directions_by_default(*, converter: SqlConverterClass) -> None:
    """
    Direction allowlist validation runs when check_direction_injection is omitted.
    """
    order = OrderMother.create(direction=Direction.DESC)

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        criteria = CriteriaMother.with_orders(orders=[order])
        allowlists = _sql_allowlist_kwargs(criteria=criteria, table='user', columns=['id', 'name'])
        allowlists['valid_directions'] = [Direction.ASC]
        converter.convert(
            criteria=criteria,
            table='user',
            columns=['id', 'name'],
            **allowlists,
        )


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_validates_pagination_by_default(*, converter: SqlConverterClass) -> None:
    """
    Pagination bounds validation runs when check_pagination_bounds is omitted.
    """
    criteria = Criteria(page_size=50000, page_number=1)

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match='Pagination <<<page_size>>> <<<50000>>> exceeds maximum allowed value <<<10000>>>.',
    ):
        converter.convert(
            criteria=criteria,
            table='user',
            max_page_size=10000,
            **_sql_allowlist_kwargs(criteria=criteria, table='user'),
        )


@mark.unit_testing
def test_body_to_criteria_converter_rejects_fields_when_allowlist_omitted() -> None:
    """
    Omitted field allowlists are treated as empty complete lists, not derived from the request.
    """
    body = {'filters': [{'field': 'password_hash', 'operator': 'EQUAL', 'value': 'x'}]}

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<password_hash>>>. Valid columns are <<<>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body)


@mark.unit_testing
def test_body_to_criteria_converter_rejects_fields_when_allowlist_empty() -> None:
    """
    Empty field allowlists reject every filter and order field.
    """
    body = {'filters': [{'field': 'name', 'operator': 'EQUAL', 'value': 'Doe'}]}

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<name>>>. Valid columns are <<<>>>.',
    ):
        BodyToCriteriaConverter.convert(body=body, valid_fields=[])


@mark.unit_testing
def test_body_to_criteria_converter_allows_empty_body_with_empty_field_allowlist() -> None:
    """
    Empty allowlists do not reject requests that contain no fields to validate.
    """
    criteria = BodyToCriteriaConverter.convert(body={}, valid_fields=[])

    assert criteria.filters == []
    assert criteria.orders == []


@mark.unit_testing
@mark.parametrize(
    'converter',
    [param(converter, id=converter.__name__) for converter in _SQL_CONVERTERS],
)
def test_sql_converter_rejects_criteria_fields_when_column_allowlist_omitted(*, converter: SqlConverterClass) -> None:
    """
    Omitted column allowlists are treated as empty complete lists for criteria field validation.
    """
    criteria = Criteria(filters=[Filter(field='secret', operator=Operator.EQUAL, value='x')])

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<secret>>>. Valid columns are <<<>>>.',
    ):
        converter.convert(criteria=criteria, table='user', valid_tables=['user'])
