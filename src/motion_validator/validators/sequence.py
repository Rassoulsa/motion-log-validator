from motion_validator.models import EventType, ValidationResult


class CommandToTargetSequenceValidator:
    name = "command_to_target_sequence"

    def validate(self, events):
        commands = [e for e in events if e.event_type == EventType.MOVE_COMMAND]

        if not commands:
            return ValidationResult(
                rule_name=self.name,
                passed=False,
                message="No move command found.",
                evidence_lines=[],
            )

        for command in commands:
            for event in events:
                if (
                    event.axis == command.axis
                    and event.event_type == EventType.TARGET_REACHED
                    and event.line_number > command.line_number
                ):
                    return ValidationResult(
                        rule_name=self.name,
                        passed=True,
                        message=f"Command followed by target reached for axis {command.axis}.",
                        evidence_lines=[command.line_number, event.line_number],
                    )

        return ValidationResult(
            rule_name=self.name,
            passed=False,
            message="No valid command to target reached sequence found.",
            evidence_lines=[c.line_number for c in commands],
        )