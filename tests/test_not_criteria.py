"""
Test the NotCriteria class.
"""

from criteria_pattern.criteria import NotCriteria
from tests.mother import CriteriaMother


def test_not_criteria_string_representation() -> None:
    """
    Test that the string representation of NotCriteria class is correct.
    """
    criteria = NotCriteria(criteria=CriteriaMother.create())

    assert repr(criteria) == f'<NotCriteria(criteria=<Criteria(filters={criteria.filters}, orders={criteria.orders})>)>'


def test_not_criteria_not_operator() -> None:
    """
    Test the NotCriteria class not operator.
    """
    assert isinstance(~CriteriaMother.create(), NotCriteria)


def test_not_criteria_not_method() -> None:
    """
    Test the NotCriteria class not method.
    """
    assert isinstance(CriteriaMother.create().not_(), NotCriteria)
