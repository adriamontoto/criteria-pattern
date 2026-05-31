"""
Test SQL identifier quoting helpers.
"""

from pytest import mark

from criteria_pattern.converters.sql_identifier import quote_backtick_identifier


@mark.unit_testing
def test_quote_backtick_identifier_escapes_embedded_backticks() -> None:
    """
    Test MySQL/MariaDB identifiers escape embedded backticks.
    """
    assert quote_backtick_identifier(identifier='id` OR 1=1 --') == '`id`` OR 1=1 --`'
