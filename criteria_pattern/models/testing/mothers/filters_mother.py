"""
FiltersMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import Any

from object_mother_pattern.models import BaseMother
from object_mother_pattern.mothers import IntegerMother

from criteria_pattern.models import Filter
from criteria_pattern.models.filters import Filters

from .filter import FilterMother


class FiltersMother(BaseMother[Filters]):
    """
    FiltersMother class is responsible for generating random filters value.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers import FiltersMother

    filters = FiltersMother.create()
    print(filters)
    # >>> [Filter(field=FilterField(value='QgTvRjzW'), operator=FilterOperator(value=<Operator.IS_NOT_NULL: 'IS NOT NULL'>), value=FilterValue(value='CSQkE'))]
    ```
    """  # noqa: E501

    @classmethod
    @override
    def create(cls, *, value: list[Filter[Any]] | None = None) -> Filters:
        """
        Create a random filters value. If a specific filters value is provided via `value`, it is returned after
        validation. Otherwise, a random filters value is generated.

        Args:
            value (list[Filter[Any]] | None, optional): A specific filters value to return. If None, a random filters
            value is generated.

        Returns:
            Filters: A random filters value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import FiltersMother

        filters = FiltersMother.create()
        print(filters)
        # >>> [Filter(field=FilterField(value='QgTvRjzW'), operator=FilterOperator(value=<Operator.IS_NOT_NULL: 'IS NOT NULL'>), value=FilterValue(value='CSQkE'))]
        ```
        """  # noqa: E501
        if value is not None:
            return Filters(value=value)

        value = []
        for _ in range(IntegerMother.positive_or_zero(max=10)):
            value.append(FilterMother.create())

        return Filters(value=value)

    @classmethod
    def of_length(cls, *, length: int) -> Filters:
        """
        Create a random filters value with a specific length.

        Args:
            length (int): The length of the filters value.

        Returns:
            Filters: A random filters value with the specified length.
        """
        return cls.create(value=[FilterMother.create() for _ in range(length)])
