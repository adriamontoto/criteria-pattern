"""
MySQL SQL converter for Criteria objects.
"""

from collections.abc import Mapping, Sequence
from typing import Any, assert_never

from criteria_pattern import Criteria, Direction, Operator
from criteria_pattern.converters import sql_identifier, sql_validation
from criteria_pattern.errors import (
    InvalidColumnError,
    InvalidDirectionError,
    InvalidOperatorError,
    InvalidTableError,
    PaginationBoundsError,
)
from criteria_pattern.models.criteria import AndCriteria, NotCriteria, OrCriteria


class CriteriaToMysqlConverter:
    """
    Convert `Criteria` objects into MySQL `SELECT` statements.

    The converter preserves `AND`, `OR`, and `NOT` criteria composition and returns positional parameters for MySQL
    drivers that use `%s` placeholders. Allowlist checks are enabled by default through the `check_*_injection` flags.

    Example:
    ```python
    from criteria_pattern import Criteria, Filter, Operator
    from criteria_pattern.converters import CriteriaToMysqlConverter

    is_adult = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
    email_is_gmail = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@gmail.com')])
    email_is_yahoo = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@yahoo.com')])

    query, parameters = CriteriaToMysqlConverter.convert(criteria=is_adult & (email_is_gmail | email_is_yahoo), table='user')
    print(query)
    print(parameters)
    # >>> SELECT * FROM user WHERE (age >= %s AND (email LIKE CONCAT('%', %s) OR email LIKE CONCAT('%', %s)));
    # >>> [18, '@gmail.com', '@yahoo.com']
    ```
    """  # noqa: E501  # fmt: skip

    @classmethod
    def convert(  # noqa: C901
        cls,
        criteria: Criteria,
        table: str,
        columns: Sequence[str] | None = None,
        columns_mapping: Mapping[str, str] | None = None,
        check_table_injection: bool = True,
        check_column_injection: bool = True,
        check_criteria_injection: bool = True,
        check_operator_injection: bool = True,
        check_direction_injection: bool = True,
        check_pagination_bounds: bool = True,
        valid_tables: Sequence[str] | None = None,
        valid_columns: Sequence[str] | None = None,
        valid_operators: Sequence[Operator] | None = None,
        valid_directions: Sequence[Direction] | None = None,
        max_page_size: int = 10000,
        max_page_number: int = 1000000,
    ) -> tuple[str, list[Any]]:
        """
        Convert criteria into a MySQL query and positional parameters.

        Field names from filters and orders are resolved through `columns_mapping` before SQL is rendered. Validation
        flags only check values against the corresponding allowlists; callers should pass allowlists whenever accepting
        table, column, operator, direction, or pagination input from untrusted sources.

        Args:
            criteria (Criteria): Criteria to convert.
            table (str): Name of the table to query.
            columns (Sequence[str], optional): Columns to select. Defaults to `['*']`.
            columns_mapping (Mapping[str, str], optional): External field names mapped to SQL column names.
            check_criteria_injection (bool, optional): Validate filter and order fields against `valid_columns`.
            check_table_injection (bool, optional): Validate `table` against `valid_tables`.
            check_column_injection (bool, optional): Validate selected columns and mapped columns against
                `valid_columns`.
            check_operator_injection (bool, optional): Validate filter operators against `valid_operators`.
            check_direction_injection (bool, optional): Validate order directions against `valid_directions`.
            check_pagination_bounds (bool, optional): Validate page size and page number against configured maxima.
            valid_tables (Sequence[str], optional): Allowed table names.
            valid_columns (Sequence[str], optional): Allowed selectable and criteria column names.
            valid_operators (Sequence[Operator], optional): Allowed filter operators.
            valid_directions (Sequence[Direction], optional): Allowed order directions.
            max_page_size (int, optional): Maximum allowed page size when pagination validation is enabled.
            max_page_number (int, optional): Maximum allowed page number when pagination validation is enabled.

        Raises:
            InvalidTableError: If the table is not in the list of valid tables (only if check_table_injection=True).
            InvalidColumnError: If the column is not in the list of valid columns (only if check_column_injection=True).
            InvalidOperatorError: If the operator is not in the list of valid operators (only if check_operator_injection=True).
            InvalidDirectionError: If the direction is not in the list of valid directions (only if check_direction_injection=True).
            PaginationBoundsError: If pagination parameters exceed maximum bounds (only if check_pagination_bounds=True).

        Returns:
            tuple[str, list[Any]]: MySQL query string and positional query parameters.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator
        from criteria_pattern.converters import CriteriaToMysqlConverter

        is_adult = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
        email_is_gmail = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@gmail.com')])
        email_is_yahoo = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@yahoo.com')])

        query, parameters = CriteriaToMysqlConverter.convert(criteria=is_adult & (email_is_gmail | email_is_yahoo), table='user')
        print(query)
        print(parameters)
        # >>> SELECT * FROM user WHERE (age >= %s AND (email LIKE CONCAT('%', %s) OR email LIKE CONCAT('%', %s)));
        # >>> [18, '@gmail.com', '@yahoo.com']
        ```
        """  # noqa: E501  # fmt: skip
        columns = columns or ['*']
        columns_mapping = columns_mapping or {}
        valid_tables = valid_tables or []
        valid_columns = valid_columns or []
        valid_operators = valid_operators or []
        valid_directions = valid_directions or []

        if check_table_injection:
            cls._validate_table(table=table, valid_tables=valid_tables)

        if check_column_injection:
            cls._validate_columns(columns=columns, columns_mapping=columns_mapping, valid_columns=valid_columns)

        if check_criteria_injection:
            sql_validation.validate_criteria(
                criteria=criteria,
                columns_mapping=columns_mapping,
                valid_columns=valid_columns,
            )

        if check_operator_injection:
            cls._validate_operators(criteria=criteria, valid_operators=valid_operators)

        if check_direction_injection:
            cls._validate_directions(criteria=criteria, valid_directions=valid_directions)

        if check_pagination_bounds:
            cls._validate_pagination_bounds(
                criteria=criteria,
                max_page_size=max_page_size,
                max_page_number=max_page_number,
            )

        quoted_columns = [
            '*' if column == '*' else sql_identifier.quote_backtick_identifier(identifier=column) for column in columns
        ]
        quoted_table = sql_identifier.quote_backtick_qualified_name(name=table)
        query = f'SELECT {", ".join(quoted_columns)} FROM {quoted_table}'  # noqa: S608  # nosec
        parameters: list[Any] = []
        parameters_counter = 0

        if criteria.has_filters():
            where_clause, parameters = cls._process_filters(criteria=criteria, columns_mapping=columns_mapping)
            query += f' WHERE {where_clause}'
            parameters_counter = len(parameters)

        if criteria.has_orders():
            order_clause = cls._process_orders(criteria=criteria, columns_mapping=columns_mapping)
            query += f' ORDER BY {order_clause}'

        if criteria.has_page_size():
            parameters.append(criteria.page_size)
            query += ' LIMIT %s'
            parameters_counter += 1

        if criteria.has_pagination():
            offset_value = criteria.page_size * (criteria.page_number - 1)  # type: ignore[operator]
            parameters.append(offset_value)
            query += ' OFFSET %s'
            parameters_counter += 1

        return f'{query};', parameters

    @classmethod
    def _validate_table(cls, *, table: str, valid_tables: Sequence[str]) -> None:
        """
        Validate the table name to prevent SQL injection.

        Args:
            table (str): Name of the table to query.
            valid_tables (Sequence[str]): List of valid tables to query.

        Raises:
            InvalidTableError: If the table is not in the list of valid tables.
        """
        if table not in valid_tables:
            raise InvalidTableError(table=table, valid_tables=valid_tables)

    @classmethod
    def _validate_columns(
        cls,
        *,
        columns: Sequence[str],
        columns_mapping: Mapping[str, str],
        valid_columns: Sequence[str],
    ) -> None:
        """
        Validate the column names to prevent SQL injection.

        Args:
            columns (Sequence[str]): Columns of the table to select.
            columns_mapping (Mapping[str, str]): Mapping of column names to aliases.
            valid_columns (Sequence[str]): List of valid columns to select.

        Raises:
            InvalidColumnError: If the column is not in the list of valid columns.
        """
        for column in columns:
            if column not in valid_columns:
                raise InvalidColumnError(column=column, valid_columns=valid_columns)

        for column in columns_mapping.values():
            if column not in valid_columns:
                raise InvalidColumnError(column=column, valid_columns=valid_columns)

    @classmethod
    def _validate_operators(cls, *, criteria: Criteria, valid_operators: Sequence[Operator]) -> None:
        """
        Validate the Criteria object operators to prevent SQL injection.

        Args:
            criteria (Criteria): Criteria to validate.
            valid_operators (Sequence[Operator]): List of valid operators to use.

        Raises:
            InvalidOperatorError: If the operator is not in the list of valid operators.
        """
        for filter in criteria.filters:
            if filter.operator not in valid_operators:
                raise InvalidOperatorError(operator=Operator(value=filter.operator), valid_operators=valid_operators)

    @classmethod
    def _validate_directions(cls, *, criteria: Criteria, valid_directions: Sequence[Direction]) -> None:
        """
        Validate the Criteria object directions to prevent SQL injection.

        Args:
            criteria (Criteria): Criteria to validate.
            valid_directions (Sequence[Direction]): List of valid directions to use.

        Raises:
            InvalidDirectionError: If the direction is not in the list of valid directions.
        """
        for order in criteria.orders:
            if order.direction not in valid_directions:
                raise InvalidDirectionError(
                    direction=Direction(value=order.direction),
                    valid_directions=valid_directions,
                )

    @classmethod
    def _validate_pagination_bounds(cls, *, criteria: Criteria, max_page_size: int, max_page_number: int) -> None:
        """
        Validate the Criteria object pagination parameters to prevent integer overflow.

        Args:
            criteria (Criteria): Criteria to validate.
            max_page_size (int): Maximum allowed page_size.
            max_page_number (int): Maximum allowed page_number.

        Raises:
            PaginationBoundsError: If pagination parameters exceed maximum bounds.
        """
        if criteria.page_size is not None and criteria.page_size > max_page_size:
            raise PaginationBoundsError(parameter='page_size', value=criteria.page_size, max_value=max_page_size)

        if criteria.page_number is not None and criteria.page_number > max_page_number:
            raise PaginationBoundsError(parameter='page_number', value=criteria.page_number, max_value=max_page_number)

    @classmethod
    def _process_filters(cls, *, criteria: Criteria, columns_mapping: Mapping[str, str]) -> tuple[str, list[Any]]:
        """
        Process the Criteria object to return an SQL WHERE clause.

        Args:
            criteria (Criteria): Criteria to process.
            columns_mapping (Mapping[str, str]): Mapping of column names to aliases.

        Returns:
            tuple[str, list[Any]]: Processed filter string for SQL WHERE clause and parameters for the SQL query.
        """
        return cls._process_filters_recursive(criteria=criteria, columns_mapping=columns_mapping)

    @classmethod
    def _process_filters_recursive(  # noqa: C901
        cls,
        *,
        criteria: Criteria,
        columns_mapping: Mapping[str, str],
        parameters: list[Any] | None = None,
    ) -> tuple[str, list[Any]]:
        """
        Process the Criteria object to return an SQL WHERE clause.

        Args:
            criteria (Criteria): Criteria to process.
            columns_mapping (Mapping[str, str]): Mapping of column names to aliases.
            parameters (list[Any], optional): List to collect parameters. Default to empty list.

        Returns:
            tuple[str, list[Any]]: Processed filter string for SQL WHERE clause and parameters for the SQL query.
        """
        if parameters is None:
            parameters = []

        filters = ''

        if isinstance(criteria, AndCriteria):
            left_parameters: list[Any] = []
            left_conditions, left_parameters = cls._process_filters_recursive(
                criteria=criteria.left,
                columns_mapping=columns_mapping,
                parameters=left_parameters,
            )

            right_parameters: list[Any] = []
            right_conditions, right_parameters = cls._process_filters_recursive(
                criteria=criteria.right,
                columns_mapping=columns_mapping,
                parameters=right_parameters,
            )

            parameters.extend(left_parameters)
            parameters.extend(right_parameters)

            if left_conditions and right_conditions:
                filters += f'({left_conditions} AND {right_conditions})'

            elif left_conditions:
                filters += left_conditions

            elif right_conditions:
                filters += right_conditions

            return filters, parameters

        if isinstance(criteria, OrCriteria):
            left_parameters = []
            left_conditions, left_parameters = cls._process_filters_recursive(
                criteria=criteria.left,
                columns_mapping=columns_mapping,
                parameters=left_parameters,
            )

            right_parameters = []
            right_conditions, right_parameters = cls._process_filters_recursive(
                criteria=criteria.right,
                columns_mapping=columns_mapping,
                parameters=right_parameters,
            )

            parameters.extend(left_parameters)
            parameters.extend(right_parameters)

            if left_conditions and right_conditions:
                filters += f'({left_conditions} OR {right_conditions})'

            elif left_conditions:
                filters += left_conditions

            elif right_conditions:
                filters += right_conditions

            return filters, parameters

        if isinstance(criteria, NotCriteria):
            not_parameters: list[Any] = []
            not_conditions, not_parameters = cls._process_filters_recursive(
                criteria=criteria.criteria,
                columns_mapping=columns_mapping,
                parameters=not_parameters,
            )

            parameters.extend(not_parameters)

            if not_conditions:
                filters += f'NOT ({not_conditions})'

            return filters, parameters

        filter_conditions = []
        for filter in criteria.filters:
            filter_field = sql_validation.resolve_sql_column(field=filter.field, columns_mapping=columns_mapping)
            quoted_filter_field = sql_identifier.quote_backtick_identifier(identifier=filter_field)
            placeholder = '%s'

            operator = Operator(value=filter.operator)
            match operator:
                case Operator.EQUAL:
                    filter_conditions.append(f'{quoted_filter_field} = {placeholder}')
                    parameters.append(filter.value)

                case Operator.NOT_EQUAL:
                    filter_conditions.append(f'{quoted_filter_field} != {placeholder}')
                    parameters.append(filter.value)

                case Operator.GREATER:
                    filter_conditions.append(f'{quoted_filter_field} > {placeholder}')
                    parameters.append(filter.value)

                case Operator.GREATER_OR_EQUAL:
                    filter_conditions.append(f'{quoted_filter_field} >= {placeholder}')
                    parameters.append(filter.value)

                case Operator.LESS:
                    filter_conditions.append(f'{quoted_filter_field} < {placeholder}')
                    parameters.append(filter.value)

                case Operator.LESS_OR_EQUAL:
                    filter_conditions.append(f'{quoted_filter_field} <= {placeholder}')
                    parameters.append(filter.value)

                case Operator.LIKE:
                    filter_conditions.append(f'{quoted_filter_field} LIKE {placeholder}')
                    parameters.append(filter.value)

                case Operator.NOT_LIKE:
                    filter_conditions.append(f'{quoted_filter_field} NOT LIKE {placeholder}')
                    parameters.append(filter.value)

                case Operator.CONTAINS:
                    filter_conditions.append(f"{quoted_filter_field} LIKE CONCAT('%', {placeholder}, '%')")
                    parameters.append(filter.value)

                case Operator.NOT_CONTAINS:
                    filter_conditions.append(f"{quoted_filter_field} NOT LIKE CONCAT('%', {placeholder}, '%')")
                    parameters.append(filter.value)

                case Operator.STARTS_WITH:
                    filter_conditions.append(f"{quoted_filter_field} LIKE CONCAT({placeholder}, '%')")
                    parameters.append(filter.value)

                case Operator.NOT_STARTS_WITH:
                    filter_conditions.append(f"{quoted_filter_field} NOT LIKE CONCAT({placeholder}, '%')")
                    parameters.append(filter.value)

                case Operator.ENDS_WITH:
                    filter_conditions.append(f"{quoted_filter_field} LIKE CONCAT('%', {placeholder})")
                    parameters.append(filter.value)

                case Operator.NOT_ENDS_WITH:
                    filter_conditions.append(f"{quoted_filter_field} NOT LIKE CONCAT('%', {placeholder})")
                    parameters.append(filter.value)

                case Operator.BETWEEN:
                    start_placeholder = '%s'
                    end_placeholder = '%s'
                    parameters.append(filter.value[0])
                    parameters.append(filter.value[1])
                    filter_conditions.append(f'{quoted_filter_field} BETWEEN {start_placeholder} AND {end_placeholder}')

                case Operator.NOT_BETWEEN:
                    start_placeholder = '%s'
                    end_placeholder = '%s'
                    parameters.append(filter.value[0])
                    parameters.append(filter.value[1])
                    filter_conditions.append(f'{quoted_filter_field} NOT BETWEEN {start_placeholder} AND {end_placeholder}')

                case Operator.IS_NULL:
                    filter_conditions.append(f'{quoted_filter_field} IS NULL')

                case Operator.IS_NOT_NULL:
                    filter_conditions.append(f'{quoted_filter_field} IS NOT NULL')

                case Operator.IN:
                    values = filter.value
                    placeholders: list[str] = []
                    for value in values:
                        parameters.append(value)
                        placeholders.append('%s')
                    filter_conditions.append(f'{quoted_filter_field} IN ({", ".join(placeholders)})')

                case Operator.NOT_IN:
                    values = filter.value
                    placeholders_not_in: list[str] = []
                    for value in values:
                        parameters.append(value)
                        placeholders_not_in.append('%s')
                    filter_conditions.append(f'{quoted_filter_field} NOT IN ({", ".join(placeholders_not_in)})')

                case _:  # pragma: no cover
                    assert_never(operator)

        filters = ' AND '.join(filter_conditions)

        return filters, parameters

    @classmethod
    def _process_orders(cls, *, criteria: Criteria, columns_mapping: Mapping[str, str]) -> str:
        """
        Process the Criteria object to return an SQL ORDER BY clause.

        Args:
            criteria (Criteria): Criteria to process.
            columns_mapping (Mapping[str, str]): Mapping of column names to aliases.

        Returns:
            str: Processed order string for SQL ORDER BY clause.
        """
        orders = ''

        for order in criteria.orders:
            order_field = sql_validation.resolve_sql_column(field=order.field, columns_mapping=columns_mapping)
            quoted_order_field = sql_identifier.quote_backtick_identifier(identifier=order_field)

            direction = Direction(value=order.direction)
            match direction:
                case Direction.ASC:
                    orders += f'{quoted_order_field} ASC, '

                case Direction.DESC:
                    orders += f'{quoted_order_field} DESC, '

                case _:  # pragma: no cover
                    assert_never(direction)

        return orders.rstrip(', ')
