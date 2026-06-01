"""
PostgreSQL SQL converter for Criteria objects.
"""

from collections.abc import Iterator, Mapping, Sequence
from typing import Any, assert_never

from criteria_pattern import Criteria, Direction, Operator
from criteria_pattern.errors import (
    IntegrityError,
    InvalidColumnError,
    InvalidDirectionError,
    InvalidOperatorError,
    InvalidTableError,
    PaginationBoundsError,
)
from criteria_pattern.models.criteria import AndCriteria, NotCriteria, OrCriteria


class CriteriaToPostgresqlConverter:
    """
    Convert `Criteria` objects into PostgreSQL `SELECT` statements.

    The converter preserves `AND`, `OR`, and `NOT` criteria composition, quotes selected columns and table identifiers,
    and returns named parameters suitable for PostgreSQL drivers that support `%(name)s` placeholders. Allowlist checks
    are enabled by default through the `check_*_injection` flags.

    Example:
    ```python
    from criteria_pattern import Criteria, Filter, Operator
    from criteria_pattern.converters import CriteriaToPostgresqlConverter

    is_adult = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
    email_is_gmail = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@gmail.com')])
    email_is_yahoo = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@yahoo.com')])

    query, parameters = CriteriaToPostgresqlConverter.convert(
        criteria=is_adult & (email_is_gmail | email_is_yahoo),
        table='user',
        valid_columns=['age', 'email'],
        valid_operators=[Operator.GREATER_OR_EQUAL, Operator.ENDS_WITH],
    )
    print(query)
    print(parameters)
    # >>> SELECT * FROM "user" WHERE ("age" >= %(parameter_0)s AND ("email" LIKE '%%' || %(parameter_1)s OR "email" LIKE '%%' || %(parameter_2)s));
    # >>> {'parameter_0': 18, 'parameter_1': '@gmail.com', 'parameter_2': '@yahoo.com'}
    ```
    """  # noqa: E501  # fmt: skip

    DEFAULT_MAX_CRITERIA_COMPOSITION_DEPTH = 32
    DEFAULT_MAX_IN_VALUES = 100
    DEFAULT_MAX_PAGE_SIZE = 1000
    DEFAULT_MAX_PAGE_NUMBER = 10000
    DEFAULT_MAX_OPERATOR_ALLOWLIST = len(Operator)
    LIKE_VALUE_OPERATORS = frozenset(
        {
            Operator.LIKE,
            Operator.NOT_LIKE,
            Operator.CONTAINS,
            Operator.NOT_CONTAINS,
            Operator.STARTS_WITH,
            Operator.NOT_STARTS_WITH,
            Operator.ENDS_WITH,
            Operator.NOT_ENDS_WITH,
        }
    )
    SQL_LIKE_ESCAPE_CLAUSE = " ESCAPE '\\'"

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
        max_page_size: int = DEFAULT_MAX_PAGE_SIZE,
        max_page_number: int = DEFAULT_MAX_PAGE_NUMBER,
        max_criteria_depth: int = DEFAULT_MAX_CRITERIA_COMPOSITION_DEPTH,
        max_in_values: int = DEFAULT_MAX_IN_VALUES,
        max_operator_allowlist: int = DEFAULT_MAX_OPERATOR_ALLOWLIST,
    ) -> tuple[str, dict[str, Any]]:
        """
        Convert criteria into a PostgreSQL query and parameter mapping.

        Filter values are parameterized. Validation is on by default. Each `valid_*` allowlist is complete; omitting it
        or passing `[]` denies that dimension. Omitted `valid_tables` allows only the `table` argument.

        Args:
            criteria (Criteria): Criteria to convert.
            table (str): Table to query.
            columns (Sequence[str], optional): Selected columns. Default `['*']` (`'*'` skips column allowlist check).
            columns_mapping (Mapping[str, str], optional): Criteria field to SQL column names.
            check_table_injection (bool, optional): Validate `table` against `valid_tables`. Default `True`.
            check_column_injection (bool, optional): Validate `columns` and mapping targets. Default `True`.
            check_criteria_injection (bool, optional): Validate criteria fields after mapping. Default `True`.
            check_operator_injection (bool, optional): Validate operators against `valid_operators`. Default `True`.
            check_direction_injection (bool, optional): Validate directions against `valid_directions`. Default `True`.
            check_pagination_bounds (bool, optional): Cap criteria pagination. Default `True`.
            valid_tables (Sequence[str], optional): Allowed tables; omitted allows only `table`.
            valid_columns (Sequence[str], optional): Allowed columns and criteria fields; omitted or `[]` allows none.
            valid_operators (Sequence[Operator], optional): Allowed operators; omitted or `[]` allows none.
            valid_directions (Sequence[Direction], optional): Allowed directions; omitted or `[]` allows none.
            max_page_size (int, optional): Max `criteria.page_size`. Default `1000`.
            max_page_number (int, optional): Max `criteria.page_number`. Default `10000`.
            max_criteria_depth (int, optional): Max `AND` / `OR` / `NOT` nesting depth. Default `32`.
            max_in_values (int, optional): Max values per `IN` / `NOT_IN` list. Default `100`.
            max_operator_allowlist (int, optional): Max size of `valid_operators` when set. Default `len(Operator)`.

        Raises:
            IntegrityError: Limit exceeded (`max_criteria_depth`, `max_in_values`, `max_operator_allowlist`).
            InvalidTableError: Table not allowed when `check_table_injection` is enabled.
            InvalidColumnError: Column or field not allowed when column/criteria checks are enabled.
            InvalidOperatorError: Operator not allowed when `check_operator_injection` is enabled.
            InvalidDirectionError: Direction not allowed when `check_direction_injection` is enabled.
            PaginationBoundsError: Pagination above maxima when `check_pagination_bounds` is enabled.

        Returns:
            tuple[str, dict[str, Any]]: PostgreSQL query string and named query parameters.

        Example:
        ```python
        from criteria_pattern import Criteria, Filter, Operator
        from criteria_pattern.converters import CriteriaToPostgresqlConverter

        is_adult = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
        email_is_gmail = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@gmail.com')])
        email_is_yahoo = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@yahoo.com')])

        query, parameters = CriteriaToPostgresqlConverter.convert(
            criteria=is_adult & (email_is_gmail | email_is_yahoo),
            table='user',
            valid_columns=['age', 'email'],
            valid_operators=[Operator.GREATER_OR_EQUAL, Operator.ENDS_WITH],
        )
        print(query)
        print(parameters)
        # >>> SELECT * FROM "user" WHERE ("age" >= %(parameter_0)s AND ("email" LIKE '%%' || %(parameter_1)s OR "email" LIKE '%%' || %(parameter_2)s));
        # >>> {'parameter_0': 18, 'parameter_1': '@gmail.com', 'parameter_2': '@yahoo.com'}
        ```
        """  # noqa: E501  # fmt: skip
        columns = columns or ['*']
        columns_mapping = columns_mapping or {}
        cls._validate_criteria_bounds(
            criteria=criteria,
            max_criteria_depth=max_criteria_depth,
            max_in_values=max_in_values,
        )
        if check_operator_injection and valid_operators is not None:
            cls._ensure_operator_allowlist_size(
                operators=valid_operators,
                limit=max_operator_allowlist,
            )
        if check_table_injection:
            cls._validate_table(
                table=table,
                valid_tables=list(valid_tables) if valid_tables is not None else [table],
            )

        if check_column_injection:
            cls._validate_columns(
                columns=columns,
                columns_mapping=columns_mapping,
                valid_columns=list(valid_columns) if valid_columns is not None else [],
            )

        if check_criteria_injection:
            cls._validate_criteria(
                criteria=criteria,
                columns_mapping=columns_mapping,
                valid_columns=list(valid_columns) if valid_columns is not None else [],
            )

        if check_operator_injection:
            cls._validate_operators(
                criteria=criteria,
                valid_operators=list(valid_operators) if valid_operators is not None else [],
            )

        if check_direction_injection:
            cls._validate_directions(
                criteria=criteria,
                valid_directions=list(valid_directions) if valid_directions is not None else [],
            )

        if check_pagination_bounds:
            cls._validate_pagination_bounds(
                criteria=criteria,
                max_page_size=max_page_size,
                max_page_number=max_page_number,
            )

        quoted_columns = [
            '*' if column == '*' else cls._quote_double_quoted_identifier(identifier=column) for column in columns
        ]
        quoted_table = cls._quote_double_quoted_qualified_name(name=table)
        query = f'SELECT {", ".join(quoted_columns)} FROM {quoted_table}'  # noqa: S608  # nosec
        parameters: dict[str, Any] = {}
        parameters_counter = 0

        if criteria.has_filters():
            where_clause, parameters = cls._process_filters(criteria=criteria, columns_mapping=columns_mapping)
            query += f' WHERE {where_clause}'
            parameters_counter = len(parameters)

        if criteria.has_orders():
            order_clause = cls._process_orders(criteria=criteria, columns_mapping=columns_mapping)
            query += f' ORDER BY {order_clause}'

        if criteria.has_page_size():
            limit_parameter = f'limit_{parameters_counter}'
            parameters[limit_parameter] = criteria.page_size
            query += f' LIMIT %({limit_parameter})s'
            parameters_counter += 1

        if criteria.has_pagination():
            offset_parameter = f'offset_{parameters_counter}'
            offset_value = criteria.page_size * (criteria.page_number - 1)  # type: ignore[operator]
            parameters[offset_parameter] = offset_value
            query += f' OFFSET %({offset_parameter})s'
            parameters_counter += 1

        return f'{query};', parameters

    @classmethod
    def _process_filters(cls, *, criteria: Criteria, columns_mapping: Mapping[str, str]) -> tuple[str, dict[str, Any]]:
        """
        Process the Criteria object to return an SQL WHERE clause.

        Args:
            criteria (Criteria): Criteria to process.
            columns_mapping (Mapping[str, str]): Mapping of column names to aliases.

        Returns:
            tuple[str, dict[str, Any]]: Processed filter string for SQL WHERE clause and parameters for the SQL query.
        """
        return cls._process_filters_recursive(criteria=criteria, columns_mapping=columns_mapping)

    @classmethod
    def _process_filters_recursive(  # noqa: C901
        cls,
        *,
        criteria: Criteria,
        columns_mapping: Mapping[str, str],
        parameters_counter: int = 0,
    ) -> tuple[str, dict[str, Any]]:
        """
        Process the Criteria object to return an SQL WHERE clause.

        Args:
            criteria (Criteria): Criteria to process.
            columns_mapping (Mapping[str, str]): Mapping of column names to aliases.
            parameters_counter (int): Counter for parameter names to ensure uniqueness.

        Returns:
            tuple[str, dict[str, Any]]: Processed filter string for SQL WHERE clause and parameters for the SQL query.
        """
        filters = ''
        parameters: dict[str, Any] = {}

        if isinstance(criteria, AndCriteria):
            left_conditions, left_parameters = cls._process_filters_recursive(
                criteria=criteria.left,
                columns_mapping=columns_mapping,
                parameters_counter=parameters_counter,
            )
            parameters_counter += len(left_parameters)
            parameters.update(left_parameters)

            right_conditions, right_parameters = cls._process_filters_recursive(
                criteria=criteria.right,
                columns_mapping=columns_mapping,
                parameters_counter=parameters_counter,
            )
            parameters_counter += len(right_parameters)
            parameters.update(right_parameters)

            if left_conditions and right_conditions:
                filters += f'({left_conditions} AND {right_conditions})'

            elif left_conditions:
                filters += left_conditions

            elif right_conditions:
                filters += right_conditions

            return filters, parameters

        if isinstance(criteria, OrCriteria):
            left_conditions, left_parameters = cls._process_filters_recursive(
                criteria=criteria.left,
                columns_mapping=columns_mapping,
                parameters_counter=parameters_counter,
            )
            parameters_counter += len(left_parameters)
            parameters.update(left_parameters)

            right_conditions, right_parameters = cls._process_filters_recursive(
                criteria=criteria.right,
                columns_mapping=columns_mapping,
                parameters_counter=parameters_counter,
            )
            parameters_counter += len(right_parameters)
            parameters.update(right_parameters)

            if left_conditions and right_conditions:
                filters += f'({left_conditions} OR {right_conditions})'

            elif left_conditions:
                filters += left_conditions

            elif right_conditions:
                filters += right_conditions

            return filters, parameters

        if isinstance(criteria, NotCriteria):
            not_conditions, not_parameters = cls._process_filters_recursive(
                criteria=criteria.criteria,
                columns_mapping=columns_mapping,
                parameters_counter=parameters_counter,
            )
            parameters_counter += len(not_parameters)
            parameters.update(not_parameters)

            if not_conditions:
                filters += f'NOT ({not_conditions})'

            return filters, parameters

        filter_conditions = []
        for filter in criteria.filters:
            filter_field = cls._resolve_sql_column(field=filter.field, columns_mapping=columns_mapping)
            quoted_filter_field = cls._quote_double_quoted_identifier(identifier=filter_field)
            operator = Operator(value=filter.operator)
            parameter_name = f'parameter_{parameters_counter}'
            parameter_value = (
                cls._escape_like_pattern_value(value=filter.value)
                if operator in cls.LIKE_VALUE_OPERATORS
                else filter.value
            )
            parameters[parameter_name] = parameter_value
            placeholder = f'%({parameter_name})s'
            parameters_counter += 1

            match operator:
                case Operator.EQUAL:
                    filter_conditions.append(f'{quoted_filter_field} = {placeholder}')

                case Operator.NOT_EQUAL:
                    filter_conditions.append(f'{quoted_filter_field} != {placeholder}')

                case Operator.GREATER:
                    filter_conditions.append(f'{quoted_filter_field} > {placeholder}')

                case Operator.GREATER_OR_EQUAL:
                    filter_conditions.append(f'{quoted_filter_field} >= {placeholder}')

                case Operator.LESS:
                    filter_conditions.append(f'{quoted_filter_field} < {placeholder}')

                case Operator.LESS_OR_EQUAL:
                    filter_conditions.append(f'{quoted_filter_field} <= {placeholder}')

                case Operator.LIKE:
                    filter_conditions.append(f'{quoted_filter_field} LIKE {placeholder}{cls.SQL_LIKE_ESCAPE_CLAUSE}')

                case Operator.NOT_LIKE:
                    filter_conditions.append(
                        f'{quoted_filter_field} NOT LIKE {placeholder}{cls.SQL_LIKE_ESCAPE_CLAUSE}'
                    )

                case Operator.CONTAINS:
                    filter_conditions.append(
                        f"{quoted_filter_field} LIKE '%%' || {placeholder} || '%%'{cls.SQL_LIKE_ESCAPE_CLAUSE}"
                    )

                case Operator.NOT_CONTAINS:
                    filter_conditions.append(
                        f"{quoted_filter_field} NOT LIKE '%%' || {placeholder} || '%%'{cls.SQL_LIKE_ESCAPE_CLAUSE}"
                    )

                case Operator.STARTS_WITH:
                    filter_conditions.append(
                        f"{quoted_filter_field} LIKE {placeholder} || '%%'{cls.SQL_LIKE_ESCAPE_CLAUSE}"
                    )

                case Operator.NOT_STARTS_WITH:
                    filter_conditions.append(
                        f"{quoted_filter_field} NOT LIKE {placeholder} || '%%'{cls.SQL_LIKE_ESCAPE_CLAUSE}"
                    )

                case Operator.ENDS_WITH:
                    filter_conditions.append(
                        f"{quoted_filter_field} LIKE '%%' || {placeholder}{cls.SQL_LIKE_ESCAPE_CLAUSE}"
                    )

                case Operator.NOT_ENDS_WITH:
                    filter_conditions.append(
                        f"{quoted_filter_field} NOT LIKE '%%' || {placeholder}{cls.SQL_LIKE_ESCAPE_CLAUSE}"
                    )

                case Operator.BETWEEN:
                    parameters.pop(parameter_name)
                    parameters_counter -= 1

                    start_parameter_name = f'parameter_{parameters_counter}'
                    end_parameter_name = f'parameter_{parameters_counter + 1}'
                    parameters[start_parameter_name] = filter.value[0]
                    parameters[end_parameter_name] = filter.value[1]
                    start_placeholder = f'%({start_parameter_name})s'
                    end_placeholder = f'%({end_parameter_name})s'
                    parameters_counter += 2

                    filter_conditions.append(f'{quoted_filter_field} BETWEEN {start_placeholder} AND {end_placeholder}')

                case Operator.NOT_BETWEEN:
                    parameters.pop(parameter_name)
                    parameters_counter -= 1

                    start_parameter_name = f'parameter_{parameters_counter}'
                    end_parameter_name = f'parameter_{parameters_counter + 1}'
                    parameters[start_parameter_name] = filter.value[0]
                    parameters[end_parameter_name] = filter.value[1]
                    start_placeholder = f'%({start_parameter_name})s'
                    end_placeholder = f'%({end_parameter_name})s'
                    parameters_counter += 2

                    filter_conditions.append(
                        f'{quoted_filter_field} NOT BETWEEN {start_placeholder} AND {end_placeholder}'
                    )

                case Operator.IS_NULL:
                    parameters.pop(parameter_name)
                    parameters_counter -= 1

                    filter_conditions.append(f'{quoted_filter_field} IS NULL')

                case Operator.IS_NOT_NULL:
                    parameters.pop(parameter_name)
                    parameters_counter -= 1

                    filter_conditions.append(f'{quoted_filter_field} IS NOT NULL')

                case Operator.IN:
                    parameters.pop(parameter_name)
                    parameters_counter -= 1

                    values = filter.value
                    placeholders = []
                    for i, value in enumerate(values):
                        param_name = f'parameter_{parameters_counter + i}'
                        parameters[param_name] = value
                        placeholders.append(f'%({param_name})s')
                    parameters_counter += len(values)

                    filter_conditions.append(f'{quoted_filter_field} IN ({", ".join(placeholders)})')

                case Operator.NOT_IN:
                    parameters.pop(parameter_name)
                    parameters_counter -= 1

                    values = filter.value
                    placeholders = []
                    for i, value in enumerate(values):
                        param_name = f'parameter_{parameters_counter + i}'
                        parameters[param_name] = value
                        placeholders.append(f'%({param_name})s')
                    parameters_counter += len(values)

                    filter_conditions.append(f'{quoted_filter_field} NOT IN ({", ".join(placeholders)})')

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
            order_field = cls._resolve_sql_column(field=order.field, columns_mapping=columns_mapping)
            quoted_order_field = cls._quote_double_quoted_identifier(identifier=order_field)

            direction = Direction(value=order.direction)
            match direction:
                case Direction.ASC:
                    orders += f'{quoted_order_field} ASC, '

                case Direction.DESC:
                    orders += f'{quoted_order_field} DESC, '

                case _:  # pragma: no cover
                    assert_never(direction)

        return orders.rstrip(', ')

    @classmethod
    def _resolve_sql_column(cls, *, field: str, columns_mapping: Mapping[str, str]) -> str:
        """
        Resolve a criteria field to the SQL column used in generated queries.

        Args:
            field (str): Criteria field name.
            columns_mapping (Mapping[str, str]): Criteria field to SQL column mapping.

        Returns:
            str: SQL column name.
        """
        return columns_mapping.get(field, field)

    @classmethod
    def _validate_table(cls, *, table: str, valid_tables: Sequence[str]) -> None:
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

    @classmethod
    def _validate_columns(
        cls, *, columns: Sequence[str], columns_mapping: Mapping[str, str], valid_columns: Sequence[str]
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

    @classmethod
    def _validate_criteria(
        cls, *, criteria: Criteria, columns_mapping: Mapping[str, str], valid_columns: Sequence[str]
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
            column = cls._resolve_sql_column(field=filter.field, columns_mapping=columns_mapping)
            if column not in valid_columns:
                raise InvalidColumnError(column=column, valid_columns=valid_columns)
        for order in criteria.orders:
            column = cls._resolve_sql_column(field=order.field, columns_mapping=columns_mapping)
            if column not in valid_columns:
                raise InvalidColumnError(column=column, valid_columns=valid_columns)

    @classmethod
    def _validate_operators(cls, *, criteria: Criteria, valid_operators: Sequence[Operator]) -> None:
        """
        Validate criteria filter operators against an allowlist.

        Args:
            criteria (Criteria): Criteria to validate.
            valid_operators (Sequence[Operator]): Allowed operators.

        Raises:
            InvalidOperatorError: If an operator is not allowed.
        """
        for filter in criteria.filters:
            if filter.operator not in valid_operators:
                raise InvalidOperatorError(operator=Operator(value=filter.operator), valid_operators=valid_operators)

    @classmethod
    def _validate_directions(cls, *, criteria: Criteria, valid_directions: Sequence[Direction]) -> None:
        """
        Validate criteria order directions against an allowlist.

        Args:
            criteria (Criteria): Criteria to validate.
            valid_directions (Sequence[Direction]): Allowed directions.

        Raises:
            InvalidDirectionError: If a direction is not allowed.
        """
        for order in criteria.orders:
            if order.direction not in valid_directions:
                raise InvalidDirectionError(
                    direction=Direction(value=order.direction), valid_directions=valid_directions
                )

    @classmethod
    def _validate_pagination_bounds(cls, *, criteria: Criteria, max_page_size: int, max_page_number: int) -> None:
        """
        Validate pagination parameters against configured maxima.

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
    def _escape_double_quoted_identifier(cls, *, identifier: str) -> str:
        """
        Escape a PostgreSQL/SQLite double-quoted identifier body.

        Args:
            identifier (str): Unquoted identifier text.

        Returns:
            str: Escaped identifier body without surrounding quotes.
        """
        return identifier.replace('"', '""')

    @classmethod
    def _quote_double_quoted_identifier(cls, *, identifier: str) -> str:
        """
        Quote a PostgreSQL/SQLite identifier.

        Args:
            identifier (str): Identifier to quote.

        Returns:
            str: Quoted identifier.
        """
        return f'"{cls._escape_double_quoted_identifier(identifier=identifier)}"'

    @classmethod
    def _quote_double_quoted_qualified_name(cls, *, name: str) -> str:
        """
        Quote a schema-qualified PostgreSQL/SQLite name.

        Args:
            name (str): Qualified or unqualified table name.

        Returns:
            str: Quoted qualified name.
        """
        return '.'.join(cls._quote_double_quoted_identifier(identifier=part) for part in name.split('.'))

    @classmethod
    def _escape_like_pattern_value(cls, *, value: Any) -> Any:
        """
        Escape SQL LIKE wildcard characters in a bound parameter value.

        Args:
            value (Any): Filter value to escape.

        Returns:
            Any: Escaped string values, or the original value for non-strings.
        """
        if not isinstance(value, str):
            return value
        return value.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')

    @classmethod
    def _ensure_operator_allowlist_size(
        cls,
        *,
        operators: Sequence[Operator],
        limit: int,
    ) -> None:
        """
        Ensure an explicit operator allowlist does not exceed a configured maximum.

        Args:
            operators (Sequence[Operator]): Operator allowlist provided by the caller.
            limit (int): Maximum allowed operators in the allowlist.

        Raises:
            IntegrityError: If the allowlist exceeds the limit.
        """
        if len(operators) > limit:
            raise IntegrityError(
                message=f'{cls.__name__} valid_operators exceeds maximum limit of <<<{limit}>>>.',
            )

    @classmethod
    def _criteria_composition_depth(cls, *, criteria: Criteria) -> int:
        """
        Measure the nesting depth of boolean criteria composition.

        Args:
            criteria (Criteria): Criteria tree to measure.

        Returns:
            int: Composition depth where plain criteria leaves are zero.
        """
        if isinstance(criteria, AndCriteria | OrCriteria):
            return 1 + max(
                cls._criteria_composition_depth(criteria=criteria.left),
                cls._criteria_composition_depth(criteria=criteria.right),
            )
        if isinstance(criteria, NotCriteria):
            return 1 + cls._criteria_composition_depth(criteria=criteria.criteria)
        return 0

    @classmethod
    def _ensure_criteria_composition_depth(cls, *, criteria: Criteria, limit: int) -> None:
        """
        Ensure boolean criteria composition does not exceed a configured depth.

        Args:
            criteria (Criteria): Criteria tree to validate.
            limit (int): Maximum allowed composition depth.

        Raises:
            IntegrityError: If composition depth exceeds the limit.
        """
        depth = cls._criteria_composition_depth(criteria=criteria)
        if depth > limit:
            raise IntegrityError(
                message=(
                    f'{cls.__name__} criteria composition depth <<<{depth}>>> exceeds maximum limit of <<<{limit}>>>.'
                ),
            )

    @classmethod
    def _iter_criteria_filters(cls, *, criteria: Criteria) -> Iterator[Any]:
        """
        Yield every filter in a criteria tree, including composed criteria.

        Args:
            criteria (Criteria): Criteria tree to traverse.

        Yields:
            Filter: Each filter contained in the tree.
        """
        if isinstance(criteria, AndCriteria | OrCriteria):
            yield from cls._iter_criteria_filters(criteria=criteria.left)
            yield from cls._iter_criteria_filters(criteria=criteria.right)
            return
        if isinstance(criteria, NotCriteria):
            yield from cls._iter_criteria_filters(criteria=criteria.criteria)
            return
        yield from criteria.filters

    @classmethod
    def _ensure_criteria_in_list_sizes(cls, *, criteria: Criteria, limit: int) -> None:
        """
        Ensure IN and NOT IN filter values do not exceed a configured maximum.

        Args:
            criteria (Criteria): Criteria tree to validate.
            limit (int): Maximum allowed values per IN list.

        Raises:
            IntegrityError: If any IN list exceeds the limit.
        """
        for filter in cls._iter_criteria_filters(criteria=criteria):
            operator = Operator(value=filter.operator)
            if operator not in (Operator.IN, Operator.NOT_IN):
                continue
            if not isinstance(filter.value, (list, tuple)):
                continue
            if len(filter.value) > limit:
                raise IntegrityError(
                    message=(
                        f'{cls.__name__} IN values for field <<<{filter.field}>>> '
                        f'exceeds maximum limit of <<<{limit}>>>.'
                    ),
                )

    @classmethod
    def _validate_criteria_bounds(
        cls,
        *,
        criteria: Criteria,
        max_criteria_depth: int,
        max_in_values: int,
    ) -> None:
        """
        Validate structural bounds for SQL conversion input.

        Args:
            criteria (Criteria): Criteria tree to validate.
            max_criteria_depth (int): Maximum allowed composition depth.
            max_in_values (int): Maximum allowed values per IN list.

        Raises:
            IntegrityError: If any configured bound is exceeded.
        """
        cls._ensure_criteria_composition_depth(criteria=criteria, limit=max_criteria_depth)
        cls._ensure_criteria_in_list_sizes(criteria=criteria, limit=max_in_values)
