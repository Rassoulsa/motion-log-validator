from motion_validator.models import EventType, ParsedEvent, ValidationResult
from motion_validator.validators.base import BaseValidator


class TargetReachedExistsValidator(BaseValidator):
    name = "target_reached_exists"

    def validate(self, events: list[ParsedEvent]) -> ValidationResult:
        target_events = [
            event for event in events if event.event_type == EventType.TARGET_REACHED
        ]

        if target_events:
            return ValidationResult(
                rule_name=self.name,
                passed=True,
                message="Target reached event found.",
                evidence_lines=[event.line_number for event in target_events],
            )

        return ValidationResult(
            rule_name=self.name,
            passed=False,
            message="No target reached event found.",
            evidence_lines=[],
        )