"""
FilterMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import TypeVar

from object_mother_pattern.models import BaseMother

from criteria_pattern.models.filter import Filter

from .filter_field_mother import FilterFieldMother
from .filter_operator_mother import FilterOperatorMother
from .filter_value_mother import FilterValueMother

T = TypeVar('T')


class FilterMother(BaseMother[Filter[T]]):
    """
    FilterMother class is responsible for generating random filter objects.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers import FilterMother

    filter = FilterMother.create()
    print(filter)
    # >>> Filter(field=oRe6OqcZ6zqXaZOYWRy, operator=NOT BETWEEN, value=TW6v6voKkiABfee1ueyJXeRhX)
    ```
    """

    @classmethod
    @override
    def create(cls, *, field: str | None = None, operator: str | None = None, value: T | None = None) -> Filter[T]:
        """
        Create a random filter value. If specific filter parameters are provided via `field`, `operator` and `value`,
        they are used to create the filter after validation. Otherwise, a random filter value is generated.

        Args:
            field (str | None, optional): The field to filter. Defaults to None.
            operator (str | None, optional): The operator to use. Defaults to None.
            value (T | None, optional): The value to filter. Defaults to None.

        Raises:
            TypeError: If `field` is not a string.
            ValueError: If `field` is empty.
            ValueError: If `field` is not trimmed.
            ValueError: If `field` contains non-alphanumeric characters.
            TypeError: If `operator` is not an Operator.

        Returns:
            Filter[T]: A random filter value with the specified parameters.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import FilterMother

        filter = FilterMother.create()
        print(filter)
        # >>> Filter(field=oRe6OqcZ6zqXaZOYWRy, operator=NOT BETWEEN, value=TW6v6voKkiABfee1ueyJXeRhX)
        ```
        """
        return Filter(
            field=FilterFieldMother.create(value=field).value,
            operator=FilterOperatorMother.create(value=operator).value,
            value=FilterValueMother.create(value=value).value,
        )
