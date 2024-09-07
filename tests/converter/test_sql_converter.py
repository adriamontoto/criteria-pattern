"""
Test SqlConverter class.
"""

from collections.abc import Collection

from pytest import mark

from criteria_pattern import OrderDirection
from criteria_pattern.converter import SqlConverter
from criteria_pattern.filter_operator import FilterOperator
from tests.mother import CriteriaMother


def test_sql_converter_with_empty_criteria_and_all_columns() -> None:
    """
    Test SqlConverter class with an empty Criteria object and all columns.
    """
    query = SqlConverter.convert(criteria=CriteriaMother.empty(), table='user')

    assert query == 'SELECT * FROM user;'


def test_sql_converter_with_empty_criteria() -> None:
    """
    Test SqlConverter class with an empty Criteria object.
    """
    query = SqlConverter.convert(criteria=CriteriaMother.empty(), table='user', columns=['id', 'name'])

    assert query == 'SELECT id, name FROM user;'


def test_sql_converter_with_equal_filter() -> None:
    """
    Test SqlConverter class with an EQUAL filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.EQUAL, value='John Doe'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name = 'John Doe';"


def test_sql_converter_with_not_equal_filter() -> None:
    """
    Test SqlConverter class with a NOT EQUAL filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_EQUAL, value='John Doe'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name != 'John Doe';"


def test_sql_converter_with_greater_filter() -> None:
    """
    Test SqlConverter class with a GREATER filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.GREATER, value=18),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE age > '18';"


def test_sql_converter_with_greater_or_equal_filter() -> None:
    """
    Test SqlConverter class with a GREATER OR EQUAL filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.GREATER_OR_EQUAL, value=18),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE age >= '18';"


def test_sql_converter_with_less_filter() -> None:
    """
    Test SqlConverter class with a LESS filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.LESS, value=18),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE age < '18';"


def test_sql_converter_with_less_or_equal_filter() -> None:
    """
    Test SqlConverter class with a LESS OR EQUAL filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.LESS_OR_EQUAL, value=18),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE age <= '18';"


def test_sql_converter_with_like_filter() -> None:
    """
    Test SqlConverter class with a LIKE filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.LIKE, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE 'John';"


def test_sql_converter_with_not_like_filter() -> None:
    """
    Test SqlConverter class with a NOT LIKE filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_LIKE, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE 'John';"


def test_sql_converter_with_contains_filter() -> None:
    """
    Test SqlConverter class with a CONTAINS filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.CONTAINS, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE '%John%';"


def test_sql_converter_with_not_contains_filter() -> None:
    """
    Test SqlConverter class with a NOT CONTAINS filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_CONTAINS, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE '%John%';"


def test_sql_converter_with_starts_with_filter() -> None:
    """
    Test SqlConverter class with a STARTS WITH filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.STARTS_WITH, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE 'John%';"


def test_sql_converter_with_not_starts_with_filter() -> None:
    """
    Test SqlConverter class with a NOT STARTS WITH filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_STARTS_WITH, value='John'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE 'John%';"


def test_sql_converter_with_ends_with_filter() -> None:
    """
    Test SqlConverter class with a ENDS WITH filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.ENDS_WITH, value='Doe'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name LIKE '%Doe';"


def test_sql_converter_with_not_ends_with_filter() -> None:
    """
    Test SqlConverter class with a NOT ENDS WITH filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_ENDS_WITH, value='Doe'),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE name NOT LIKE '%Doe';"


@mark.parametrize('value', [(18, 30), [18, 30]])
def test_sql_converter_with_between_filter(value: Collection[int]) -> None:
    """
    Test SqlConverter class with a BETWEEN filter.

    Args:
        value (Collection[int]): Filter value.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.BETWEEN, value=value),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE age BETWEEN '18' AND '30';"


@mark.parametrize('value', [(18, 30), [18, 30]])
def test_sql_converter_with_not_between_filter(value: Collection[int]) -> None:
    """
    Test SqlConverter class with a NOT BETWEEN filter.

    Args:
        value (Collection[int]): Filter value.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='age', operator=FilterOperator.NOT_BETWEEN, value=value),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == "SELECT id, name, email FROM user WHERE age NOT BETWEEN '18' AND '30';"


@mark.parametrize('value', [('John', 'Jane', 'Mike'), ['John']])
def test_sql_converter_with_in_filter(value: Collection[str]) -> None:
    """
    Test SqlConverter class with an IN filter.

    Args:
        value (Collection[str]): Filter value.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.IN, value=value),
        table='user',
        columns=['id', 'name', 'email'],
    )

    sequence = ', '.join([f"'{v}'" for v in value])
    assert query == f'SELECT id, name, email FROM user WHERE name IN ({sequence});'  # noqa: S608


@mark.parametrize('value', [('John', 'Jane', 'Mike'), ['John']])
def test_sql_converter_with_not_in_filter(value: Collection[str]) -> None:
    """
    Test SqlConverter class with a NOT IN filter.

    Args:
        value (Collection[str]): Filter value.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='name', operator=FilterOperator.NOT_IN, value=value),
        table='user',
        columns=['id', 'name', 'email'],
    )

    sequence = ', '.join([f"'{v}'" for v in value])
    assert query == f'SELECT id, name, email FROM user WHERE name NOT IN ({sequence});'  # noqa: S608


def test_sql_converter_with_is_null_filter() -> None:
    """
    Test SqlConverter class with an IS NULL filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='email', operator=FilterOperator.IS_NULL, value=None),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE email IS NULL;'


def test_sql_converter_with_is_not_null_filter() -> None:
    """
    Test SqlConverter class with an IS NOT NULL filter.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_filter(field='email', operator=FilterOperator.IS_NOT_NULL, value=None),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user WHERE email IS NOT NULL;'


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
    query1 = SqlConverter.convert(criteria=criteria1 & criteria2, table='user', columns=['*'])
    query2 = SqlConverter.convert(criteria=criteria2 & criteria1, table='user', columns=['*'])

    assert query1 == "SELECT * FROM user WHERE (name = 'John Doe' AND email IS NOT NULL);"
    assert query2 == "SELECT * FROM user WHERE (email IS NOT NULL AND name = 'John Doe');"


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
    query1 = SqlConverter.convert(criteria=criteria1 | criteria2, table='user', columns=['*'])
    query2 = SqlConverter.convert(criteria=criteria2 | criteria1, table='user', columns=['*'])

    assert query1 == "SELECT * FROM user WHERE (name = 'John Doe' OR email IS NOT NULL);"
    assert query2 == "SELECT * FROM user WHERE (email IS NOT NULL OR name = 'John Doe');"


def test_sql_converter_with_not_criteria() -> None:
    """
    Test SqlConverter class with a NOT Criteria object.
    """
    criteria = CriteriaMother.create(
        filters=[{'field': 'name', 'operator': FilterOperator.EQUAL, 'value': 'John Doe'}],
    )
    query = SqlConverter.convert(criteria=~criteria, table='user', columns=['*'])

    assert query == "SELECT * FROM user WHERE NOT (name = 'John Doe');"


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
    query = SqlConverter.convert(criteria=criteria1 & (criteria2 | ~criteria3), table='user', columns=['*'])

    assert query == "SELECT * FROM user WHERE (name = 'John Doe' AND (email IS NOT NULL OR NOT (age < '18')));"


def test_sql_converter_with_asc_order() -> None:
    """
    Test SqlConverter class with an ASC order.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_order(field='name', direction=OrderDirection.ASC),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user ORDER BY name ASC;'


def test_sql_converter_with_desc_order() -> None:
    """
    Test SqlConverter class with a DESC order.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.with_order(field='name', direction=OrderDirection.DESC),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT id, name, email FROM user ORDER BY name DESC;'


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
    query = SqlConverter.convert(criteria=criteria, table='user', columns=['*'])

    assert query == 'SELECT * FROM user ORDER BY name ASC, email DESC;'


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
    query = SqlConverter.convert(criteria=criteria1 & criteria2, table='user', columns=['*'])

    assert query == 'SELECT * FROM user ORDER BY name ASC, age ASC;'


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
    query = SqlConverter.convert(
        criteria=criteria1 & (criteria2 | ~criteria3), table='user', columns=['id', 'name', 'email']
    )

    assert query == "SELECT id, name, email FROM user WHERE (name = 'John Doe' AND (email IS NOT NULL OR NOT (age < '18'))) ORDER BY email DESC;"  # noqa: E501 # fmt: skip


def test_sql_converter_with_columns_mapping() -> None:
    """
    Test SqlConverter class with columns mapping.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.create(
            filters=[{'field': 'full_name', 'operator': FilterOperator.EQUAL, 'value': 'John Doe'}],
            orders=[{'field': 'full_name', 'direction': OrderDirection.ASC}],
        ),
        table='user',
        columns=['id', 'name', 'email'],
        columns_mapping={'full_name': 'name'},
    )

    assert query == "SELECT id, name, email FROM user WHERE name = 'John Doe' ORDER BY name ASC;"


def test_sql_converter_with_columns_mapping_with_spaces() -> None:
    """
    Test SqlConverter class with columns mapping with spaces.
    """
    query = SqlConverter.convert(
        criteria=CriteriaMother.create(
            filters=[{'field': 'full name', 'operator': FilterOperator.EQUAL, 'value': 'John Doe'}],
            orders=[{'field': 'full name', 'direction': OrderDirection.ASC}],
        ),
        table='user',
        columns=['id', 'name', 'email'],
        columns_mapping={'full name': 'name'},
    )

    assert query == "SELECT id, name, email FROM user WHERE name = 'John Doe' ORDER BY name ASC;"
