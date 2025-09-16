"""
Test CriteriaToSqliteConverter class.
"""

from typing import Any

from object_mother_pattern import IntegerMother
from pytest import mark, raises as assert_raises
from sqlglot import parse_one

from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.converters import CriteriaToSqliteConverter
from criteria_pattern.errors import InvalidColumnError, InvalidDirectionError, InvalidOperatorError, InvalidTableError
from criteria_pattern.models.testing.mothers import CriteriaMother, FilterMother, OrderMother


def assert_valid_sqlite_syntax(*, query: str) -> None:
    """
    Helper function to validate that the generated SQL query is valid SQLite syntax using sqlglot.

    Args:
        query (str): The SQL query to validate.

    Raises:
        AssertionError: If the query is not valid SQLite syntax.
    """
    try:
        parsed = parse_one(sql=query, dialect='sqlite')
        normalized = parsed.sql(dialect='sqlite')

        assert normalized is not None

    except Exception as exception:
        raise AssertionError('Invalid SQLite syntax.') from exception


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_empty_criteria_and_all_columns() -> None:
    """
    Test CriteriaToSqliteConverter class with an empty Criteria object and all columns.
    """
    query, parameters = CriteriaToSqliteConverter.convert(criteria=CriteriaMother.empty(), table='user')

    assert query == 'SELECT * FROM "user";'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_empty_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with an empty Criteria object.
    """
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.empty(),
        table='user',
        columns=['id', 'name'],
    )

    assert query == 'SELECT "id", "name" FROM "user";'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_equal_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with an EQUAL filter.
    """
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" = :parameter_0;'
    assert parameters == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_not_equal_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a NOT EQUAL filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_EQUAL, value='John Doe')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" != :parameter_0;'
    assert parameters == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_greater_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a GREATER filter.
    """
    filter = Filter(field='age', operator=Operator.GREATER, value=18)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "age" > :parameter_0;'
    assert parameters == {'parameter_0': 18}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_greater_or_equal_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a GREATER OR EQUAL filter.
    """
    filter = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "age" >= :parameter_0;'
    assert parameters == {'parameter_0': 18}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_less_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a LESS filter.
    """
    filter = Filter(field='age', operator=Operator.LESS, value=18)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "age" < :parameter_0;'
    assert parameters == {'parameter_0': 18}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_less_or_equal_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a LESS OR EQUAL filter.
    """
    filter = Filter(field='age', operator=Operator.LESS_OR_EQUAL, value=18)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "age" <= :parameter_0;'
    assert parameters == {'parameter_0': 18}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_like_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a LIKE filter.
    """
    filter = Filter(field='name', operator=Operator.LIKE, value='John')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" LIKE :parameter_0;'
    assert parameters == {'parameter_0': 'John'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_not_like_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a NOT LIKE filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_LIKE, value='John')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" NOT LIKE :parameter_0;'
    assert parameters == {'parameter_0': 'John'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_contains_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a CONTAINS filter.
    """
    filter = Filter(field='name', operator=Operator.CONTAINS, value='John')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" LIKE \'%\' || :parameter_0 || \'%\';'
    assert parameters == {'parameter_0': 'John'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_not_contains_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a NOT CONTAINS filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_CONTAINS, value='John')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" NOT LIKE \'%\' || :parameter_0 || \'%\';'
    assert parameters == {'parameter_0': 'John'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_starts_with_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a STARTS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.STARTS_WITH, value='John')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" LIKE :parameter_0 || \'%\';'
    assert parameters == {'parameter_0': 'John'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_not_starts_with_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a NOT STARTS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_STARTS_WITH, value='John')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" NOT LIKE :parameter_0 || \'%\';'
    assert parameters == {'parameter_0': 'John'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_ends_with_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a ENDS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.ENDS_WITH, value='Doe')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" LIKE \'%\' || :parameter_0;'
    assert parameters == {'parameter_0': 'Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_not_ends_with_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a NOT ENDS WITH filter.
    """
    filter = Filter(field='name', operator=Operator.NOT_ENDS_WITH, value='Doe')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" NOT LIKE \'%\' || :parameter_0;'
    assert parameters == {'parameter_0': 'Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_between_filter_list() -> None:
    """
    Test CriteriaToSqliteConverter class with a BETWEEN filter using a list of values.
    """
    filter = Filter(field='age', operator=Operator.BETWEEN, value=[18, 30])
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "age" BETWEEN :parameter_0 AND :parameter_1;'
    assert parameters == {'parameter_0': 18, 'parameter_1': 30}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_between_filter_tuple() -> None:
    """
    Test CriteriaToSqliteConverter class with a BETWEEN filter using a tuple of values.
    """
    filter = Filter(field='age', operator=Operator.BETWEEN, value=(18, 30))
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "age" BETWEEN :parameter_0 AND :parameter_1;'
    assert parameters == {'parameter_0': 18, 'parameter_1': 30}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_not_between_filter_list() -> None:
    """
    Test CriteriaToSqliteConverter class with a NOT BETWEEN filter.
    """
    filter = Filter(field='age', operator=Operator.NOT_BETWEEN, value=[18, 30])
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "age" NOT BETWEEN :parameter_0 AND :parameter_1;'
    assert parameters == {'parameter_0': 18, 'parameter_1': 30}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_not_between_filter_tuple() -> None:
    """
    Test CriteriaToSqliteConverter class with a NOT BETWEEN filter using a tuple of values.
    """
    filter = Filter(field='age', operator=Operator.NOT_BETWEEN, value=(18, 30))
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "age" NOT BETWEEN :parameter_0 AND :parameter_1;'
    assert parameters == {'parameter_0': 18, 'parameter_1': 30}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_is_null_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with an IS NULL filter.
    """
    filter = Filter(field='email', operator=Operator.IS_NULL, value=None)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "email" IS NULL;'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_is_not_null_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with an IS NOT NULL filter.
    """
    filter = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "email" IS NOT NULL;'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_in_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with an IN filter.
    """
    filter = Filter(field='status', operator=Operator.IN, value=['active', 'pending', 'inactive'])
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'status'],
    )

    assert query == 'SELECT "id", "name", "status" FROM "user" WHERE "status" IN (:parameter_0, :parameter_1, :parameter_2);'  # noqa: E501  # fmt: skip
    assert parameters == {'parameter_0': 'active', 'parameter_1': 'pending', 'parameter_2': 'inactive'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_not_in_filter() -> None:
    """
    Test CriteriaToSqliteConverter class with a NOT IN filter.
    """
    filter = Filter(field='status', operator=Operator.NOT_IN, value=['deleted', 'banned'])
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name', 'status'],
    )

    assert query == 'SELECT "id", "name", "status" FROM "user" WHERE "status" NOT IN (:parameter_0, :parameter_1);'
    assert parameters == {'parameter_0': 'deleted', 'parameter_1': 'banned'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_and_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with an AND Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    criteria1 = CriteriaMother.with_filters(filters=[filter1])
    criteria2 = CriteriaMother.with_filters(filters=[filter2])
    query1, parameters1 = CriteriaToSqliteConverter.convert(
        criteria=criteria1 & criteria2,
        table='user',
        columns=['*'],
    )
    query2, parameters2 = CriteriaToSqliteConverter.convert(
        criteria=criteria2 & criteria1,
        table='user',
        columns=['*'],
    )

    assert query1 == 'SELECT * FROM "user" WHERE ("name" = :parameter_0 AND "email" IS NOT NULL);'
    assert parameters1 == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query1)
    assert query2 == 'SELECT * FROM "user" WHERE ("email" IS NOT NULL AND "name" = :parameter_0);'
    assert parameters2 == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query2)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_or_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with an OR Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    criteria1 = CriteriaMother.with_filters(filters=[filter1])
    criteria2 = CriteriaMother.with_filters(filters=[filter2])
    query1, parameters1 = CriteriaToSqliteConverter.convert(criteria=criteria1 | criteria2, table='user', columns=['*'])
    query2, parameters2 = CriteriaToSqliteConverter.convert(criteria=criteria2 | criteria1, table='user', columns=['*'])

    assert query1 == 'SELECT * FROM "user" WHERE ("name" = :parameter_0 OR "email" IS NOT NULL);'
    assert parameters1 == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query1)
    assert query2 == 'SELECT * FROM "user" WHERE ("email" IS NOT NULL OR "name" = :parameter_0);'
    assert parameters2 == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query2)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_not_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with a NOT Criteria object.
    """
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria = CriteriaMother.with_filters(filters=[filter])
    query, parameters = CriteriaToSqliteConverter.convert(criteria=~criteria, table='user', columns=['*'])

    assert query == 'SELECT * FROM "user" WHERE NOT ("name" = :parameter_0);'
    assert parameters == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_and_criteria_empty_left() -> None:
    """
    Test CriteriaToSqliteConverter class with an AND Criteria where left side is empty.
    """
    empty_criteria = Criteria()
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria_with_filter = CriteriaMother.with_filters(filters=[filter])

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=empty_criteria & criteria_with_filter,
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user" WHERE "name" = :parameter_0;'
    assert parameters == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_and_criteria_empty_right() -> None:
    """
    Test CriteriaToSqliteConverter class with an AND Criteria where right side is empty.
    """
    empty_criteria = Criteria()
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria_with_filter = CriteriaMother.with_filters(filters=[filter])

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=criteria_with_filter & empty_criteria,
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user" WHERE "name" = :parameter_0;'
    assert parameters == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_and_criteria_both_empty() -> None:
    """
    Test CriteriaToSqliteConverter class with an AND Criteria where both sides are empty.
    """
    empty_criteria1 = Criteria()
    empty_criteria2 = Criteria()

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=empty_criteria1 & empty_criteria2,
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user";'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_or_criteria_empty_left() -> None:
    """
    Test CriteriaToSqliteConverter class with an OR Criteria where left side is empty.
    """
    empty_criteria = Criteria()
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria_with_filter = CriteriaMother.with_filters(filters=[filter])

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=empty_criteria | criteria_with_filter,
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user" WHERE "name" = :parameter_0;'
    assert parameters == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_or_criteria_empty_right() -> None:
    """
    Test CriteriaToSqliteConverter class with an OR Criteria where right side is empty.
    """
    empty_criteria = Criteria()
    filter = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    criteria_with_filter = CriteriaMother.with_filters(filters=[filter])

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=criteria_with_filter | empty_criteria,
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user" WHERE "name" = :parameter_0;'
    assert parameters == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_or_criteria_both_empty() -> None:
    """
    Test CriteriaToSqliteConverter class with an OR Criteria where both sides are empty.
    """
    empty_criteria1 = Criteria()
    empty_criteria2 = Criteria()

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=empty_criteria1 | empty_criteria2,
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user";'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_not_empty_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with a NOT of empty Criteria.
    """
    empty_criteria = Criteria()

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=~empty_criteria,
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user";'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_complex_empty_combination() -> None:
    """
    Test CriteriaToSqliteConverter with complex combinations including empty criteria.
    This replicates the issue from main.py adapted for SQLite.
    """
    criteria = Criteria()
    orders = [Order(field='created_date', direction=Direction.DESC), Order(field='identifier', direction=Direction.ASC)]
    match_by_organization = Criteria(
        filters=[Filter(field='organization_identifier', operator=Operator.EQUAL, value='test')],
        orders=orders,
    )

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=match_by_organization & criteria,
        table='test_table',
    )

    assert query == 'SELECT * FROM "test_table" WHERE "organization_identifier" = :parameter_0 ORDER BY "created_date" DESC, "identifier" ASC;'  # noqa: E501 # fmt: skip
    assert parameters == {'parameter_0': 'test'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_nested_empty_and_criteria() -> None:
    """
    Test CriteriaToSqliteConverter with nested AND where both sides are empty.
    This forces the recursive processor to hit the branch where both conditions are empty.
    """
    empty_criteria1 = Criteria()
    empty_criteria2 = Criteria()
    filter_criteria = Filter(field='name', operator=Operator.EQUAL, value='John')
    main_criteria = CriteriaMother.with_filters(filters=[filter_criteria])

    nested_empty = empty_criteria1 & empty_criteria2
    combined = main_criteria & nested_empty

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=combined,
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user" WHERE "name" = :parameter_0;'
    assert parameters == {'parameter_0': 'John'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_nested_empty_or_criteria() -> None:
    """
    Test CriteriaToSqliteConverter with nested OR where both sides are empty.
    This forces the recursive processor to hit the branch where both conditions are empty.
    """
    empty_criteria1 = Criteria()
    empty_criteria2 = Criteria()
    filter_criteria = Filter(field='name', operator=Operator.EQUAL, value='John')
    main_criteria = CriteriaMother.with_filters(filters=[filter_criteria])

    nested_empty = empty_criteria1 | empty_criteria2
    combined = main_criteria | nested_empty

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=combined,
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user" WHERE "name" = :parameter_0;'
    assert parameters == {'parameter_0': 'John'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_nested_empty_not_criteria() -> None:
    """
    Test CriteriaToSqliteConverter with nested NOT of empty criteria.
    This forces the recursive processor to hit the branch where NOT condition is empty.
    """
    empty_criteria = Criteria()
    filter_criteria = Filter(field='name', operator=Operator.EQUAL, value='John')
    main_criteria = CriteriaMother.with_filters(filters=[filter_criteria])

    not_empty = ~empty_criteria
    combined = main_criteria & not_empty

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=combined,
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user" WHERE "name" = :parameter_0;'
    assert parameters == {'parameter_0': 'John'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_mixed_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with a mixed Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    filter3 = Filter(field='age', operator=Operator.LESS, value=18)
    criteria1 = CriteriaMother.with_filters(filters=[filter1])
    criteria2 = CriteriaMother.with_filters(filters=[filter2])
    criteria3 = CriteriaMother.with_filters(filters=[filter3])
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=criteria1 & (criteria2 | ~criteria3),
        table='user',
        columns=['*'],
    )

    assert query == 'SELECT * FROM "user" WHERE ("name" = :parameter_0 AND ("email" IS NOT NULL OR NOT ("age" < :parameter_1)));'  # noqa: E501 # fmt: skip
    assert parameters == {'parameter_0': 'John Doe', 'parameter_1': 18}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_asc_order() -> None:
    """
    Test CriteriaToSqliteConverter class with an ASC order.
    """
    order = Order(field='name', direction=Direction.ASC)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_orders(orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" ORDER BY "name" ASC;'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_desc_order() -> None:
    """
    Test CriteriaToSqliteConverter class with a DESC order.
    """
    order = Order(field='name', direction=Direction.DESC)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_orders(orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" ORDER BY "name" DESC;'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_multiple_orders_on_the_same_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with multiple orders on the same Criteria object.
    """
    order1 = Order(field='name', direction=Direction.ASC)
    order2 = Order(field='email', direction=Direction.DESC)
    criteria = CriteriaMother.with_orders(orders=[order1, order2])
    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user', columns=['*'])

    assert query == 'SELECT * FROM "user" ORDER BY "name" ASC, "email" DESC;'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_multiple_orders_on_different_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with multiple orders on different Criteria objects.
    """
    order1 = Order(field='name', direction=Direction.ASC)
    order2 = Order(field='age', direction=Direction.ASC)
    order3 = Order(field='email', direction=Direction.DESC)
    criteria1 = CriteriaMother.with_orders(orders=[order1, order2])
    criteria2 = CriteriaMother.with_orders(orders=[order3])
    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria1 & criteria2, table='user', columns=['*'])

    assert query == 'SELECT * FROM "user" ORDER BY "name" ASC, "age" ASC, "email" DESC;'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_filtered_and_ordered_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with a filtered and ordered Criteria object.
    """
    filter1 = Filter(field='name', operator=Operator.EQUAL, value='John Doe')
    filter2 = Filter(field='email', operator=Operator.IS_NOT_NULL, value=None)
    filter3 = Filter(field='age', operator=Operator.LESS, value=18)
    order1 = Order(field='email', direction=Direction.DESC)
    order2 = Order(field='name', direction=Direction.ASC)
    criteria1 = CriteriaMother.create(value=Criteria(filters=[filter1], orders=[order1]))
    criteria2 = CriteriaMother.create(value=Criteria(filters=[filter2], orders=[order2]))
    criteria3 = CriteriaMother.create(value=Criteria(filters=[filter3]))
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=criteria1 & (criteria2 | ~criteria3),
        table='user',
        columns=['id', 'name', 'email'],
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE ("name" = :parameter_0 AND ("email" IS NOT NULL OR NOT ("age" < :parameter_1))) ORDER BY "email" DESC, "name" ASC;'  # noqa: E501 # fmt: skip
    assert parameters == {'parameter_0': 'John Doe', 'parameter_1': 18}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_columns_mapping() -> None:
    """
    Test CriteriaToSqliteConverter class with columns mapping.
    """
    filter = Filter(field='full_name', operator=Operator.EQUAL, value='John Doe')
    order = Order(field='full_name', direction=Direction.ASC)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=Criteria(filters=[filter], orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
        columns_mapping={'full_name': 'name'},
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" = :parameter_0 ORDER BY "name" ASC;'
    assert parameters == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_columns_mapping_with_spaces() -> None:
    """
    Test CriteriaToSqliteConverter class with columns mapping with spaces.
    """
    filter = Filter(field='full name', operator=Operator.EQUAL, value='John Doe')
    order = Order(field='full name', direction=Direction.ASC)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=Criteria(filters=[filter], orders=[order]),
        table='user',
        columns=['id', 'name', 'email'],
        columns_mapping={'full name': 'name'},
    )

    assert query == 'SELECT "id", "name", "email" FROM "user" WHERE "name" = :parameter_0 ORDER BY "name" ASC;'
    assert parameters == {'parameter_0': 'John Doe'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_table_injection_check_disabled() -> None:
    """
    Test CriteriaToSqliteConverter class with table injection when check_table_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;', operator=Operator.EQUAL)

    CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user; DROP TABLE user;',
        valid_tables=['user'],
    )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_table_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with table injection.
    """
    with assert_raises(
        expected_exception=InvalidTableError,
        match='Invalid table specified <<<user; DROP TABLE user;>>>. Valid tables are <<<user>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.create(),
            table='user; DROP TABLE user;',
            check_table_injection=True,
            valid_tables=['user'],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_without_table_injection() -> None:
    """
    Test CriteriaToSqliteConverter class without table injection.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user',
        check_table_injection=True,
        valid_tables=['user'],
    )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_column_injection_check_disabled() -> None:
    """
    Test CriteriaToSqliteConverter class with columns injection when check_columns_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user',
        columns=['id; DROP TABLE user;', 'name'],
    )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_column_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with columns injection.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            columns=['id; DROP TABLE user;', 'name'],
            check_column_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_column_injection_with_star_invalid() -> None:
    """
    Test CriteriaToSqliteConverter class with columns injection where columns attribute is a star and is invalid.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match=r'Invalid column specified <<<\*>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            check_column_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_column_injection_with_star_valid() -> None:
    """
    Test CriteriaToSqliteConverter class with columns injection where columns attribute is a star and is valid.
    """
    filter: Filter[Any] = FilterMother.create(field='*', operator=Operator.EQUAL)

    CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.create(filters=[filter]),
        table='user',
        check_column_injection=True,
        valid_columns=['*', 'id', 'name'],
    )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_column_injection_with_star_and_columns() -> None:
    """
    Test CriteriaToSqliteConverter class with columns injection with star and columns.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match=r'Invalid column specified <<<\*>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            columns=['*', 'id', 'name'],
            check_column_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_column_mapping_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with columns injection.
    """
    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.create(),
            table='user',
            columns=['id', 'name'],
            columns_mapping={'fullname': 'name', 'id': 'id; DROP TABLE user;'},
            check_column_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_filter_field_injection_check_disabled() -> None:
    """
    Test CriteriaToSqliteConverter class with filter field injection when check_criteria_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;', operator=Operator.EQUAL)

    CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        valid_columns=['id', 'name'],
    )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_filter_field_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with filter field injection.
    """
    filter: Filter[Any] = FilterMother.create(field='id; DROP TABLE user;')

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.with_filters(filters=[filter]),
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_filter_value_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with filter value injection.
    """
    filter = Filter(field='id', operator=Operator.EQUAL, value='1; DROP TABLE user;')
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        check_criteria_injection=True,
        valid_columns=['id', 'name'],
    )

    assert query == 'SELECT "id", "name" FROM "user" WHERE "id" = :parameter_0;'
    assert parameters == {'parameter_0': '1; DROP TABLE user;'}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_order_field_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with order field injection.
    """
    order = OrderMother.create(field='id; DROP TABLE user;')

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.with_orders(orders=[order]),
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_two_order_fields_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with order field injection.
    """
    order1 = OrderMother.create(field='name')
    order2 = OrderMother.create(field='id; DROP TABLE user;')
    criteria1 = CriteriaMother.with_orders(orders=[order1])
    criteria2 = CriteriaMother.with_orders(orders=[order2])

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<id; DROP TABLE user;>>>. Valid columns are <<<id, name>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=criteria1 & criteria2,
            table='user',
            columns=['id', 'name'],
            check_criteria_injection=True,
            valid_columns=['id', 'name'],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_operator_injection_check_disabled() -> None:
    """
    Test CriteriaToSqliteConverter class with operator injection when check_operator_injection is disabled.
    """
    filter: Filter[Any] = FilterMother.create()

    CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        valid_operators=[Operator.GREATER, Operator.LESS],
    )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_operator_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with operator injection.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.with_filters(filters=[filter]),
            table='user',
            columns=['id', 'name'],
            check_operator_injection=True,
            valid_operators=[Operator.GREATER, Operator.LESS],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_valid_operator() -> None:
    """
    Test CriteriaToSqliteConverter class with valid operator.
    """
    filter: Filter[Any] = FilterMother.create(field='id', operator=Operator.GREATER, value=1)

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_filters(filters=[filter]),
        table='user',
        columns=['id', 'name'],
        check_operator_injection=True,
        valid_operators=[Operator.GREATER, Operator.LESS],
    )

    assert query == 'SELECT "id", "name" FROM "user" WHERE "id" > :parameter_0;'
    assert parameters == {'parameter_0': 1}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_multiple_filters_operator_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with multiple filters where one has invalid operator.
    """
    filter1: Filter[Any] = FilterMother.create(operator=Operator.GREATER)
    filter2: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<EQUAL>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.with_filters(filters=[filter1, filter2]),
            table='user',
            columns=['id', 'name'],
            check_operator_injection=True,
            valid_operators=[Operator.GREATER, Operator.LESS],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_complex_criteria_operator_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with complex criteria containing invalid operator.
    """
    criteria1 = CriteriaMother.create(filters=[FilterMother.create(operator=Operator.GREATER)])
    criteria2 = CriteriaMother.create(filters=[FilterMother.create(operator=Operator.LESS)])
    criteria3 = CriteriaMother.create(filters=[FilterMother.create(operator=Operator.LIKE)])

    with assert_raises(
        expected_exception=InvalidOperatorError,
        match='Invalid operator specified <<<LIKE>>>. Valid operators are <<<GREATER, LESS>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=criteria1 & (criteria2 | criteria3),
            table='user',
            columns=['id', 'name', 'age'],
            check_operator_injection=True,
            valid_operators=[Operator.GREATER, Operator.LESS],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_direction_injection_check_disabled() -> None:
    """
    Test CriteriaToSqliteConverter class with direction injection when check_direction_injection is disabled.
    """
    order: Order = OrderMother.create()

    CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_orders(orders=[order]),
        table='user',
        columns=['id', 'name'],
        valid_directions=[Direction.ASC],
    )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_direction_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with direction injection.
    """
    order: Order = OrderMother.create(direction=Direction.DESC)

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.with_orders(orders=[order]),
            table='user',
            columns=['id', 'name'],
            check_direction_injection=True,
            valid_directions=[Direction.ASC],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_valid_direction() -> None:
    """
    Test CriteriaToSqliteConverter class with valid direction.
    """
    order: Order = OrderMother.create(field='id', direction=Direction.ASC)

    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=CriteriaMother.with_orders(orders=[order]),
        table='user',
        columns=['id', 'name'],
        check_direction_injection=True,
        valid_directions=[Direction.ASC, Direction.DESC],
    )

    assert query == 'SELECT "id", "name" FROM "user" ORDER BY "id" ASC;'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_multiple_orders_direction_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with multiple orders where one has invalid direction.
    """
    order1: Order = OrderMother.create(direction=Direction.ASC)
    order2: Order = OrderMother.create(direction=Direction.DESC)

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=CriteriaMother.with_orders(orders=[order1, order2]),
            table='user',
            columns=['id', 'name'],
            check_direction_injection=True,
            valid_directions=[Direction.ASC],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_complex_criteria_direction_injection() -> None:
    """
    Test CriteriaToSqliteConverter class with complex criteria containing invalid direction.
    """
    criteria1 = CriteriaMother.create(orders=[OrderMother.create(direction=Direction.ASC)])
    criteria2 = CriteriaMother.create(orders=[OrderMother.create(direction=Direction.DESC)])

    with assert_raises(
        expected_exception=InvalidDirectionError,
        match='Invalid direction specified <<<DESC>>>. Valid directions are <<<ASC>>>.',
    ):
        CriteriaToSqliteConverter.convert(
            criteria=criteria1 & criteria2,
            table='user',
            columns=['id', 'name', 'age'],
            check_direction_injection=True,
            valid_directions=[Direction.ASC],
        )


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_pagination() -> None:
    """
    Test CriteriaToSqliteConverter class with pagination.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    criteria = Criteria(page_size=page_size, page_number=page_number)
    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user')

    expected_offset = (page_number - 1) * page_size
    expected_query = 'SELECT * FROM "user" LIMIT :limit_0 OFFSET :offset_1;'  # noqa: S608

    assert query == expected_query
    assert parameters == {'limit_0': page_size, 'offset_1': expected_offset}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_without_pagination() -> None:
    """
    Test CriteriaToSqliteConverter class without pagination.
    """
    criteria = Criteria()
    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user')

    assert query == 'SELECT * FROM "user";'
    assert parameters == {}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_filters_and_pagination() -> None:
    """
    Test CriteriaToSqliteConverter class with filters and pagination.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    filter = Filter(field='name', operator=Operator.EQUAL, value='John')
    criteria = Criteria(filters=[filter], page_size=page_size, page_number=page_number)
    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user')

    expected_offset = (page_number - 1) * page_size
    expected_query = 'SELECT * FROM "user" WHERE "name" = :parameter_0 LIMIT :limit_1 OFFSET :offset_2;'  # noqa: S608

    assert query == expected_query
    assert parameters == {'parameter_0': 'John', 'limit_1': page_size, 'offset_2': expected_offset}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_orders_and_pagination() -> None:
    """
    Test CriteriaToSqliteConverter class with orders and pagination.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    order = Order(field='name', direction=Direction.ASC)
    criteria = Criteria(orders=[order], page_size=page_size, page_number=page_number)
    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user')

    expected_offset = (page_number - 1) * page_size
    expected_query = 'SELECT * FROM "user" ORDER BY "name" ASC LIMIT :limit_0 OFFSET :offset_1;'  # noqa: S608

    assert query == expected_query
    assert parameters == {'limit_0': page_size, 'offset_1': expected_offset}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_filters_orders_and_pagination() -> None:
    """
    Test CriteriaToSqliteConverter class with filters, orders, and pagination.
    """
    page_size = IntegerMother.positive()
    page_number = IntegerMother.positive()

    filter = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    order = Order(field='name', direction=Direction.DESC)
    criteria = Criteria(filters=[filter], orders=[order], page_size=page_size, page_number=page_number)
    query, parameters = CriteriaToSqliteConverter.convert(
        criteria=criteria,
        table='user',
        columns=['id', 'name', 'age'],
    )

    expected_offset = (page_number - 1) * page_size
    expected_query = 'SELECT "id", "name", "age" FROM "user" WHERE "age" >= :parameter_0 ORDER BY "name" DESC LIMIT :limit_1 OFFSET :offset_2;'  # noqa: S608, E501

    assert query == expected_query
    assert parameters == {'parameter_0': 18, 'limit_1': page_size, 'offset_2': expected_offset}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_pagination_first_page() -> None:
    """
    Test CriteriaToSqliteConverter class with pagination for first page.
    """
    criteria = Criteria(page_size=10, page_number=1)
    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user')

    assert query == 'SELECT * FROM "user" LIMIT :limit_0 OFFSET :offset_1;'
    assert parameters == {'limit_0': 10, 'offset_1': 0}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_pagination_second_page() -> None:
    """
    Test CriteriaToSqliteConverter class with pagination for second page.
    """
    criteria = Criteria(page_size=10, page_number=2)
    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user')

    assert query == 'SELECT * FROM "user" LIMIT :limit_0 OFFSET :offset_1;'
    assert parameters == {'limit_0': 10, 'offset_1': 10}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_pagination_with_combined_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with pagination using combined criteria.
    """
    filter1 = Filter(field='active', operator=Operator.EQUAL, value=True)
    filter2 = Filter(field='age', operator=Operator.GREATER, value=18)

    criteria1 = Criteria(filters=[filter1], page_size=20, page_number=3)
    criteria2 = Criteria(filters=[filter2])

    combined_criteria = criteria1 & criteria2
    query, parameters = CriteriaToSqliteConverter.convert(criteria=combined_criteria, table='user')

    expected_offset = (3 - 1) * 20
    expected_query = (
        'SELECT * FROM "user" WHERE ("active" = :parameter_0 AND "age" > :parameter_1) LIMIT :limit_2 OFFSET :offset_3;'  # noqa: S608, E501
    )

    assert query == expected_query
    assert parameters == {'parameter_0': True, 'parameter_1': 18, 'limit_2': 20, 'offset_3': expected_offset}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_page_size_only() -> None:
    """
    Test CriteriaToSqliteConverter generates LIMIT without OFFSET when only page_size is provided.
    """
    page_size = IntegerMother.positive()
    criteria = Criteria(page_size=page_size)

    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user')

    expected_query = 'SELECT * FROM "user" LIMIT :limit_0;'

    assert query == expected_query
    assert parameters == {'limit_0': page_size}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_filters_and_page_size_only() -> None:
    """
    Test CriteriaToSqliteConverter with filters and LIMIT without OFFSET.
    """
    filter: Filter[Any] = FilterMother.create(operator=Operator.EQUAL)
    page_size = IntegerMother.positive()

    criteria = Criteria(filters=[filter], page_size=page_size)

    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user')

    expected_query = f'SELECT * FROM "user" WHERE "{filter.field}" = :parameter_0 LIMIT :limit_1;'  # noqa: S608

    assert query == expected_query
    assert parameters == {'parameter_0': filter.value, 'limit_1': page_size}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_orders_and_page_size_only() -> None:
    """
    Test CriteriaToSqliteConverter with orders and LIMIT without OFFSET.
    """
    order = OrderMother.create(direction=Direction.ASC)
    page_size = IntegerMother.positive()

    criteria = Criteria(orders=[order], page_size=page_size)

    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user')

    expected_query = f'SELECT * FROM "user" ORDER BY "{order.field}" ASC LIMIT :limit_0;'  # noqa: S608

    assert query == expected_query
    assert parameters == {'limit_0': page_size}
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_with_multiple_filters_in_same_criteria() -> None:
    """
    Test CriteriaToSqliteConverter class with multiple filters in the same Criteria object.
    This should produce AND conditions between filters.
    """
    filter1 = Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)
    filter2 = Filter(field='email', operator=Operator.ENDS_WITH, value='@gmail.com')

    criteria = Criteria(filters=[filter1, filter2])
    query, parameters = CriteriaToSqliteConverter.convert(criteria=criteria, table='user')

    expected_query = 'SELECT * FROM "user" WHERE "age" >= :parameter_0 AND "email" LIKE \'%\' || :parameter_1;'
    expected_parameters = {'parameter_0': 18, 'parameter_1': '@gmail.com'}

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_and_criteria_pagination_left_has_right_none() -> None:
    """
    Test CriteriaToSqliteConverter with AndCriteria where left has pagination, right has none.
    Should use left pagination.
    """
    left_criteria = Criteria(
        filters=[Filter(field='age', operator=Operator.GREATER, value=18)],
        page_size=10,
        page_number=2,
    )
    right_criteria = Criteria(filters=[Filter(field='status', operator=Operator.EQUAL, value='active')])

    and_criteria = left_criteria & right_criteria
    query, parameters = CriteriaToSqliteConverter.convert(criteria=and_criteria, table='user')

    expected_query = 'SELECT * FROM "user" WHERE ("age" > :parameter_0 AND "status" = :parameter_1) LIMIT :limit_2 OFFSET :offset_3;'  # noqa: E501  # fmt: skip
    expected_parameters = {'parameter_0': 18, 'parameter_1': 'active', 'limit_2': 10, 'offset_3': 10}

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_and_criteria_pagination_left_none_right_has() -> None:
    """
    Test CriteriaToSqliteConverter with AndCriteria where left has no pagination, right has pagination.
    Should fallback to right pagination (NEW BEHAVIOR).
    """
    left_criteria = Criteria(filters=[Filter(field='age', operator=Operator.GREATER, value=18)])
    right_criteria = Criteria(
        filters=[Filter(field='status', operator=Operator.EQUAL, value='active')],
        page_size=15,
        page_number=3,
    )

    and_criteria = left_criteria & right_criteria
    query, parameters = CriteriaToSqliteConverter.convert(criteria=and_criteria, table='user')

    expected_query = 'SELECT * FROM "user" WHERE ("age" > :parameter_0 AND "status" = :parameter_1) LIMIT :limit_2 OFFSET :offset_3;'  # noqa: E501  # fmt: skip
    expected_parameters = {'parameter_0': 18, 'parameter_1': 'active', 'limit_2': 15, 'offset_3': 30}

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_and_criteria_pagination_both_have() -> None:
    """
    Test CriteriaToSqliteConverter with AndCriteria where both have pagination.
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
    query, parameters = CriteriaToSqliteConverter.convert(criteria=and_criteria, table='user')

    expected_query = 'SELECT * FROM "user" WHERE ("age" > :parameter_0 AND "status" = :parameter_1) LIMIT :limit_2 OFFSET :offset_3;'  # noqa: E501  # fmt: skip
    expected_parameters = {'parameter_0': 18, 'parameter_1': 'active', 'limit_2': 10, 'offset_3': 10}

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_and_criteria_pagination_both_none() -> None:
    """
    Test CriteriaToSqliteConverter with AndCriteria where neither has pagination.
    Should have no pagination (existing behavior).
    """
    left_criteria = Criteria(filters=[Filter(field='age', operator=Operator.GREATER, value=18)])
    right_criteria = Criteria(filters=[Filter(field='status', operator=Operator.EQUAL, value='active')])

    and_criteria = left_criteria & right_criteria
    query, parameters = CriteriaToSqliteConverter.convert(criteria=and_criteria, table='user')

    expected_query = 'SELECT * FROM "user" WHERE ("age" > :parameter_0 AND "status" = :parameter_1);'
    expected_parameters = {'parameter_0': 18, 'parameter_1': 'active'}

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_or_criteria_pagination_left_has_right_none() -> None:
    """
    Test CriteriaToSqliteConverter with OrCriteria where left has pagination, right has none.
    Should use left pagination.
    """
    left_criteria = Criteria(
        filters=[Filter(field='age', operator=Operator.GREATER, value=18)],
        page_size=10,
        page_number=2,
    )
    right_criteria = Criteria(filters=[Filter(field='status', operator=Operator.EQUAL, value='active')])

    or_criteria = left_criteria | right_criteria
    query, parameters = CriteriaToSqliteConverter.convert(criteria=or_criteria, table='user')

    expected_query = 'SELECT * FROM "user" WHERE ("age" > :parameter_0 OR "status" = :parameter_1) LIMIT :limit_2 OFFSET :offset_3;'  # noqa: E501  # fmt: skip
    expected_parameters = {'parameter_0': 18, 'parameter_1': 'active', 'limit_2': 10, 'offset_3': 10}

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_sqlite_syntax(query=query)


@mark.unit_testing
def test_criteria_to_sqlite_converter_or_criteria_pagination_left_none_right_has() -> None:
    """
    Test CriteriaToSqliteConverter with OrCriteria where left has no pagination, right has pagination.
    Should fallback to right pagination (NEW BEHAVIOR).
    """
    left_criteria = Criteria(filters=[Filter(field='age', operator=Operator.GREATER, value=18)])
    right_criteria = Criteria(
        filters=[Filter(field='status', operator=Operator.EQUAL, value='active')],
        page_size=15,
        page_number=3,
    )

    or_criteria = left_criteria | right_criteria
    query, parameters = CriteriaToSqliteConverter.convert(criteria=or_criteria, table='user')

    expected_query = 'SELECT * FROM "user" WHERE ("age" > :parameter_0 OR "status" = :parameter_1) LIMIT :limit_2 OFFSET :offset_3;'  # noqa: E501  # fmt: skip
    expected_parameters = {'parameter_0': 18, 'parameter_1': 'active', 'limit_2': 15, 'offset_3': 30}

    assert query == expected_query
    assert parameters == expected_parameters
    assert_valid_sqlite_syntax(query=query)
