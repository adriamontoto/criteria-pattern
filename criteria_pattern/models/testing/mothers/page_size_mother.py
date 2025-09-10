"""
PageSizeMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from object_mother_pattern.models import BaseMother
from object_mother_pattern.mothers import IntegerMother

from criteria_pattern import PageSize


class PageSizeMother(BaseMother[PageSize]):
    """
    PageSizeMother class is responsible for generating random page size values.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers import PageSizeMother

    size = PageSizeMother.create()
    print(size)
    # >>> 1
    ```
    """

    @classmethod
    @override
    def create(cls, *, value: int | None = None) -> PageSize:
        """
        Create a random page size value. If a specific page size value is provided via `value`, it is returned after
        validation. Otherwise, a random page size value is generated.

        Args:
            value (int | None, optional): Page size value. Defaults to None.

        Raises:
            TypeError: If `value` is not an integer.
            ValueError: If `value` is not a positive integer.

        Returns:
            PageSize: A random page size value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import PageSizeMother

        size = PageSizeMother.create()
        print(size)
        # >>> 1
        ```
        """
        if value is not None:
            return PageSize(value=value)

        return PageSize(value=IntegerMother.positive())
