from datetime import datetime, time

from motion_validator.models import EventType, ParsedEvent, RawLogLine
from motion_validator import patterns


def parse_timestamp(value: str) -> time | None:
    try:
        return datetime.strptime(value, "%H:%M:%S").time()
    except ValueError:
        return None


def parse_line(raw_line: RawLogLine) -> ParsedEvent:
    line_text = raw_line.raw_text.strip()
    match = patterns.TIMESTAMP_PATTERN.match(line_text)

    timestamp = None
    message = line_text

    if match:
        timestamp = parse_timestamp(match.group("timestamp"))
        message = match.group("message").strip()

    move_match = patterns.MOVE_COMMAND_PATTERN.match(message)
    if move_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.MOVE_COMMAND,
            axis=move_match.group("axis").strip(),
            raw_text=raw_line.raw_text,
            metadata={
                "position_inc": int(move_match.group("position")),
                "velocity_rpm": int(move_match.group("velocity")),
            },
        )

    velocity_match = patterns.VELOCITY_UPDATE_PATTERN.match(message)
    if velocity_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.VELOCITY_UPDATE,
            axis=velocity_match.group("axis").strip(),
            raw_text=raw_line.raw_text,
        )

    target_signal_match = patterns.TARGET_SIGNAL_PATTERN.match(message)
    if target_signal_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.TARGET_SIGNAL,
            axis=target_signal_match.group("axis").strip(),
            raw_text=raw_line.raw_text,
            metadata={"transition": target_signal_match.group("transition").strip()},
        )

    target_reached_match = patterns.TARGET_REACHED_PATTERN.match(message)
    if target_reached_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.TARGET_REACHED,
            axis=target_reached_match.group("axis").strip(),
            raw_text=raw_line.raw_text,
            metadata={"position": int(target_reached_match.group("position"))},
        )

    target_reached_alt_match = patterns.TARGET_REACHED_ALT_PATTERN.match(message)
    if target_reached_alt_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.TARGET_REACHED,
            axis=target_reached_alt_match.group("axis").strip(),
            raw_text=raw_line.raw_text,
        )

    standby_request_match = patterns.STANDBY_REQUEST_PATTERN.match(message)
    if standby_request_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.STANDBY_REQUEST,
            axis=standby_request_match.group("axis").strip(),
            raw_text=raw_line.raw_text,
        )

    standby_confirmed_match = patterns.STANDBY_CONFIRMED_PATTERN.match(message)
    if standby_confirmed_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.STANDBY_CONFIRMED,
            axis=standby_confirmed_match.group("axis").strip(),
            raw_text=raw_line.raw_text,
            metadata={"standby_timestamp": int(standby_confirmed_match.group("timestamp_value"))},
        )

    standby_entered_match = patterns.STANDBY_ENTERED_PATTERN.match(message)
    if standby_entered_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.STANDBY_CONFIRMED,
            axis=standby_entered_match.group("axis").strip(),
            raw_text=raw_line.raw_text,
        )

    error_status_match = patterns.ERROR_STATUS_PATTERN.match(message)
    if error_status_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.ERROR_STATUS,
            axis=None,
            raw_text=raw_line.raw_text,
            metadata={
                "drive_status": error_status_match.group("drive_status"),
                "error_code": error_status_match.group("error_code"),
            },
        )

    overshoot_match = patterns.OVERSHOOT_PATTERN.match(message)
    if overshoot_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.OVERSHOOT,
            axis=None,
            raw_text=raw_line.raw_text,
            metadata={"overshoot": int(overshoot_match.group("overshoot"))},
        )

    sensor_update_match = patterns.SENSOR_UPDATE_PATTERN.match(message)
    if sensor_update_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.SENSOR_UPDATE,
            axis=None,
            raw_text=raw_line.raw_text,
            metadata={
                "sensor_name": sensor_update_match.group("sensor_name").strip(),
                "sensor_value": sensor_update_match.group("sensor_value").strip(),
            },
        )

    control_panel_match = patterns.CONTROL_PANEL_RELEASED_PATTERN.match(message)
    if control_panel_match:
        return ParsedEvent(
            line_number=raw_line.line_number,
            timestamp=timestamp,
            event_type=EventType.CONTROL_PANEL_RELEASED,
            axis=None,
            raw_text=raw_line.raw_text,
        )

    return ParsedEvent(
        line_number=raw_line.line_number,
        timestamp=timestamp,
        event_type=EventType.UNKNOWN,
        axis=None,
        raw_text=raw_line.raw_text,
    )


def parse_lines(raw_lines: list[RawLogLine]) -> list[ParsedEvent]:
    return [parse_line(line) for line in raw_lines]


def parse_log_file(file_path: str) -> list[ParsedEvent]:
    from motion_validator.reader import read_log_file

    raw_lines = read_log_file(file_path)
    return parse_lines(raw_lines)