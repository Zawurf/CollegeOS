from dataclasses import dataclass


@dataclass
class Location:

    latitude: float | None = None
    longitude: float | None = None
    distance_from_college: float | None = None
    inside_campus: bool = False
    zone: str = "Unknown"