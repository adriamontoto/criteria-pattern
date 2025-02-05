"""
This module contains the Filter class.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import Generic, TypeVar

from .filter_operator import FilterOperator

T = TypeVar('T')


class Filter(Generic[T]):
    """
    Filter class.

    Example:
    ```python
    from criteria_pattern import Filter, FilterOperator

    filter = Filter(field='name', operator=FilterOperator.EQUAL, value='John')
    print(filter)
    # >>> 'name' EQUAL 'John'
    ```
    """

    __field: str
    __operator: FilterOperator
    __value: T

    def __init__(self, field: str, operator: FilterOperator, value: T) -> None:
        """
        Filter constructor.

        Args:
            field (str): Field name.
            operator (FilterOperator): Filter operator.
            value (T): Filter value.

        Example:
        ```python
        from criteria_pattern import Filter, FilterOperator

        filter = Filter(field='name', operator=FilterOperator.EQUAL, value='John')
        print(filter)
        # >>> 'name' EQUAL 'John'
        ```
        """
        self.__field = field
        self.__operator = operator
        self.__value = value

    @override
    def __repr__(self) -> str:
        """
        Get string representation of Filter.

        Returns:
            str: String representation of Filter.

        Example:
        ```python
        from criteria_pattern import Filter, FilterOperator

        filter = Filter(field='name', operator=FilterOperator.EQUAL, value='John')
        print(repr(filter))
        # >>> 'name' EQUAL 'John'
        ```
        """
        return f'{self.field!r} {self.operator} {self.value!r}'

    @property
    def field(self) -> str:
        """
        Get field.

        Returns:
            str: Field name.

        Example:
        ```python
        from criteria_pattern import Filter, FilterOperator

        filter = Filter(field='name', operator=FilterOperator.EQUAL, value='John')
        print(filter.field)
        # >>> name
        ```
        """
        return self.__field

    @property
    def operator(self) -> FilterOperator:
        """
        Get operator.

        Returns:
            FilterOperator: Filter operator.

        Example:
        ```python
        from criteria_pattern import Filter, FilterOperator

        filter = Filter(field='name', operator=FilterOperator.EQUAL, value='John')
        print(filter.operator)
        # >>> EQUAL
        ```
        """
        return self.__operator

    @property
    def value(self) -> T:
        """
        Get value.

        Returns:
            T: Filter value.

        Example:
        ```python
        from criteria_pattern import Filter, FilterOperator

        filter = Filter(field='name', operator=FilterOperator.EQUAL, value='John')
        print(filter.value)
        # >>> John
        ```
        """
        return self.__value
