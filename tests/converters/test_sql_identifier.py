"""
Test SQL identifier quoting helpers.
"""

from pytest import mark

from criteria_pattern import Criteria, Filter, Operator
from criteria_pattern.converters.criteria_to_mysql_converter import CriteriaToMysqlConverter
from criteria_pattern.converters.criteria_to_postgresql_converter import CriteriaToPostgresqlConverter
from criteria_pattern.converters.criteria_to_sqlite_converter import CriteriaToSqliteConverter


@mark.unit_testing
def test_quote_backtick_identifier_escapes_embedded_backticks() -> None:
    """
    Test MySQL/MariaDB identifiers escape embedded backticks.
    """
    assert CriteriaToMysqlConverter._quote_backtick_identifier(identifier='id` OR 1=1 --') == '`id`` OR 1=1 --`'


@mark.unit_testing
def test_quote_double_quoted_identifier_escapes_embedded_quotes() -> None:
    """
    Test PostgreSQL/SQLite identifiers escape embedded double quotes.
    """
    assert (
        CriteriaToPostgresqlConverter._quote_double_quoted_identifier(identifier='id" OR 1=1 --') == '"id"" OR 1=1 --"'
    )


@mark.unit_testing
def test_postgresql_convert_escapes_embedded_double_quotes_in_generated_sql() -> None:
    """
    Test PostgreSQL converter escapes double quotes in identifiers used in generated SQL.
    """
    malicious = 'id" OR 1=1 --'
    criteria = Criteria(filters=[Filter(field=malicious, operator=Operator.EQUAL, value=1)])

    query, _ = CriteriaToPostgresqlConverter.convert(
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

    assert query == 'SELECT "id"" OR 1=1 --" FROM "id"" OR 1=1 --" WHERE "id"" OR 1=1 --" = %(parameter_0)s;'


@mark.unit_testing
def test_sqlite_convert_escapes_embedded_double_quotes_in_generated_sql() -> None:
    """
    Test SQLite converter escapes double quotes in identifiers used in generated SQL.
    """
    malicious = 'id" OR 1=1 --'
    criteria = Criteria(filters=[Filter(field=malicious, operator=Operator.EQUAL, value=1)])

    query, _ = CriteriaToSqliteConverter.convert(
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

    assert query == 'SELECT "id"" OR 1=1 --" FROM "id"" OR 1=1 --" WHERE "id"" OR 1=1 --" = :parameter_0;'
