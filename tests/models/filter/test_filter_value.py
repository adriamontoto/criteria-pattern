"""
Test FilterValue value object.
"""

from typing import Any

from pytest import mark

from criteria_pattern.models.filter import FilterValue
from criteria_pattern.models.testing.mothers.filter import FilterValueMother


@mark.unit_testing
def test_filter_value_object_happy_path() -> None:
    """
    Test FilterValue object happy path.
    """
    value: FilterValue[Any] = FilterValueMother.create()
    filter = FilterValue(value=value)

    assert type(filter.value) is type(value)
    assert filter.value == value
