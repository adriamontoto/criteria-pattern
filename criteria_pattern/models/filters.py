"""
Filters module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from typing import Any, NoReturn

from value_object_pattern.models.collections import ListValueObject

from criteria_pattern.errors import IntegrityError

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

    def __init__(self, *, value: list[Filter[Any]], title: str | None = None, parameter: str | None = None) -> None:
        """
        Initialize a list of filters.

        Args:
            value (list[Filter]): The list of filters.
            title (str | None, optional): The title of the filters. Default is None.
            parameter (str | None, optional): The parameter name of the filters. Default is None.

        Example:
        ```python
        from criteria_pattern.models import Filter, Operator
        from criteria_pattern.models.filters import Filters

        filters = Filters(value=[Filter(field='name', operator=Operator.EQUAL, value='John')])
        print(filters)
        # >>> ['Filter(field=name, operator=EQUAL, value=John)']
        ```
        """
        super().__init__(value=value, title=title, parameter=parameter)

    @override
    def _raise_value_is_not_list(self, value: Any) -> NoReturn:
        """
        Raises a IntegrityError if the value object `value` is not a list.

        Args:
            value (Any): The provided value.

        Raises:
            IntegrityError: If the `value` is not a list.
        """
        raise IntegrityError(message=f'ListValueObject value <<<{value}>>> must be a list. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip  # pragma: no cover

    @override
    def _raise_value_is_not_of_type(self, value: Any) -> NoReturn:
        """
        Raises a IntegrityError if the value object `value` is not of type `T`.

        Args:
            value (Any): The provided value.

        Raises:
            IntegrityError: If the `value` is not of type `T`.
        """
        raise IntegrityError(message=f'ListValueObject value <<<{value}>>> must be of type <<<{self._type.__name__}>>> type. Got <<<{type(value).__name__}>>> type.')  # type: ignore[attr-defined]  # noqa: E501  # fmt: skip
