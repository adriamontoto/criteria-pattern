"""
PageNumberMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from object_mother_pattern.models import BaseMother
from object_mother_pattern.mothers import IntegerMother

from criteria_pattern import PageNumber


class PageNumberMother(BaseMother[PageNumber]):
    """
    PageNumberMother class is responsible for generating random page number values.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers import PageNumberMother

    number = PageNumberMother.create()
    print(number)
    # >>> 1
    ```
    """

    @classmethod
    @override
    def create(cls, *, value: int | None = None) -> PageNumber:
        """
        Create a random page number value. If a specific page number value is provided via `value`, it is returned after
        validation. Otherwise, a random page number value is generated.

        Args:
            value (int | None, optional): Page number value. Defaults to None.

        Raises:
            TypeError: If `value` is not an integer.
            ValueError: If `value` is not a positive integer.

        Returns:
            PageNumber: A random page number value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers import PageNumberMother

        number = PageNumberMother.create()
        print(number)
        # >>> 1
        ```
        """
        if value is not None:
            return PageNumber(value=value)

        return PageNumber(value=IntegerMother.positive())
