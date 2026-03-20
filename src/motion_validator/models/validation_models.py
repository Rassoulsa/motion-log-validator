from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ValidationResult:
    rule_name: str
    passed: bool
    message: str
    evidence_lines: list[int] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)