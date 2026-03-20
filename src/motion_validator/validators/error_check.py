from motion_validator.models import EventType, ValidationResult


class NoDriveErrorValidator:
    name = "no_drive_error"

    def validate(self, events):
        error_events = [e for e in events if e.event_type == EventType.ERROR_STATUS]

        if not error_events:
            return ValidationResult(
                rule_name=self.name,
                passed=True,
                message="No drive error events found.",
                evidence_lines=[],
            )

        for event in error_events:
            error_code = event.metadata.get("error_code")

            if error_code and error_code != "0000":
                return ValidationResult(
                    rule_name=self.name,
                    passed=False,
                    message=f"Drive error detected: {error_code}",
                    evidence_lines=[event.line_number],
                )

        return ValidationResult(
            rule_name=self.name,
            passed=True,
            message="No drive errors detected.",
            evidence_lines=[e.line_number for e in error_events],
        )