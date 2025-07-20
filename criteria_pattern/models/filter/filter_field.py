"""
FilterField module.
"""

from value_object_pattern.usables import (
    NotEmptyStringValueObject,
    PrintableStringValueObject,
    TrimmedStringValueObject,
)


class FilterField(NotEmptyStringValueObject, TrimmedStringValueObject, PrintableStringValueObject):
    """
    FilterField class.

    Example:
    ```python
    from criteria_pattern.models.filter.filter_field import FilterField

    field = FilterField(value='name')
    print(field)
    # >>> name
    ```
    """
