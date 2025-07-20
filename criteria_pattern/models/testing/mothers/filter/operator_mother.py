"""
OperatorMother module.
"""

from object_mother_pattern.models import EnumerationMother

from criteria_pattern import Operator


class OperatorMother(EnumerationMother[Operator]):
    """
    OperatorMother class is responsible for generating random Operator values.

    Example:
    ```python
    from criteria_pattern.models.testing.mothers.filter import OperatorMother

    operator = OperatorMother.create()
    print(operator)
    # >>> EQUAL
    ```
    """
