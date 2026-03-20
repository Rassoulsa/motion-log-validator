from motion_validator.models import EventType, ValidationResult


class StandbyAfterTargetValidator:
    name = "standby_after_target"

    def validate(self, events):
        target_events = [event for event in events if event.event_type == EventType.TARGET_REACHED]

        if not target_events:
            return ValidationResult(
                rule_name=self.name,
                passed=False,
                message="No target reached event found for standby validation.",
                evidence_lines=[],
            )

        for target_event in target_events:
            for event in events:
                if (
                    event.axis == target_event.axis
                    and event.event_type == EventType.STANDBY_CONFIRMED
                    and event.line_number > target_event.line_number
                ):
                    return ValidationResult(
                        rule_name=self.name,
                        passed=True,
                        message=f"Standby confirmed after target reached for axis {target_event.axis}.",
                        evidence_lines=[target_event.line_number, event.line_number],
                    )

        return ValidationResult(
            rule_name=self.name,
            passed=False,
            message="No standby confirmation found after target reached.",
            evidence_lines=[event.line_number for event in target_events],
        )