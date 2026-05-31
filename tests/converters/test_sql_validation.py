"""
Test shared SQL validation helpers.
"""

from pytest import mark, raises as assert_raises

from criteria_pattern import Criteria, Filter, Operator
from criteria_pattern.converters.criteria_to_mysql_converter import CriteriaToMysqlConverter
from criteria_pattern.errors import InvalidColumnError


@mark.unit_testing
def test_validate_criteria_rejects_unmapped_sql_column() -> None:
    """
    Test criteria validation rejects mapped SQL columns that are not allowlisted.
    """
    criteria = Criteria(filters=[Filter(field='public_name', operator=Operator.EQUAL, value='Doe')])

    with assert_raises(
        expected_exception=InvalidColumnError,
        match='Invalid column specified <<<secret_column>>>. Valid columns are <<<public_name>>>.',
    ):
        CriteriaToMysqlConverter._validate_criteria(
            criteria=criteria,
            columns_mapping={'public_name': 'secret_column'},
            valid_columns=['public_name'],
        )
