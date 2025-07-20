"""
FilterOperator module.
"""

from value_object_pattern import EnumerationValueObject

from .operator import Operator


class FilterOperator(EnumerationValueObject[Operator]):
    """
    FilterOperator class.

    Example:
    ```python
    from criteria_pattern.models.filter.filter_operator import FilterOperator

    operator = FilterOperator(value='EQUAL')
    print(operator)
    # >>> EQUAL
    ```
    """
