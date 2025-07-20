"""
Filters module.
"""

from typing import Any

from value_object_pattern.models.collections import ListValueObject

from .filter import Filter


class Filters(ListValueObject[Filter[Any]]):
    """
    Filters class is a list of filters.

    Example:
    ```python
    from criteria_pattern.models import Filter, Operator
    from criteria_pattern.models.filters import Filters

    filters = Filters(value=[Filter(field='name', operator=Operator.EQUAL, value='John')])
    print(filters)
    # >>> ['Filter(field=name, operator=EQUAL, value=John)']
    ```
    """

    def __init__(self, *, value: list[Filter[Any]]) -> None:
        """
        Initialize a list of filters.

        Args:
            value (list[Filter]): The list of filters.

        Example:
        ```python
        from criteria_pattern.models import Filter, Operator
        from criteria_pattern.models.filters import Filters

        filters = Filters(value=[Filter(field='name', operator=Operator.EQUAL, value='John')])
        print(filters)
        # >>> ['Filter(field=name, operator=EQUAL, value=John)']
        ```
        """
        super().__init__(value=value)
