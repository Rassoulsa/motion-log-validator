from dataclasses import dataclass


@dataclass(slots=True)
class RawLogLine:
    line_number: int
    raw_text: str