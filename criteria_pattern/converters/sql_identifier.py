"""
SQL identifier quoting helpers for dialect converters.
"""


def escape_backtick_identifier(*, identifier: str) -> str:
    """
    Escape a MySQL/MariaDB backtick-quoted identifier body.

    Args:
        identifier (str): Unquoted identifier text.

    Returns:
        str: Escaped identifier body without surrounding backticks.
    """
    return identifier.replace('`', '``')


def quote_backtick_identifier(*, identifier: str) -> str:
    """
    Quote a MySQL/MariaDB identifier.

    Args:
        identifier (str): Identifier to quote.

    Returns:
        str: Quoted identifier.
    """
    return f'`{escape_backtick_identifier(identifier=identifier)}`'


def quote_backtick_qualified_name(*, name: str) -> str:
    """
    Quote a schema-qualified MySQL/MariaDB name.

    Args:
        name (str): Qualified or unqualified table name.

    Returns:
        str: Quoted qualified name.
    """
    return '.'.join(quote_backtick_identifier(identifier=part) for part in name.split('.'))
