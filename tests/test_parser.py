from motion_validator.models import EventType, RawLogLine
from motion_validator.parser import parse_line

def test_parse_move_command():
    line = RawLogLine(
        line_number=1,
        raw_text="12:17:05 DBG_MSG > servo Z-Axis       to be moved, pos(inc):     1228 | vel(rpm):       25",
    )

    event = parse_line(line)

    assert event.event_type == EventType.MOVE_COMMAND
    assert event.axis == "Z-Axis"
    assert event.metadata["position_inc"] == 1228
    assert event.metadata["velocity_rpm"] == 25


def test_parse_velocity_update():
    line = RawLogLine(
        line_number=2,
        raw_text="12:17:05 DBG_MSG > velocity update sent for Z-Axis",
    )

    event = parse_line(line)

    assert event.event_type == EventType.VELOCITY_UPDATE
    assert event.axis == "Z-Axis"



def test_parse_target_reached():
    line = RawLogLine(
        line_number=3,
        raw_text="12:17:06 DBG_MSG > >>>--->target reached: Z-Axis, position: 52977",
    )

    event = parse_line(line)

    assert event.event_type == EventType.TARGET_REACHED
    assert event.axis == "Z-Axis"
    assert event.metadata["position"] == 52977




def test_parse_standby_confirmed():
    line = RawLogLine(
        line_number=4,
        raw_text="12:17:06 DBG_MSG > servo Z-Axis standby timestamp: 1665016",
    )

    event = parse_line(line)

    assert event.event_type == EventType.STANDBY_CONFIRMED
    assert event.axis == "Z-Axis"
    assert event.metadata["standby_timestamp"] == 1665016



def test_parse_error_status():
    line = RawLogLine(
        line_number=5,
        raw_text="12:19:44 DBG_MSG > drive status|error: 0000|0000",
    )

    event = parse_line(line)

    assert event.event_type == EventType.ERROR_STATUS
    assert event.metadata["error_code"] == "0000"





def test_parse_unknown():
    line = RawLogLine(
        line_number=6,
        raw_text="12:17:01 DBG_MSG > something random here",
    )

    event = parse_line(line)

    assert event.event_type == EventType.UNKNOWN
