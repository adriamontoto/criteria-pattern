"""
Criteria to MySQL converter module.
"""

from collections.abc import Mapping, Sequence
from typing import Any, assert_never

from criteria_pattern import Criteria, Direction, Operator
from criteria_pattern.errors import InvalidColumnError, InvalidTableError
from criteria_pattern.models.criteria import AndCriteria, NotCriteria, OrCriteria


class CriteriaToMysqlConverter:
    """
    Criteria to MySQL converter.

    Example:
    ```python
    from criteria_pattern import Criteria, Filter, Operator
    from criteria_pattern.converter import CriteriaToMysqlConverter

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
    def convert(
        cls,
        criteria: Criteria,
        table: str,
        columns: Sequence[str] | None = None,
        columns_mapping: Mapping[str, str] | None = None,
        check_table_injection: bool = False,
        check_column_injection: bool = False,
        check_criteria_injection: bool = False,
        valid_tables: Sequence[str] | None = None,
        valid_columns: Sequence[str] | None = None,
    ) -> tuple[str, list[Any]]:
        """
        Convert the Criteria object to a MySQL query.

        Args:
            criteria (Criteria): Criteria to convert.
            table (str): Name of the table to query.
            columns (Sequence[str], optional): Columns of the table to select. Default to *.
            columns_mapping (Mapping[str, str], optional): Mapping of column names to aliases. Default to empty dict.
            check_criteria_injection (bool, optional): Raise an error if the criteria field is not in the list of valid
            columns. Default to False.
            check_table_injection (bool, optional): Raise an error if the table is not in the list of valid tables.
            Default to False.
            check_column_injection (bool, optional): Raise an error if the column is not in the list of valid columns.
            Default to False.
            valid_tables (Sequence[str], optional): List of valid tables to query. Default to empty list.
            valid_columns (Sequence[str], optional): List of valid columns to select. Default to empty list.

        Raises:
            InvalidTableError: If the table is not in the list of valid tables (only if check_table_injection=True).
            InvalidColumnError: If the column is not in the list of valid columns (only if check_column_injection=True).

        Returns:
            tuple[str, list[Any]]: The MySQL query string and the query parameters as a list.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator
        from criteria_pattern.converter import CriteriaToMysqlConverter

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

        if check_table_injection:
            cls._validate_table(table=table, valid_tables=valid_tables)

        if check_column_injection:
            cls._validate_columns(columns=columns, columns_mapping=columns_mapping, valid_columns=valid_columns)

        if check_criteria_injection:
            cls._validate_criteria(criteria=criteria, valid_columns=valid_columns)

        query = f'SELECT {", ".join(columns)} FROM {table}'  # noqa: S608  # nosec
        parameters: list[Any] = []

        if criteria.has_filters():
            where_clause, parameters = cls._process_filters(criteria=criteria, columns_mapping=columns_mapping)
            query += f' WHERE {where_clause}'

        if criteria.has_orders():
            order_clause = cls._process_orders(criteria=criteria, columns_mapping=columns_mapping)
            query += f' ORDER BY {order_clause}'

        if criteria.has_page_size():
            query += f' LIMIT {criteria.page_size}'

        if criteria.has_pagination():
            query += f' OFFSET {criteria.page_size * (criteria.page_number - 1)}'  # type: ignore[operator]

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
    def _validate_criteria(cls, *, criteria: Criteria, valid_columns: Sequence[str]) -> None:
        """
        Validate the Criteria object to prevent SQL injection.

        Args:
            criteria (Criteria): Criteria to validate.
            valid_columns (Sequence[str]): List of valid columns to select.

        Raises:
            InvalidColumnError: If the column is not in the list of valid columns.
        """
        for filter in criteria.filters:
            if filter.field not in valid_columns:
                raise InvalidColumnError(column=filter.field, valid_columns=valid_columns)

        for order in criteria.orders:
            if order.field not in valid_columns:
                raise InvalidColumnError(column=order.field, valid_columns=valid_columns)

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

            filters += f'({left_conditions} AND {right_conditions})'

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

            filters += f'({left_conditions} OR {right_conditions})'

            return filters, parameters

        if isinstance(criteria, NotCriteria):
            not_parameters: list[Any] = []
            not_conditions, not_parameters = cls._process_filters_recursive(
                criteria=criteria.criteria,
                columns_mapping=columns_mapping,
                parameters=not_parameters,
            )

            parameters.extend(not_parameters)

            filters += f'NOT ({not_conditions})'

            return filters, parameters

        for filter in criteria.filters:
            filter_field = columns_mapping.get(filter.field, filter.field)
            placeholder = '%s'

            operator = Operator(value=filter.operator)
            match operator:
                case Operator.EQUAL:
                    filters += f'{filter_field} = {placeholder}'
                    parameters.append(filter.value)

                case Operator.NOT_EQUAL:
                    filters += f'{filter_field} != {placeholder}'
                    parameters.append(filter.value)

                case Operator.GREATER:
                    filters += f'{filter_field} > {placeholder}'
                    parameters.append(filter.value)

                case Operator.GREATER_OR_EQUAL:
                    filters += f'{filter_field} >= {placeholder}'
                    parameters.append(filter.value)

                case Operator.LESS:
                    filters += f'{filter_field} < {placeholder}'
                    parameters.append(filter.value)

                case Operator.LESS_OR_EQUAL:
                    filters += f'{filter_field} <= {placeholder}'
                    parameters.append(filter.value)

                case Operator.LIKE:
                    filters += f'{filter_field} LIKE {placeholder}'
                    parameters.append(filter.value)

                case Operator.NOT_LIKE:
                    filters += f'{filter_field} NOT LIKE {placeholder}'
                    parameters.append(filter.value)

                case Operator.CONTAINS:
                    filters += f"{filter_field} LIKE CONCAT('%', {placeholder}, '%')"
                    parameters.append(filter.value)

                case Operator.NOT_CONTAINS:
                    filters += f"{filter_field} NOT LIKE CONCAT('%', {placeholder}, '%')"
                    parameters.append(filter.value)

                case Operator.STARTS_WITH:
                    filters += f"{filter_field} LIKE CONCAT({placeholder}, '%')"
                    parameters.append(filter.value)

                case Operator.NOT_STARTS_WITH:
                    filters += f"{filter_field} NOT LIKE CONCAT({placeholder}, '%')"
                    parameters.append(filter.value)

                case Operator.ENDS_WITH:
                    filters += f"{filter_field} LIKE CONCAT('%', {placeholder})"
                    parameters.append(filter.value)

                case Operator.NOT_ENDS_WITH:
                    filters += f"{filter_field} NOT LIKE CONCAT('%', {placeholder})"
                    parameters.append(filter.value)

                case Operator.BETWEEN:
                    start_placeholder = '%s'
                    end_placeholder = '%s'
                    parameters.append(filter.value[0])
                    parameters.append(filter.value[1])
                    filters += f'{filter_field} BETWEEN {start_placeholder} AND {end_placeholder}'

                case Operator.NOT_BETWEEN:
                    start_placeholder = '%s'
                    end_placeholder = '%s'
                    parameters.append(filter.value[0])
                    parameters.append(filter.value[1])
                    filters += f'{filter_field} NOT BETWEEN {start_placeholder} AND {end_placeholder}'

                case Operator.IS_NULL:
                    filters += f'{filter_field} IS NULL'

                case Operator.IS_NOT_NULL:
                    filters += f'{filter_field} IS NOT NULL'

                case Operator.IN:
                    values = filter.value
                    placeholders: list[str] = []
                    for value in values:
                        parameters.append(value)
                        placeholders.append('%s')
                    filters += f'{filter_field} IN ({", ".join(placeholders)})'

                case Operator.NOT_IN:
                    values = filter.value
                    placeholders_not_in: list[str] = []
                    for value in values:
                        parameters.append(value)
                        placeholders_not_in.append('%s')
                    filters += f'{filter_field} NOT IN ({", ".join(placeholders_not_in)})'

                case _:  # pragma: no cover
                    assert_never(operator)

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
            order_field = columns_mapping.get(order.field, order.field)

            direction = Direction(value=order.direction)
            match direction:
                case Direction.ASC:
                    orders += f'{order_field} ASC, '

                case Direction.DESC:
                    orders += f'{order_field} DESC, '

                case _:  # pragma: no cover
                    assert_never(direction)

        return orders.rstrip(', ')
