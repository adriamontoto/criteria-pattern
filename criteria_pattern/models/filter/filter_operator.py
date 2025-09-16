"""
FilterOperator module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import Any, NoReturn

from value_object_pattern import EnumerationValueObject

from criteria_pattern.errors import IntegrityError

from .operator import Operator


class FilterOperator(EnumerationValueObject[Operator]):
    """
    FilterOperator class.

    Example:
    ```python
    from criteria_pattern.models.filter.filter_operator import FilterOperator

    operator = FilterOperator(value='EQUAL')
    print(operator)
    # >>> EQUAL
    ```
    """

    @override
    def _raise_value_is_not_from_enumeration(self, value: Any) -> NoReturn:
        """
        Raises a IntegrityError exception if the value is not from the enumeration.

        Args:
            value (Any): The provided value.

        Raises:
            IntegrityError: If the value is not from the enumeration.
        """
        raise IntegrityError(message=f'EnumerationValueObject value <<<{value}>>> must be from the enumeration <<<{self._enumeration.__name__}>>>. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
