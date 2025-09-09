"""
This module contains the Filter class.
"""

from typing import Generic, TypeVar

from value_object_pattern import BaseModel

from .filter_field import FilterField
from .filter_operator import FilterOperator
from .filter_value import FilterValue

T = TypeVar('T')


class Filter(BaseModel, Generic[T]):  # noqa: UP046
    """
    Filter class.

    Example:
    ```python
    from criteria_pattern import Filter

    filter = Filter(field='name', operator='EQUAL', value='John')
    print(filter)
    # >>> Filter(field=name, operator=EQUAL, value=John)
    ```
    """

    _field: FilterField
    _operator: FilterOperator
    _value: FilterValue[T]

    def __init__(self, *, field: str, operator: str, value: T) -> None:
        """
        Filter constructor.

        Args:
            field (str): Field name that will be filtered.
            operator (str): Operator that will be used to filter the field.
            value (T): Value that will be used to filter the field.

        Raises:
            TypeError: If the provided `field` is not a string.
            ValueError: If the provided `field` is empty.
            ValueError: If the provided `field` is not trimmed.
            ValueError: If the provided `field` is not alphanumeric.
            TypeError: If the provided `operator` is not an Operator.
            TypeError: If the provided `value` is not of type `T`.

        Example:
        ```python
        from criteria_pattern import Filter

        filter = Filter(field='name', operator='EQUAL', value='John')
        print(filter)
        # >>> Filter(field=name, operator=EQUAL, value=John)
        ```
        """
        self._field = FilterField(value=field, title='Filter', parameter='field')
        self._operator = FilterOperator(value=operator, title='Filter', parameter='operator')
        self._value = FilterValue(value=value, title='Filter', parameter='value')

    @property
    def field(self) -> str:
        """
        Get field.

        Returns:
            str: Field name.

        Example:
        ```python
        from criteria_pattern import Filter

        filter = Filter(field='name', operator='EQUAL', value='John')
        print(filter.field)
        # >>> name
        ```
        """
        return self._field.value

    @property
    def operator(self) -> str:
        """
        Get operator.

        Returns:
            str: Filter operator.

        Example:
        ```python
        from criteria_pattern import Filter

        filter = Filter(field='name', operator='EQUAL', value='John')
        print(filter.operator)
        # >>> EQUAL
        ```
        """
        return self._operator.value.value

    @property
    def value(self) -> T:
        """
        Get value.

        Returns:
            T: Filter value.

        Example:
        ```python
        from criteria_pattern import Filter

        filter = Filter(field='name', operator='EQUAL', value='John')
        print(filter.value)
        # >>> John
        ```
        """
        return self._value.value
