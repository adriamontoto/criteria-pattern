"""
Converter from flat URL query parameters to Criteria objects.
"""

from collections.abc import Mapping, Sequence
from typing import Any, ClassVar
from urllib.parse import parse_qs, urlparse

from criteria_pattern import Criteria, Filter, Operator
from criteria_pattern.errors import IntegrityError, InvalidColumnError, InvalidOperatorError, PaginationBoundsError


class SimpleUrlToCriteriaConverter:
    """
    Convert suffix-based URL query parameters into `Criteria` objects.

    Each non-pagination query parameter becomes a filter. A parameter suffix selects the operator, for example
    `age_ge=18` becomes `field='age'` with `Operator.GREATER_OR_EQUAL`; a parameter with no suffix uses equality.

    Example:
    ```python
    from criteria_pattern import Operator
    from criteria_pattern.converters import SimpleUrlToCriteriaConverter

    url = 'https://api.example.com/users?name=Doe&age_ge=18&page_size=20&page_number=1'
    criteria = SimpleUrlToCriteriaConverter.convert(
        url=url,
        valid_fields=['name', 'age'],
        valid_operators=[Operator.EQUAL, Operator.GREATER_OR_EQUAL],
    )
    print(criteria)
    # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='Doe')), Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER_OR_EQUAL: 'GREATER_OR_EQUAL'>), value=FilterValue(value=18))], orders=[], page_size=20, page_number=1)
    ```
    """  # noqa: E501  # fmt: skip

    DEFAULT_MAX_FILTERS = 100
    DEFAULT_MAX_IN_VALUES = 100
    DEFAULT_MAX_PAGE_SIZE = 1000
    DEFAULT_MAX_PAGE_NUMBER = 10000
    DEFAULT_MAX_OPERATOR_ALLOWLIST = len(Operator)

    _SUFFIX_OPERATOR_MAPPING: ClassVar[dict[str, Operator]] = {
        '': Operator.EQUAL,
        'eq': Operator.EQUAL,
        'ne': Operator.NOT_EQUAL,
        'gt': Operator.GREATER,
        'ge': Operator.GREATER_OR_EQUAL,
        'gte': Operator.GREATER_OR_EQUAL,
        'lt': Operator.LESS,
        'le': Operator.LESS_OR_EQUAL,
        'lte': Operator.LESS_OR_EQUAL,
        'like': Operator.LIKE,
        'not_like': Operator.NOT_LIKE,
        'contains': Operator.CONTAINS,
        'not_contains': Operator.NOT_CONTAINS,
        'starts_with': Operator.STARTS_WITH,
        'not_starts_with': Operator.NOT_STARTS_WITH,
        'ends_with': Operator.ENDS_WITH,
        'not_ends_with': Operator.NOT_ENDS_WITH,
        'between': Operator.BETWEEN,
        'not_between': Operator.NOT_BETWEEN,
        'is_null': Operator.IS_NULL,
        'is_not_null': Operator.IS_NOT_NULL,
        'in': Operator.IN,
        'not_in': Operator.NOT_IN,
    }

    _PAGE_SIZE_PARAMETER: ClassVar[str] = 'page_size'
    _PAGE_NUMBER_PARAMETER: ClassVar[str] = 'page_number'
    _PAGINATION_PARAMETERS: ClassVar[set[str]] = {_PAGE_SIZE_PARAMETER, _PAGE_NUMBER_PARAMETER}

    @classmethod
    def convert(
        cls,
        *,
        url: str,
        fields_mapping: Mapping[str, str] | None = None,
        suffix_operator_mapping: Mapping[str, Operator] | None = None,
        check_field_injection: bool = True,
        check_operator_injection: bool = True,
        check_pagination_bounds: bool = True,
        valid_fields: Sequence[str] | None = None,
        valid_operators: Sequence[Operator] | None = None,
        max_page_size: int = DEFAULT_MAX_PAGE_SIZE,
        max_page_number: int = DEFAULT_MAX_PAGE_NUMBER,
        max_filters: int = DEFAULT_MAX_FILTERS,
        max_in_values: int = DEFAULT_MAX_IN_VALUES,
        max_operator_allowlist: int = DEFAULT_MAX_OPERATOR_ALLOWLIST,
    ) -> Criteria:
        """
        Convert a URL or bare query string into criteria.

        Validation is on by default. Each `valid_*` allowlist is complete; omitting it or passing `[]` denies that
        dimension. Does not parse orders. Mapping arguments apply before validation.

        Args:
            url (str): URL or query string; each non-pagination parameter becomes an `AND` filter.
            fields_mapping (Mapping[str, str], optional): Public field names mapped to internal names.
            suffix_operator_mapping (Mapping[str, Operator], optional): Extra suffix aliases (for example `_gte`).
            check_field_injection (bool, optional): Validate fields against `valid_fields`. Default `True`.
            check_operator_injection (bool, optional): Validate operators against `valid_operators`. Default `True`.
            check_pagination_bounds (bool, optional): Cap `page_size` and `page_number`. Default `True`.
            valid_fields (Sequence[str], optional): Allowed field names after mapping; omitted or `[]` allows none.
            valid_operators (Sequence[Operator], optional): Allowed operators; omitted or `[]` allows none.
            max_page_size (int, optional): Max `page_size`. Default `1000`.
            max_page_number (int, optional): Max `page_number`. Default `10000`.
            max_filters (int, optional): Max filter parameters (excluding pagination keys). Default `100`.
            max_in_values (int, optional): Max values per `IN` / `NOT_IN` list. Default `100`.
            max_operator_allowlist (int, optional): Max size of `valid_operators` when set. Default `len(Operator)`.

        Raises:
            IntegrityError: Unparseable parameter or exceeded a structural limit.
            InvalidColumnError: Field not allowed when `check_field_injection` is enabled.
            InvalidOperatorError: Operator not allowed when `check_operator_injection` is enabled.
            PaginationBoundsError: Pagination above maxima when bounds check is enabled.

        Returns:
            Criteria: Parsed criteria.
        """
        fields_mapping = fields_mapping or {}
        suffix_operator_mapping = cls._build_suffix_operator_mapping(mapping=suffix_operator_mapping)
        query_parameters = cls._parse_query_parameters(url=url)
        filters = cls._parse_filters(
            query_parameters=query_parameters,
            fields_mapping=fields_mapping,
            suffix_operator_mapping=suffix_operator_mapping,
            max_filters=max_filters,
            max_in_values=max_in_values,
        )
        page_size = cls._parse_page_size(query_parameters=query_parameters)
        page_number = cls._parse_page_number(query_parameters=query_parameters)

        criteria = Criteria(filters=filters or None, page_size=page_size, page_number=page_number)

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
    def _build_suffix_operator_mapping(cls, *, mapping: Mapping[str, Operator] | None) -> dict[str, Operator]:
        """
        Build the normalized suffix-to-operator mapping.

        Args:
            mapping (Mapping[str, Operator], optional): Custom suffix operator mapping.

        Returns:
            dict[str, Operator]: The normalized suffix operator mapping.
        """
        suffix_operator_mapping = {
            cls._normalize_suffix(suffix=suffix): operator for suffix, operator in cls._SUFFIX_OPERATOR_MAPPING.items()
        }

        for suffix, operator in (mapping or {}).items():
            suffix_operator_mapping[cls._normalize_suffix(suffix=suffix)] = operator

        return suffix_operator_mapping

    @staticmethod
    def _normalize_suffix(*, suffix: str) -> str:
        """
        Normalize a suffix key.

        Args:
            suffix (str): The suffix to normalize.

        Returns:
            str: The normalized suffix.
        """
        return suffix.strip().lower().removeprefix('_')

    @staticmethod
    def _parse_query_parameters(*, url: str) -> dict[str, list[str]]:
        """
        Parse query parameters from a URL or a bare query string.

        Args:
            url (str): The URL or query string to parse.

        Returns:
            dict[str, list[str]]: The parsed query parameters.
        """
        query = urlparse(url=url).query
        if query:
            return parse_qs(qs=query, keep_blank_values=True)

        query = url.removeprefix('?').split('#', maxsplit=1)[0]
        if '=' in query or '&' in query:
            return parse_qs(qs=query, keep_blank_values=True)

        return {}

    @classmethod
    def _parse_filters(
        cls,
        *,
        query_parameters: Mapping[str, Sequence[str]],
        fields_mapping: Mapping[str, str],
        suffix_operator_mapping: Mapping[str, Operator],
        max_filters: int,
        max_in_values: int,
    ) -> list[Filter[Any]]:
        """
        Parse simple query parameters into `Filter` objects.

        Args:
            query_parameters (Mapping[str, Sequence[str]]): The query parameters from the URL.
            fields_mapping (Mapping[str, str]): The mapping of external to internal field names.
            suffix_operator_mapping (Mapping[str, Operator]): The suffix operator mapping.

        Raises:
            IntegrityError: If a filter value is invalid for its operator.

        Returns:
            list[Filter[Any]]: The parsed filters.
        """
        filters: list[Filter[Any]] = []

        for name, values in query_parameters.items():
            if name in cls._PAGINATION_PARAMETERS:
                continue

            cls._ensure_index_below_limit(
                index=len(filters),
                limit=max_filters,
                resource='filters',
            )

            field_name, operator = cls._parse_filter_name(
                name=name,
                suffix_operator_mapping=suffix_operator_mapping,
            )
            actual_field = fields_mapping.get(field_name, field_name)

            try:
                parsed_value = cls._parse_filter_value(
                    raw_values=values,
                    operator=operator,
                    max_in_values=max_in_values,
                )

            except IntegrityError as exception:
                if 'exceeds maximum limit' in str(exception):
                    raise
                raw_value = ','.join(values)
                raise IntegrityError(
                    message=f'SimpleUrlToCriteriaConverter filter <<<{name}>>> has invalid value <<<{raw_value}>>> for operator <<<{operator.value}>>>.'  # noqa: E501
                ) from exception

            filters.append(Filter(field=actual_field, operator=operator, value=parsed_value))

        return filters

    @classmethod
    def _parse_filter_name(
        cls,
        *,
        name: str,
        suffix_operator_mapping: Mapping[str, Operator],
    ) -> tuple[str, Operator]:
        """
        Parse a filter query parameter name into a field and operator.

        Args:
            name (str): The query parameter name.
            suffix_operator_mapping (Mapping[str, Operator]): The suffix operator mapping.

        Returns:
            tuple[str, Operator]: The field name and operator.
        """
        normalized_name = name.lower()
        for suffix in sorted((suffix for suffix in suffix_operator_mapping if suffix), key=len, reverse=True):
            token = f'_{suffix}'
            if normalized_name.endswith(token):
                return name[: -len(token)], suffix_operator_mapping[suffix]

        return name, suffix_operator_mapping['']

    @classmethod
    def _parse_filter_value(cls, *, raw_values: Sequence[str], operator: Operator, max_in_values: int) -> object:
        """
        Parse the raw filter values based on the operator.

        Args:
            raw_values (Sequence[str]): The raw values from the query parameter.
            operator (Operator): The operator to use for parsing.

        Raises:
            IntegrityError: If raw values are invalid for the operator.

        Returns:
            object: The parsed filter value.
        """
        if operator in (Operator.IS_NULL, Operator.IS_NOT_NULL):
            return None

        if operator in (Operator.BETWEEN, Operator.NOT_BETWEEN):
            return cls._parse_between_values(raw_values=raw_values)

        if operator in (Operator.IN, Operator.NOT_IN):
            return cls._parse_list_values(raw_values=raw_values, max_in_values=max_in_values)

        return cls._convert_primitive(value=raw_values[0])

    @classmethod
    def _parse_between_values(cls, *, raw_values: Sequence[str]) -> list[Any]:
        """
        Parse between operator values.

        Args:
            raw_values (Sequence[str]): The raw values from the query parameter.

        Raises:
            IntegrityError: If exactly two values are not provided.

        Returns:
            list[Any]: The parsed between values.
        """
        parts = cls._split_values(raw_values=raw_values, keep_empty=True)
        if len(parts) != 2:
            raise IntegrityError(
                message=f'SimpleUrlToCriteriaConverter filter <<<{",".join(raw_values)}>>> expects exactly two values.'
            )

        return [cls._convert_primitive(value=part) for part in parts]

    @classmethod
    def _parse_list_values(cls, *, raw_values: Sequence[str], max_in_values: int) -> list[Any]:
        """
        Parse IN and NOT_IN operator values.

        Args:
            raw_values (Sequence[str]): The raw values from the query parameter.

        Raises:
            IntegrityError: If at least one value is not provided.

        Returns:
            list[Any]: The parsed list values.
        """
        parts = cls._split_values(raw_values=raw_values, keep_empty=False)
        if not parts:
            raise IntegrityError(
                message=f'SimpleUrlToCriteriaConverter filter <<<{",".join(raw_values)}>>> expects at least one value.'
            )

        parsed_values = [cls._convert_primitive(value=part) for part in parts]
        cls._ensure_sequence_size(
            values=parsed_values,
            limit=max_in_values,
            resource=f'IN values for filter <<<{",".join(raw_values)}>>>',
        )
        return parsed_values

    @staticmethod
    def _split_values(*, raw_values: Sequence[str], keep_empty: bool) -> list[str]:
        """
        Split raw query parameter values by commas.

        Args:
            raw_values (Sequence[str]): The raw values from the query parameter.
            keep_empty (bool): Whether empty values should be kept.

        Returns:
            list[str]: The split values.
        """
        parts: list[str] = []
        for raw_value in raw_values:
            for part in raw_value.split(','):
                stripped_part = part.strip()
                if keep_empty or stripped_part:
                    parts.append(stripped_part)

        return parts

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
    def _parse_page_number(cls, *, query_parameters: Mapping[str, Sequence[str]]) -> int | None:
        """
        Parse the 'page_number' query parameter.

        Args:
            query_parameters (Mapping[str, Sequence[str]]): The query parameters from the URL.

        Returns:
            int | None: The parsed page number or None if not present.
        """
        values = query_parameters.get(cls._PAGE_NUMBER_PARAMETER)
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
        values = query_parameters.get(cls._PAGE_SIZE_PARAMETER)
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
