from motion_validator.models import EventType, ParsedEvent
from motion_validator.validators.standby import StandbyAfterTargetValidator


def test_standby_after_target_pass():
    events = [
        ParsedEvent(
            line_number=1,
            timestamp=None,
            event_type=EventType.TARGET_REACHED,
            axis="Z-Axis",
            raw_text="",
        ),
        ParsedEvent(
            line_number=2,
            timestamp=None,
            event_type=EventType.STANDBY_CONFIRMED,
            axis="Z-Axis",
            raw_text="",
        ),
    ]

    validator = StandbyAfterTargetValidator()
    result = validator.validate(events)

    assert result.passed is True


def test_standby_after_target_fail_when_missing():
    events = [
        ParsedEvent(
            line_number=1,
            timestamp=None,
            event_type=EventType.TARGET_REACHED,
            axis="Z-Axis",
            raw_text="",
        )
    ]

    validator = StandbyAfterTargetValidator()
    result = validator.validate(events)

    assert result.passed is False


def test_standby_after_target_fail_when_before_target():
    events = [
        ParsedEvent(
            line_number=1,
            timestamp=None,
            event_type=EventType.STANDBY_CONFIRMED,
            axis="Z-Axis",
            raw_text="",
        ),
        ParsedEvent(
            line_number=2,
            timestamp=None,
            event_type=EventType.TARGET_REACHED,
            axis="Z-Axis",
            raw_text="",
        ),
    ]

    validator = StandbyAfterTargetValidator()
    result = validator.validate(events)

    assert result.passed is False