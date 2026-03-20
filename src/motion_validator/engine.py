from motion_validator.models import ValidationReport
from motion_validator.parser import parse_log_file
from motion_validator.validators.duration import DurationBelowThresholdValidator
from motion_validator.validators.error_check import NoDriveErrorValidator
from motion_validator.validators.sequence import CommandToTargetSequenceValidator
from motion_validator.validators.standby import StandbyAfterTargetValidator
from motion_validator.validators.target_reached import TargetReachedExistsValidator


class ValidationEngine:
    def __init__(self):
        self.validators = [
            TargetReachedExistsValidator(),
            StandbyAfterTargetValidator(),
            CommandToTargetSequenceValidator(),
            NoDriveErrorValidator(),
            DurationBelowThresholdValidator(),
        ]

    def run(self, file_path: str) -> ValidationReport:
        events = parse_log_file(file_path)

        results = []
        for validator in self.validators:
            result = validator.validate(events)
            results.append(result)

        overall_pass = all(r.passed for r in results)

        return ValidationReport(
            source_file=file_path,
            total_lines=len(events),
            parsed_events=len(events),
            overall_pass=overall_pass,
            results=results,
        )