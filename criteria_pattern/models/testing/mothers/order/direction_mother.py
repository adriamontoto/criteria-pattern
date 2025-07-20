"""
DirectionMother module.
"""

from object_mother_pattern.models import EnumerationMother

from criteria_pattern import Direction


class DirectionMother(EnumerationMother[Direction]):
    """
    DirectionMother class is responsible for generating random direction values.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers.order import DirectionMother

    direction = DirectionMother.create()
    print(direction)
    # >>> ASC
    ```
    """
