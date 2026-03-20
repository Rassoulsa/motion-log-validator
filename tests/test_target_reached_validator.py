from motion_validator.models import EventType, ParsedEvent
from motion_validator.validators.target_reached import TargetReachedExistsValidator


def test_target_reached_exists_pass():
    events = [
        ParsedEvent(
            line_number=1,
            timestamp=None,
            event_type=EventType.TARGET_REACHED,
            axis="Z-Axis",
            raw_text="",
        )
    ]

    validator = TargetReachedExistsValidator()
    result = validator.validate(events)

    assert result.passed is True


def test_target_reached_exists_fail():
    events = []

    validator = TargetReachedExistsValidator()
    result = validator.validate(events)

    assert result.passed is False