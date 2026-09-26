from dataclasses import dataclass


@dataclass
class Memory:
    last_notification: tuple | None = None
    last_auto_log: tuple | None = None