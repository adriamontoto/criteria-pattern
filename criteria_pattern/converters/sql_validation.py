"""
Shared SQL converter validation helpers.
"""

from collections.abc import Mapping, Sequence

from criteria_pattern import Criteria, Direction, Operator
from criteria_pattern.errors import (
    InvalidColumnError,
    InvalidDirectionError,
    InvalidOperatorError,
    InvalidTableError,
    PaginationBoundsError,
)


def resolve_sql_column(*, field: str, columns_mapping: Mapping[str, str]) -> str:
    """
    Resolve a criteria field to the SQL column used in generated queries.

    Args:
        field (str): Criteria field name.
        columns_mapping (Mapping[str, str]): Criteria field to SQL column mapping.

    Returns:
        str: SQL column name.
    """
    return columns_mapping.get(field, field)


def validate_table(*, table: str, valid_tables: Sequence[str]) -> None:
    """
    Validate the table name against an allowlist.

    Args:
        table (str): Name of the table to query.
        valid_tables (Sequence[str]): Allowed table names.

    Raises:
        InvalidTableError: If the table is not allowed.
    """
    if table not in valid_tables:
        raise InvalidTableError(table=table, valid_tables=valid_tables)


def validate_columns(
    *,
    columns: Sequence[str],
    columns_mapping: Mapping[str, str],
    valid_columns: Sequence[str],
) -> None:
    """
    Validate selected and mapped column names against an allowlist.

    Args:
        columns (Sequence[str]): Columns of the table to select.
        columns_mapping (Mapping[str, str]): Mapping of criteria fields to SQL columns.
        valid_columns (Sequence[str]): Allowed column names.

    Raises:
        InvalidColumnError: If a column is not allowed.
    """
    for column in columns:
        if column == '*':
            continue

        if column not in valid_columns:
            raise InvalidColumnError(column=column, valid_columns=valid_columns)

    for column in columns_mapping.values():
        if column not in valid_columns:
            raise InvalidColumnError(column=column, valid_columns=valid_columns)


def validate_criteria(
    *,
    criteria: Criteria,
    columns_mapping: Mapping[str, str],
    valid_columns: Sequence[str],
) -> None:
    """
    Validate criteria filter and order fields against an allowlist.

    Filter and order fields are validated after applying `columns_mapping`, so `valid_columns` must contain the SQL
    column names that will appear in the generated query.

    Args:
        criteria (Criteria): Criteria to validate.
        columns_mapping (Mapping[str, str]): Mapping of criteria fields to SQL columns.
        valid_columns (Sequence[str]): Allowed SQL column names.

    Raises:
        InvalidColumnError: If a resolved field maps to a column that is not allowed.
    """
    for filter in criteria.filters:
        column = resolve_sql_column(field=filter.field, columns_mapping=columns_mapping)
        if column not in valid_columns:
            raise InvalidColumnError(column=column, valid_columns=valid_columns)

    for order in criteria.orders:
        column = resolve_sql_column(field=order.field, columns_mapping=columns_mapping)
        if column not in valid_columns:
            raise InvalidColumnError(column=column, valid_columns=valid_columns)
