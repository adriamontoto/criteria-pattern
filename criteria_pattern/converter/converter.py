"""
Converter interface.
"""

from abc import ABC, abstractmethod
from typing import Any

from criteria_pattern import Criteria


class Converter(ABC):
    """
    Converter interface.
    """

    @abstractmethod
    def convert(self, criteria: Criteria) -> Any:
        """
        Convert the Criteria object to a specific format.
        """
        ...
