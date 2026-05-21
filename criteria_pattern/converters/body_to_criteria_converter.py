"""
Converter from decoded request bodies to Criteria objects.
"""

from collections.abc import Mapping, Sequence
from typing import Any, ClassVar, cast

from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.errors import (
    IntegrityError,
    InvalidColumnError,
    InvalidDirectionError,
    InvalidOperatorError,
    PaginationBoundsError,
)


class BodyToCriteriaConverter:
    """
    Convert mapping-based request bodies into `Criteria` objects.

    The expected body shape is a mapping with optional `filters`, `orders`, `page_size`, and `page_number` keys. Filters
    and orders are parsed from lists of dictionaries, with optional field and operator alias mapping before validation.

    Example:
    ```python
    from criteria_pattern.converters import BodyToCriteriaConverter

    body = {
        'filters': [
            {'field': 'name', 'operator': 'EQUAL', 'value': 'Doe'},
            {'field': 'price', 'operator': 'GREATER_THAN', 'value': 10},
        ],
        'page_size': 20,
        'page_number': 1,
    }
    criteria = BodyToCriteriaConverter.convert(body=body)
    print(criteria)
    # >>> Criteria(filters=[Filter(field=FilterField(value='name'), operator=FilterOperator(value=<Operator.EQUAL: 'EQUAL'>), value=FilterValue(value='Doe')), Filter(field=FilterField(value='price'), operator=FilterOperator(value=<Operator.GREATER: 'GREATER'>), value=FilterValue(value=10))], orders=[], page_size=20, page_number=1)
    ```
    """  # noqa: E501  # fmt: skip

    _ALLOWED_BODY_KEYS: ClassVar[set[str]] = {'filters', 'orders', 'page_size', 'page_number'}
    _FILTER_KEYS: ClassVar[set[str]] = {'field', 'operator', 'value'}
    _ORDER_KEYS: ClassVar[set[str]] = {'field', 'direction'}
    _MISSING: ClassVar[object] = object()
    _OPERATOR_MAPPING: ClassVar[dict[str, Operator]] = {
        'EQUAL': Operator.EQUAL,
        'EQ': Operator.EQUAL,
        'NOT_EQUAL': Operator.NOT_EQUAL,
        'NE': Operator.NOT_EQUAL,
        'GREATER': Operator.GREATER,
        'GREATER_THAN': Operator.GREATER,
        'GT': Operator.GREATER,
        'GREATER_OR_EQUAL': Operator.GREATER_OR_EQUAL,
        'GREATER_THAN_OR_EQUAL': Operator.GREATER_OR_EQUAL,
        'GREATER_THAN_OR_EQUALS': Operator.GREATER_OR_EQUAL,
        'GREATER_EQUAL': Operator.GREATER_OR_EQUAL,
        'GTE': Operator.GREATER_OR_EQUAL,
        'GE': Operator.GREATER_OR_EQUAL,
        'LESS': Operator.LESS,
        'LESS_THAN': Operator.LESS,
        'LT': Operator.LESS,
        'LESS_OR_EQUAL': Operator.LESS_OR_EQUAL,
        'LESS_THAN_OR_EQUAL': Operator.LESS_OR_EQUAL,
        'LESS_THAN_OR_EQUALS': Operator.LESS_OR_EQUAL,
        'LESS_EQUAL': Operator.LESS_OR_EQUAL,
        'LTE': Operator.LESS_OR_EQUAL,
        'LE': Operator.LESS_OR_EQUAL,
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

    @classmethod
    def convert(
        cls,
        *,
        body: Mapping[str, Any],
        fields_mapping: Mapping[str, str] | None = None,
        operator_mapping: Mapping[str, Operator] | None = None,
        check_field_injection: bool = False,
        check_operator_injection: bool = False,
        check_direction_injection: bool = False,
        check_pagination_bounds: bool = False,
        valid_fields: Sequence[str] | None = None,
        valid_operators: Sequence[Operator] | None = None,
        valid_directions: Sequence[Direction] | None = None,
        max_page_size: int = 10000,
        max_page_number: int = 1000000,
    ) -> Criteria:
        """
        Convert a decoded body mapping into criteria.

        `fields_mapping` translates public field names into internal field names before `Filter` and `Order` objects are
        created. `operator_mapping` can add or override accepted operator aliases. Validation flags check the parsed
        criteria against the provided allowlists.

        Args:
            body (Mapping[str, Any]): The decoded body dictionary.
            fields_mapping (Mapping[str, str], optional): Public field names mapped to internal field names.
            operator_mapping (Mapping[str, Operator], optional): Additional accepted operator aliases.
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
            IntegrityError: If the body shape is invalid.
            InvalidColumnError: If an invalid field name is found in filters or orders.
            InvalidOperatorError: If an invalid operator is found in filters.
            InvalidDirectionError: If an invalid direction is found in orders.
            PaginationBoundsError: If pagination parameters exceed maximum bounds.

        Returns:
            Criteria: The parsed criteria.
        """
        valid_fields = valid_fields or []
        valid_operators = valid_operators or []
        valid_directions = valid_directions or []
        fields_mapping = fields_mapping or {}
        operator_mapping = cls._build_operator_mapping(mapping=operator_mapping)
        body_mapping = cls._validate_body(body=body)

        criteria = Criteria(
            filters=cls._parse_filters(
                value=body_mapping.get('filters'),
                fields_mapping=fields_mapping,
                operator_mapping=operator_mapping,
            )
            or None,
            orders=cls._parse_orders(value=body_mapping.get('orders'), fields_mapping=fields_mapping) or None,
            page_size=body_mapping.get('page_size'),
            page_number=body_mapping.get('page_number'),
        )

        if check_field_injection:
            cls._validate_fields(criteria=criteria, valid_fields=valid_fields)

        if check_operator_injection:
            cls._validate_operators(criteria=criteria, valid_operators=valid_operators)

        if check_direction_injection:
            cls._validate_directions(criteria=criteria, valid_directions=valid_directions)

        if check_pagination_bounds:
            cls._validate_pagination_bounds(
                criteria=criteria,
                max_page_size=max_page_size,
                max_page_number=max_page_number,
            )

        return criteria

    @classmethod
    def _validate_body(cls, *, body: Mapping[str, Any]) -> Mapping[str, Any]:
        """
        Validate the body mapping.

        Args:
            body (Mapping[str, Any]): The decoded body dictionary.

        Raises:
            IntegrityError: If the body is not a mapping or has invalid keys.

        Returns:
            Mapping[str, Any]: The validated body mapping.
        """
        body_object: object = body
        if not isinstance(body_object, Mapping):
            raise IntegrityError(
                message=f'BodyToCriteriaConverter body <<<{body_object}>>> must be a mapping. Got <<<{type(body_object).__name__}>>> type.'  # noqa: E501
            )

        body_mapping = body_object
        invalid_keys = [key for key in body_mapping if not isinstance(key, str)]
        if invalid_keys:
            raise IntegrityError(
                message=f'BodyToCriteriaConverter body keys <<<{", ".join(str(key) for key in invalid_keys)}>>> must be strings.'  # noqa: E501
            )

        typed_body = cast(Mapping[str, Any], body_mapping)
        cls._validate_keys(
            keys=set(typed_body),
            allowed_keys=cls._ALLOWED_BODY_KEYS,
            required_keys=set(),
            path='body',
        )
        return typed_body

    @classmethod
    def _build_operator_mapping(cls, *, mapping: Mapping[str, Operator] | None) -> dict[str, Operator]:
        """
        Build the normalized operator alias mapping.

        Args:
            mapping (Mapping[str, Operator], optional): Custom operator mapping.

        Returns:
            dict[str, Operator]: The normalized operator mapping.
        """
        operator_mapping = {
            cls._normalize_operator_key(operator=operator): operator for operator in cls._OPERATOR_MAPPING.values()
        }
        operator_mapping.update(
            {cls._normalize_operator_key(operator=alias): operator for alias, operator in cls._OPERATOR_MAPPING.items()}
        )

        for alias, operator in (mapping or {}).items():
            operator_mapping[cls._normalize_operator_key(operator=alias)] = operator

        return operator_mapping

    @staticmethod
    def _normalize_operator_key(*, operator: str) -> str:
        """
        Normalize an operator alias for case-insensitive lookup.

        Args:
            operator (str): The operator key to normalize.

        Returns:
            str: The normalized operator key.
        """
        return operator.strip().upper().replace(' ', '_').replace('-', '_')

    @classmethod
    def _parse_filters(
        cls,
        *,
        value: Any,
        fields_mapping: Mapping[str, str],
        operator_mapping: Mapping[str, Operator],
    ) -> list[Filter[Any]]:
        """
        Parse body filters into `Filter` objects.

        Args:
            value (Any): The raw filters body value.
            fields_mapping (Mapping[str, str]): The mapping of external to internal field names.
            operator_mapping (Mapping[str, Operator]): The operator mapping.

        Raises:
            IntegrityError: If filters are invalid.

        Returns:
            list[Filter[Any]]: The parsed filters.
        """
        if value is None:
            return []

        if not isinstance(value, list):
            raise IntegrityError(
                message=f'BodyToCriteriaConverter filters <<<{value}>>> must be a list. Got <<<{type(value).__name__}>>> type.'  # noqa: E501
            )

        filters: list[Filter[Any]] = []
        for index, item in enumerate(value):
            filter_body = cls._validate_filter_body(value=item, index=index)
            operator = cls._parse_operator(
                value=filter_body['operator'], index=index, operator_mapping=operator_mapping
            )
            raw_field = filter_body['field']
            field = fields_mapping.get(raw_field, raw_field) if isinstance(raw_field, str) else raw_field
            filters.append(
                Filter.from_primitives(
                    primitives={
                        'field': field,
                        'operator': operator,
                        'value': cls._parse_filter_value(
                            value=filter_body.get('value', cls._MISSING),
                            operator=operator,
                            index=index,
                        ),
                    }
                )
            )

        return filters

    @classmethod
    def _validate_filter_body(cls, *, value: Any, index: int) -> Mapping[str, Any]:
        """
        Validate a filter body.

        Args:
            value (Any): The raw filter body value.
            index (int): The filter index.

        Raises:
            IntegrityError: If the filter body is invalid.

        Returns:
            Mapping[str, Any]: The validated filter body.
        """
        filter_body = cls._ensure_mapping(value=value, path=f'filters[{index}]')
        cls._validate_keys(
            keys=set(filter_body),
            allowed_keys=cls._FILTER_KEYS,
            required_keys={'field', 'operator'},
            path=f'filters[{index}]',
        )
        return filter_body

    @classmethod
    def _parse_operator(
        cls,
        *,
        value: Any,
        index: int,
        operator_mapping: Mapping[str, Operator],
    ) -> Operator:
        """
        Parse a filter operator.

        Args:
            value (Any): The raw operator value.
            index (int): The filter index.
            operator_mapping (Mapping[str, Operator]): The operator mapping.

        Raises:
            IntegrityError: If the operator is unsupported.

        Returns:
            Operator: The parsed operator.
        """
        if isinstance(value, Operator):
            return value

        if not isinstance(value, str):
            raise IntegrityError(
                message=f'BodyToCriteriaConverter filter <<<filters[{index}]>>> has unsupported operator <<<{value}>>>.'  # noqa: E501
            )

        operator = operator_mapping.get(cls._normalize_operator_key(operator=value))
        if operator is None:
            raise IntegrityError(
                message=f'BodyToCriteriaConverter filter <<<filters[{index}]>>> has unsupported operator <<<{value}>>>.'  # noqa: E501
            )

        return operator

    @classmethod
    def _parse_filter_value(cls, *, value: Any, operator: Operator, index: int) -> Any:
        """
        Parse a filter value according to operator value-shape requirements.

        Args:
            value (Any): The raw filter value.
            operator (Operator): The parsed operator.
            index (int): The filter index.

        Raises:
            IntegrityError: If the filter value is invalid.

        Returns:
            Any: The parsed filter value.
        """
        if operator in (Operator.IS_NULL, Operator.IS_NOT_NULL):
            return None

        if value is cls._MISSING:
            raise IntegrityError(message=f'BodyToCriteriaConverter filter <<<filters[{index}]>>> has missing value.')

        if operator in (Operator.BETWEEN, Operator.NOT_BETWEEN):
            return cls._parse_between_value(value=value, index=index)

        if operator in (Operator.IN, Operator.NOT_IN):
            return cls._parse_list_value(value=value, index=index)

        return value

    @staticmethod
    def _parse_between_value(*, value: Any, index: int) -> list[Any]:
        """
        Parse a BETWEEN filter value.

        Args:
            value (Any): The raw filter value.
            index (int): The filter index.

        Raises:
            IntegrityError: If exactly two values are not provided.

        Returns:
            list[Any]: The parsed BETWEEN values.
        """
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise IntegrityError(
                message=f'BodyToCriteriaConverter filter <<<filters[{index}]>>> expects exactly two values for BETWEEN operators.'  # noqa: E501
            )

        return list(value)

    @staticmethod
    def _parse_list_value(*, value: Any, index: int) -> list[Any]:
        """
        Parse an IN filter value.

        Args:
            value (Any): The raw filter value.
            index (int): The filter index.

        Raises:
            IntegrityError: If at least one list value is not provided.

        Returns:
            list[Any]: The parsed list values.
        """
        if not isinstance(value, (list, tuple)) or not value:
            raise IntegrityError(
                message=f'BodyToCriteriaConverter filter <<<filters[{index}]>>> expects at least one value for IN operators.'  # noqa: E501
            )

        return list(value)

    @classmethod
    def _parse_orders(cls, *, value: Any, fields_mapping: Mapping[str, str]) -> list[Order]:
        """
        Parse body orders into `Order` objects.

        Args:
            value (Any): The raw orders body value.
            fields_mapping (Mapping[str, str]): The mapping of external to internal field names.

        Raises:
            IntegrityError: If orders are invalid.

        Returns:
            list[Order]: The parsed orders.
        """
        if value is None:
            return []

        if not isinstance(value, list):
            raise IntegrityError(
                message=f'BodyToCriteriaConverter orders <<<{value}>>> must be a list. Got <<<{type(value).__name__}>>> type.'  # noqa: E501
            )

        orders: list[Order] = []
        for index, item in enumerate(value):
            order_body = cls._validate_order_body(value=item, index=index)
            raw_field = order_body['field']
            field = fields_mapping.get(raw_field, raw_field) if isinstance(raw_field, str) else raw_field
            orders.append(
                Order.from_primitives(
                    primitives={
                        'field': field,
                        'direction': cls._parse_direction(value=order_body['direction'], index=index),
                    }
                )
            )

        return orders

    @classmethod
    def _validate_order_body(cls, *, value: Any, index: int) -> Mapping[str, Any]:
        """
        Validate an order body.

        Args:
            value (Any): The raw order body value.
            index (int): The order index.

        Raises:
            IntegrityError: If the order body is invalid.

        Returns:
            Mapping[str, Any]: The validated order body.
        """
        order_body = cls._ensure_mapping(value=value, path=f'orders[{index}]')
        cls._validate_keys(
            keys=set(order_body),
            allowed_keys=cls._ORDER_KEYS,
            required_keys=cls._ORDER_KEYS,
            path=f'orders[{index}]',
        )
        return order_body

    @classmethod
    def _parse_direction(cls, *, value: Any, index: int) -> Direction:
        """
        Parse an order direction.

        Args:
            value (Any): The raw direction value.
            index (int): The order index.

        Raises:
            IntegrityError: If the direction is unsupported.

        Returns:
            Direction: The parsed direction.
        """
        if isinstance(value, Direction):
            return value

        if not isinstance(value, str):
            raise IntegrityError(
                message=f'BodyToCriteriaConverter order <<<orders[{index}]>>> has unsupported direction <<<{value}>>>.'  # noqa: E501
            )

        direction = cls._DIRECTION_MAPPING.get(value.strip().upper())
        if direction is None:
            raise IntegrityError(
                message=f'BodyToCriteriaConverter order <<<orders[{index}]>>> has unsupported direction <<<{value}>>>.'  # noqa: E501
            )

        return direction

    @classmethod
    def _ensure_mapping(cls, *, value: Any, path: str) -> Mapping[str, Any]:
        """
        Ensure a nested body value is a mapping.

        Args:
            value (Any): The nested value.
            path (str): The nested body path.

        Raises:
            IntegrityError: If the value is not a mapping or has non-string keys.

        Returns:
            Mapping[str, Any]: The validated mapping.
        """
        if not isinstance(value, Mapping):
            raise IntegrityError(
                message=f'BodyToCriteriaConverter {path} <<<{value}>>> must be a mapping. Got <<<{type(value).__name__}>>> type.'  # noqa: E501
            )

        invalid_keys = [key for key in value if not isinstance(key, str)]
        if invalid_keys:
            raise IntegrityError(
                message=f'BodyToCriteriaConverter {path} keys <<<{", ".join(str(key) for key in invalid_keys)}>>> must be strings.'  # noqa: E501
            )

        return cast(Mapping[str, Any], value)

    @staticmethod
    def _validate_keys(*, keys: set[str], allowed_keys: set[str], required_keys: set[str], path: str) -> None:
        """
        Validate mapping keys.

        Args:
            keys (set[str]): The provided keys.
            allowed_keys (set[str]): The allowed keys.
            required_keys (set[str]): The required keys.
            path (str): The body path.

        Raises:
            IntegrityError: If required keys are missing or unknown keys are provided.
        """
        missing_keys = required_keys - keys
        if missing_keys:
            raise IntegrityError(
                message=f'BodyToCriteriaConverter {path} has missing keys <<<{", ".join(sorted(missing_keys))}>>>.'
            )

        unknown_keys = keys - allowed_keys
        if unknown_keys:
            raise IntegrityError(
                message=f'BodyToCriteriaConverter {path} has unsupported keys <<<{", ".join(sorted(unknown_keys))}>>>.'
            )

    @classmethod
    def _validate_fields(cls, *, criteria: Criteria, valid_fields: Sequence[str]) -> None:
        """
        Validate that all field names in the criteria are allowed.

        Args:
            criteria (Criteria): The criteria to validate.
            valid_fields (Sequence[str]): The sequence of valid field names.

        Raises:
            InvalidColumnError: If an invalid field name is found in filters or orders.
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
