from dataclasses import dataclass, field

from motion_validator.models.validation_models import ValidationResult


@dataclass(slots=True)
class ValidationReport:
    source_file: str
    total_lines: int
    parsed_events: int
    overall_pass: bool
    results: list[ValidationResult] = field(default_factory=list)