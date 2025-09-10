"""
PageSize module.
"""

from value_object_pattern.usables import PositiveIntegerValueObject


class PageSize(PositiveIntegerValueObject):
    """
    PageSize class.

    Example:
    ```python
    from criteria_pattern import PageSize

    page_size = PageSize(value=20)
    print(page_size)
    # >>> 20
    ```
    """
