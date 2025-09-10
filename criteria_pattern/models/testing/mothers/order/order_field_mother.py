"""
OrderFieldMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from object_mother_pattern.models import BaseMother
from object_mother_pattern.mothers import StringMother

from criteria_pattern.models.order import OrderField


class OrderFieldMother(BaseMother[OrderField]):
    """
    OrderFieldMother class is responsible for generating random order field values.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers.order import OrderFieldMother

    field = OrderFieldMother.create()
    print(field)
    # >>> zFUml6ODZq5wyG
    ```
    """

    @classmethod
    @override
    def create(cls, *, value: str | None = None) -> OrderField:
        """
        Create a random order field value. If a specific order field value is provided via `value`, it is returned
        after validation. Otherwise, a random order field value is generated.

        Args:
            value (str | None, optional): Order field value. Defaults to None.

        Raises:
            TypeError: If `value` is not a string.
            ValueError: If `value` is empty.
            ValueError: If `value` is not trimmed.
            ValueError: If `value` contains non-alphanumeric characters.

        Returns:
            OrderField: A random order field value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers.order import OrderFieldMother

        field = OrderFieldMother.create()
        print(field)
        # >>> zFUml6ODZq5wyG
        ```
        """
        if value is not None:
            return OrderField(value=value)

        return OrderField(value=StringMother.create(min_length=5))
