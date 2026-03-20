from motion_validator.models import EventType, ParsedEvent
from motion_validator.validators.error_check import NoDriveErrorValidator


def test_no_error_pass():
    events = [
        ParsedEvent(
            line_number=1,
            timestamp=None,
            event_type=EventType.ERROR_STATUS,
            axis=None,
            raw_text="",
            metadata={"error_code": "0000"},
        )
    ]

    validator = NoDriveErrorValidator()
    result = validator.validate(events)

    assert result.passed is True


def test_error_fail():
    events = [
        ParsedEvent(
            line_number=1,
            timestamp=None,
            event_type=EventType.ERROR_STATUS,
            axis=None,
            raw_text="",
            metadata={"error_code": "1234"},
        )
    ]

    validator = NoDriveErrorValidator()
    result = validator.validate(events)

    assert result.passed is False