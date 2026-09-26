from dataclasses import dataclass

@dataclass
class AttendanceStats:
    total: int
    attended: int
    safe_bunks: int
    need_to_attend: int
    min_attendance: int