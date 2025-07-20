"""
OrderDirectionMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from object_mother_pattern.models import BaseMother

from criteria_pattern.models.order import OrderDirection

from .direction_mother import DirectionMother


class OrderDirectionMother(BaseMother[OrderDirection]):
    """
    OrderDirectionMother class is responsible for generating random order direction values.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers.order import OrderDirectionMother

    direction = OrderDirectionMother.create()
    print(direction)
    # >>> ASC
    ```
    """

    @classmethod
    @override
    def create(cls, *, value: str | None = None) -> OrderDirection:
        """
        Create a random direction value. If a specific direction value is provided via `value`, it is
        returned after validation. Otherwise, a random direction value is generated.

        Args:
            value (str | None, optional): Direction value. Defaults to None.

        Raises:
            TypeError: If `value` is not a Direction.

        Returns:
            OrderDirection: A random direction value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers.order import OrderDirectionMother

        direction = OrderDirectionMother.create()
        print(direction)
        # >>> ASC
        ```
        """
        if value is not None:
            return OrderDirection(value=value)

        return OrderDirection(value=DirectionMother.create())
