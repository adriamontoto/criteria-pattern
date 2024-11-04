"""
Raw SQL converter module.
"""

from typing import Any, assert_never

from criteria_pattern import Criteria, FilterOperator, OrderDirection
from criteria_pattern.criteria import AndCriteria, NotCriteria, OrCriteria


class SqlConverter:
    """
    Raw SQL converter.
    """

    @classmethod
    def convert(
        cls,
        criteria: Criteria,
        table: str,
        columns: list[str] | None = None,
        columns_mapping: dict[str, str] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """
        Convert the Criteria object to a raw SQL query.

        Args:
            criteria (Criteria): Criteria to convert.
            table (str): Name of the table to query.
            columns (list[str]): Columns of the table to select. Default to *.

        Returns:
            tuple[str, dict[str, Any]]: The raw SQL query string and the query parameters.
        """
        if columns is None:
            columns = ['*']

        if columns_mapping is None:
            columns_mapping = {}

        query = f'SELECT {", ".join(columns)} FROM {table}'  # noqa: S608  # nosec
        parameters: dict[str, Any] = {}

        if criteria.has_filters():
            where_clause, parameters = cls._process_filters(criteria=criteria, columns_mapping=columns_mapping)
            query += f' WHERE {where_clause}'

        if criteria.has_orders():
            order_clause = cls._process_orders(criteria=criteria, columns_mapping=columns_mapping)
            query += f' ORDER BY {order_clause}'

        return f'{query};', parameters

    @classmethod
    def _process_filters(cls, criteria: Criteria, columns_mapping: dict[str, str]) -> tuple[str, dict[str, Any]]:
        """
        Process the Criteria object to return an SQL WHERE clause.

        Args:
            criteria (Criteria): Criteria to process.
            columns_mapping (dict[str, str]): Mapping of column names to aliases.

        Returns:
            tuple[str, dict[str, Any]]: Processed filter string for SQL WHERE clause and parameters for the SQL query.
        """
        return cls._process_filters_recursive(criteria=criteria, columns_mapping=columns_mapping)

    @classmethod
    def _process_filters_recursive(  # noqa: C901
        cls,
        criteria: Criteria,
        columns_mapping: dict[str, str],
        parameters_counter: int = 0,
    ) -> tuple[str, dict[str, Any]]:
        """
        Process the Criteria object to return an SQL WHERE clause.

        Args:
            criteria (Criteria): Criteria to process.
            columns_mapping (dict[str, str]): Mapping of column names to aliases.
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

            filters += f'({left_conditions} AND {right_conditions})'

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

            filters += f'({left_conditions} OR {right_conditions})'

            return filters, parameters

        if isinstance(criteria, NotCriteria):
            not_conditions, not_parameters = cls._process_filters_recursive(
                criteria=criteria.criteria,
                columns_mapping=columns_mapping,
                parameters_counter=parameters_counter,
            )
            parameters_counter += len(not_parameters)
            parameters.update(not_parameters)

            filters += f'NOT ({not_conditions})'

            return filters, parameters

        for filter in criteria.filters:
            filter_field = columns_mapping.get(filter.field, filter.field)
            parameter_name = f'parameter_{parameters_counter}'
            parameters[parameter_name] = filter.value
            placeholder = f'%({parameter_name})s'
            parameters_counter += 1

            match filter.operator:
                case FilterOperator.EQUAL:
                    filters += f'{filter_field} = {placeholder}'

                case FilterOperator.NOT_EQUAL:
                    filters += f'{filter_field} != {placeholder}'

                case FilterOperator.GREATER:
                    filters += f'{filter_field} > {placeholder}'

                case FilterOperator.GREATER_OR_EQUAL:
                    filters += f'{filter_field} >= {placeholder}'

                case FilterOperator.LESS:
                    filters += f'{filter_field} < {placeholder}'

                case FilterOperator.LESS_OR_EQUAL:
                    filters += f'{filter_field} <= {placeholder}'

                case FilterOperator.LIKE:
                    filters += f'{filter_field} LIKE {placeholder}'

                case FilterOperator.NOT_LIKE:
                    filters += f'{filter_field} NOT LIKE {placeholder}'

                case FilterOperator.CONTAINS:
                    filters += f"{filter_field} LIKE '%%' || {placeholder} || '%%'"

                case FilterOperator.NOT_CONTAINS:
                    filters += f"{filter_field} NOT LIKE '%%' || {placeholder} || '%%'"

                case FilterOperator.STARTS_WITH:
                    filters += f"{filter_field} LIKE {placeholder} || '%%'"

                case FilterOperator.NOT_STARTS_WITH:
                    filters += f"{filter_field} NOT LIKE {placeholder} || '%%'"

                case FilterOperator.ENDS_WITH:
                    filters += f"{filter_field} LIKE '%%' || {placeholder}"

                case FilterOperator.NOT_ENDS_WITH:
                    filters += f"{filter_field} NOT LIKE '%%' || {placeholder}"

                case FilterOperator.BETWEEN:
                    parameters.pop(parameter_name)
                    parameters_counter -= 1

                    start_parameter_name = f'parameter_{parameters_counter}'
                    end_parameter_name = f'parameter_{parameters_counter + 1}'
                    parameters[start_parameter_name] = filter.value[0]
                    parameters[end_parameter_name] = filter.value[1]
                    start_placeholder = f'%({start_parameter_name})s'
                    end_placeholder = f'%({end_parameter_name})s'
                    parameters_counter += 2

                    filters += f'{filter_field} BETWEEN {start_placeholder} AND {end_placeholder}'

                case FilterOperator.NOT_BETWEEN:
                    parameters.pop(parameter_name)
                    parameters_counter -= 1

                    start_parameter_name = f'parameter_{parameters_counter}'
                    end_parameter_name = f'parameter_{parameters_counter + 1}'
                    parameters[start_parameter_name] = filter.value[0]
                    parameters[end_parameter_name] = filter.value[1]
                    start_placeholder = f'%({start_parameter_name})s'
                    end_placeholder = f'%({end_parameter_name})s'
                    parameters_counter += 2

                    filters += f'{filter_field} NOT BETWEEN {start_placeholder} AND {end_placeholder}'

                case FilterOperator.IS_NULL:
                    parameters.pop(parameter_name)
                    parameters_counter -= 1

                    filters += f'{filter_field} IS NULL'

                case FilterOperator.IS_NOT_NULL:
                    parameters.pop(parameter_name)
                    parameters_counter -= 1

                    filters += f'{filter_field} IS NOT NULL'

                case _:  # pragma: no cover
                    assert_never(filter.operator)

        return filters, parameters

    @classmethod
    def _process_orders(cls, criteria: Criteria, columns_mapping: dict[str, str]) -> str:
        """
        Process the Criteria object to return an SQL ORDER BY clause.

        Args:
            criteria (Criteria): Criteria to process.
            columns_mapping (dict[str, str]): Mapping of column names to aliases.

        Returns:
            str: Processed order string for SQL ORDER BY clause.
        """
        orders = ''

        for order in criteria.orders:
            order_field = columns_mapping.get(order.field, order.field)

            match order.direction:
                case OrderDirection.ASC:
                    orders += f'{order_field} ASC, '

                case OrderDirection.DESC:
                    orders += f'{order_field} DESC, '

                case _:  # pragma: no cover
                    assert_never(order.direction)

        return orders.rstrip(', ')
