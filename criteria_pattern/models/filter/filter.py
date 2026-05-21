"""
Filter model for one field/operator/value condition.

Filters are storage-agnostic. They describe the requested comparison and leave dialect-specific rendering to converter
classes.
"""

from typing import Generic, TypeVar

from value_object_pattern import BaseModel

from .filter_field import FilterField
from .filter_operator import FilterOperator
from .filter_value import FilterValue

T = TypeVar('T')


class Filter(BaseModel, Generic[T]):  # noqa: UP046
    """
    Represent a single filtering condition.

    A filter validates and stores the field name, operator, and comparison value. The value is intentionally generic so
    operators such as `BETWEEN`, `IN`, and `IS_NULL` can use the shapes expected by downstream converters.

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
        Initialize a filter condition.

        Args:
            field (str): Field name to filter. It must be a non-empty, trimmed, printable string.
            operator (str): Operator name or `Operator` value to apply to the field.
            value (T): Comparison value to pass through to converters.

        Raises:
            IntegrityError: If the provided `field` is not a string.
            IntegrityError: If the provided `field` is empty.
            IntegrityError: If the provided `field` is not trimmed.
            IntegrityError: If the provided `field` is not alphanumeric.
            IntegrityError: If the provided `operator` is not an Operator.
            IntegrityError: If the provided `value` is not of type `T`.

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
        Get the validated field name.

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
        Get the validated operator value.

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
        Get the original comparison value.

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
