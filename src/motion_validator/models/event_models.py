from dataclasses import dataclass, field
from datetime import time
from enum import Enum
from typing import Any


class EventType(str, Enum):
    MOVE_COMMAND = "move_command"
    VELOCITY_UPDATE = "velocity_update"
    TARGET_SIGNAL = "target_signal"
    TARGET_REACHED = "target_reached"
    STANDBY_REQUEST = "standby_request"
    STANDBY_CONFIRMED = "standby_confirmed"
    ERROR_STATUS = "error_status"
    OVERSHOOT = "overshoot"
    SENSOR_UPDATE = "sensor_update"
    CONTROL_PANEL_RELEASED = "control_panel_released"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class ParsedEvent:
    line_number: int
    timestamp: time | None
    event_type: EventType
    axis: str | None
    raw_text: str
    value: str | int | float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)