"""
Converter interface.
"""

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from criteria_pattern import Criteria

T = TypeVar('T')


class Converter(ABC):
    """
    Converter interface.
    """

    @abstractmethod
    def convert(self, criteria: Criteria[T]) -> Any:
        """
        Convert the Criteria object to a specific format.
        """
        ...
