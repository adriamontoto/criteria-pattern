"""
Integrity error exception for invalid criteria input.
"""

from .criteria_pattern_base_error import CriteriaPatternBaseError


class IntegrityError(CriteriaPatternBaseError):
    """
    Raised when a value object or converter input violates structural validation.

    This error covers invalid primitive types, missing required values, unsupported request shapes, and consistency
    checks such as providing `page_number` without `page_size`.
    """
