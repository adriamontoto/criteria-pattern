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
    from criteria_pattern import Direction, Operator
    from criteria_pattern.converters import UrlToCriteriaConverter

    url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=Doe&filters[1][field]=age&filters[1][operator]=GREATER_OR_EQUAL&filters[1][value]=18&orders[1][field]=age&orders[1][direction]=DESC'
    criteria = UrlToCriteriaConverter.convert(
        url=url,
        valid_fields=['name', 'age'],
        valid_operators=[Operator.EQUAL, Operator.GREATER_OR_EQUAL],
        valid_directions=[Direction.DESC],
    )
    print(criteria)
    # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='Doe')), Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER_OR_EQUAL: 'GREATER OR EQUAL'>), value=FilterValue(value=18))], orders=[Order(direction=OrderDirection(value=<Direction.DESC: 'DESC'>), field=OrderField(value='age'))], page_number=None, page_size=None)
    ```
    """  # noqa: E501  # fmt: skip

    DEFAULT_MAX_FILTERS = 100
    DEFAULT_MAX_ORDERS = 100
    DEFAULT_MAX_IN_VALUES = 100
    DEFAULT_MAX_PAGE_SIZE = 1000
    DEFAULT_MAX_PAGE_NUMBER = 10000
    DEFAULT_MAX_OPERATOR_ALLOWLIST = len(Operator)

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
        max_page_size: int = DEFAULT_MAX_PAGE_SIZE,
        max_page_number: int = DEFAULT_MAX_PAGE_NUMBER,
        max_filters: int = DEFAULT_MAX_FILTERS,
        max_orders: int = DEFAULT_MAX_ORDERS,
        max_in_values: int = DEFAULT_MAX_IN_VALUES,
        max_operator_allowlist: int = DEFAULT_MAX_OPERATOR_ALLOWLIST,
    ) -> Criteria:
        """
        Convert a URL containing structured query parameters into criteria.

        Validation is on by default. Each `valid_*` allowlist is complete; omitting it or passing `[]` denies that
        dimension. `fields_mapping` is applied before validation.

        Args:
            url (str): URL with bracketed parameters (`filters[n][field]`, `orders[n][direction]`, etc.).
            fields_mapping (Mapping[str, str], optional): Public field names mapped to internal names.
            check_field_injection (bool, optional): Validate fields against `valid_fields`. Default `True`.
            check_operator_injection (bool, optional): Validate operators against `valid_operators`. Default `True`.
            check_direction_injection (bool, optional): Validate directions against `valid_directions`. Default `True`.
            check_pagination_bounds (bool, optional): Cap `page_size` and `page_number`. Default `True`.
            valid_fields (Sequence[str], optional): Allowed field names after mapping; omitted or `[]` allows none.
            valid_operators (Sequence[Operator], optional): Allowed operators; omitted or `[]` allows none.
            valid_directions (Sequence[Direction], optional): Allowed directions; omitted or `[]` allows none.
            max_page_size (int, optional): Max `page_size`. Default `1000`.
            max_page_number (int, optional): Max `page_number`. Default `10000`.
            max_filters (int, optional): Max `filters[n]` entries. Default `100`.
            max_orders (int, optional): Max `orders[n]` entries. Default `100`.
            max_in_values (int, optional): Max values per `IN` / `NOT_IN` list. Default `100`.
            max_operator_allowlist (int, optional): Max size of `valid_operators` when set. Default `len(Operator)`.

        Raises:
            IntegrityError: Malformed query or exceeded a structural limit.
            InvalidColumnError: Field not allowed when `check_field_injection` is enabled.
            InvalidOperatorError: Operator not allowed when `check_operator_injection` is enabled.
            InvalidDirectionError: Direction not allowed when `check_direction_injection` is enabled.
            PaginationBoundsError: Pagination above maxima when bounds check is enabled.

        Returns:
            Criteria: Parsed criteria.

        Example:
        ```python
        from criteria_pattern import Direction, Operator
        from criteria_pattern.converters import UrlToCriteriaConverter

        url = 'https://api.example.com/users?filters[0][field]=name&filters[0][operator]=EQUAL&filters[0][value]=Doe&filters[1][field]=age&filters[1][operator]=GREATER_OR_EQUAL&filters[1][value]=18&orders[1][field]=age&orders[1][direction]=DESC'
        criteria = UrlToCriteriaConverter.convert(
            url=url,
            valid_fields=['name', 'age'],
            valid_operators=[Operator.EQUAL, Operator.GREATER_OR_EQUAL],
            valid_directions=[Direction.DESC],
        )
        print(criteria)
        # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='Doe')), Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER_OR_EQUAL: 'GREATER OR EQUAL'>), value=FilterValue(value=18))], orders=[Order(direction=OrderDirection(value=<Direction.DESC: 'DESC'>), field=OrderField(value='age'))], page_number=None, page_size=None)
        ```
        """  # noqa: E501  # fmt: skip
        fields_mapping = fields_mapping or {}
        query_params = parse_qs(qs=urlparse(url=url).query, keep_blank_values=True)

        filters = cls._parse_filters(
            query_parameters=query_params,
            fields_mapping=fields_mapping,
            max_filters=max_filters,
            max_in_values=max_in_values,
        )
        orders = cls._parse_orders(
            query_parameters=query_params,
            fields_mapping=fields_mapping,
            max_orders=max_orders,
        )
        page_size = cls._parse_page_size(query_parameters=query_params)
        page_number = cls._parse_page_number(query_parameters=query_params)

        criteria = Criteria(
            filters=filters or None,
            orders=orders or None,
            page_size=page_size,
            page_number=page_number,
        )

        if check_operator_injection and valid_operators is not None:
            cls._ensure_operator_allowlist_size(
                operators=valid_operators,
                limit=max_operator_allowlist,
            )

        if check_field_injection:
            cls._validate_criteria(
                criteria=criteria,
                columns_mapping={},
                valid_columns=list(valid_fields) if valid_fields is not None else [],
            )

        if check_operator_injection:
            cls._validate_operators(
                criteria=criteria,
                valid_operators=list(valid_operators) if valid_operators is not None else [],
            )

        if check_direction_injection:
            cls._validate_directions(
                criteria=criteria,
                valid_directions=list(valid_directions) if valid_directions is not None else [],
            )

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
    def _parse_filters(  # noqa: C901
        cls,
        *,
        query_parameters: Mapping[str, Sequence[str]],
        fields_mapping: Mapping[str, str],
        max_filters: int,
        max_in_values: int,
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

            cls._ensure_index_below_limit(
                index=index,
                limit=max_filters,
                resource=f'filter <<<filters[{index}]>>>',
            )

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
                parsed_value = cls._parse_filter_value(
                    raw_value=value_raw,
                    operator=operator,
                    max_in_values=max_in_values,
                )

            except IntegrityError as exception:
                if 'exceeds maximum limit' in str(exception):
                    raise
                raise IntegrityError(message=f'UrlToCriteriaConverter filter <<<filters[{idx}]>>> has invalid value <<<{value_raw}>>> for operator <<<{operator.value}>>>.') from exception  # noqa: E501  # fmt: skip

            actual_field = fields_mapping.get(field_name, field_name)
            filters.append(Filter(field=actual_field, operator=operator, value=parsed_value))

        return filters

    @classmethod
    def _parse_filter_value(cls, *, raw_value: str | None, operator: Operator, max_in_values: int) -> object:
        """
        Parse a raw filter value according to operator value-shape requirements.

        Args:
            raw_value (str | None): The raw value from the query parameter.
            operator (Operator): The operator to use for parsing.

        Raises:
            IntegrityError: If the raw value is missing.
            IntegrityError: If the raw value was expected to have two comma-separated values.

        Returns:
            object: The parsed filter value.
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

            parsed_values = [cls._convert_primitive(value=part) for part in parts]
            cls._ensure_sequence_size(
                values=parsed_values,
                limit=max_in_values,
                resource=f'IN values for filter <<<{raw_value}>>>',
            )
            return parsed_values

        return cls._convert_primitive(value=raw_value)

    @staticmethod
    def _convert_primitive(*, value: str) -> object:
        """
        Convert a raw string value to a primitive Python type.

        Args:
            value (str): The raw string value to convert.

        Returns:
            object: The converted primitive value.
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
        max_orders: int,
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

            cls._ensure_index_below_limit(
                index=index,
                limit=max_orders,
                resource=f'order <<<orders[{index}]>>>',
            )

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
            return values[0]  # type: ignore[ty:invalid-return-type]

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
            return values[0]  # type: ignore[ty:invalid-return-type]

    @classmethod
    def _ensure_index_below_limit(cls, *, index: int, limit: int, resource: str) -> None:
        """
        Ensure a zero-based collection index stays below a configured maximum.

        Args:
            index (int): Current index.
            limit (int): Maximum allowed count for the collection.
            resource (str): Human-readable resource name such as filters or orders.

        Raises:
            IntegrityError: If the index reaches or exceeds the limit.
        """
        if index >= limit:
            raise IntegrityError(
                message=f'{cls.__name__} {resource} exceeds maximum limit of <<<{limit}>>>.',
            )

    @classmethod
    def _ensure_sequence_size(cls, *, values: Sequence[Any], limit: int, resource: str) -> None:
        """
        Ensure a sequence does not exceed a configured maximum length.

        Args:
            values (Sequence[Any]): Values to validate.
            limit (int): Maximum allowed length.
            resource (str): Human-readable resource name such as IN values.

        Raises:
            IntegrityError: If the sequence exceeds the limit.
        """
        if len(values) > limit:
            raise IntegrityError(
                message=f'{cls.__name__} {resource} exceeds maximum limit of <<<{limit}>>>.',
            )

    @classmethod
    def _ensure_operator_allowlist_size(
        cls,
        *,
        operators: Sequence[Operator],
        limit: int,
    ) -> None:
        """
        Ensure an explicit operator allowlist does not exceed a configured maximum.

        Args:
            operators (Sequence[Operator]): Operator allowlist provided by the caller.
            limit (int): Maximum allowed operators in the allowlist.

        Raises:
            IntegrityError: If the allowlist exceeds the limit.
        """
        if len(operators) > limit:
            raise IntegrityError(
                message=f'{cls.__name__} valid_operators exceeds maximum limit of <<<{limit}>>>.',
            )
