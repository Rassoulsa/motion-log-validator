from abc import ABC, abstractmethod

from motion_validator.models import ParsedEvent, ValidationResult


class BaseValidator(ABC):
    name: str

    @abstractmethod
    def validate(self, events: list[ParsedEvent]) -> ValidationResult:
        pass