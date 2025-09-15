"""
Url to criteria converter.
"""

from collections.abc import Mapping, Sequence
from re import Pattern, compile as re_compile
from typing import Any, ClassVar
from urllib.parse import parse_qs, unquote_plus, urlparse

from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.errors import InvalidColumnError, InvalidDirectionError, InvalidOperatorError


class UrlToCriteriaConverter:
    """
    Converts a URL query string into a Criteria object.

    Example:
    ```python
    from criteria_pattern.converters import UrlToCriteriaConverter

    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=Doe&filters[1][field]=age&filters[1][operator]=GREATER_OR_EQUAL&filters[1][value]=18&orders[1][field]=age&orders[1][direction]=DESC'
    criteria = UrlToCriteriaConverter.convert(url=url)
    print(criteria)
    # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='Doe')), Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER_OR_EQUAL: 'GREATER OR EQUAL'>), value=FilterValue(value=18))], orders=[Order(direction=OrderDirection(value=<Direction.DESC: 'DESC'>), field=OrderField(value='age'))], page_number=None, page_size=None)
    ```
    """  # noqa: E501  # fmt: skip

    _OPERATOR_MAPPING: ClassVar[dict[str, Operator]] = {
        'EQUAL': Operator.EQUAL,
        'NOT_EQUAL': Operator.NOT_EQUAL,
        'GREATER': Operator.GREATER,
        'GREATER_OR_EQUAL': Operator.GREATER_OR_EQUAL,
        'LESS': Operator.LESS,
        'LESS_OR_EQUAL': Operator.LESS_OR_EQUAL,
        'LIKE': Operator.LIKE,
        'NOT_LIKE': Operator.NOT_LIKE,
        'CONTAINS': Operator.CONTAINS,
        'NOT_CONTAINS': Operator.NOT_CONTAINS,
        'STARTS_WITH': Operator.STARTS_WITH,
        'NOT_STARTS_WITH': Operator.NOT_STARTS_WITH,
        'ENDS_WITH': Operator.ENDS_WITH,
        'NOT_ENDS_WITH': Operator.NOT_ENDS_WITH,
        'BETWEEN': Operator.BETWEEN,
        'NOT_BETWEEN': Operator.NOT_BETWEEN,
        'IS_NULL': Operator.IS_NULL,
        'IS_NOT_NULL': Operator.IS_NOT_NULL,
        'IN': Operator.IN,
        'NOT_IN': Operator.NOT_IN,
    }

    _DIRECTION_MAPPING: ClassVar[dict[str, Direction]] = {
        'ASC': Direction.ASC,
        'DESC': Direction.DESC,
    }

    _MAX_FIELDS: ClassVar[int] = 100
    _FILTERS_REGEX: ClassVar[Pattern[str]] = re_compile(pattern=r'^filters\[(\w+)]\[(\w+)]$')
    _ORDERS_REGEX: ClassVar[Pattern[str]] = re_compile(pattern=r'^orders\[(\w+)]\[(\w+)]$')

    @classmethod
    def convert(
        cls,
        *,
        url: str,
        fields_mapping: Mapping[str, str] | None = None,
        check_field_injection: bool = False,
        check_operator_injection: bool = False,
        check_direction_injection: bool = False,
        valid_fields: Sequence[str] | None = None,
        valid_operators: Sequence[Operator] | None = None,
        valid_directions: Sequence[Direction] | None = None,
    ) -> Criteria:
        """
        Converts an URL query string into a Criteria object.

        Args:
            url (str): The URL containing the query string.
            fields_mapping (Mapping[str, str], optional): Mapping of field names to aliases. Default to empty dict.
            check_field_injection (bool, optional): Whether to check for field injection.
            check_operator_injection (bool, optional): Whether to check for operator injection.
            check_direction_injection (bool, optional): Whether to check for direction injection.
            valid_fields (Sequence[str], optional): A list of valid field names. Default to empty list.
            valid_operators (Sequence[Operator], optional): A list of valid operators. Default to empty list.
            valid_directions (Sequence[Direction], optional): A list of valid directions. Default to empty list.

        Raises:
            TypeError: If the filter index is not an integer.
            ValueError: If the filter has missing field.
            ValueError: If the filter has missing operator.
            ValueError: If the filter has unsupported operator.
            ValueError: If the filter has missing value.
            TypeError: If the order index is not an integer.
            ValueError: If the order has missing field.
            ValueError: If the order has missing direction.
            ValueError: If the order has unsupported direction.
            InvalidColumnError: If an invalid field name is found in filters.
            InvalidColumnError: If an invalid field name is found in orders.
            InvalidOperatorError: If an invalid operator is found in filters.
            InvalidDirectionError: If an invalid direction is found in orders.

        Example:
        ```python
        from criteria_pattern.converters import UrlToCriteriaConverter

        url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=Doe&filters[1][field]=age&filters[1][operator]=GREATER_OR_EQUAL&filters[1][value]=18&orders[1][field]=age&orders[1][direction]=DESC'
        criteria = UrlToCriteriaConverter.convert(url=url)
        print(criteria)
        # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='Doe')), Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER_OR_EQUAL: 'GREATER OR EQUAL'>), value=FilterValue(value=18))], orders=[Order(direction=OrderDirection(value=<Direction.DESC: 'DESC'>), field=OrderField(value='age'))], page_number=None, page_size=None)
        ```
        """  # noqa: E501  # fmt: skip
        valid_fields = valid_fields or []
        fields_mapping = fields_mapping or {}
        valid_operators = valid_operators or []
        valid_directions = valid_directions or []

        query_params = parse_qs(qs=urlparse(url=url).query, keep_blank_values=True)

        filters = cls._parse_filters(query_parameters=query_params, fields_mapping=fields_mapping)
        orders = cls._parse_orders(query_parameters=query_params, fields_mapping=fields_mapping)
        page_size = cls._parse_page_size(query_parameters=query_params)
        page_number = cls._parse_page_number(query_parameters=query_params)

        criteria = Criteria(
            filters=filters or None,
            orders=orders or None,
            page_size=page_size,
            page_number=page_number,
        )

        if check_field_injection:
            cls._validate_fields(criteria=criteria, valid_fields=valid_fields)

        if check_operator_injection:
            cls._validate_operators(criteria=criteria, valid_operators=valid_operators)

        if check_direction_injection:
            cls._validate_directions(criteria=criteria, valid_directions=valid_directions)

        return criteria

    @classmethod
    def _parse_filters(  # noqa: C901
        cls,
        *,
        query_parameters: Mapping[str, Sequence[str]],
        fields_mapping: Mapping[str, str],
    ) -> list[Filter[Any]]:
        """
        Parse the 'filters' query parameters.

        Args:
            query_parameters (Mapping[str, Sequence[str]]): The query parameters from the URL.
            fields_mapping (Mapping[str, str]): The mapping of external to internal field names.

        Raises:
            TypeError: If the filter index is not an integer.
            ValueError: If the filter has missing field.
            ValueError: If the filter has missing operator.
            ValueError: If the filter has unsupported operator.
            ValueError: If the filter has missing value.

        Returns:
            list[Filter]: The parsed list of filter criteria.
        """
        filters: list[Filter[Any]] = []
        bucket: dict[int, dict[str, str]] = {}

        for name, values in query_parameters.items():
            match = cls._FILTERS_REGEX.match(string=name)
            if not match or not values:
                continue

            index_string, key = match.groups()
            try:
                index = int(index_string)

            except ValueError as exception:
                raise TypeError(f'UrlToCriteriaConverter filter <<<filters[{index_string}]>>> must be an integer.') from exception  # noqa: E501  # fmt: skip

            if index >= cls._MAX_FIELDS:
                raise ValueError(f'UrlToCriteriaConverter filter <<<filters[{index}]>>> exceeds maximum limit of <<<{cls._MAX_FIELDS}>>>.')  # noqa: E501  # fmt: skip

            bucket.setdefault(index, {})[key] = values[0]

        for idx in sorted(bucket):
            field_name = bucket[idx].get('field')
            if field_name is None:
                raise ValueError(f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has missing field.')

            operator_raw = bucket[idx].get('operator')
            if operator_raw is None:
                raise ValueError(f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has missing operator.')

            value_raw = bucket[idx].get('value')
            if value_raw is None:
                raise ValueError(f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has missing value.')

            operator_key = operator_raw.upper().strip()
            operator = cls._OPERATOR_MAPPING.get(operator_key)
            if not operator:
                raise ValueError(f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has unsupported operator <<<{operator_raw}>>>.')  # noqa: E501  # fmt: skip

            try:
                parsed_value = cls._parse_filter_value(raw_value=value_raw, operator=operator)

            except ValueError as exception:
                raise ValueError(f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has invalid value <<<{value_raw}>>> for operator <<<{operator.value}>>>.') from exception  # noqa: E501  # fmt: skip

            actual_field = fields_mapping.get(field_name, field_name)
            filters.append(Filter(field=actual_field, operator=operator, value=parsed_value))

        return filters

    @classmethod
    def _parse_filter_value(cls, *, raw_value: str | None, operator: Operator) -> Any:
        """
        Parse the raw filter value based on the operator.

        Args:
            raw_value (str | None): The raw value from the query parameter.
            operator (Operator): The operator to use for parsing.

        Raises:
            ValueError: If the raw value is missing.
            ValueError: If the raw value was expected to have two comma-separated values.

        Returns:
            Any: The parsed filter value.
        """
        if operator in (Operator.IS_NULL, Operator.IS_NOT_NULL):
            return None

        if raw_value is None:
            raise ValueError('UrlToCriteriaConverter filter has missing value.')  # pragma: no cover

        raw_value = unquote_plus(string=raw_value)
        if operator in (Operator.BETWEEN, Operator.NOT_BETWEEN):
            parts = [part.strip() for part in raw_value.split(',')]
            if len(parts) != 2:
                raise ValueError(f'UrlToCriteriaConverter filter <<<{raw_value}>>> expects exactly two comma-separated values.')  # noqa: E501  # fmt: skip

            return [cls._convert_primitive(value=part) for part in parts]

        if operator in (Operator.IN, Operator.NOT_IN):
            parts = [part.strip() for part in raw_value.split(',') if part.strip()]
            if not parts:
                raise ValueError(f'UrlToCriteriaConverter filter <<<{raw_value}>>> expects at least one comma-separated value.')  # noqa: E501  # fmt: skip

            return [cls._convert_primitive(value=part) for part in parts]

        return cls._convert_primitive(value=raw_value)

    @staticmethod
    def _convert_primitive(*, value: str) -> Any:
        """
        Convert a raw string value to a primitive Python type.

        Args:
            value (str): The raw string value to convert.

        Returns:
            Any: The converted primitive value.
        """
        lower_value = value.lower()
        if lower_value in ('true', 'false'):
            return lower_value == 'true'

        if lower_value in ('null', 'none'):
            return None

        if value == '':
            return ''

        try:
            return int(value)

        except ValueError:
            pass

        try:
            return float(value)

        except ValueError:
            pass

        return value

    @classmethod
    def _parse_orders(
        cls,
        *,
        query_parameters: Mapping[str, Sequence[str]],
        fields_mapping: Mapping[str, str],
    ) -> list[Order]:
        """
        Parse the 'orders' query parameters.

        Args:
            query_parameters (Mapping[str, Sequence[str]]): The query parameters from the URL.
            fields_mapping (Mapping[str, str]): The mapping of external to internal field names.

        Raises:
            TypeError: If the order index is not an integer.
            ValueError: If the order has missing field.
            ValueError: If the order has missing direction.
            ValueError: If the order has unsupported direction.

        Returns:
            list[Order]: The parsed list of order criteria.
        """
        orders: list[Order] = []
        bucket: dict[int, dict[str, str]] = {}

        for name, values in query_parameters.items():
            match = cls._ORDERS_REGEX.match(string=name)
            if not match or not values:
                continue

            index_string, key = match.groups()
            try:
                index = int(index_string)

            except ValueError as exception:
                raise TypeError(f'UrlToCriteriaConverter order <<<orders[{index_string}]>>> must be an integer.') from exception  # noqa: E501  # fmt: skip

            if index >= cls._MAX_FIELDS:
                raise ValueError(f'UrlToCriteriaConverter order <<<orders[{index}]>>> exceeds maximum limit of <<<{cls._MAX_FIELDS}>>>.')  # noqa: E501  # fmt: skip

            bucket.setdefault(index, {})[key] = values[0]

        for idx in sorted(bucket):
            field_name = bucket[idx].get('field')
            if field_name is None:
                raise ValueError(f'UrlToCriteriaConverter order <<<orders[{idx}]>>> has missing field.')

            direction_raw = bucket[idx].get('direction')
            if direction_raw is None:
                raise ValueError(f'UrlToCriteriaConverter order <<<orders[{idx}]>>> has missing direction.')

            direction_key = direction_raw.upper().strip()
            direction = cls._DIRECTION_MAPPING.get(direction_key)
            if not direction:
                raise ValueError(f'UrlToCriteriaConverter order <<<orders[{idx}]>>> has unsupported direction <<<{direction_raw}>>>.')  # noqa: E501  # fmt: skip

            actual_field = fields_mapping.get(field_name, field_name)
            orders.append(Order(field=actual_field, direction=direction))

        return orders

    @classmethod
    def _parse_page_number(cls, *, query_parameters: Mapping[str, Sequence[str]]) -> int | None:
        """
        Parse the 'page_number' query parameter.

        Args:
            query_parameters (Mapping[str, Sequence[str]]): The query parameters from the URL.

        Returns:
            int | None: The parsed page number or None if not present.
        """
        values = query_parameters.get('page_number')
        if not values:
            return None

        try:
            return int(values[0])

        except ValueError:
            return values[0]  # type: ignore[return-value]

    @classmethod
    def _parse_page_size(cls, *, query_parameters: Mapping[str, Sequence[str]]) -> int | None:
        """
        Parse the 'page_size' query parameter.

        Args:
            query_parameters (Mapping[str, Sequence[str]]): The query parameters from the URL.

        Returns:
            int | None: The parsed page size or None if not present.
        """
        values = query_parameters.get('page_size')
        if not values:
            return None

        try:
            return int(values[0])

        except ValueError:
            return values[0]  # type: ignore[return-value]

    @classmethod
    def _validate_fields(cls, *, criteria: Criteria, valid_fields: Sequence[str]) -> None:
        """
        Validate that all field names in the criteria are allowed.

        Args:
            criteria (Criteria): The criteria to validate.
            valid_fields (Sequence[str]): The sequence of valid field names.

        Raises:
            InvalidColumnError: If an invalid field name is found in filters.
            InvalidColumnError: If an invalid field name is found in orders.
        """
        for field in criteria.filters:
            if field.field not in valid_fields:
                raise InvalidColumnError(column=field.field, valid_columns=valid_fields)

        for order in criteria.orders:
            if order.field not in valid_fields:
                raise InvalidColumnError(column=order.field, valid_columns=valid_fields)

    @classmethod
    def _validate_operators(cls, *, criteria: Criteria, valid_operators: Sequence[Operator]) -> None:
        """
        Validate the Criteria object operators to prevent injection.

        Args:
            criteria (Criteria): Criteria to validate.
            valid_operators (Sequence[Operator]): List of valid operators to use.

        Raises:
            InvalidOperatorError: If the operator is not in the list of valid operators.
        """
        for filter in criteria.filters:
            if filter.operator not in valid_operators:
                raise InvalidOperatorError(operator=Operator(value=filter.operator), valid_operators=valid_operators)

    @classmethod
    def _validate_directions(cls, *, criteria: Criteria, valid_directions: Sequence[Direction]) -> None:
        """
        Validate the Criteria object directions to prevent injection.

        Args:
            criteria (Criteria): Criteria to validate.
            valid_directions (Sequence[Direction]): List of valid directions to use.

        Raises:
            InvalidDirectionError: If the direction is not in the list of valid directions.
        """
        for order in criteria.orders:
            if order.direction not in valid_directions:
                raise InvalidDirectionError(
                    direction=Direction(value=order.direction),
                    valid_directions=valid_directions,
                )
