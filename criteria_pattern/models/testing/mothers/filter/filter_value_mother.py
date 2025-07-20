"""
FilterValueMother.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import TypeVar

from object_mother_pattern.models import BaseMother

from criteria_pattern.models.filter import FilterValue

T = TypeVar('T')


class FilterValueMother(BaseMother[FilterValue[T]]):
    """
    FilterValueMother class is responsible for generating random filter value values.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers.filter import FilterValueMother

    value = FilterValueMother.create()
    print(value)
    # >>> zFUml6ODZq5wyG
    ```
    """

    @classmethod
    @override
    def create(cls, *, value: T | None = None) -> FilterValue[T]:
        """
        Create a random filter value value. If a specific filter value value is provided via `value`, it is returned
        after validation. Otherwise, a random filter value value is generated.

        Args:
            value (T | None, optional): Filter value value. Defaults to None.

        Returns:
            FilterValue: A random filter value value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers.filter import FilterValueMother

        value = FilterValueMother.create()
        print(value)
        # >>> zFUml6ODZq5wyG
        ```
        """
        if value is not None:
            return FilterValue(value=value)

        return FilterValue(value=BaseMother.invalid_type())
