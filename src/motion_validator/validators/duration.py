from datetime import datetime

from motion_validator.models import EventType, ValidationResult


class DurationBelowThresholdValidator:
    name = "duration_below_threshold"

    def __init__(self, threshold_seconds: int = 5):
        self.threshold_seconds = threshold_seconds

    def validate(self, events):
        commands = [e for e in events if e.event_type == EventType.MOVE_COMMAND]
        targets = [e for e in events if e.event_type == EventType.TARGET_REACHED]

        if not commands or not targets:
            return ValidationResult(
                rule_name=self.name,
                passed=False,
                message="Missing command or target reached for duration calculation.",
                evidence_lines=[],
            )

        command = commands[0]
        target = None

        for t in targets:
            if t.axis == command.axis and t.line_number > command.line_number:
                target = t
                break

        if not target:
            return ValidationResult(
                rule_name=self.name,
                passed=False,
                message="No matching target reached after command.",
                evidence_lines=[command.line_number],
            )

        if not command.timestamp or not target.timestamp:
            return ValidationResult(
                rule_name=self.name,
                passed=False,
                message="Missing timestamps for duration calculation.",
                evidence_lines=[command.line_number, target.line_number],
            )

        start = datetime.combine(datetime.today(), command.timestamp)
        end = datetime.combine(datetime.today(), target.timestamp)

        duration = (end - start).total_seconds()

        if duration <= self.threshold_seconds:
            return ValidationResult(
                rule_name=self.name,
                passed=True,
                message=f"Duration OK: {duration:.2f}s",
                evidence_lines=[command.line_number, target.line_number],
                details={"duration": duration},
            )

        return ValidationResult(
            rule_name=self.name,
            passed=False,
            message=f"Duration too high: {duration:.2f}s",
            evidence_lines=[command.line_number, target.line_number],
            details={"duration": duration},
        )