"""
Test CriteriaToMysqlConverter class.
"""

from collections.abc import Mapping, Sequence
from typing import Any

from object_mother_pattern import IntegerMother
from pytest import mark, raises as assert_raises
from sqlglot import parse_one

from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.converters import CriteriaToMysqlConverter
from criteria_pattern.errors import (
    IntegrityError,
    InvalidColumnError,
    InvalidDirectionError,
    InvalidOperatorError,
    InvalidTableError,
    PaginationBoundsError,
)
from criteria_pattern.models.testing.mothers import CriteriaMother, FilterMother, OrderMother


def assert_valid_mysql_syntax(*, query: str, parameters: list[Any]) -> None:
    """
    Helper function to validate that the generated SQL query is valid MySQL syntax using sqlglot.

    Args:
        query (str): The SQL query to validate.
        parameters (list[Any]): The parameters to use in the query.

    Raises:
        AssertionError: If the query is not valid MySQL syntax.
    """

    def to_literal(parameter: Any) -> str:
        if parameter is None:
            return 'NULL'

        if isinstance(parameter, bool):
            return 'TRUE' if parameter else 'FALSE'

        if isinstance(parameter, (int | float)):
            return str(parameter)

        string = str(parameter).replace("'", "''")
        return f"'{string}'"

    parameterized_query = query
    for _, parameter in enumerate(parameters):
        parameterized_query = parameterized_query.replace('%s', to_literal(parameter=parameter), 1)

    try:
        parsed = parse_one(sql=parameterized_query, dialect='mysql')
        normalized = parsed.sql(dialect='mysql')

        assert normalized is not None

    except Exception as exception:
        raise AssertionError('Invalid MySQL syntax.') from exception


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


@mark.unit_testing
def test_criteria_to_mysql_converter_with_empty_criteria_and_all_columns() -> None:
    """
    Test CriteriaToMysqlConverter class with an empty Criteria object and all columns.
    """
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.empty(),
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user`;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_empty_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with an empty Criteria object.
    """
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.empty(),
        table='user',
        columns=['id', 'name'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name` FROM `user`;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_equal_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with an EQUAL filter.
    """
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `name` = %s;'
    assert parameters == ['John Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_equal_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT EQUAL filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_EQUAL, value='John Doe')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `name` != %s;'
    assert parameters == ['John Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_greater_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a GREATER filter.
    """
    filter = Filter(field='age', operator=Operator.GREATER, value=18)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `age` > %s;'
    assert parameters == [18]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_greater_or_equal_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a GREATER OR EQUAL filter.
    """
    filter = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `age` >= %s;'
    assert parameters == [18]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_less_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a LESS filter.
    """
    filter = Filter(field='age', operator=Operator.LESS, value=18)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `age` < %s;'
    assert parameters == [18]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_less_or_equal_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a LESS OR EQUAL filter.
    """
    filter = Filter(field='age', operator=Operator.LESS_OR_EQUAL, value=18)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `age` <= %s;'
    assert parameters == [18]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_like_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a LIKE filter.
    """
    filter = Filter(field='name', operator=Operator.LIKE, value='John')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert CriteriaToMysqlConverter.SQL_LIKE_ESCAPE_CLAUSE in query
    assert parameters == ['John']


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_like_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT LIKE filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_LIKE, value='John')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert CriteriaToMysqlConverter.SQL_LIKE_ESCAPE_CLAUSE in query
    assert parameters == ['John']


@mark.unit_testing
def test_criteria_to_mysql_converter_with_contains_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a CONTAINS filter.
    """
    filter = Filter(field='name', operator=Operator.CONTAINS, value='John')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert CriteriaToMysqlConverter.SQL_LIKE_ESCAPE_CLAUSE in query
    assert parameters == ['John']


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_contains_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT CONTAINS filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_CONTAINS, value='John')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert CriteriaToMysqlConverter.SQL_LIKE_ESCAPE_CLAUSE in query
    assert parameters == ['John']


@mark.unit_testing
def test_criteria_to_mysql_converter_with_starts_with_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a STARTS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.STARTS_WITH, value='John')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert CriteriaToMysqlConverter.SQL_LIKE_ESCAPE_CLAUSE in query
    assert parameters == ['John']


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_starts_with_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT STARTS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_STARTS_WITH, value='John')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert CriteriaToMysqlConverter.SQL_LIKE_ESCAPE_CLAUSE in query
    assert parameters == ['John']


@mark.unit_testing
def test_criteria_to_mysql_converter_with_ends_with_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a ENDS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.ENDS_WITH, value='Doe')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert CriteriaToMysqlConverter.SQL_LIKE_ESCAPE_CLAUSE in query
    assert parameters == ['Doe']


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_ends_with_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT ENDS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_ENDS_WITH, value='Doe')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert CriteriaToMysqlConverter.SQL_LIKE_ESCAPE_CLAUSE in query
    assert parameters == ['Doe']


@mark.unit_testing
def test_criteria_to_mysql_converter_with_between_filter_list() -> None:
    """
    Test CriteriaToMysqlConverter class with a BETWEEN filter using a list of values.
    """
    filter = Filter(field='age', operator=Operator.BETWEEN, value=[18, 30])
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `age` BETWEEN %s AND %s;'
    assert parameters == [18, 30]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_between_filter_tuple() -> None:
    """
    Test CriteriaToMysqlConverter class with a BETWEEN filter using a tuple of values.
    """
    filter = Filter(field='age', operator=Operator.BETWEEN, value=(18, 30))
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `age` BETWEEN %s AND %s;'
    assert parameters == [18, 30]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_between_filter_list() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT BETWEEN filter.
    """
    filter = Filter(field='age', operator=Operator.NOT_BETWEEN, value=[18, 30])
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `age` NOT BETWEEN %s AND %s;'
    assert parameters == [18, 30]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_between_filter_tuple() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT BETWEEN filter using a tuple of values.
    """
    filter = Filter(field='age', operator=Operator.NOT_BETWEEN, value=(18, 30))
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `age` NOT BETWEEN %s AND %s;'
    assert parameters == [18, 30]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_is_null_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with an IS NULL filter.
    """
    filter = Filter(field='email', operator=Operator.IS_NULL, value=None)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `email` IS NULL;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_is_not_null_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with an IS NOT NULL filter.
    """
    filter = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `email` IS NOT NULL;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_in_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with an IN filter.
    """
    filter = Filter(field='status', operator=Operator.IN, value=['active', 'pending', 'inactive'])
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'status'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `status` FROM `user` WHERE `status` IN (%s, %s, %s);'  # noqa: E501  # fmt: skip
    assert parameters == ['active', 'pending', 'inactive']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_in_filter() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT IN filter.
    """
    filter = Filter(field='status', operator=Operator.NOT_IN, value=['deleted', 'banned'])
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'status'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `status` FROM `user` WHERE `status` NOT IN (%s, %s);'
    assert parameters == ['deleted', 'banned']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_and_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with an AND Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    criteria1 = CriteriaMother.with_filters(filters=[filter1])
    criteria2 = CriteriaMother.with_filters(filters=[filter2])
    query1, parameters1 = CriteriaToMysqlConverter.convert(
        criteria=criteria1 & criteria2,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )
    query2, parameters2 = CriteriaToMysqlConverter.convert(
        criteria=criteria2 & criteria1,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query1 == 'SELECT * FROM `user` WHERE (`name` = %s AND `email` IS NOT NULL);'
    assert parameters1 == ['John Doe']
    assert_valid_mysql_syntax(query=query1, parameters=parameters1)
    assert query2 == 'SELECT * FROM `user` WHERE (`email` IS NOT NULL AND `name` = %s);'
    assert parameters2 == ['John Doe']
    assert_valid_mysql_syntax(query=query2, parameters=parameters2)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_or_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with an OR Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    criteria1 = CriteriaMother.with_filters(filters=[filter1])
    criteria2 = CriteriaMother.with_filters(filters=[filter2])
    query1, parameters1 = CriteriaToMysqlConverter.convert(
        criteria=criteria1 | criteria2,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )
    query2, parameters2 = CriteriaToMysqlConverter.convert(
        criteria=criteria2 | criteria1,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query1 == 'SELECT * FROM `user` WHERE (`name` = %s OR `email` IS NOT NULL);'
    assert parameters1 == ['John Doe']
    assert_valid_mysql_syntax(query=query1, parameters=parameters1)
    assert query2 == 'SELECT * FROM `user` WHERE (`email` IS NOT NULL OR `name` = %s);'
    assert parameters2 == ['John Doe']
    assert_valid_mysql_syntax(query=query2, parameters=parameters2)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT Criteria object.
    """
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria = CriteriaMother.with_filters(filters=[filter])
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=~criteria,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` WHERE NOT (`name` = %s);'
    assert parameters == ['John Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_and_criteria_empty_left() -> None:
    """
    Test CriteriaToMysqlConverter class with an AND Criteria where left side is empty.
    """
    empty_criteria = Criteria()
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria_with_filter = CriteriaMother.with_filters(filters=[filter])

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=empty_criteria & criteria_with_filter,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` WHERE `name` = %s;'
    assert parameters == ['John Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_and_criteria_empty_right() -> None:
    """
    Test CriteriaToMysqlConverter class with an AND Criteria where right side is empty.
    """
    empty_criteria = Criteria()
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria_with_filter = CriteriaMother.with_filters(filters=[filter])

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria_with_filter & empty_criteria,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` WHERE `name` = %s;'
    assert parameters == ['John Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_and_criteria_both_empty() -> None:
    """
    Test CriteriaToMysqlConverter class with an AND Criteria where both sides are empty.
    """
    empty_criteria1 = Criteria()
    empty_criteria2 = Criteria()

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=empty_criteria1 & empty_criteria2,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user`;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_or_criteria_empty_left() -> None:
    """
    Test CriteriaToMysqlConverter class with an OR Criteria where left side is empty.
    """
    empty_criteria = Criteria()
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria_with_filter = CriteriaMother.with_filters(filters=[filter])

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=empty_criteria | criteria_with_filter,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` WHERE `name` = %s;'
    assert parameters == ['John Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_or_criteria_empty_right() -> None:
    """
    Test CriteriaToMysqlConverter class with an OR Criteria where right side is empty.
    """
    empty_criteria = Criteria()
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria_with_filter = CriteriaMother.with_filters(filters=[filter])

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria_with_filter | empty_criteria,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` WHERE `name` = %s;'
    assert parameters == ['John Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_or_criteria_both_empty() -> None:
    """
    Test CriteriaToMysqlConverter class with an OR Criteria where both sides are empty.
    """
    empty_criteria1 = Criteria()
    empty_criteria2 = Criteria()

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=empty_criteria1 | empty_criteria2,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user`;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_empty_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT of empty Criteria.
    """
    empty_criteria = Criteria()

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=~empty_criteria,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user`;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_complex_empty_combination() -> None:
    """
    Test CriteriaToMysqlConverter with complex combinations including empty criteria.
    This replicates the issue from main.py adapted for MySQL.
    """
    criteria = Criteria()
    orders = [Order(field='created_date', direction=Direction.DESC), Order(field='identifier', direction=Direction.ASC)]
    match_by_organization = Criteria(
        filters=[Filter(field='organization_identifier', operator=Operator.EQUAL, value='test')],
        orders=orders,
    )

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=match_by_organization & criteria,
        table='test_table',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == (
        'SELECT * FROM `test_table` WHERE `organization_identifier` = %s '
        'ORDER BY `created_date` DESC, `identifier` ASC;'
    )
    assert parameters == ['test']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_nested_empty_and_criteria() -> None:
    """
    Test CriteriaToMysqlConverter with nested AND where both sides are empty.
    This forces the recursive processor to hit the branch where both conditions are empty.
    """
    empty_criteria1 = Criteria()
    empty_criteria2 = Criteria()
    filter_criteria = Filter(field='name', operator=Operator.EQUAL, value='John')
    main_criteria = CriteriaMother.with_filters(filters=[filter_criteria])

    nested_empty = empty_criteria1 & empty_criteria2
    combined = main_criteria & nested_empty

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=combined,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` WHERE `name` = %s;'
    assert parameters == ['John']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_nested_empty_or_criteria() -> None:
    """
    Test CriteriaToMysqlConverter with nested OR where both sides are empty.
    This forces the recursive processor to hit the branch where both conditions are empty.
    """
    empty_criteria1 = Criteria()
    empty_criteria2 = Criteria()
    filter_criteria = Filter(field='name', operator=Operator.EQUAL, value='John')
    main_criteria = CriteriaMother.with_filters(filters=[filter_criteria])

    nested_empty = empty_criteria1 | empty_criteria2
    combined = main_criteria | nested_empty

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=combined,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` WHERE `name` = %s;'
    assert parameters == ['John']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_nested_empty_not_criteria() -> None:
    """
    Test CriteriaToMysqlConverter with nested NOT of empty criteria.
    This forces the recursive processor to hit the branch where NOT condition is empty.
    """
    empty_criteria = Criteria()
    filter_criteria = Filter(field='name', operator=Operator.EQUAL, value='John')
    main_criteria = CriteriaMother.with_filters(filters=[filter_criteria])

    not_empty = ~empty_criteria
    combined = main_criteria & not_empty

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=combined,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` WHERE `name` = %s;'
    assert parameters == ['John']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_mixed_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with a mixed Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    filter3 = Filter(field='age', operator=Operator.LESS, value=18)
    criteria1 = CriteriaMother.with_filters(filters=[filter1])
    criteria2 = CriteriaMother.with_filters(filters=[filter2])
    criteria3 = CriteriaMother.with_filters(filters=[filter3])
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria1 & (criteria2 | ~criteria3),
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == "SELECT * FROM `user` WHERE (`name` = %s AND (`email` IS NOT NULL OR NOT (`age` < %s)));"  # noqa: E501 # fmt: skip
    assert parameters == ['John Doe', 18]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_asc_order() -> None:
    """
    Test CriteriaToMysqlConverter class with an ASC order.
    """
    order = Order(field='name', direction=Direction.ASC)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_orders(orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` ORDER BY `name` ASC;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_desc_order() -> None:
    """
    Test CriteriaToMysqlConverter class with a DESC order.
    """
    order = Order(field='name', direction=Direction.DESC)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_orders(orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` ORDER BY `name` DESC;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_multiple_orders_on_the_same_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with multiple orders on the same Criteria object.
    """
    order1 = Order(field='name', direction=Direction.ASC)
    order2 = Order(field='email', direction=Direction.DESC)
    criteria = CriteriaMother.with_orders(orders=[order1, order2])
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` ORDER BY `name` ASC, `email` DESC;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_multiple_orders_on_different_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with multiple orders on different Criteria objects.
    """
    order1 = Order(field='name', direction=Direction.ASC)
    order2 = Order(field='age', direction=Direction.ASC)
    order3 = Order(field='email', direction=Direction.DESC)
    criteria1 = CriteriaMother.with_orders(orders=[order1, order2])
    criteria2 = CriteriaMother.with_orders(orders=[order3])
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria1 & criteria2,
        table='user',
        columns=['*'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` ORDER BY `name` ASC, `age` ASC, `email` DESC;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_filtered_and_ordered_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with a filtered and ordered Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    filter3 = Filter(field='age', operator=Operator.LESS, value=18)
    order1 = Order(field='email', direction=Direction.DESC)
    order2 = Order(field='name', direction=Direction.ASC)
    criteria1 = CriteriaMother.create(value=Criteria(filters=[filter1], orders=[order1]))
    criteria2 = CriteriaMother.create(value=Criteria(filters=[filter2], orders=[order2]))
    criteria3 = CriteriaMother.create(value=Criteria(filters=[filter3]))
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria1 & (criteria2 | ~criteria3),
        table='user',
        columns=['id', 'name', 'email'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == "SELECT `id`, `name`, `email` FROM `user` WHERE (`name` = %s AND (`email` IS NOT NULL OR NOT (`age` < %s))) ORDER BY `email` DESC, `name` ASC;"  # noqa: E501 # fmt: skip
    assert parameters == ['John Doe', 18]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_columns_mapping() -> None:
    """
    Test CriteriaToMysqlConverter class with columns mapping.
    """
    filter = Filter(field='full_name', operator=Operator.EQUAL, value='John Doe')
    order = Order(field='full_name', direction=Direction.ASC)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=Criteria(filters=[filter], orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
        columns_mapping={'full_name': 'name'},
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `name` = %s ORDER BY `name` ASC;'
    assert parameters == ['John Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_columns_mapping_with_spaces() -> None:
    """
    Test CriteriaToMysqlConverter class with columns mapping with spaces.
    """
    filter = Filter(field='full name', operator=Operator.EQUAL, value='John Doe')
    order = Order(field='full name', direction=Direction.ASC)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=Criteria(filters=[filter], orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
        columns_mapping={'full name': 'name'},
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name`, `email` FROM `user` WHERE `name` = %s ORDER BY `name` ASC;'
    assert parameters == ['John Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_table_injection_check_disabled() -> None:
    """
    Test CriteriaToMysqlConverter class with table injection when check_table_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;', operator=Operator.EQUAL)

    CriteriaToMysqlConverter.convert(
        check_table_injection=False,
        criteria=CriteriaMother.create(filters=[filter]),
        table='user; DROP TABLE user;',
        valid_tables=['user'],
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_table_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with table injection.
    """
    with assert_raises(
        expected_exception=InvalidTableError,
        match='Invalid table specified <<<user; DROP TABLE user;>>>. Valid tables are <<<user>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user; DROP TABLE user;',
            check_table_injection=True,
            valid_tables=['user'],
            check_column_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_without_table_injection() -> None:
    """
    Test CriteriaToMysqlConverter class without table injection.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user',
        check_table_injection=True,
        valid_tables=['user'],
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_column_injection_check_disabled() -> None:
    """
    Test CriteriaToMysqlConverter class with columns injection when check_columns_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    CriteriaToMysqlConverter.convert(
        check_column_injection=False,
        criteria=CriteriaMother.create(filters=[filter]),
        table='user',
        columns=['id; DROP TABLE user;', 'name'],
        check_table_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_column_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with columns injection.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            columns=['id; DROP TABLE user;', 'name'],
            check_column_injection=True,
            valid_columns=['id', 'name'],
            check_table_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_column_injection_with_star_invalid() -> None:
    """
    Test CriteriaToMysqlConverter class with columns injection for a non-allowlisted column.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match=r'Invalid column specified <<<evil>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.empty(),
            table='user',
            columns=['evil'],
            check_column_injection=True,
            valid_columns=['id', 'name'],
            check_table_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_column_injection_with_star_valid() -> None:
    """
    Test CriteriaToMysqlConverter class with columns injection where columns attribute is a star and is valid.
    """
    filter: Filter[Any] = FilterMother.create(field='*', operator=Operator.EQUAL)

    CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        check_column_injection=True,
        valid_columns=['*', 'id', 'name'],
        check_table_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_column_injection_with_star_and_columns() -> None:
    """
    Test CriteriaToMysqlConverter class with columns injection with star and columns.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match=r'Invalid column specified <<<evil>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.empty(),
            table='user',
            columns=['*', 'id', 'name', 'evil'],
            check_column_injection=True,
            valid_columns=['id', 'name'],
            check_table_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_column_mapping_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with columns injection.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            columns=['id', 'name'],
            columns_mapping={'fullname': 'name', 'id': 'id; DROP TABLE user;'},
            check_column_injection=True,
            valid_columns=['id', 'name'],
            check_table_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_filter_field_injection_check_disabled() -> None:
    """
    Test CriteriaToMysqlConverter class with filter field injection when check_criteria_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;', operator=Operator.EQUAL)

    CriteriaToMysqlConverter.convert(
        check_criteria_injection=False,
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        valid_columns=['id', 'name'],
        check_table_injection=False,
        check_column_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_filter_field_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with filter field injection.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;')

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.with_filters(filters=[filter]),
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
            check_table_injection=False,
            check_column_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_filter_value_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with filter value injection.
    """
    filter = Filter(field='id', operator=Operator.EQUAL, value='1; DROP TABLE user;')
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        check_criteria_injection=True,
        valid_columns=['id', 'name'],
        check_table_injection=False,
        check_column_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name` FROM `user` WHERE `id` = %s;'
    assert parameters == ['1; DROP TABLE user;']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_order_field_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with order field injection.
    """
    order = OrderMother.create(field='id; DROP TABLE user;')

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.with_orders(orders=[order]),
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
            check_table_injection=False,
            check_column_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_two_order_fields_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with order field injection.
    """
    order1 = OrderMother.create(field='name')
    order2 = OrderMother.create(field='id; DROP TABLE user;')
    criteria1 = CriteriaMother.with_orders(orders=[order1])
    criteria2 = CriteriaMother.with_orders(orders=[order2])

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=criteria1 & criteria2,
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
            check_table_injection=False,
            check_column_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_operator_injection_check_disabled() -> None:
    """
    Test CriteriaToMysqlConverter class with operator injection when check_operator_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create()

    CriteriaToMysqlConverter.convert(
        check_operator_injection=False,
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        valid_operators=[Operator.GREATER, Operator.LESS],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_operator_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with operator injection.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.with_filters(filters=[filter]),
            table='user',
            columns=['id', 'name'],
            check_operator_injection=True,
            valid_operators=[Operator.GREATER, Operator.LESS],
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_valid_operator() -> None:
    """
    Test CriteriaToMysqlConverter class with valid operator.
    """
    filter: Filter[Any] = FilterMother.create(field='id', operator=Operator.GREATER, value=1)

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        check_operator_injection=True,
        valid_operators=[Operator.GREATER, Operator.LESS],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name` FROM `user` WHERE `id` > %s;'
    assert parameters == [1]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_multiple_filters_operator_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with multiple filters where one has invalid operator.
    """
    filter1: Filter[Any] = FilterMother.create(operator=Operator.GREATER)
    filter2: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.with_filters(filters=[filter1, filter2]),
            table='user',
            columns=['id', 'name'],
            check_operator_injection=True,
            valid_operators=[Operator.GREATER, Operator.LESS],
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_complex_criteria_operator_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with complex criteria containing invalid operator.
    """
    criteria1 = CriteriaMother.create(filters=[FilterMother.create(operator=Operator.GREATER)])
    criteria2 = CriteriaMother.create(filters=[FilterMother.create(operator=Operator.LESS)])
    criteria3 = CriteriaMother.create(filters=[FilterMother.create(operator=Operator.LIKE)])

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<LIKE>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=criteria1 & (criteria2 | criteria3),
            table='user',
            columns=['id', 'name', 'age'],
            check_operator_injection=True,
            valid_operators=[Operator.GREATER, Operator.LESS],
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_direction_injection_check_disabled() -> None:
    """
    Test CriteriaToMysqlConverter class with direction injection when check_direction_injection is disabled.
    """
    order: Order = OrderMother.create()

    CriteriaToMysqlConverter.convert(
        check_direction_injection=False,
        criteria=CriteriaMother.with_orders(orders=[order]),
        table='user',
        columns=['id', 'name'],
        valid_directions=[Direction.ASC],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_pagination_bounds=False,
    )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_direction_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with direction injection.
    """
    order: Order = OrderMother.create(direction=Direction.DESC)

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.with_orders(orders=[order]),
            table='user',
            columns=['id', 'name'],
            check_direction_injection=True,
            valid_directions=[Direction.ASC],
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_valid_direction() -> None:
    """
    Test CriteriaToMysqlConverter class with valid direction.
    """
    order: Order = OrderMother.create(field='id', direction=Direction.ASC)

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_orders(orders=[order]),
        table='user',
        columns=['id', 'name'],
        check_direction_injection=True,
        valid_directions=[Direction.ASC, Direction.DESC],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`, `name` FROM `user` ORDER BY `id` ASC;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_multiple_orders_direction_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with multiple orders where one has invalid direction.
    """
    order1: Order = OrderMother.create(direction=Direction.ASC)
    order2: Order = OrderMother.create(direction=Direction.DESC)

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.with_orders(orders=[order1, order2]),
            table='user',
            columns=['id', 'name'],
            check_direction_injection=True,
            valid_directions=[Direction.ASC],
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_complex_criteria_direction_injection() -> None:
    """
    Test CriteriaToMysqlConverter class with complex criteria containing invalid direction.
    """
    criteria1 = CriteriaMother.create(orders=[OrderMother.create(direction=Direction.ASC)])
    criteria2 = CriteriaMother.create(orders=[OrderMother.create(direction=Direction.DESC)])

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=criteria1 & criteria2,
            table='user',
            columns=['id', 'name', 'age'],
            check_direction_injection=True,
            valid_directions=[Direction.ASC],
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_pagination() -> None:
    """
    Test CriteriaToMysqlConverter class with pagination.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    criteria = Criteria(page_size=page_size, page_number=page_number)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_offset = (page_number - 1) * page_size
    expected_query = 'SELECT * FROM `user` LIMIT %s OFFSET %s;'
    expected_parameters = [page_size, expected_offset]

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_without_pagination() -> None:
    """
    Test CriteriaToMysqlConverter class without pagination.
    """
    criteria = Criteria()
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user`;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_filters_and_pagination() -> None:
    """
    Test CriteriaToMysqlConverter class with filters and pagination.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    filter = Filter(field='name', operator=Operator.EQUAL, value='John')
    criteria = Criteria(filters=[filter], page_size=page_size, page_number=page_number)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_offset = (page_number - 1) * page_size
    expected_query = 'SELECT * FROM `user` WHERE `name` = %s LIMIT %s OFFSET %s;'
    expected_parameters = ['John', page_size, expected_offset]

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_orders_and_pagination() -> None:
    """
    Test CriteriaToMysqlConverter class with orders and pagination.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    order = Order(field='name', direction=Direction.ASC)
    criteria = Criteria(orders=[order], page_size=page_size, page_number=page_number)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_offset = (page_number - 1) * page_size
    expected_query = 'SELECT * FROM `user` ORDER BY `name` ASC LIMIT %s OFFSET %s;'
    expected_parameters = [page_size, expected_offset]

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_filters_orders_and_pagination() -> None:
    """
    Test CriteriaToMysqlConverter class with filters, orders, and pagination.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    filter = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    order = Order(field='name', direction=Direction.DESC)
    criteria = Criteria(filters=[filter], orders=[order], page_size=page_size, page_number=page_number)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        columns=['id', 'name', 'age'],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_offset = (page_number - 1) * page_size
    expected_query = 'SELECT `id`, `name`, `age` FROM `user` WHERE `age` >= %s ORDER BY `name` DESC LIMIT %s OFFSET %s;'

    expected_parameters = [18, page_size, expected_offset]
    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_pagination_first_page() -> None:
    """
    Test CriteriaToMysqlConverter class with pagination for first page.
    """
    criteria = Criteria(page_size=10, page_number=1)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` LIMIT %s OFFSET %s;'
    assert parameters == [10, 0]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_pagination_second_page() -> None:
    """
    Test CriteriaToMysqlConverter class with pagination for second page.
    """
    criteria = Criteria(page_size=10, page_number=2)
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT * FROM `user` LIMIT %s OFFSET %s;'
    assert parameters == [10, 10]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_pagination_with_combined_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with pagination using combined criteria.
    """
    filter1 = Filter(field='active', operator=Operator.EQUAL, value=True)
    filter2 = Filter(field='age', operator=Operator.GREATER, value=18)

    criteria1 = Criteria(filters=[filter1], page_size=20, page_number=3)
    criteria2 = Criteria(filters=[filter2])

    combined_criteria = criteria1 & criteria2
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=combined_criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_offset = (3 - 1) * 20
    expected_query = 'SELECT * FROM `user` WHERE (`active` = %s AND `age` > %s) LIMIT %s OFFSET %s;'
    expected_parameters = [True, 18, 20, expected_offset]

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_page_size_only() -> None:
    """
    Test CriteriaToMysqlConverter generates LIMIT without OFFSET when only page_size is provided.
    """
    page_size = IntegerMother.positive()
    criteria = Criteria(page_size=page_size)

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_query = 'SELECT * FROM `user` LIMIT %s;'

    assert query == expected_query
    assert parameters == [page_size]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_filters_and_page_size_only() -> None:
    """
    Test CriteriaToMysqlConverter with filters and LIMIT without OFFSET.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)
    page_size = IntegerMother.positive()

    criteria = Criteria(filters=[filter], page_size=page_size)

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_query = f'SELECT * FROM `user` WHERE `{filter.field}` = %s LIMIT %s;'  # noqa: S608

    assert query == expected_query
    assert parameters == [filter.value, page_size]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_orders_and_page_size_only() -> None:
    """
    Test CriteriaToMysqlConverter with orders and LIMIT without OFFSET.
    """
    order = OrderMother.create(direction=Direction.ASC)
    page_size = IntegerMother.positive()

    criteria = Criteria(orders=[order], page_size=page_size)

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_query = f'SELECT * FROM `user` ORDER BY `{order.field}` ASC LIMIT %s;'  # noqa: S608

    assert query == expected_query
    assert parameters == [page_size]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_multiple_filters_in_same_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with multiple filters in the same Criteria object.
    This should produce AND conditions between filters.
    """
    filter1 = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    filter2 = Filter(field='email', operator=Operator.ENDS_WITH, value='@gmail.com')

    criteria = Criteria(filters=[filter1, filter2])
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_parameters = [18, '@gmail.com']

    assert CriteriaToMysqlConverter.SQL_LIKE_ESCAPE_CLAUSE in query
    assert parameters == expected_parameters


@mark.unit_testing
def test_criteria_to_mysql_converter_and_criteria_pagination_left_has_right_none() -> None:
    """
    Test CriteriaToMysqlConverter with AndCriteria where left has pagination, right has none.
    Should use left pagination.
    """
    left_criteria = Criteria(
        filters=[Filter(field='age', operator=Operator.GREATER, value=18)],
        page_size=10,
        page_number=2,
    )
    right_criteria = Criteria(filters=[Filter(field='status', operator=Operator.EQUAL, value='active')])

    and_criteria = left_criteria & right_criteria
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=and_criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_query = 'SELECT * FROM `user` WHERE (`age` > %s AND `status` = %s) LIMIT %s OFFSET %s;'  # noqa: E501  # fmt: skip
    expected_parameters = [18, 'active', 10, 10]

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_and_criteria_pagination_left_none_right_has() -> None:
    """
    Test CriteriaToMysqlConverter with AndCriteria where left has no pagination, right has pagination.
    Should fallback to right pagination (NEW BEHAVIOR).
    """
    left_criteria = Criteria(filters=[Filter(field='age', operator=Operator.GREATER, value=18)])
    right_criteria = Criteria(
        filters=[Filter(field='status', operator=Operator.EQUAL, value='active')],
        page_size=15,
        page_number=3,
    )

    and_criteria = left_criteria & right_criteria
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=and_criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_query = 'SELECT * FROM `user` WHERE (`age` > %s AND `status` = %s) LIMIT %s OFFSET %s;'  # noqa: E501  # fmt: skip
    expected_parameters = [18, 'active', 15, 30]

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_and_criteria_pagination_both_have() -> None:
    """
    Test CriteriaToMysqlConverter with AndCriteria where both have pagination.
    Should use left pagination (existing behavior).
    """
    left_criteria = Criteria(
        filters=[Filter(field='age', operator=Operator.GREATER, value=18)],
        page_size=10,
        page_number=2,
    )
    right_criteria = Criteria(
        filters=[Filter(field='status', operator=Operator.EQUAL, value='active')],
        page_size=20,
        page_number=5,
    )

    and_criteria = left_criteria & right_criteria
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=and_criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_query = 'SELECT * FROM `user` WHERE (`age` > %s AND `status` = %s) LIMIT %s OFFSET %s;'  # noqa: E501  # fmt: skip
    expected_parameters = [18, 'active', 10, 10]

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_and_criteria_pagination_both_none() -> None:
    """
    Test CriteriaToMysqlConverter with AndCriteria where neither has pagination.
    Should have no pagination (existing behavior).
    """
    left_criteria = Criteria(filters=[Filter(field='age', operator=Operator.GREATER, value=18)])
    right_criteria = Criteria(filters=[Filter(field='status', operator=Operator.EQUAL, value='active')])

    and_criteria = left_criteria & right_criteria
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=and_criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_query = 'SELECT * FROM `user` WHERE (`age` > %s AND `status` = %s);'
    expected_parameters = [18, 'active']

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_or_criteria_pagination_left_has_right_none() -> None:
    """
    Test CriteriaToMysqlConverter with OrCriteria where left has pagination, right has none.
    Should use left pagination.
    """
    left_criteria = Criteria(
        filters=[Filter(field='age', operator=Operator.GREATER, value=18)],
        page_size=10,
        page_number=2,
    )
    right_criteria = Criteria(filters=[Filter(field='status', operator=Operator.EQUAL, value='active')])

    or_criteria = left_criteria | right_criteria
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=or_criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_query = 'SELECT * FROM `user` WHERE (`age` > %s OR `status` = %s) LIMIT %s OFFSET %s;'
    expected_parameters = [18, 'active', 10, 10]

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_or_criteria_pagination_left_none_right_has() -> None:
    """
    Test CriteriaToMysqlConverter with OrCriteria where left has no pagination, right has pagination.
    Should fallback to right pagination (NEW BEHAVIOR).
    """
    left_criteria = Criteria(filters=[Filter(field='age', operator=Operator.GREATER, value=18)])
    right_criteria = Criteria(
        filters=[Filter(field='status', operator=Operator.EQUAL, value='active')],
        page_size=15,
        page_number=3,
    )

    or_criteria = left_criteria | right_criteria
    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=or_criteria,
        table='user',
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    expected_query = 'SELECT * FROM `user` WHERE (`age` > %s OR `status` = %s) LIMIT %s OFFSET %s;'
    expected_parameters = [18, 'active', 15, 30]

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_pagination_bounds_check_disabled() -> None:
    """
    Test CriteriaToMysqlConverter with pagination bounds check disabled (should not raise).
    """
    page_size = IntegerMother.positive(max=50000)
    page_number = IntegerMother.positive(max=50000)
    criteria = Criteria(page_size=page_size, page_number=page_number)

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_pagination_bounds=False,
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
    )

    expected_offset = (page_number - 1) * page_size
    expected_query = 'SELECT * FROM `user` LIMIT %s OFFSET %s;'

    assert query == expected_query
    assert parameters == [page_size, expected_offset]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_page_size_bounds_exceeded() -> None:
    """
    Test CriteriaToMysqlConverter raises PaginationBoundsError when page_size exceeds limit.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()
    criteria = Criteria(page_size=page_size, page_number=page_number)

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match=f'Pagination <<<page_size>>> <<<{page_size}>>> exceeds maximum allowed value <<<0>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=criteria,
            table='user',
            check_pagination_bounds=True,
            max_page_size=0,
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_page_number_bounds_exceeded() -> None:
    """
    Test CriteriaToMysqlConverter raises PaginationBoundsError when page_number exceeds limit.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()
    criteria = Criteria(page_size=page_size, page_number=page_number)

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match=f'Pagination <<<page_number>>> <<<{page_number}>>> exceeds maximum allowed value <<<0>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=criteria,
            table='user',
            check_pagination_bounds=True,
            max_page_number=0,
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_valid_pagination_bounds() -> None:
    """
    Test CriteriaToMysqlConverter with valid pagination parameters within bounds.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()
    criteria = Criteria(page_size=page_size, page_number=page_number)

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_pagination_bounds=True,
        max_page_size=10000,
        max_page_number=10000,
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
    )

    expected_offset = (page_number - 1) * page_size
    expected_query = 'SELECT * FROM `user` LIMIT %s OFFSET %s;'

    assert query == expected_query
    assert parameters == [page_size, expected_offset]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_none_pagination_bounds_check() -> None:
    """
    Test CriteriaToMysqlConverter with no pagination and bounds checking enabled.
    """
    criteria = CriteriaMother.without_pagination()

    CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table='user',
        check_pagination_bounds=True,
        max_page_size=IntegerMother.positive(),
        max_page_number=IntegerMother.positive(),
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
    )


@mark.unit_testing
def test_criteria_to_mysql_converter_escape_like_pattern_value_escapes_wildcards() -> None:
    """
    Test MySQL converter escapes SQL wildcard characters in LIKE pattern values.
    """
    assert CriteriaToMysqlConverter._escape_like_pattern_value(value='100%_off') == '100\\%\\_off'


@mark.unit_testing
def test_criteria_to_mysql_converter_escapes_like_wildcards_in_contains_query() -> None:
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
def test_criteria_to_mysql_converter_quote_backtick_identifier_escapes_embedded_backticks() -> None:
    """
    Test MySQL converter escapes embedded backticks in identifiers.
    """
    assert CriteriaToMysqlConverter._quote_backtick_identifier(identifier='id` OR 1=1 --') == '`id`` OR 1=1 --`'


@mark.unit_testing
def test_criteria_to_mysql_converter_convert_escapes_embedded_backticks_in_generated_sql() -> None:
    """
    Test MySQL converter escapes backticks in identifiers used in generated SQL.
    """
    malicious = 'id` OR 1=1 --'
    criteria = Criteria(filters=[Filter(field=malicious, operator=Operator.EQUAL, value=1)])

    query, parameters = CriteriaToMysqlConverter.convert(
        criteria=criteria,
        table=malicious,
        columns=[malicious],
        check_table_injection=False,
        check_column_injection=False,
        check_criteria_injection=False,
        check_operator_injection=False,
        check_direction_injection=False,
        check_pagination_bounds=False,
    )

    assert query == 'SELECT `id`` OR 1=1 --` FROM `id`` OR 1=1 --` WHERE `id`` OR 1=1 --` = %s;'
    assert parameters == [1]


@mark.unit_testing
def test_criteria_to_mysql_converter_rejects_deep_criteria_composition() -> None:
    """
    Test MySQL converter rejects criteria trees deeper than the configured maximum.
    """
    nested = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')])
    for _ in range(CriteriaToMysqlConverter.DEFAULT_MAX_CRITERIA_COMPOSITION_DEPTH + 1):
        other = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')])
        nested = other & nested

    with assert_raises(
        expected_exception=IntegrityError,
        match='criteria composition depth',
    ):
        CriteriaToMysqlConverter.convert(
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
def test_criteria_to_mysql_converter_rejects_default_max_page_size() -> None:
    """
    Test MySQL converter applies default pagination maxima when bounds checking is enabled.
    """
    criteria = Criteria(page_size=CriteriaToMysqlConverter.DEFAULT_MAX_PAGE_SIZE + 1, page_number=1)

    with assert_raises(
        expected_exception=PaginationBoundsError,
        match=f'exceeds maximum allowed value <<<{CriteriaToMysqlConverter.DEFAULT_MAX_PAGE_SIZE}>>>',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=criteria,
            table='users',
            **_sql_allowlist_kwargs(criteria=criteria, table='users'),
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_validate_criteria_rejects_unmapped_sql_column() -> None:
    """
    Test MySQL converter rejects mapped SQL columns that are not allowlisted.
    """
    criteria = Criteria(filters=[Filter(field='public_name', operator=Operator.EQUAL, value='Doe')])

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<secret_column>>>. Valid columns are <<<public_name>>>.',
    ):
        CriteriaToMysqlConverter._validate_criteria(
            criteria=criteria,
            columns_mapping={'public_name': 'secret_column'},
            valid_columns=['public_name'],
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_and_criteria_depth_counts_boolean_nodes() -> None:
    """
    Test MySQL converter measures composed criteria depth on boolean nodes only.
    """
    left = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')])
    right = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
    composed = left & right

    assert CriteriaToMysqlConverter._criteria_composition_depth(criteria=composed) == 1


@mark.unit_testing
def test_criteria_to_mysql_converter_rejects_large_operator_allowlist() -> None:
    """
    Test MySQL converter rejects explicit operator allowlists above the configured maximum.
    """
    operators = [Operator.EQUAL] * (CriteriaToMysqlConverter.DEFAULT_MAX_OPERATOR_ALLOWLIST + 1)
    criteria = Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')])

    with assert_raises(
        expected_exception=IntegrityError,
        match='valid_operators exceeds maximum limit',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=criteria,
            table='users',
            valid_operators=operators,
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_rejects_large_not_in_list_in_composed_criteria() -> None:
    """
    Test MySQL converter rejects NOT IN lists above the limit inside composed criteria.
    """
    large_values = list(range(CriteriaToMysqlConverter.DEFAULT_MAX_IN_VALUES + 1))
    inner = Criteria(filters=[Filter(field='status', operator=Operator.NOT_IN, value=large_values)])
    criteria = inner & Criteria(filters=[Filter(field='name', operator=Operator.EQUAL, value='Doe')])

    with assert_raises(
        expected_exception=IntegrityError,
        match='IN values for field <<<status>>>',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=criteria,
            table='users',
            max_in_values=CriteriaToMysqlConverter.DEFAULT_MAX_IN_VALUES,
            check_table_injection=False,
            check_column_injection=False,
            check_criteria_injection=False,
            check_operator_injection=False,
            check_direction_injection=False,
            check_pagination_bounds=False,
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_ignores_non_list_in_values_during_bounds_check() -> None:
    """
    Test MySQL converter skips IN bounds checks when the filter value is not a list or tuple.
    """
    criteria = Criteria(filters=[Filter(field='status', operator=Operator.IN, value='active')])

    CriteriaToMysqlConverter._ensure_criteria_in_list_sizes(
        criteria=criteria,
        limit=CriteriaToMysqlConverter.DEFAULT_MAX_IN_VALUES,
    )
