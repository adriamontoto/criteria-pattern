"""
Raw SQL converter module.
"""

from typing import assert_never

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
    ) -> str:
        """
        Convert the Criteria object to a raw SQL query.

        Args:
            criteria (Criteria): Criteria to convert.
            table (str): Name of the table to query.
            columns (list[str]): Columns of the table to select. Default to *.

        Returns:
            str: The raw SQL query string.
        """
        if columns is None:
            columns = ['*']

        if columns_mapping is None:
            columns_mapping = {}

        query = f'SELECT {", ".join(columns)} FROM {table}'  # noqa: S608  # nosec

        if criteria.has_filters():
            where_clause = cls._process_filters(criteria=criteria, columns_mapping=columns_mapping)
            query += f' WHERE {where_clause}'

        if criteria.has_orders():
            order_clause = cls._process_orders(criteria=criteria, columns_mapping=columns_mapping)
            query += f' ORDER BY {order_clause}'

        return f'{query};'

    @classmethod
    def _process_filters(cls, criteria: Criteria, columns_mapping: dict[str, str]) -> str:  # noqa: C901
        """
        Process the Criteria object to return an SQL WHERE clause.

        Args:
            criteria (Criteria): Criteria to process.
            columns_mapping (dict[str, str]): Mapping of column names to aliases.

        Returns:
            str: Processed filter string for SQL WHERE clause.
        """
        filters = ''

        if isinstance(criteria, AndCriteria):
            left_conditions = cls._process_filters(criteria=criteria.left, columns_mapping=columns_mapping)
            right_conditions = cls._process_filters(criteria=criteria.right, columns_mapping=columns_mapping)
            filters += f'({left_conditions} AND {right_conditions})'

            return filters

        if isinstance(criteria, OrCriteria):
            left_conditions = cls._process_filters(criteria=criteria.left, columns_mapping=columns_mapping)
            right_conditions = cls._process_filters(criteria=criteria.right, columns_mapping=columns_mapping)
            filters += f'({left_conditions} OR {right_conditions})'

            return filters

        if isinstance(criteria, NotCriteria):
            not_conditions = cls._process_filters(criteria=criteria.criteria, columns_mapping=columns_mapping)
            filters += f'NOT ({not_conditions})'

            return filters

        for filter in criteria.filters:
            filter_field = columns_mapping.get(filter.field, filter.field)

            match filter.operator:
                case FilterOperator.EQUAL:
                    filters += f"{filter_field} = '{filter.value}'"

                case FilterOperator.NOT_EQUAL:
                    filters += f"{filter_field} != '{filter.value}'"

                case FilterOperator.GREATER:
                    filters += f"{filter_field} > '{filter.value}'"

                case FilterOperator.GREATER_OR_EQUAL:
                    filters += f"{filter_field} >= '{filter.value}'"

                case FilterOperator.LESS:
                    filters += f"{filter_field} < '{filter.value}'"

                case FilterOperator.LESS_OR_EQUAL:
                    filters += f"{filter_field} <= '{filter.value}'"

                case FilterOperator.LIKE:
                    filters += f"{filter_field} LIKE '{filter.value}'"

                case FilterOperator.NOT_LIKE:
                    filters += f"{filter_field} NOT LIKE '{filter.value}'"

                case FilterOperator.CONTAINS:
                    filters += f"{filter_field} LIKE '%{filter.value}%'"

                case FilterOperator.NOT_CONTAINS:
                    filters += f"{filter_field} NOT LIKE '%{filter.value}%'"

                case FilterOperator.STARTS_WITH:
                    filters += f"{filter_field} LIKE '{filter.value}%'"

                case FilterOperator.NOT_STARTS_WITH:
                    filters += f"{filter_field} NOT LIKE '{filter.value}%'"

                case FilterOperator.ENDS_WITH:
                    filters += f"{filter_field} LIKE '%{filter.value}'"

                case FilterOperator.NOT_ENDS_WITH:
                    filters += f"{filter_field} NOT LIKE '%{filter.value}'"

                case FilterOperator.BETWEEN:
                    filters += f"{filter_field} BETWEEN '{filter.value[0]}' AND '{filter.value[1]}'"

                case FilterOperator.NOT_BETWEEN:
                    filters += f"{filter_field} NOT BETWEEN '{filter.value[0]}' AND '{filter.value[1]}'"

                case FilterOperator.IN:
                    sequence = ', '.join([f"'{value}'" for value in filter.value])
                    filters += f'{filter_field} IN ({sequence})'

                case FilterOperator.NOT_IN:
                    sequence = ', '.join([f"'{value}'" for value in filter.value])
                    filters += f'{filter_field} NOT IN ({sequence})'

                case FilterOperator.IS_NULL:
                    filters += f'{filter_field} IS NULL'

                case FilterOperator.IS_NOT_NULL:
                    filters += f'{filter_field} IS NOT NULL'

                case _:  # pragma: no cover
                    assert_never(filter.operator)

        return filters

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
