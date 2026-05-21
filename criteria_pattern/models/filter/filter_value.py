"""
Generic value object for filter comparison values.
"""

from typing import TypeVar

from value_object_pattern import ValueObject

T = TypeVar('T')


class FilterValue(ValueObject[T]):
    """
    Store the raw value associated with a filter condition.

    The value is not coerced here. Request converters parse incoming primitives before constructing filters, and SQL
    converters decide how to bind scalar, range, list, and null-like operator values.

    Example:
    ```python
    from criteria_pattern.models.filter.filter_value import FilterValue

    value = FilterValue(value='John')
    print(value)
    # >>> John
    ```
    """
