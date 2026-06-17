#!/usr/bin/env python3
"""Inspect the installed criteria-pattern API for agent-facing verification."""

from __future__ import annotations

import inspect
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any


def _prefer_local_checkout() -> None:
    """Prefer a parent checkout containing criteria_pattern when this script is run from the repo."""
    for parent in Path(__file__).resolve().parents:
        if (parent / 'criteria_pattern').is_dir():
            sys.path.insert(0, str(parent))
            return


def _print_signature(name: str, target: Callable[..., Any]) -> None:
    print(f'{name}{inspect.signature(target)}')


def main() -> None:
    _prefer_local_checkout()

    import criteria_pattern
    from criteria_pattern import Direction, Operator
    from criteria_pattern.converters import (
        BodyToCriteriaConverter,
        CriteriaToMariadbConverter,
        CriteriaToMysqlConverter,
        CriteriaToPostgresqlConverter,
        CriteriaToSqliteConverter,
        SimpleUrlToCriteriaConverter,
        UrlToCriteriaConverter,
    )

    print(f'criteria_pattern version: {criteria_pattern.__version__}')
    print(f'public exports: {", ".join(criteria_pattern.__all__)}')
    print(f'operators ({len(Operator)}): {", ".join(operator.name for operator in Operator)}')
    print(f'directions ({len(Direction)}): {", ".join(direction.name for direction in Direction)}')
    print()
    _print_signature('BodyToCriteriaConverter.convert', BodyToCriteriaConverter.convert)
    _print_signature('UrlToCriteriaConverter.convert', UrlToCriteriaConverter.convert)
    _print_signature('SimpleUrlToCriteriaConverter.convert', SimpleUrlToCriteriaConverter.convert)
    _print_signature('CriteriaToPostgresqlConverter.convert', CriteriaToPostgresqlConverter.convert)
    _print_signature('CriteriaToMysqlConverter.convert', CriteriaToMysqlConverter.convert)
    _print_signature('CriteriaToMariadbConverter.convert', CriteriaToMariadbConverter.convert)
    _print_signature('CriteriaToSqliteConverter.convert', CriteriaToSqliteConverter.convert)


if __name__ == '__main__':
    main()
