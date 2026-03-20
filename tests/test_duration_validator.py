from datetime import time

from motion_validator.models import EventType, ParsedEvent
from motion_validator.validators.duration import DurationBelowThresholdValidator


def test_duration_pass():
    events = [
        ParsedEvent(1, time(12, 0, 0), EventType.MOVE_COMMAND, "Z-Axis", ""),
        ParsedEvent(2, time(12, 0, 3), EventType.TARGET_REACHED, "Z-Axis", ""),
    ]

    validator = DurationBelowThresholdValidator(threshold_seconds=5)
    result = validator.validate(events)

    assert result.passed is True


def test_duration_fail():
    events = [
        ParsedEvent(1, time(12, 0, 0), EventType.MOVE_COMMAND, "Z-Axis", ""),
        ParsedEvent(2, time(12, 0, 10), EventType.TARGET_REACHED, "Z-Axis", ""),
    ]

    validator = DurationBelowThresholdValidator(threshold_seconds=5)
    result = validator.validate(events)

    assert result.passed is False