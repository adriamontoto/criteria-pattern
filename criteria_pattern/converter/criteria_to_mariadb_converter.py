"""
Criteria to MariaDB converter module.
"""

from .criteria_to_mysql_converter import CriteriaToMysqlConverter


class CriteriaToMariadbConverter(CriteriaToMysqlConverter):
    """
    Criteria to MariaDB converter.

    MariaDB is highly compatible with MySQL, so this converter inherits from the MySQL converter. This separate class
    allows for future MariaDB-specific optimizations or features.

    Example:
    ```python
    from criteria_pattern import Criteria, Filter, Operator
    from criteria_pattern.converter import CriteriaToMariadbConverter

    is_adult = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
    email_is_gmail = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@gmail.com')])
    email_is_yahoo = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@yahoo.com')])

    query, parameters = CriteriaToMariadbConverter.convert(criteria=is_adult & (email_is_gmail | email_is_yahoo), table='user')
    print(query)
    print(parameters)
    # >>> SELECT * FROM user WHERE (age >= %s AND (email LIKE CONCAT('%', %s) OR email LIKE CONCAT('%', %s)));
    # >>> [18, '@gmail.com', '@yahoo.com']
    ```
    """  # noqa: E501  # fmt: skip
