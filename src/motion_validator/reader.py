from pathlib import Path

from motion_validator.models import RawLogLine


def read_log_file(file_path: str | Path) -> list[RawLogLine]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        return [
            RawLogLine(line_number=index, raw_text=line.rstrip("\n"))
            for index, line in enumerate(file, start=1)
        ]