"""
FilterMother class to create Filter objects.
"""

from secrets import choice
from typing import Any, NotRequired, TypedDict
from typing_extensions import Unpack

from faker import Faker

from criteria_pattern import Filter, FilterOperator


class FilterPrimitives(TypedDict):
    """
    Filter class primitives.
    """

    field: NotRequired[str]
    operator: NotRequired[FilterOperator]
    value: NotRequired[Any]


class FilterMother:
    """
    FilterMother class to create Filter objects.
    """

    @staticmethod
    def create(**kwargs: Unpack[FilterPrimitives]) -> Filter[Any]:
        """
        Create a Filter object with the given parameters. If an argument is not provided, random values will be used.

        Args:
            field (str | None): The field to filter. Default to None.
            operator (FilterOperator | None): The operator to use. Default to None.
            value (Any | None): The value to filter. Default to None.

        Returns:
            Filter: A Filter object.
        """
        field = kwargs.get('field', default=Faker().word())
        operator = kwargs.get('operator', default=FilterOperator(value=choice(seq=list(FilterOperator))))
        value = kwargs.get('value', default=Faker().word())

        return Filter(field=field, operator=operator, value=value)
