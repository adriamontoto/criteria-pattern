"""
Test SqlConverter class.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.converter import SqlConverter
from criteria_pattern.errors import InvalidColumnError, InvalidTableError
from criteria_pattern.models.testing.mothers import CriteriaMother, FilterMother, OrderMother


@mark.unit_testing
def test_sql_converter_with_empty_criteria_and_all_columns() -> None:
    """
    Test SqlConverter class with an empty Criteria object and all columns.
    """
    query, parameters = SqlConverter.convert(criteria=CriteriaMother.empty(), table='user')

    assert query == 'SELECT * FROM user;'
    assert parameters == {}


@mark.unit_testing
def test_sql_converter_with_empty_criteria() -> None:
    """
    Test SqlConverter class with an empty Criteria object.
    """
    query, parameters = SqlConverter.convert(criteria=CriteriaMother.empty(), table='user', columns=['id', 'name'])

    assert query == 'SELECT id, name FROM user;'
    assert parameters == {}


@mark.unit_testing
def test_sql_converter_with_equal_filter() -> None:
    """
    Test SqlConverter class with an EQUAL filter.
    """
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE name = %(parameter_0)s;'
    assert parameters == {'parameter_0': 'John Doe'}


@mark.unit_testing
def test_sql_converter_with_not_equal_filter() -> None:
    """
    Test SqlConverter class with a NOT EQUAL filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_EQUAL, value='John Doe')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE name != %(parameter_0)s;'
    assert parameters == {'parameter_0': 'John Doe'}


@mark.unit_testing
def test_sql_converter_with_greater_filter() -> None:
    """
    Test SqlConverter class with a GREATER filter.
    """
    filter = Filter(field='age', operator=Operator.GREATER, value=18)
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age > %(parameter_0)s;'
    assert parameters == {'parameter_0': 18}


@mark.unit_testing
def test_sql_converter_with_greater_or_equal_filter() -> None:
    """
    Test SqlConverter class with a GREATER OR EQUAL filter.
    """
    filter = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age >= %(parameter_0)s;'
    assert parameters == {'parameter_0': 18}


@mark.unit_testing
def test_sql_converter_with_less_filter() -> None:
    """
    Test SqlConverter class with a LESS filter.
    """
    filter = Filter(field='age', operator=Operator.LESS, value=18)
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age < %(parameter_0)s;'
    assert parameters == {'parameter_0': 18}


@mark.unit_testing
def test_sql_converter_with_less_or_equal_filter() -> None:
    """
    Test SqlConverter class with a LESS OR EQUAL filter.
    """
    filter = Filter(field='age', operator=Operator.LESS_OR_EQUAL, value=18)
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age <= %(parameter_0)s;'
    assert parameters == {'parameter_0': 18}


@mark.unit_testing
def test_sql_converter_with_like_filter() -> None:
    """
    Test SqlConverter class with a LIKE filter.
    """
    filter = Filter(field='name', operator=Operator.LIKE, value='John')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE name LIKE %(parameter_0)s;'
    assert parameters == {'parameter_0': 'John'}


@mark.unit_testing
def test_sql_converter_with_not_like_filter() -> None:
    """
    Test SqlConverter class with a NOT LIKE filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_LIKE, value='John')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE name NOT LIKE %(parameter_0)s;'
    assert parameters == {'parameter_0': 'John'}


@mark.unit_testing
def test_sql_converter_with_contains_filter() -> None:
    """
    Test SqlConverter class with a CONTAINS filter.
    """
    filter = Filter(field='name', operator=Operator.CONTAINS, value='John')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE '%%' || %(parameter_0)s || '%%';"
    assert parameters == {'parameter_0': 'John'}


@mark.unit_testing
def test_sql_converter_with_not_contains_filter() -> None:
    """
    Test SqlConverter class with a NOT CONTAINS filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_CONTAINS, value='John')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE '%%' || %(parameter_0)s || '%%';"
    assert parameters == {'parameter_0': 'John'}


@mark.unit_testing
def test_sql_converter_with_starts_with_filter() -> None:
    """
    Test SqlConverter class with a STARTS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.STARTS_WITH, value='John')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE %(parameter_0)s || '%%';"
    assert parameters == {'parameter_0': 'John'}


@mark.unit_testing
def test_sql_converter_with_not_starts_with_filter() -> None:
    """
    Test SqlConverter class with a NOT STARTS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_STARTS_WITH, value='John')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE %(parameter_0)s || '%%';"
    assert parameters == {'parameter_0': 'John'}


@mark.unit_testing
def test_sql_converter_with_ends_with_filter() -> None:
    """
    Test SqlConverter class with a ENDS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.ENDS_WITH, value='Doe')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE '%%' || %(parameter_0)s;"
    assert parameters == {'parameter_0': 'Doe'}


@mark.unit_testing
def test_sql_converter_with_not_ends_with_filter() -> None:
    """
    Test SqlConverter class with a NOT ENDS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_ENDS_WITH, value='Doe')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE '%%' || %(parameter_0)s;"
    assert parameters == {'parameter_0': 'Doe'}


@mark.unit_testing
def test_sql_converter_with_between_filter_list() -> None:
    """
    Test SqlConverter class with a BETWEEN filter using a list of values.

    Args:
        value (Collection[int]): Filter value.
    """
    filter = Filter(field='age', operator=Operator.BETWEEN, value=[18, 30])
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age BETWEEN %(parameter_0)s AND %(parameter_1)s;'
    assert parameters == {'parameter_0': 18, 'parameter_1': 30}


@mark.unit_testing
def test_sql_converter_with_between_filter_tuple() -> None:
    """
    Test SqlConverter class with a BETWEEN filter using a tuple of values.
    """
    filter = Filter(field='age', operator=Operator.BETWEEN, value=(18, 30))
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age BETWEEN %(parameter_0)s AND %(parameter_1)s;'
    assert parameters == {'parameter_0': 18, 'parameter_1': 30}


@mark.unit_testing
def test_sql_converter_with_not_between_filter_list() -> None:
    """
    Test SqlConverter class with a NOT BETWEEN filter.

    Args:
        value (Collection[int]): Filter value.
    """
    filter = Filter(field='age', operator=Operator.NOT_BETWEEN, value=[18, 30])
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age NOT BETWEEN %(parameter_0)s AND %(parameter_1)s;'
    assert parameters == {'parameter_0': 18, 'parameter_1': 30}


@mark.unit_testing
def test_sql_converter_with_not_between_filter_tuple() -> None:
    """
    Test SqlConverter class with a NOT BETWEEN filter using a tuple of values.
    """
    filter = Filter(field='age', operator=Operator.NOT_BETWEEN, value=(18, 30))
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age NOT BETWEEN %(parameter_0)s AND %(parameter_1)s;'
    assert parameters == {'parameter_0': 18, 'parameter_1': 30}


@mark.unit_testing
def test_sql_converter_with_is_null_filter() -> None:
    """
    Test SqlConverter class with an IS NULL filter.
    """
    filter = Filter(field='email', operator=Operator.IS_NULL, value=None)
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE email IS NULL;'
    assert parameters == {}


@mark.unit_testing
def test_sql_converter_with_is_not_null_filter() -> None:
    """
    Test SqlConverter class with an IS NOT NULL filter.
    """
    filter = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE email IS NOT NULL;'
    assert parameters == {}


@mark.unit_testing
def test_sql_converter_with_in_filter() -> None:
    """
    Test SqlConverter class with an IN filter.
    """
    filter = Filter(field='status', operator=Operator.IN, value=['active', 'pending', 'inactive'])
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'status'],
    )

    assert query == 'SELECT id, name, status FROM user WHERE status IN (%(parameter_0)s, %(parameter_1)s, %(parameter_2)s);'  # noqa: E501  # fmt: skip
    assert parameters == {'parameter_0': 'active', 'parameter_1': 'pending', 'parameter_2': 'inactive'}


@mark.unit_testing
def test_sql_converter_with_not_in_filter() -> None:
    """
    Test SqlConverter class with a NOT IN filter.
    """
    filter = Filter(field='status', operator=Operator.NOT_IN, value=['deleted', 'banned'])
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'status'],
    )

    assert query == 'SELECT id, name, status FROM user WHERE status NOT IN (%(parameter_0)s, %(parameter_1)s);'
    assert parameters == {'parameter_0': 'deleted', 'parameter_1': 'banned'}


@mark.unit_testing
def test_sql_converter_with_and_criteria() -> None:
    """
    Test SqlConverter class with an AND Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    criteria1 = CriteriaMother.with_filters(filters=[filter1])
    criteria2 = CriteriaMother.with_filters(filters=[filter2])
    query1, parameters1 = SqlConverter.convert(criteria=criteria1 & criteria2, table='user', columns=['*'])
    query2, parameters2 = SqlConverter.convert(criteria=criteria2 & criteria1, table='user', columns=['*'])

    assert query1 == 'SELECT * FROM user WHERE (name = %(parameter_0)s AND email IS NOT NULL);'
    assert parameters1 == {'parameter_0': 'John Doe'}
    assert query2 == 'SELECT * FROM user WHERE (email IS NOT NULL AND name = %(parameter_0)s);'
    assert parameters2 == {'parameter_0': 'John Doe'}


@mark.unit_testing
def test_sql_converter_with_or_criteria() -> None:
    """
    Test SqlConverter class with an OR Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    criteria1 = CriteriaMother.with_filters(filters=[filter1])
    criteria2 = CriteriaMother.with_filters(filters=[filter2])
    query1, parameters1 = SqlConverter.convert(criteria=criteria1 | criteria2, table='user', columns=['*'])
    query2, parameters2 = SqlConverter.convert(criteria=criteria2 | criteria1, table='user', columns=['*'])

    assert query1 == 'SELECT * FROM user WHERE (name = %(parameter_0)s OR email IS NOT NULL);'
    assert parameters1 == {'parameter_0': 'John Doe'}
    assert query2 == 'SELECT * FROM user WHERE (email IS NOT NULL OR name = %(parameter_0)s);'
    assert parameters2 == {'parameter_0': 'John Doe'}


@mark.unit_testing
def test_sql_converter_with_not_criteria() -> None:
    """
    Test SqlConverter class with a NOT Criteria object.
    """
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria = CriteriaMother.with_filters(filters=[filter])
    query, parameters = SqlConverter.convert(criteria=~criteria, table='user', columns=['*'])

    assert query == 'SELECT * FROM user WHERE NOT (name = %(parameter_0)s);'
    assert parameters == {'parameter_0': 'John Doe'}


@mark.unit_testing
def test_sql_converter_with_mixed_criteria() -> None:
    """
    Test SqlConverter class with a mixed Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    filter3 = Filter(field='age', operator=Operator.LESS, value=18)
    criteria1 = CriteriaMother.with_filters(filters=[filter1])
    criteria2 = CriteriaMother.with_filters(filters=[filter2])
    criteria3 = CriteriaMother.with_filters(filters=[filter3])
    query, parameters = SqlConverter.convert(criteria=criteria1 & (criteria2 | ~criteria3), table='user', columns=['*'])

    assert query == "SELECT * FROM user WHERE (name = %(parameter_0)s AND (email IS NOT NULL OR NOT (age < %(parameter_1)s)));"  # noqa: E501 # fmt: skip
    assert parameters == {'parameter_0': 'John Doe', 'parameter_1': 18}


@mark.unit_testing
def test_sql_converter_with_asc_order() -> None:
    """
    Test SqlConverter class with an ASC order.
    """
    order = Order(field='name', direction=Direction.ASC)
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_orders(orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user ORDER BY name ASC;'
    assert parameters == {}


@mark.unit_testing
def test_sql_converter_with_desc_order() -> None:
    """
    Test SqlConverter class with a DESC order.
    """
    order = Order(field='name', direction=Direction.DESC)
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_orders(orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user ORDER BY name DESC;'
    assert parameters == {}


@mark.unit_testing
def test_sql_converter_with_multiple_orders_on_the_same_criteria() -> None:
    """
    Test SqlConverter class with multiple orders on the same Criteria object.
    """
    order1 = Order(field='name', direction=Direction.ASC)
    order2 = Order(field='email', direction=Direction.DESC)
    criteria = CriteriaMother.with_orders(orders=[order1, order2])
    query, parameters = SqlConverter.convert(criteria=criteria, table='user', columns=['*'])

    assert query == 'SELECT * FROM user ORDER BY name ASC, email DESC;'
    assert parameters == {}


@mark.unit_testing
def test_sql_converter_with_multiple_orders_on_different_criteria() -> None:
    """
    Test SqlConverter class with multiple orders on different Criteria objects.
    """
    order1 = Order(field='name', direction=Direction.ASC)
    order2 = Order(field='age', direction=Direction.ASC)
    order3 = Order(field='email', direction=Direction.DESC)
    criteria1 = CriteriaMother.with_orders(orders=[order1, order2])
    criteria2 = CriteriaMother.with_orders(orders=[order3])
    query, parameters = SqlConverter.convert(criteria=criteria1 & criteria2, table='user', columns=['*'])

    assert query == 'SELECT * FROM user ORDER BY name ASC, age ASC, email DESC;'
    assert parameters == {}


@mark.unit_testing
def test_sql_converter_with_filtered_and_ordered_criteria() -> None:
    """
    Test SqlConverter class with a filtered and ordered Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    filter3 = Filter(field='age', operator=Operator.LESS, value=18)
    order1 = Order(field='email', direction=Direction.DESC)
    order2 = Order(field='name', direction=Direction.ASC)
    criteria1 = CriteriaMother.create(value=Criteria(filters=[filter1], orders=[order1]))
    criteria2 = CriteriaMother.create(value=Criteria(filters=[filter2], orders=[order2]))
    criteria3 = CriteriaMother.create(value=Criteria(filters=[filter3]))
    query, parameters = SqlConverter.convert(
        criteria=criteria1 & (criteria2 | ~criteria3),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE (name = %(parameter_0)s AND (email IS NOT NULL OR NOT (age < %(parameter_1)s))) ORDER BY email DESC, name ASC;"  # noqa: E501 # fmt: skip
    assert parameters == {'parameter_0': 'John Doe', 'parameter_1': 18}


@mark.unit_testing
def test_sql_converter_with_columns_mapping() -> None:
    """
    Test SqlConverter class with columns mapping.
    """
    filter = Filter(field='full_name', operator=Operator.EQUAL, value='John Doe')
    order = Order(field='full_name', direction=Direction.ASC)
    query, parameters = SqlConverter.convert(
        criteria=Criteria(filters=[filter], orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
        columns_mapping={'full_name': 'name'},
    )

    assert query == 'SELECT id, name, email FROM user WHERE name = %(parameter_0)s ORDER BY name ASC;'
    assert parameters == {'parameter_0': 'John Doe'}


@mark.unit_testing
def test_sql_converter_with_columns_mapping_with_spaces() -> None:
    """
    Test SqlConverter class with columns mapping with spaces.
    """
    filter = Filter(field='full name', operator=Operator.EQUAL, value='John Doe')
    order = Order(field='full name', direction=Direction.ASC)
    query, parameters = SqlConverter.convert(
        criteria=Criteria(filters=[filter], orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
        columns_mapping={'full name': 'name'},
    )

    assert query == 'SELECT id, name, email FROM user WHERE name = %(parameter_0)s ORDER BY name ASC;'
    assert parameters == {'parameter_0': 'John Doe'}


@mark.unit_testing
def test_sql_converter_with_table_injection_check_disabled() -> None:
    """
    Test SqlConverter class with table injection when check_table_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;', operator=Operator.EQUAL)

    SqlConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user; DROP TABLE user;',
        valid_tables=['user'],
    )


@mark.unit_testing
def test_sql_converter_with_table_injection() -> None:
    """
    Test SqlConverter class with table injection.
    """
    with assert_raises(
        expected_exception=InvalidTableError,
        match='Invalid table specified: <<<user; DROP TABLE user;>>>. Valid tables are: <<<user>>>.',
    ):
        SqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user; DROP TABLE user;',
            check_table_injection=True,
            valid_tables=['user'],
        )


@mark.unit_testing
def test_sql_converter_without_table_injection() -> None:
    """
    Test SqlConverter class without table injection.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    SqlConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user',
        check_table_injection=True,
        valid_tables=['user'],
    )


@mark.unit_testing
def test_sql_converter_with_column_injection_check_disabled() -> None:
    """
    Test SqlConverter class with columns injection when check_columns_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    SqlConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user',
        columns=['id; DROP TABLE user;', 'name'],
    )


@mark.unit_testing
def test_sql_converter_with_column_injection() -> None:
    """
    Test SqlConverter class with columns injection.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified: <<<id; DROP TABLE user;>>>. Valid columns are: <<<id, name>>>.',
    ):
        SqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            columns=['id; DROP TABLE user;', 'name'],
            check_column_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_sql_converter_with_column_injection_with_star_invalid() -> None:
    """
    Test SqlConverter class with columns injection where columns attribute is a star and is invalid.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match=r'Invalid column specified: <<<\*>>>. Valid columns are: <<<id, name>>>.',
    ):
        SqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            check_column_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_sql_converter_with_column_injection_with_star_valid() -> None:
    """
    Test SqlConverter class with columns injection where columns attribute is a star and is valid.
    """
    filter: Filter[Any] = FilterMother.create(field='*', operator=Operator.EQUAL)

    SqlConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user',
        check_column_injection=True,
        valid_columns=['*', 'id', 'name'],
    )


@mark.unit_testing
def test_sql_converter_with_column_injection_with_star_and_columns() -> None:
    """
    Test SqlConverter class with columns injection with star and columns.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match=r'Invalid column specified: <<<\*>>>. Valid columns are: <<<id, name>>>.',
    ):
        SqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            columns=['*', 'id', 'name'],
            check_column_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_sql_converter_with_column_mapping_injection() -> None:
    """
    Test SqlConverter class with columns injection.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified: <<<id; DROP TABLE user;>>>. Valid columns are: <<<id, name>>>.',
    ):
        SqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            columns=['id', 'name'],
            columns_mapping={'fullname': 'name', 'id': 'id; DROP TABLE user;'},
            check_column_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_sql_converter_with_filter_field_injection_check_disabled() -> None:
    """
    Test SqlConverter class with filter field injection when check_criteria_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;', operator=Operator.EQUAL)

    SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        valid_columns=['id', 'name'],
    )


@mark.unit_testing
def test_sql_converter_with_filter_field_injection() -> None:
    """
    Test SqlConverter class with filter field injection.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;')

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified: <<<id; DROP TABLE user;>>>. Valid columns are: <<<id, name>>>.',
    ):
        SqlConverter.convert(
            criteria=CriteriaMother.with_filters(filters=[filter]),
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_sql_converter_with_filter_value_injection() -> None:
    """
    Test SqlConverter class with filter value injection.
    """
    filter = Filter(field='id', operator=Operator.EQUAL, value='1; DROP TABLE user;')
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        check_criteria_injection=True,
        valid_columns=['id', 'name'],
    )

    assert query == 'SELECT id, name FROM user WHERE id = %(parameter_0)s;'
    assert parameters == {'parameter_0': '1; DROP TABLE user;'}


@mark.unit_testing
def test_sql_converter_with_order_field_injection() -> None:
    """
    Test SqlConverter class with order field injection.
    """
    order = OrderMother.create(field='id; DROP TABLE user;')

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified: <<<id; DROP TABLE user;>>>. Valid columns are: <<<id, name>>>.',
    ):
        SqlConverter.convert(
            criteria=CriteriaMother.with_orders(orders=[order]),
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_sql_converter_with_two_order_fields_injection() -> None:
    """
    Test SqlConverter class with order field injection.
    """
    order1 = OrderMother.create(field='name')
    order2 = OrderMother.create(field='id; DROP TABLE user;')
    criteria1 = CriteriaMother.with_orders(orders=[order1])
    criteria2 = CriteriaMother.with_orders(orders=[order2])

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified: <<<id; DROP TABLE user;>>>. Valid columns are: <<<id, name>>>.',
    ):
        SqlConverter.convert(
            criteria=criteria1 & criteria2,
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
        )
