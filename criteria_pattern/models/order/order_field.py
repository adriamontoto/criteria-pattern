"""
OrderField module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import Any, NoReturn

from value_object_pattern.usables import (
    NotEmptyStringValueObject,
    PrintableStringValueObject,
    TrimmedStringValueObject,
)

from criteria_pattern.errors import IntegrityError


class OrderField(NotEmptyStringValueObject, TrimmedStringValueObject, PrintableStringValueObject):
    """
    OrderField class.

    Example:
    ```python
    from criteria_pattern.models.order.order_field import OrderField

    field = OrderField(value='name')
    print(field)
    # >>> name
    ```
    """

    @override
    def _raise_value_is_not_string(self, value: Any) -> NoReturn:
        """
        Raises a IntegrityError if the value object `value` is not a string.

        Args:
            value (Any): The provided value.

        Raises:
            IntegrityError: If the `value` is not a string.
        """
        raise IntegrityError(message=f'StringValueObject value <<<{value}>>> must be a string. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    @override
    def _raise_value_is_empty_string(self, value: str) -> NoReturn:
        """
        Raises a IntegrityError if the value object `value` is an empty string.

        Args:
            value (str): The provided value.

        Raises:
            IntegrityError: If the `value` is an empty string.
        """
        raise IntegrityError(message=f'NotEmptyStringValueObject value <<<{value}>>> is an empty string. Only non-empty strings are allowed.')  # noqa: E501  # fmt: skip

    @override
    def _raise_value_is_not_trimmed(self, value: str) -> NoReturn:
        """
        Raises a IntegrityError if the value object `value` is not trimmed.

        Args:
            value (str): The provided value.

        Raises:
            IntegrityError: If the `value` is not trimmed.
        """
        raise IntegrityError(message=f'TrimmedStringValueObject value <<<{value}>>> contains leading or trailing whitespaces. Only trimmed values are allowed.')  # noqa: E501  # fmt: skip

    @override
    def _raise_value_is_not_printable(self, value: str) -> NoReturn:
        """
        Raises a IntegrityError if the value object `value` is not printable.

        Args:
            value (str): The provided value.

        Raises:
            IntegrityError: If the `value` is not printable.
        """
        raise IntegrityError(message=f'PrintableStringValueObject value <<<{value}>>> contains invalid characters. Only printable characters are allowed.')  # noqa: E501  # fmt: skip
