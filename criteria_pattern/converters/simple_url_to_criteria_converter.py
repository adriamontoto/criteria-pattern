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
    from criteria_pattern.converters import SimpleUrlToCriteriaConverter

    url = 'https://api.example.com/users?name=Doe&age_ge=18&page_size=20&page_number=1'
    criteria = SimpleUrlToCriteriaConverter.convert(url=url)
    print(criteria)
    # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='Doe')), Filter(field=FilterField(value='age'), operator=FilterOperator(value=<Operator.GREATER_OR_EQUAL: 'GREATER_OR_EQUAL'>), value=FilterValue(value=18))], orders=[], page_size=20, page_number=1)
    ```
    """  # noqa: E501  # fmt: skip

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
        check_field_injection: bool = False,
        check_operator_injection: bool = False,
        check_pagination_bounds: bool = False,
        valid_fields: Sequence[str] | None = None,
        valid_operators: Sequence[Operator] | None = None,
        max_page_size: int = 10000,
        max_page_number: int = 1000000,
    ) -> Criteria:
        """
        Convert a URL or bare query string into criteria.

        `fields_mapping` translates public field names into internal field names. `suffix_operator_mapping` can add or
        override suffixes such as `_gte` or `_contains`. Validation flags check the parsed criteria against the provided
        allowlists.

        Args:
            url (str): The URL containing the query string.
            fields_mapping (Mapping[str, str], optional): Public field names mapped to internal field names.
            suffix_operator_mapping (Mapping[str, Operator], optional): Additional suffix-to-operator aliases.
            check_field_injection (bool, optional): Validate parsed fields against `valid_fields`.
            check_operator_injection (bool, optional): Validate parsed operators against `valid_operators`.
            check_pagination_bounds (bool, optional): Validate pagination values against configured maxima.
            valid_fields (Sequence[str], optional): Allowed parsed field names.
            valid_operators (Sequence[Operator], optional): Allowed parsed operators.
            max_page_size (int, optional): Maximum allowed page size when pagination validation is enabled.
            max_page_number (int, optional): Maximum allowed page number when pagination validation is enabled.

        Raises:
            IntegrityError: If a list operator has invalid values.
            InvalidColumnError: If an invalid field name is found in filters.
            InvalidOperatorError: If an invalid operator is found in filters.
            PaginationBoundsError: If pagination parameters exceed maximum bounds.

        Returns:
            Criteria: The parsed criteria.
        """
        valid_fields = valid_fields or []
        valid_operators = valid_operators or []
        fields_mapping = fields_mapping or {}
        suffix_operator_mapping = cls._build_suffix_operator_mapping(mapping=suffix_operator_mapping)

        query_parameters = cls._parse_query_parameters(url=url)
        filters = cls._parse_filters(
            query_parameters=query_parameters,
            fields_mapping=fields_mapping,
            suffix_operator_mapping=suffix_operator_mapping,
        )
        page_size = cls._parse_page_size(query_parameters=query_parameters)
        page_number = cls._parse_page_number(query_parameters=query_parameters)

        criteria = Criteria(filters=filters or None, page_size=page_size, page_number=page_number)

        if check_field_injection:
            cls._validate_fields(criteria=criteria, valid_fields=valid_fields)

        if check_operator_injection:
            cls._validate_operators(criteria=criteria, valid_operators=valid_operators)

        if check_pagination_bounds:
            cls._validate_pagination_bounds(
                criteria=criteria,
                max_page_size=max_page_size,
                max_page_number=max_page_number,
            )

        return criteria

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

            field_name, operator = cls._parse_filter_name(
                name=name,
                suffix_operator_mapping=suffix_operator_mapping,
            )
            actual_field = fields_mapping.get(field_name, field_name)

            try:
                parsed_value = cls._parse_filter_value(raw_values=values, operator=operator)

            except IntegrityError as exception:
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
    def _parse_filter_value(cls, *, raw_values: Sequence[str], operator: Operator) -> Any:
        """
        Parse the raw filter values based on the operator.

        Args:
            raw_values (Sequence[str]): The raw values from the query parameter.
            operator (Operator): The operator to use for parsing.

        Raises:
            IntegrityError: If raw values are invalid for the operator.

        Returns:
            Any: The parsed filter value.
        """
        if operator in (Operator.IS_NULL, Operator.IS_NOT_NULL):
            return None

        if operator in (Operator.BETWEEN, Operator.NOT_BETWEEN):
            return cls._parse_between_values(raw_values=raw_values)

        if operator in (Operator.IN, Operator.NOT_IN):
            return cls._parse_list_values(raw_values=raw_values)

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
    def _parse_list_values(cls, *, raw_values: Sequence[str]) -> list[Any]:
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

        return [cls._convert_primitive(value=part) for part in parts]

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
        values = query_parameters.get(cls._PAGE_SIZE_PARAMETER)
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
        """
        for field in criteria.filters:
            if field.field not in valid_fields:
                raise InvalidColumnError(column=field.field, valid_columns=valid_fields)

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
    def _validate_pagination_bounds(cls, *, criteria: Criteria, max_page_size: int, max_page_number: int) -> None:
        """
        Validate the Criteria object pagination parameters to prevent integer overflow.

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
