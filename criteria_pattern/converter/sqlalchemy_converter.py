"""
SQLAlchemy converter module.
"""

from importlib.util import find_spec

if find_spec(name='sqlalchemy') is None:
    raise ImportError("SQLAlchemy is not installed. Please install it using 'pip install criteria-pattern[sqlalchemy]'")

from typing import Any, TypeVar, assert_never

from sqlalchemy import Column, and_, or_
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.elements import ColumnElement, UnaryExpression

from criteria_pattern import Criteria, FilterOperator, OrderDirection
from criteria_pattern.criteria import AndCriteria, OrCriteria

T = TypeVar('T', bound=DeclarativeMeta)


class SQLAlchemyConverter:
    """
    SQLAlchemy converter.
    """

    def convert(self, criteria: Criteria, model: type[T]) -> Query[T]:
        """
        Convert the Criteria object to a SQLAlchemy Query.

        Args:
            criteria (Criteria): Criteria to convert.
            model (DeclarativeMeta): SQLAlchemy model.

        Returns:
            Query: Query object.
        """
        query: Query[T] = Query(model)
        filters = self._process_filters(criteria=criteria, model=model)
        if filters:
            query = query.filter(*filters)

        orders = self._process_orders(criteria=criteria, model=model)
        if orders:
            query = query.order_by(*orders)

        return query

    def _process_filters(self, criteria: Criteria, model: type[T]) -> list[ColumnElement[bool]]:  # noqa: C901
        """
        Process the Criteria and return a list of conditions.

        Args:
            criteria (Criteria): Criteria to process.
            model (DeclarativeMeta): SQLAlchemy model.

        Returns:
            list[BinaryExpression]: List of conditions.
        """
        conditions: list[ColumnElement[bool]] = []

        if isinstance(criteria, AndCriteria):
            left_conditions = self._process_filters(criteria=criteria.left, model=model)
            right_conditions = self._process_filters(criteria=criteria.right, model=model)
            conditions.append(and_(*left_conditions, *right_conditions))

            return conditions

        if isinstance(criteria, OrCriteria):
            left_conditions = self._process_filters(criteria=criteria.left, model=model)
            right_conditions = self._process_filters(criteria=criteria.right, model=model)
            conditions.append(or_(*left_conditions, *right_conditions))

            return conditions

        for filter in criteria.filters:
            field: Column[Any] = getattr(model, filter.field)
            match filter.operator:
                case FilterOperator.EQUAL:
                    conditions.append(field == filter.value)

                case FilterOperator.NOT_EQUAL:
                    conditions.append(field != filter.value)

                case FilterOperator.GREATER:
                    conditions.append(field > filter.value)

                case FilterOperator.GREATER_OR_EQUAL:
                    conditions.append(field >= filter.value)

                case FilterOperator.LESS:
                    conditions.append(field < filter.value)

                case FilterOperator.LESS_OR_EQUAL:
                    conditions.append(field <= filter.value)

                case FilterOperator.LIKE:
                    conditions.append(field.like(filter.value))

                case FilterOperator.IN:
                    conditions.append(field.in_(filter.value))

                case FilterOperator.NOT_IN:
                    conditions.append(~field.in_(filter.value))

                case FilterOperator.IS_NULL:
                    conditions.append(field.is_(None))

                case FilterOperator.IS_NOT_NULL:
                    conditions.append(field.isnot(None))

                case FilterOperator.BETWEEN:
                    conditions.append(field.between(filter.value[0], filter.value[1]))

                case FilterOperator.NOT_BETWEEN:
                    conditions.append(~field.between(filter.value[0], filter.value[1]))

                case FilterOperator.CONTAINS:
                    conditions.append(field.contains(filter.value))

                case FilterOperator.NOT_CONTAINS:
                    conditions.append(~field.contains(filter.value))

                case FilterOperator.STARTS_WITH:
                    conditions.append(field.startswith(filter.value))

                case FilterOperator.ENDS_WITH:
                    conditions.append(field.endswith(filter.value))

                case _:
                    assert_never(filter.operator)

        return conditions

    def _process_orders(self, criteria: Criteria, model: type[T]) -> list[UnaryExpression[Any]]:
        """
        Process the Criteria and return a list of order fields.

        Args:
            criteria (Criteria): Criteria to process.
            model (DeclarativeMeta): SQLAlchemy model.

        Returns:
            list[Column]: List of order fields.
        """
        orders = []

        for order in criteria.orders:
            field: Column[Any] = getattr(model, order.field)
            match order.direction:
                case OrderDirection.ASC:
                    orders.append(field.asc())

                case OrderDirection.DESC:
                    orders.append(field.desc())

                case _:
                    assert_never(order.direction)

        return orders
