"""
Test SqlConverter class.
"""

from collections.abc import Collection

from pytest import mark, raises as assert_raises

from criteria_pattern import OrderDirection
from criteria_pattern.converter import SqlConverter
from criteria_pattern.exceptions import InvalidColumnError, InvalidTableError
from criteria_pattern.filter_operator import FilterOperator
from tests.mother import CriteriaMother


def test_sql_converter_with_empty_criteria_and_all_columns() -> None:
    """
    Test SqlConverter class with an empty Criteria object and all columns.
    """
    query, parameters = SqlConverter.convert(criteria=CriteriaMother.empty(), table='user')

    assert query == 'SELECT * FROM user;'
    assert parameters == {}


def test_sql_converter_with_empty_criteria() -> None:
    """
    Test SqlConverter class with an empty Criteria object.
    """
    query, parameters = SqlConverter.convert(criteria=CriteriaMother.empty(), table='user', columns=['id', 'name'])

    assert query == 'SELECT id, name FROM user;'
    assert parameters == {}


def test_sql_converter_with_equal_filter() -> None:
    """
    Test SqlConverter class with an EQUAL filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.EQUAL, value='John Doe'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE name = %(parameter_0)s;'
    assert parameters == {'parameter_0': 'John Doe'}


def test_sql_converter_with_not_equal_filter() -> None:
    """
    Test SqlConverter class with a NOT EQUAL filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_EQUAL, value='John Doe'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE name != %(parameter_0)s;'
    assert parameters == {'parameter_0': 'John Doe'}


def test_sql_converter_with_greater_filter() -> None:
    """
    Test SqlConverter class with a GREATER filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.GREATER, value=18),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age > %(parameter_0)s;'
    assert parameters == {'parameter_0': 18}


def test_sql_converter_with_greater_or_equal_filter() -> None:
    """
    Test SqlConverter class with a GREATER OR EQUAL filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.GREATER_OR_EQUAL, value=18),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age >= %(parameter_0)s;'
    assert parameters == {'parameter_0': 18}


def test_sql_converter_with_less_filter() -> None:
    """
    Test SqlConverter class with a LESS filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.LESS, value=18),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age < %(parameter_0)s;'
    assert parameters == {'parameter_0': 18}


def test_sql_converter_with_less_or_equal_filter() -> None:
    """
    Test SqlConverter class with a LESS OR EQUAL filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.LESS_OR_EQUAL, value=18),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age <= %(parameter_0)s;'
    assert parameters == {'parameter_0': 18}


def test_sql_converter_with_like_filter() -> None:
    """
    Test SqlConverter class with a LIKE filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.LIKE, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE name LIKE %(parameter_0)s;'
    assert parameters == {'parameter_0': 'John'}


def test_sql_converter_with_not_like_filter() -> None:
    """
    Test SqlConverter class with a NOT LIKE filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_LIKE, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE name NOT LIKE %(parameter_0)s;'
    assert parameters == {'parameter_0': 'John'}


def test_sql_converter_with_contains_filter() -> None:
    """
    Test SqlConverter class with a CONTAINS filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.CONTAINS, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE '%%' || %(parameter_0)s || '%%';"
    assert parameters == {'parameter_0': 'John'}


def test_sql_converter_with_not_contains_filter() -> None:
    """
    Test SqlConverter class with a NOT CONTAINS filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_CONTAINS, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE '%%' || %(parameter_0)s || '%%';"
    assert parameters == {'parameter_0': 'John'}


def test_sql_converter_with_starts_with_filter() -> None:
    """
    Test SqlConverter class with a STARTS WITH filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.STARTS_WITH, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE %(parameter_0)s || '%%';"
    assert parameters == {'parameter_0': 'John'}


def test_sql_converter_with_not_starts_with_filter() -> None:
    """
    Test SqlConverter class with a NOT STARTS WITH filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_STARTS_WITH, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE %(parameter_0)s || '%%';"
    assert parameters == {'parameter_0': 'John'}


def test_sql_converter_with_ends_with_filter() -> None:
    """
    Test SqlConverter class with a ENDS WITH filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.ENDS_WITH, value='Doe'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE '%%' || %(parameter_0)s;"
    assert parameters == {'parameter_0': 'Doe'}


def test_sql_converter_with_not_ends_with_filter() -> None:
    """
    Test SqlConverter class with a NOT ENDS WITH filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_ENDS_WITH, value='Doe'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE '%%' || %(parameter_0)s;"
    assert parameters == {'parameter_0': 'Doe'}


@mark.parametrize('value', [(18, 30), [18, 30]])
def test_sql_converter_with_between_filter(value: Collection[int]) -> None:
    """
    Test SqlConverter class with a BETWEEN filter.

    Args:
        value (Collection[int]): Filter value.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.BETWEEN, value=value),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age BETWEEN %(parameter_0)s AND %(parameter_1)s;'
    assert parameters == {'parameter_0': 18, 'parameter_1': 30}


@mark.parametrize('value', [(18, 30), [18, 30]])
def test_sql_converter_with_not_between_filter(value: Collection[int]) -> None:
    """
    Test SqlConverter class with a NOT BETWEEN filter.

    Args:
        value (Collection[int]): Filter value.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.NOT_BETWEEN, value=value),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE age NOT BETWEEN %(parameter_0)s AND %(parameter_1)s;'
    assert parameters == {'parameter_0': 18, 'parameter_1': 30}


def test_sql_converter_with_is_null_filter() -> None:
    """
    Test SqlConverter class with an IS NULL filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='email', operator=FilterOperator.IS_NULL, value=None),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE email IS NULL;'
    assert parameters == {}


def test_sql_converter_with_is_not_null_filter() -> None:
    """
    Test SqlConverter class with an IS NOT NULL filter.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='email', operator=FilterOperator.IS_NOT_NULL, value=None),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE email IS NOT NULL;'
    assert parameters == {}


def test_sql_converter_with_and_criteria() -> None:
    """
    Test SqlConverter class with an AND Criteria object.
    """
    criteria1 = CriteriaMother.create(
        filters=[{'field': 'name', 'operator': FilterOperator.EQUAL, 'value': 'John Doe'}],
    )
    criteria2 = CriteriaMother.create(
        filters=[{'field': 'email', 'operator': FilterOperator.IS_NOT_NULL, 'value': None}],
    )
    query1, parameters1 = SqlConverter.convert(criteria=criteria1 & criteria2, table='user', columns=['*'])
    query2, parameters2 = SqlConverter.convert(criteria=criteria2 & criteria1, table='user', columns=['*'])

    assert query1 == 'SELECT * FROM user WHERE (name = %(parameter_0)s AND email IS NOT NULL);'
    assert parameters1 == {'parameter_0': 'John Doe'}

    assert query2 == 'SELECT * FROM user WHERE (email IS NOT NULL AND name = %(parameter_0)s);'
    assert parameters2 == {'parameter_0': 'John Doe'}


def test_sql_converter_with_or_criteria() -> None:
    """
    Test SqlConverter class with an OR Criteria object.
    """
    criteria1 = CriteriaMother.create(
        filters=[{'field': 'name', 'operator': FilterOperator.EQUAL, 'value': 'John Doe'}],
    )
    criteria2 = CriteriaMother.create(
        filters=[{'field': 'email', 'operator': FilterOperator.IS_NOT_NULL, 'value': None}],
    )
    query1, parameters1 = SqlConverter.convert(criteria=criteria1 | criteria2, table='user', columns=['*'])
    query2, parameters2 = SqlConverter.convert(criteria=criteria2 | criteria1, table='user', columns=['*'])

    assert query1 == 'SELECT * FROM user WHERE (name = %(parameter_0)s OR email IS NOT NULL);'
    assert parameters1 == {'parameter_0': 'John Doe'}

    assert query2 == 'SELECT * FROM user WHERE (email IS NOT NULL OR name = %(parameter_0)s);'
    assert parameters2 == {'parameter_0': 'John Doe'}


def test_sql_converter_with_not_criteria() -> None:
    """
    Test SqlConverter class with a NOT Criteria object.
    """
    criteria = CriteriaMother.create(
        filters=[{'field': 'name', 'operator': FilterOperator.EQUAL, 'value': 'John Doe'}],
    )
    query, parameters = SqlConverter.convert(criteria=~criteria, table='user', columns=['*'])

    assert query == 'SELECT * FROM user WHERE NOT (name = %(parameter_0)s);'
    assert parameters == {'parameter_0': 'John Doe'}


def test_sql_converter_with_mixed_criteria() -> None:
    """
    Test SqlConverter class with a mixed Criteria object.
    """
    criteria1 = CriteriaMother.create(
        filters=[{'field': 'name', 'operator': FilterOperator.EQUAL, 'value': 'John Doe'}],
    )
    criteria2 = CriteriaMother.create(
        filters=[{'field': 'email', 'operator': FilterOperator.IS_NOT_NULL, 'value': None}],
    )
    criteria3 = CriteriaMother.create(
        filters=[{'field': 'age', 'operator': FilterOperator.LESS, 'value': 18}],
    )
    query, parameters = SqlConverter.convert(criteria=criteria1 & (criteria2 | ~criteria3), table='user', columns=['*'])

    assert query == "SELECT * FROM user WHERE (name = %(parameter_0)s AND (email IS NOT NULL OR NOT (age < %(parameter_1)s)));"  # noqa: E501 # fmt: skip
    assert parameters == {'parameter_0': 'John Doe', 'parameter_1': 18}


def test_sql_converter_with_asc_order() -> None:
    """
    Test SqlConverter class with an ASC order.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_order(field='name', direction=OrderDirection.ASC),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user ORDER BY name ASC;'
    assert parameters == {}


def test_sql_converter_with_desc_order() -> None:
    """
    Test SqlConverter class with a DESC order.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_order(field='name', direction=OrderDirection.DESC),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user ORDER BY name DESC;'
    assert parameters == {}


def test_sql_converter_with_multiple_orders_on_the_same_criteria() -> None:
    """
    Test SqlConverter class with multiple orders on the same Criteria object.
    """
    criteria = CriteriaMother.create(
        filters=[],
        orders=[
            {'field': 'name', 'direction': OrderDirection.ASC},
            {'field': 'email', 'direction': OrderDirection.DESC},
        ],
    )
    query, parameters = SqlConverter.convert(criteria=criteria, table='user', columns=['*'])

    assert query == 'SELECT * FROM user ORDER BY name ASC, email DESC;'
    assert parameters == {}


def test_sql_converter_with_multiple_orders_on_different_criteria() -> None:
    """
    Test SqlConverter class with multiple orders on different Criteria objects.
    """
    criteria1 = CriteriaMother.create(
        filters=[],
        orders=[
            {'field': 'name', 'direction': OrderDirection.ASC},
            {'field': 'age', 'direction': OrderDirection.ASC},
        ],
    )
    criteria2 = CriteriaMother.create(filters=[], orders=[{'field': 'email', 'direction': OrderDirection.DESC}])
    query, parameters = SqlConverter.convert(criteria=criteria1 & criteria2, table='user', columns=['*'])

    assert query == 'SELECT * FROM user ORDER BY name ASC, age ASC, email DESC;'
    assert parameters == {}


def test_sql_converter_with_filtered_and_ordered_criteria() -> None:
    """
    Test SqlConverter class with a filtered and ordered Criteria object.
    """
    criteria1 = CriteriaMother.create(
        filters=[{'field': 'name', 'operator': FilterOperator.EQUAL, 'value': 'John Doe'}],
        orders=[{'field': 'email', 'direction': OrderDirection.DESC}],
    )
    criteria2 = CriteriaMother.create(
        filters=[{'field': 'email', 'operator': FilterOperator.IS_NOT_NULL, 'value': None}],
        orders=[{'field': 'name', 'direction': OrderDirection.ASC}],
    )
    criteria3 = CriteriaMother.create(
        filters=[{'field': 'age', 'operator': FilterOperator.LESS, 'value': 18}],
    )
    query, parameters = SqlConverter.convert(
        criteria=criteria1 & (criteria2 | ~criteria3), table='user', columns=['id', 'name', 'email']
    )

    assert query == "SELECT id, name, email FROM user WHERE (name = %(parameter_0)s AND (email IS NOT NULL OR NOT (age < %(parameter_1)s))) ORDER BY email DESC, name ASC;"  # noqa: E501 # fmt: skip
    assert parameters == {'parameter_0': 'John Doe', 'parameter_1': 18}


def test_sql_converter_with_columns_mapping() -> None:
    """
    Test SqlConverter class with columns mapping.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.create(
            filters=[{'field': 'full_name', 'operator': FilterOperator.EQUAL, 'value': 'John Doe'}],
            orders=[{'field': 'full_name', 'direction': OrderDirection.ASC}],
        ),
        table='user',
        columns=['id', 'name', 'email'],
        columns_mapping={'full_name': 'name'},
    )

    assert query == 'SELECT id, name, email FROM user WHERE name = %(parameter_0)s ORDER BY name ASC;'
    assert parameters == {'parameter_0': 'John Doe'}


def test_sql_converter_with_columns_mapping_with_spaces() -> None:
    """
    Test SqlConverter class with columns mapping with spaces.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.create(
            filters=[{'field': 'full name', 'operator': FilterOperator.EQUAL, 'value': 'John Doe'}],
            orders=[{'field': 'full name', 'direction': OrderDirection.ASC}],
        ),
        table='user',
        columns=['id', 'name', 'email'],
        columns_mapping={'full name': 'name'},
    )

    assert query == 'SELECT id, name, email FROM user WHERE name = %(parameter_0)s ORDER BY name ASC;'
    assert parameters == {'parameter_0': 'John Doe'}


def test_sql_converter_with_table_injection_check_disabled() -> None:
    """
    Test SqlConverter class with table injection when check_table_injection is disabled.
    """
    SqlConverter.convert(criteria=CriteriaMother.create(), table='user; DROP TABLE user;', valid_tables=['user'])


def test_sql_converter_with_table_injection() -> None:
    """
    Test SqlConverter class with table injection.
    """
    with assert_raises(
        expected_exception=InvalidTableError,
        match='Invalid table specified: <<<user; DROP TABLE user;>>>.Valid tables are: <<<user>>>.',
    ):
        SqlConverter.convert(
            criteria=CriteriaMother.create(),
            table='user; DROP TABLE user;',
            check_table_injection=True,
            valid_tables=['user'],
        )


def test_sql_converter_without_table_injection() -> None:
    """
    Test SqlConverter class without table injection.
    """
    SqlConverter.convert(
        criteria=CriteriaMother.create(),
        table='user',
        check_table_injection=True,
        valid_tables=['user'],
    )


def test_sql_converter_with_column_injection_check_disabled() -> None:
    """
    Test SqlConverter class with columns injection when check_columns_injection is disabled.
    """
    SqlConverter.convert(criteria=CriteriaMother.create(), table='user', columns=['id; DROP TABLE user;', 'name'])


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


def test_sql_converter_with_column_injection_with_star_valid() -> None:
    """
    Test SqlConverter class with columns injection where columns attribute is a star and is valid.
    """
    SqlConverter.convert(
        criteria=CriteriaMother.create(),
        table='user',
        check_column_injection=True,
        valid_columns=['*', 'id', 'name'],
    )


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


def test_sql_converter_with_filter_field_injection_check_disabled() -> None:
    """
    Test SqlConverter class with filter field injection when check_criteria_injection is disabled.
    """
    SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='id; DROP TABLE user;', operator=FilterOperator.EQUAL, value=1),
        table='user',
        columns=['id', 'name'],
        valid_columns=['id', 'name'],
    )


def test_sql_converter_with_filter_field_injection() -> None:
    """
    Test SqlConverter class with filter field injection.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified: <<<id; DROP TABLE user;>>>. Valid columns are: <<<id, name>>>.',
    ):
        SqlConverter.convert(
            criteria=CriteriaMother.with_filter(field='id; DROP TABLE user;', operator=FilterOperator.EQUAL, value=1),
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
        )


def test_sql_converter_with_filter_value_injection() -> None:
    """
    Test SqlConverter class with filter value injection.
    """
    query, parameters = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='id', operator=FilterOperator.EQUAL, value='1; DROP TABLE user;'),
        table='user',
        columns=['id', 'name'],
        check_criteria_injection=True,
        valid_columns=['id', 'name'],
    )

    assert query == 'SELECT id, name FROM user WHERE id = %(parameter_0)s;'
    assert parameters == {'parameter_0': '1; DROP TABLE user;'}


def test_sql_converter_with_order_field_injection() -> None:
    """
    Test SqlConverter class with order field injection.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified: <<<id; DROP TABLE user;>>>. Valid columns are: <<<id, name>>>.',
    ):
        SqlConverter.convert(
            criteria=CriteriaMother.with_order(field='id; DROP TABLE user;', direction=OrderDirection.ASC),
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
        )


def test_sql_converter_with_two_order_fields_injection() -> None:
    """
    Test SqlConverter class with order field injection.
    """
    criteria1 = CriteriaMother.with_order(field='name', direction=OrderDirection.ASC)
    criteria2 = CriteriaMother.with_order(field='id; DROP TABLE user;', direction=OrderDirection.DESC)

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
