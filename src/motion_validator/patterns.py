import re

TIMESTAMP_PATTERN = re.compile(r"^(?P<timestamp>\d{1,2}:\d{2}:\d{2})\s+DBG_MSG\s+>\s+(?P<message>.*)$")

MOVE_COMMAND_PATTERN = re.compile(
    r"^servo\s+(?P<axis>.+?)\s+to be moved,\s+pos\(inc\):\s+(?P<position>-?\d+)\s+\|\s+vel\(rpm\):\s+(?P<velocity>-?\d+)$"
)

VELOCITY_UPDATE_PATTERN = re.compile(r"^velocity update sent for (?P<axis>.+)$")

TARGET_SIGNAL_PATTERN = re.compile(r"^TARGET\s+(?P<transition>.+?),\s+servo\s+(?P<axis>.+)$")

TARGET_REACHED_PATTERN = re.compile(
    r"^>>>--->target reached:\s+(?P<axis>.+?),\s+position:\s+(?P<position>-?\d+)$"
)

TARGET_REACHED_ALT_PATTERN = re.compile(r"^target reached,\s+servo\s+(?P<axis>.+)$")

STANDBY_REQUEST_PATTERN = re.compile(r"^EnableStandby\(\) called for (?P<axis>.+)$")

STANDBY_CONFIRMED_PATTERN = re.compile(
    r"^servo\s+(?P<axis>.+?)\s+standby timestamp:\s+(?P<timestamp_value>\d+)$"
)

STANDBY_ENTERED_PATTERN = re.compile(r"^standby entered:\s+(?P<axis>.+)$")

ERROR_STATUS_PATTERN = re.compile(
    r"^drive status\|error:\s+(?P<drive_status>[A-Fa-f0-9]+)\|(?P<error_code>[A-Fa-f0-9]+)$"
)

OVERSHOOT_PATTERN = re.compile(r"^MT-Command overshot was:\s+(?P<overshoot>-?\d+)$")

SENSOR_UPDATE_PATTERN = re.compile(
    r"^sensor byte updated for (?P<sensor_name>.+?):\s+(?P<sensor_value>[A-Fa-f0-9]+)$"
)

CONTROL_PANEL_RELEASED_PATTERN = re.compile(r"^control panel released$")