"""
FilterOperatorMother module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from object_mother_pattern.models import BaseMother

from criteria_pattern.models.filter import FilterOperator, Operator

from .operator_mother import OperatorMother


class FilterOperatorMother(BaseMother[FilterOperator]):
    """
    FilterOperatorMother class is responsible for generating random filter operator values.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers.filter import FilterOperatorMother

    operator = FilterOperatorMother.create()
    print(operator)
    # >>> EQUAL
    ```
    """

    @classmethod
    @override
    def create(cls, *, value: str | None = None) -> FilterOperator:
        """
        Create a random filter operator value. If a specific filter operator value is provided via `value`, it is
        returned after validation. Otherwise, a random filter operator value is generated.

        Args:
            value (str | None, optional): Filter operator value. Defaults to None.

        Raises:
            TypeError: If `value` is not an Operator.

        Returns:
            FilterOperator: A random filter operator value.

        Example:
        ```python
        from criteria_pattern.models.testing.mothers.filter import FilterOperatorMother

        operator = FilterOperatorMother.create()
        print(operator)
        # >>> EQUAL
        ```
        """
        if value is not None:
            return FilterOperator(value=value)

        return FilterOperator(
            value=OperatorMother.create(
                exclude=(
                    Operator.BETWEEN,
                    Operator.NOT_BETWEEN,
                    Operator.IN,
                    Operator.NOT_IN,
                )
            )
        )
