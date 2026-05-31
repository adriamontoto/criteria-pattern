"""
Converter from structured URL query parameters to Criteria objects.
"""

from collections.abc import Mapping, Sequence
from re import Pattern, compile as re_compile
from typing import Any, ClassVar
from urllib.parse import parse_qs, unquote_plus, urlparse

from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.errors import (
    IntegrityError,
    InvalidColumnError,
    InvalidDirectionError,
    InvalidOperatorError,
    PaginationBoundsError,
)


class UrlToCriteriaConverter:
    """
    Convert structured URL query parameters into `Criteria` objects.

    The converter expects bracketed parameter names such as `filters[0][field]`, `filters[0][operator]`,
    `filters[0][value]`, `orders[0][field]`, and `orders[0][direction]`. Values are parsed into Python primitives where
    possible before filters are created.

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
        check_field_injection: bool = True,
        check_operator_injection: bool = True,
        check_direction_injection: bool = True,
        check_pagination_bounds: bool = True,
        valid_fields: Sequence[str] | None = None,
        valid_operators: Sequence[Operator] | None = None,
        valid_directions: Sequence[Direction] | None = None,
        max_page_size: int = 10000,
        max_page_number: int = 1000000,
    ) -> Criteria:
        """
        Convert a URL containing structured query parameters into criteria.

        `fields_mapping` translates public field names into internal field names before `Filter` and `Order` objects are
        created. Validation flags check the parsed criteria against the provided allowlists.

        Args:
            url (str): The URL containing the query string.
            fields_mapping (Mapping[str, str], optional): Public field names mapped to internal field names.
            check_field_injection (bool, optional): Validate parsed fields against `valid_fields`.
            check_operator_injection (bool, optional): Validate parsed operators against `valid_operators`.
            check_direction_injection (bool, optional): Validate parsed directions against `valid_directions`.
            check_pagination_bounds (bool, optional): Validate pagination values against configured maxima.
            valid_fields (Sequence[str], optional): Allowed parsed field names.
            valid_operators (Sequence[Operator], optional): Allowed parsed operators.
            valid_directions (Sequence[Direction], optional): Allowed parsed directions.
            max_page_size (int, optional): Maximum allowed page size when pagination validation is enabled.
            max_page_number (int, optional): Maximum allowed page number when pagination validation is enabled.

        Raises:
            IntegrityError: If the filter index is not an integer.
            IntegrityError: If the filter has missing field.
            IntegrityError: If the filter has missing operator.
            IntegrityError: If the filter has unsupported operator.
            IntegrityError: If the filter has missing value.
            IntegrityError: If the order index is not an integer.
            IntegrityError: If the order has missing field.
            IntegrityError: If the order has missing direction.
            IntegrityError: If the order has unsupported direction.
            InvalidColumnError: If an invalid field name is found in filters.
            InvalidColumnError: If an invalid field name is found in orders.
            InvalidOperatorError: If an invalid operator is found in filters.
            InvalidDirectionError: If an invalid direction is found in orders.
            PaginationBoundsError: If pagination parameters exceed maximum bounds.

        Example:
        ```python
        from criteria_pattern.converters import UrlToCriteriaConverter

        url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=Doe&filters[1][field]=age&filters[1][operator]=GREATER_OR_EQUAL&filters[1][value]=18&orders[1][field]=age&orders[1][direction]=DESC'
        criteria = UrlToCriteriaConverter.convert(url=url)
        print(criteria)
        # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='Doe')), Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER_OR_EQUAL: 'GREATER OR EQUAL'>), value=FilterValue(value=18))], orders=[Order(direction=OrderDirection(value=<Direction.DESC: 'DESC'>), field=OrderField(value='age'))], page_number=None, page_size=None)
        ```
        """  # noqa: E501  # fmt: skip
        fields_mapping = fields_mapping or {}

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

        effective_valid_fields = cls._default_valid_fields(criteria=criteria, valid_fields=valid_fields)
        effective_valid_operators = cls._default_valid_operators(
            criteria=criteria,
            valid_operators=valid_operators,
        )
        effective_valid_directions = cls._default_valid_directions(
            criteria=criteria,
            valid_directions=valid_directions,
        )

        if check_field_injection:
            cls._validate_criteria(
                criteria=criteria,
                columns_mapping={},
                valid_columns=effective_valid_fields,
            )

        if check_operator_injection:
            cls._validate_operators(criteria=criteria, valid_operators=effective_valid_operators)

        if check_direction_injection:
            cls._validate_directions(criteria=criteria, valid_directions=effective_valid_directions)

        if check_pagination_bounds:
            cls._validate_pagination_bounds(
                criteria=criteria,
                max_page_size=max_page_size,
                max_page_number=max_page_number,
            )

        return criteria

    @classmethod
    def _resolve_sql_column(cls, *, field: str, columns_mapping: Mapping[str, str]) -> str:
        """
        Resolve a criteria field to the SQL column used in generated queries.

        Args:
            field (str): Criteria field name.
            columns_mapping (Mapping[str, str]): Criteria field to SQL column mapping.

        Returns:
            str: SQL column name.
        """
        return columns_mapping.get(field, field)

    @classmethod
    def _validate_criteria(
        cls, *, criteria: Criteria, columns_mapping: Mapping[str, str], valid_columns: Sequence[str]
    ) -> None:
        """
        Validate criteria filter and order fields against an allowlist.

        Filter and order fields are validated after applying `columns_mapping`, so `valid_columns` must contain the SQL
        column names that will appear in the generated query.

        Args:
            criteria (Criteria): Criteria to validate.
            columns_mapping (Mapping[str, str]): Mapping of criteria fields to SQL columns.
            valid_columns (Sequence[str]): Allowed SQL column names.

        Raises:
            InvalidColumnError: If a resolved field maps to a column that is not allowed.
        """
        for filter in criteria.filters:
            column = cls._resolve_sql_column(field=filter.field, columns_mapping=columns_mapping)
            if column not in valid_columns:
                raise InvalidColumnError(column=column, valid_columns=valid_columns)
        for order in criteria.orders:
            column = cls._resolve_sql_column(field=order.field, columns_mapping=columns_mapping)
            if column not in valid_columns:
                raise InvalidColumnError(column=column, valid_columns=valid_columns)

    @classmethod
    def _validate_operators(cls, *, criteria: Criteria, valid_operators: Sequence[Operator]) -> None:
        """
        Validate criteria filter operators against an allowlist.

        Args:
            criteria (Criteria): Criteria to validate.
            valid_operators (Sequence[Operator]): Allowed operators.

        Raises:
            InvalidOperatorError: If an operator is not allowed.
        """
        for filter in criteria.filters:
            if filter.operator not in valid_operators:
                raise InvalidOperatorError(operator=Operator(value=filter.operator), valid_operators=valid_operators)

    @classmethod
    def _validate_directions(cls, *, criteria: Criteria, valid_directions: Sequence[Direction]) -> None:
        """
        Validate criteria order directions against an allowlist.

        Args:
            criteria (Criteria): Criteria to validate.
            valid_directions (Sequence[Direction]): Allowed directions.

        Raises:
            InvalidDirectionError: If a direction is not allowed.
        """
        for order in criteria.orders:
            if order.direction not in valid_directions:
                raise InvalidDirectionError(
                    direction=Direction(value=order.direction), valid_directions=valid_directions
                )

    @classmethod
    def _validate_pagination_bounds(cls, *, criteria: Criteria, max_page_size: int, max_page_number: int) -> None:
        """
        Validate pagination parameters against configured maxima.

        Args:
            criteria (Criteria): Criteria to validate.
            max_page_size (int): Maximum allowed page_size.
            max_page_number (int): Maximum allowed page_number.

        Raises:
            PaginationBoundsError: If pagination parameters exceed maximum bounds.
        """
        if criteria.page_size is not None and criteria.page_size > max_page_size:
            raise PaginationBoundsError(parameter='page_size', value=criteria.page_size, max_value=max_page_size)
        if criteria.page_number is not None and criteria.page_number > max_page_number:
            raise PaginationBoundsError(parameter='page_number', value=criteria.page_number, max_value=max_page_number)

    @classmethod
    def _default_valid_fields(cls, *, criteria: Criteria, valid_fields: Sequence[str] | None) -> list[str]:
        """
        Build the effective request field allowlist.

        When `valid_fields` is omitted, allowlisted fields are derived from the parsed criteria. That default is
        intended for trusted, application-built requests. For user-controlled request data, pass an explicit
        `valid_fields` allowlist.

        Args:
            criteria (Criteria): Parsed criteria.
            valid_fields (Sequence[str] | None): Caller-provided allowlist.

        Returns:
            list[str]: Effective field allowlist.
        """
        if valid_fields is not None:
            return list(valid_fields)
        fields = {filter.field for filter in criteria.filters}
        fields.update(order.field for order in criteria.orders)
        return sorted(fields)

    @classmethod
    def _default_valid_operators(
        cls, *, criteria: Criteria, valid_operators: Sequence[Operator] | None
    ) -> list[Operator]:
        """
        Build the effective operator allowlist.

        Args:
            criteria (Criteria): Criteria being converted.
            valid_operators (Sequence[Operator] | None): Caller-provided allowlist.

        Returns:
            list[Operator]: Effective operator allowlist.
        """
        if valid_operators is not None:
            return list(valid_operators)
        return sorted(
            {Operator(value=filter.operator) for filter in criteria.filters}, key=lambda operator: operator.value
        )

    @classmethod
    def _default_valid_directions(
        cls, *, criteria: Criteria, valid_directions: Sequence[Direction] | None
    ) -> list[Direction]:
        """
        Build the effective direction allowlist.

        Args:
            criteria (Criteria): Criteria being converted.
            valid_directions (Sequence[Direction] | None): Caller-provided allowlist.

        Returns:
            list[Direction]: Effective direction allowlist.
        """
        if valid_directions is not None:
            return list(valid_directions)
        directions = {Direction(value=order.direction) for order in criteria.orders}
        if directions:
            return sorted(directions, key=lambda direction: direction.value)
        return [Direction.ASC, Direction.DESC]

    @classmethod
    def _parse_filters(  # noqa: C901
        cls,
        *,
        query_parameters: Mapping[str, Sequence[str]],
        fields_mapping: Mapping[str, str],
    ) -> list[Filter[Any]]:
        """
        Parse bracketed filter query parameters into `Filter` objects.

        Args:
            query_parameters (Mapping[str, Sequence[str]]): The query parameters from the URL.
            fields_mapping (Mapping[str, str]): The mapping of external to internal field names.

        Raises:
            IntegrityError: If the filter index is not an integer.
            IntegrityError: If the filter has missing field.
            IntegrityError: If the filter has missing operator.
            IntegrityError: If the filter has unsupported operator.
            IntegrityError: If the filter has missing value.

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
                raise IntegrityError(message=f'UrlToCriteriaConverter filter <<<filters[{index_string}]>>> must be an integer.') from exception  # noqa: E501  # fmt: skip

            if index >= cls._MAX_FIELDS:
                raise IntegrityError(message=f'UrlToCriteriaConverter filter <<<filters[{index}]>>> exceeds maximum limit of <<<{cls._MAX_FIELDS}>>>.')  # noqa: E501  # fmt: skip

            bucket.setdefault(index, {})[key] = values[0]

        for idx in sorted(bucket):
            field_name = bucket[idx].get('field')
            if field_name is None:
                raise IntegrityError(message=f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has missing field.')

            operator_raw = bucket[idx].get('operator')
            if operator_raw is None:
                raise IntegrityError(message=f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has missing operator.')  # noqa: E501  # fmt: skip

            value_raw = bucket[idx].get('value')
            if value_raw is None:
                raise IntegrityError(message=f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has missing value.')

            operator_key = operator_raw.upper().strip()
            operator = cls._OPERATOR_MAPPING.get(operator_key)
            if not operator:
                raise IntegrityError(message=f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has unsupported operator <<<{operator_raw}>>>.')  # noqa: E501  # fmt: skip

            try:
                parsed_value = cls._parse_filter_value(raw_value=value_raw, operator=operator)

            except IntegrityError as exception:
                raise IntegrityError(message=f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has invalid value <<<{value_raw}>>> for operator <<<{operator.value}>>>.') from exception  # noqa: E501  # fmt: skip

            actual_field = fields_mapping.get(field_name, field_name)
            filters.append(Filter(field=actual_field, operator=operator, value=parsed_value))

        return filters

    @classmethod
    def _parse_filter_value(cls, *, raw_value: str | None, operator: Operator) -> Any:
        """
        Parse a raw filter value according to operator value-shape requirements.

        Args:
            raw_value (str | None): The raw value from the query parameter.
            operator (Operator): The operator to use for parsing.

        Raises:
            IntegrityError: If the raw value is missing.
            IntegrityError: If the raw value was expected to have two comma-separated values.

        Returns:
            Any: The parsed filter value.
        """
        if operator in (Operator.IS_NULL, Operator.IS_NOT_NULL):
            return None

        if raw_value is None:
            raise IntegrityError(message='UrlToCriteriaConverter filter has missing value.')  # pragma: no cover

        raw_value = unquote_plus(string=raw_value)
        if operator in (Operator.BETWEEN, Operator.NOT_BETWEEN):
            parts = [part.strip() for part in raw_value.split(',')]
            if len(parts) != 2:
                raise IntegrityError(message=f'UrlToCriteriaConverter filter <<<{raw_value}>>> expects exactly two comma-separated values.')  # noqa: E501  # fmt: skip

            return [cls._convert_primitive(value=part) for part in parts]

        if operator in (Operator.IN, Operator.NOT_IN):
            parts = [part.strip() for part in raw_value.split(',') if part.strip()]
            if not parts:
                raise IntegrityError(message=f'UrlToCriteriaConverter filter <<<{raw_value}>>> expects at least one comma-separated value.')  # noqa: E501  # fmt: skip

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
            IntegrityError: If the order index is not an integer.
            IntegrityError: If the order has missing field.
            IntegrityError: If the order has missing direction.
            IntegrityError: If the order has unsupported direction.

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
                raise IntegrityError(message=f'UrlToCriteriaConverter order <<<orders[{index_string}]>>> must be an integer.') from exception  # noqa: E501  # fmt: skip

            if index >= cls._MAX_FIELDS:
                raise IntegrityError(message=f'UrlToCriteriaConverter order <<<orders[{index}]>>> exceeds maximum limit of <<<{cls._MAX_FIELDS}>>>.')  # noqa: E501  # fmt: skip

            bucket.setdefault(index, {})[key] = values[0]

        for idx in sorted(bucket):
            field_name = bucket[idx].get('field')
            if field_name is None:
                raise IntegrityError(message=f'UrlToCriteriaConverter order <<<orders[{idx}]>>> has missing field.')

            direction_raw = bucket[idx].get('direction')
            if direction_raw is None:
                raise IntegrityError(message=f'UrlToCriteriaConverter order <<<orders[{idx}]>>> has missing direction.')

            direction_key = direction_raw.upper().strip()
            direction = cls._DIRECTION_MAPPING.get(direction_key)
            if not direction:
                raise IntegrityError(message=f'UrlToCriteriaConverter order <<<orders[{idx}]>>> has unsupported direction <<<{direction_raw}>>>.')  # noqa: E501  # fmt: skip

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
