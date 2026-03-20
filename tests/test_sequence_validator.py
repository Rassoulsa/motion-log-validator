from motion_validator.models import EventType, ParsedEvent
from motion_validator.validators.sequence import CommandToTargetSequenceValidator


def test_sequence_pass():
    events = [
        ParsedEvent(1, None, EventType.MOVE_COMMAND, "Z-Axis", ""),
        ParsedEvent(2, None, EventType.TARGET_REACHED, "Z-Axis", ""),
    ]

    validator = CommandToTargetSequenceValidator()
    result = validator.validate(events)

    assert result.passed is True


def test_sequence_fail_no_target():
    events = [
        ParsedEvent(1, None, EventType.MOVE_COMMAND, "Z-Axis", ""),
    ]

    validator = CommandToTargetSequenceValidator()
    result = validator.validate(events)

    assert result.passed is False


def test_sequence_fail_wrong_order():
    events = [
        ParsedEvent(1, None, EventType.TARGET_REACHED, "Z-Axis", ""),
        ParsedEvent(2, None, EventType.MOVE_COMMAND, "Z-Axis", ""),
    ]

    validator = CommandToTargetSequenceValidator()
    result = validator.validate(events)

    assert result.passed is False