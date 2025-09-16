"""
Test Filters model.
"""

from object_mother_pattern.models import BaseMother
from pytest import mark, raises as assert_raises

from criteria_pattern.errors import IntegrityError
from criteria_pattern.models.filter import Filter
from criteria_pattern.models.filters import Filters
from criteria_pattern.models.testing.mothers import FiltersMother


@mark.unit_testing
def test_orders_model_happy_path() -> None:
    """
    Test Filters model happy path.
    """
    orders_value = FiltersMother.create()
    filters = Filters(value=orders_value.value)

    assert type(filters.value) is list
    for filter in filters.value:
        assert type(filter) is Filter


@mark.unit_testing
def test_orders_model_empty() -> None:
    """
    Test Filters model with empty value.
    """
    filters = Filters(value=[])

    assert type(filters.value) is list
    assert len(filters.value) == 0


@mark.unit_testing
def test_orders_model_invalid_type_raises_type_error() -> None:
    """
    Test Filters model with invalid type raises IntegrityError.
    """
    with assert_raises(
        expected_exception=IntegrityError,
        match=r'Filters value <<<.*>>> must be of type <<<Filter>>> type. Got <<<.*>>> type.',
    ):
        Filters(value=[BaseMother.invalid_type()])
