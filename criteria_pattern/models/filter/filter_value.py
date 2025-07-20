"""
FilterValue module.
"""

from typing import TypeVar

from value_object_pattern import ValueObject

T = TypeVar('T')


class FilterValue(ValueObject[T]):
    """
    FilterValue class.

    Example:
    ```python
    from criteria_pattern.models.filter.filter_value import FilterValue

    value = FilterValue(value='John')
    print(value)
    # >>> John
    ```
    """
