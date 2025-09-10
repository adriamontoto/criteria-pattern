"""
Test CriteriaToMysqlConverter class.
"""

from typing import Any

from object_mother_pattern import IntegerMother
from pytest import mark, raises as assert_raises
from sqlglot import parse_one

from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.converter import CriteriaToMysqlConverter
from criteria_pattern.errors import InvalidColumnError, InvalidTableError
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


@mark.unit_testing
def test_criteria_to_mysql_converter_with_empty_criteria_and_all_columns() -> None:
    """
    Test CriteriaToMysqlConverter class with an empty Criteria object and all columns.
    """
    query, parameters = CriteriaToMysqlConverter.convert(criteria=CriteriaMother.empty(), table='user')

    assert query == 'SELECT * FROM user;'
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
    )

    assert query == 'SELECT id, name FROM user;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE name = %s;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE name != %s;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE age > %s;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE age >= %s;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE age < %s;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE age <= %s;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE name LIKE %s;'
    assert parameters == ['John']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


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
    )

    assert query == 'SELECT id, name, email FROM user WHERE name NOT LIKE %s;'
    assert parameters == ['John']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


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
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE CONCAT('%', %s, '%');"
    assert parameters == ['John']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


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
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE CONCAT('%', %s, '%');"
    assert parameters == ['John']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


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
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE CONCAT(%s, '%');"
    assert parameters == ['John']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


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
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE CONCAT(%s, '%');"
    assert parameters == ['John']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


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
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE CONCAT('%', %s);"
    assert parameters == ['Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


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
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE CONCAT('%', %s);"
    assert parameters == ['Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


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
    )

    assert query == 'SELECT id, name, email FROM user WHERE age BETWEEN %s AND %s;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE age BETWEEN %s AND %s;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE age NOT BETWEEN %s AND %s;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE age NOT BETWEEN %s AND %s;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE email IS NULL;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE email IS NOT NULL;'
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
    )

    assert query == 'SELECT id, name, status FROM user WHERE status IN (%s, %s, %s);'  # noqa: E501  # fmt: skip
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
    )

    assert query == 'SELECT id, name, status FROM user WHERE status NOT IN (%s, %s);'
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
    )
    query2, parameters2 = CriteriaToMysqlConverter.convert(
        criteria=criteria2 & criteria1,
        table='user',
        columns=['*'],
    )

    assert query1 == 'SELECT * FROM user WHERE (name = %s AND email IS NOT NULL);'
    assert parameters1 == ['John Doe']
    assert_valid_mysql_syntax(query=query1, parameters=parameters1)
    assert query2 == 'SELECT * FROM user WHERE (email IS NOT NULL AND name = %s);'
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
    query1, parameters1 = CriteriaToMysqlConverter.convert(criteria=criteria1 | criteria2, table='user', columns=['*'])
    query2, parameters2 = CriteriaToMysqlConverter.convert(criteria=criteria2 | criteria1, table='user', columns=['*'])

    assert query1 == 'SELECT * FROM user WHERE (name = %s OR email IS NOT NULL);'
    assert parameters1 == ['John Doe']
    assert_valid_mysql_syntax(query=query1, parameters=parameters1)
    assert query2 == 'SELECT * FROM user WHERE (email IS NOT NULL OR name = %s);'
    assert parameters2 == ['John Doe']
    assert_valid_mysql_syntax(query=query2, parameters=parameters2)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_not_criteria() -> None:
    """
    Test CriteriaToMysqlConverter class with a NOT Criteria object.
    """
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria = CriteriaMother.with_filters(filters=[filter])
    query, parameters = CriteriaToMysqlConverter.convert(criteria=~criteria, table='user', columns=['*'])

    assert query == 'SELECT * FROM user WHERE NOT (name = %s);'
    assert parameters == ['John Doe']
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
    )

    assert query == "SELECT * FROM user WHERE (name = %s AND (email IS NOT NULL OR NOT (age < %s)));"  # noqa: E501 # fmt: skip
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
    )

    assert query == 'SELECT id, name, email FROM user ORDER BY name ASC;'
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
    )

    assert query == 'SELECT id, name, email FROM user ORDER BY name DESC;'
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
    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria, table='user', columns=['*'])

    assert query == 'SELECT * FROM user ORDER BY name ASC, email DESC;'
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
    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria1 & criteria2, table='user', columns=['*'])

    assert query == 'SELECT * FROM user ORDER BY name ASC, age ASC, email DESC;'
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
    )

    assert query == "SELECT id, name, email FROM user WHERE (name = %s AND (email IS NOT NULL OR NOT (age < %s))) ORDER BY email DESC, name ASC;"  # noqa: E501 # fmt: skip
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE name = %s ORDER BY name ASC;'
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
    )

    assert query == 'SELECT id, name, email FROM user WHERE name = %s ORDER BY name ASC;'
    assert parameters == ['John Doe']
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_table_injection_check_disabled() -> None:
    """
    Test CriteriaToMysqlConverter class with table injection when check_table_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;', operator=Operator.EQUAL)

    CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user; DROP TABLE user;',
        valid_tables=['user'],
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
    )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_column_injection_check_disabled() -> None:
    """
    Test CriteriaToMysqlConverter class with columns injection when check_columns_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user',
        columns=['id; DROP TABLE user;', 'name'],
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
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_column_injection_with_star_invalid() -> None:
    """
    Test CriteriaToMysqlConverter class with columns injection where columns attribute is a star and is invalid.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match=r'Invalid column specified <<<\*>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            check_column_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_column_injection_with_star_valid() -> None:
    """
    Test CriteriaToMysqlConverter class with columns injection where columns attribute is a star and is valid.
    """
    filter: Filter[Any] = FilterMother.create(field='*', operator=Operator.EQUAL)

    CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user',
        check_column_injection=True,
        valid_columns=['*', 'id', 'name'],
    )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_column_injection_with_star_and_columns() -> None:
    """
    Test CriteriaToMysqlConverter class with columns injection with star and columns.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match=r'Invalid column specified <<<\*>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToMysqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            columns=['*', 'id', 'name'],
            check_column_injection=True,
            valid_columns=['id', 'name'],
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
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_filter_field_injection_check_disabled() -> None:
    """
    Test CriteriaToMysqlConverter class with filter field injection when check_criteria_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;', operator=Operator.EQUAL)

    CriteriaToMysqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        valid_columns=['id', 'name'],
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
    )

    assert query == 'SELECT id, name FROM user WHERE id = %s;'
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
        )


@mark.unit_testing
def test_criteria_to_mysql_converter_with_pagination() -> None:
    """
    Test CriteriaToMysqlConverter class with pagination.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    criteria = Criteria(page_size=page_size, page_number=page_number)
    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria, table='user')

    expected_offset = (page_number - 1) * page_size
    expected_query = f'SELECT * FROM user LIMIT {page_size} OFFSET {expected_offset};'  # noqa: S608

    assert query == expected_query
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_without_pagination() -> None:
    """
    Test CriteriaToMysqlConverter class without pagination.
    """
    criteria = Criteria()
    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria, table='user')

    assert query == 'SELECT * FROM user;'
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
    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria, table='user')

    expected_offset = (page_number - 1) * page_size
    expected_query = f'SELECT * FROM user WHERE name = %s LIMIT {page_size} OFFSET {expected_offset};'  # noqa: S608

    assert query == expected_query
    assert parameters == ['John']
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
    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria, table='user')

    expected_offset = (page_number - 1) * page_size
    expected_query = f'SELECT * FROM user ORDER BY name ASC LIMIT {page_size} OFFSET {expected_offset};'  # noqa: S608

    assert query == expected_query
    assert parameters == []
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
    )

    expected_offset = (page_number - 1) * page_size
    expected_query = (
        f'SELECT id, name, age FROM user WHERE age >= %s ORDER BY name DESC LIMIT {page_size} OFFSET {expected_offset};'  # noqa: S608, E501
    )

    assert query == expected_query
    assert parameters == [18]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_pagination_first_page() -> None:
    """
    Test CriteriaToMysqlConverter class with pagination for first page.
    """
    criteria = Criteria(page_size=10, page_number=1)
    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria, table='user')

    assert query == 'SELECT * FROM user LIMIT 10 OFFSET 0;'
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_pagination_second_page() -> None:
    """
    Test CriteriaToMysqlConverter class with pagination for second page.
    """
    criteria = Criteria(page_size=10, page_number=2)
    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria, table='user')

    assert query == 'SELECT * FROM user LIMIT 10 OFFSET 10;'
    assert parameters == []
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
    query, parameters = CriteriaToMysqlConverter.convert(criteria=combined_criteria, table='user')

    expected_offset = (3 - 1) * 20
    expected_query = f'SELECT * FROM user WHERE (active = %s AND age > %s) LIMIT 20 OFFSET {expected_offset};'  # noqa: S608, E501

    assert query == expected_query
    assert parameters == [True, 18]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_page_size_only() -> None:
    """
    Test CriteriaToMysqlConverter generates LIMIT without OFFSET when only page_size is provided.
    """
    page_size = IntegerMother.positive()
    criteria = Criteria(page_size=page_size)

    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria, table='user')

    expected_query = f'SELECT * FROM user LIMIT {page_size};'  # noqa: S608

    assert query == expected_query
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_filters_and_page_size_only() -> None:
    """
    Test CriteriaToMysqlConverter with filters and LIMIT without OFFSET.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)
    page_size = IntegerMother.positive()

    criteria = Criteria(filters=[filter], page_size=page_size)

    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria, table='user')

    expected_query = f'SELECT * FROM user WHERE {filter.field} = %s LIMIT {page_size};'  # noqa: S608

    assert query == expected_query
    assert parameters == [filter.value]
    assert_valid_mysql_syntax(query=query, parameters=parameters)


@mark.unit_testing
def test_criteria_to_mysql_converter_with_orders_and_page_size_only() -> None:
    """
    Test CriteriaToMysqlConverter with orders and LIMIT without OFFSET.
    """
    order = OrderMother.create(direction=Direction.ASC)
    page_size = IntegerMother.positive()

    criteria = Criteria(orders=[order], page_size=page_size)

    query, parameters = CriteriaToMysqlConverter.convert(criteria=criteria, table='user')

    expected_query = f'SELECT * FROM user ORDER BY {order.field} ASC LIMIT {page_size};'  # noqa: S608

    assert query == expected_query
    assert parameters == []
    assert_valid_mysql_syntax(query=query, parameters=parameters)
