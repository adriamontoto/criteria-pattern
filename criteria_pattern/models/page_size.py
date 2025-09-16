"""
PageSize module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import Any, NoReturn

from value_object_pattern.usables import PositiveIntegerValueObject

from criteria_pattern.errors import IntegrityError


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

    @override
    def _raise_value_is_not_integer(self, value: Any) -> NoReturn:
        """
        Raises a IntegrityError if the value object `value` is not an integer.

        Args:
            value (Any): The provided value.

        Raises:
            IntegrityError: If the `value` is not an integer.
        """
        raise IntegrityError(message=f'IntegerValueObject value <<<{value}>>> must be an integer. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    @override
    def _raise_value_is_not_positive_integer(self, value: int) -> NoReturn:
        """
        Raises a IntegrityError if the value object `value` is not a positive integer.

        Args:
            value (int): The provided value.

        Raises:
            IntegrityError: If the `value` is not a positive integer.
        """
        raise IntegrityError(message=f'PositiveIntegerValueObject value <<<{value}>>> must be a positive integer.')
