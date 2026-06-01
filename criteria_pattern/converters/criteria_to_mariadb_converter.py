"""
MariaDB SQL converter for Criteria objects.
"""

from .criteria_to_mysql_converter import CriteriaToMysqlConverter


class CriteriaToMariadbConverter(CriteriaToMysqlConverter):
    """
    Convert `Criteria` objects into MariaDB `SELECT` statements.

    MariaDB is highly compatible with MySQL, so this converter inherits MySQL rendering, validation, and positional
    parameter behavior. See `CriteriaToMysqlConverter.convert` for the full parameter reference, including allowlist and
    structural limit arguments such as `max_operator_allowlist` and `max_criteria_depth`. This separate class keeps the
    public API explicit and leaves room for future MariaDB-specific behavior.

    Example:
    ```python
    from criteria_pattern import Criteria, Filter, Operator
    from criteria_pattern.converters import CriteriaToMariadbConverter

    is_adult = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
    email_is_gmail = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@gmail.com')])
    email_is_yahoo = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@yahoo.com')])

    query, parameters = CriteriaToMariadbConverter.convert(
        criteria=is_adult & (email_is_gmail | email_is_yahoo),
        table='user',
        valid_columns=['age', 'email'],
        valid_operators=[Operator.GREATER_OR_EQUAL, Operator.ENDS_WITH],
    )
    print(query)
    print(parameters)
    # >>> SELECT * FROM `user` WHERE (`age` >= %s AND (`email` LIKE CONCAT('%%', %s) OR `email` LIKE CONCAT('%%', %s)));
    # >>> [18, '@gmail.com', '@yahoo.com']
    ```
    """  # noqa: E501  # fmt: skip
