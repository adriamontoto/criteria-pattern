"""
SQLAlchemy converter module.
"""

from typing import assert_never

from sqlalchemy import Column, and_, or_
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.elements import BinaryExpression

from criteria_pattern import Criteria, FilterOperator
from criteria_pattern.criteria import AndCriteria, OrCriteria

from .converter import Converter


class SQLAlchemyConverter(Converter):
    """
    SQLAlchemy converter.
    """

    def convert(self, criteria: Criteria, model: DeclarativeMeta) -> Query:
        """
        Convert the Criteria object to a SQLAlchemy Query.

        Args:
            criteria (Criteria): Criteria to convert.
            model (DeclarativeMeta): SQLAlchemy model.

        Returns:
            Query: Query object.
        """
        query = Query(model)
        filters = self._process_criteria(criteria=criteria, model=model)
        if filters:
            query = query.filter(*filters)

        return query

    def _process_criteria(self, criteria: Criteria, model: DeclarativeMeta) -> list[BinaryExpression]:  # noqa: C901
        """
        Process the Criteria and return a list of conditions.

        Args:
            criteria (Criteria): Criteria to process.
            model (DeclarativeMeta): SQLAlchemy model.

        Returns:
            list[BinaryExpression]: List of conditions.
        """
        conditions = []

        if isinstance(criteria, AndCriteria):
            left_conditions = self._process_criteria(criteria=criteria.left, model=model)
            right_conditions = self._process_criteria(criteria=criteria.right, model=model)
            conditions.append(and_(*left_conditions, *right_conditions))

            return conditions

        if isinstance(criteria, OrCriteria):
            left_conditions = self._process_criteria(criteria=criteria.left, model=model)
            right_conditions = self._process_criteria(criteria=criteria.right, model=model)
            conditions.append(or_(*left_conditions, *right_conditions))

            return conditions

        for filter in criteria.filters:
            field: Column = getattr(model, filter.field)
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
