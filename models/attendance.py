from dataclasses import dataclass


@dataclass
class Attendance:

    percentage: float | None = None
    safe_bunks: int | None = None
    need_to_attend: int | None = None
    decision: str | None = None