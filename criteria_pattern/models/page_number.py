"""
PageNumber module.
"""

from value_object_pattern.usables import PositiveIntegerValueObject


class PageNumber(PositiveIntegerValueObject):
    """
    PageNumber class.

    Example:
    ```python
    from criteria_pattern import PageNumber

    page_number = PageNumber(value=1)
    print(page_number)
    # >>> 1
    ```
    """
