"""Base command contract for all business commands."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

InputModelT = TypeVar("InputModelT", bound=BaseModel)
OutputModelT = TypeVar("OutputModelT", bound=BaseModel)


class BaseCommand(ABC, Generic[InputModelT, OutputModelT]):
    """Abstract command interface."""

    @abstractmethod
    def execute(self, input_model: InputModelT) -> OutputModelT:
        """Execute business logic and return a typed result."""

        raise NotImplementedError
