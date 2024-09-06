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

    def convert(self, criteria: Criteria, table: str, columns: list[str] | None = None) -> str:
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

        query = f'SELECT {", ".join(columns)} FROM {table}'

        if criteria.filters:
            where_clause = self._process_filters(criteria=criteria)
            query += f' WHERE {where_clause}'

        if criteria.orders:
            order_clause = self._process_orders(criteria=criteria)
            query += f' ORDER BY {order_clause}'

        return f'{query};'

    def _process_filters(self, criteria: Criteria) -> str:
        """
        Process the filter string to create SQL WHERE clause.

        Args:
            criteria (Criteria): Criteria to process.

        Returns:
            str: Processed filter string for SQL WHERE clause.
        """
        filters = ''

        if isinstance(criteria, AndCriteria):
            left_conditions = self._process_filters(criteria=criteria.left)
            right_conditions = self._process_filters(criteria=criteria.right)
            filters += f'({left_conditions} AND {right_conditions})'

            return filters

        if isinstance(criteria, OrCriteria):
            left_conditions = self._process_filters(criteria=criteria.left)
            right_conditions = self._process_filters(criteria=criteria.right)
            filters += f'({left_conditions} OR {right_conditions})'

            return filters

        if isinstance(criteria, NotCriteria):
            not_conditions = self._process_filters(criteria=criteria.criteria)
            filters += f'NOT ({not_conditions})'

            return filters

        for filter in criteria.filters:
            if filter.operator in [FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL]:
                filters += f'{filter.field} {filter.operator}'

            elif filter.operator in [FilterOperator.BETWEEN, FilterOperator.NOT_BETWEEN]:
                filters += f"{filter.field} {filter.operator} '{filter.value[0]}' AND '{filter.value[1]}'"

            else:
                filters += f"{filter.field} {filter.operator} '{filter.value}'"

        return filters

    def _process_orders(self, criteria: Criteria) -> str:
        """
        Process the Criteria and return a string of order fields.

        Args:
            criteria (Criteria): Criteria to process.

        Returns:
            str: Processed order fields
        """
        orders = []

        for order in criteria.orders:
            match order.direction:
                case OrderDirection.ASC:
                    orders.append(f'{order.field} ASC')

                case OrderDirection.DESC:
                    orders.append(f'{order.field} DESC')

                case _:
                    assert_never(order.direction)

        return ', '.join(orders)
