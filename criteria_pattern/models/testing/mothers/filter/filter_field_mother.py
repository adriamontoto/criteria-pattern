"""
FilterFieldMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from object_mother_pattern.models import BaseMother
from object_mother_pattern.mothers import StringMother

from criteria_pattern.models.filter import FilterField


class FilterFieldMother(BaseMother[FilterField]):
    """
    FilterFieldMother class is responsible for generating random filter field values.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers.filter import FilterFieldMother

    field = FilterFieldMother.create()
    print(field)
    # >>> zFUml6ODZq5wyG
    ```
    """

    @classmethod
    @override
    def create(cls, *, value: str | None = None) -> FilterField:
        """
        Create a random filter field value. If a specific filter field value is provided via `value`, it is returned
        after validation. Otherwise, a random filter field value is generated.

        Args:
            value (str | None, optional): Filter field value. Defaults to None.

        Raises:
            TypeError: If `value` is not a string.
            ValueError: If `value` is empty.
            ValueError: If `value` is not trimmed.
            ValueError: If `value` contains non-alphanumeric characters.

        Returns:
            FilterField: A random filter field value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers.filter import FilterFieldMother

        field = FilterFieldMother.create()
        print(field)
        # >>> zFUml6ODZq5wyG
        ```
        """
        if value is not None:
            return FilterField(value=value)

        return FilterField(value=StringMother.create())
