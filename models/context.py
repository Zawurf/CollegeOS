from models.attendance import Attendance
from models.location import Location
from models.confidence import Confidence
from models.memory import Memory


class Context:

    def __init__(self):

        self.current_day = None
        self.current_time = None

        self.current_class = None
        self.next_class = None
        self.remaining_classes = []
        self.time_until_next_class = None

        self.attendance = Attendance()

        self.location = Location()

        self.confidence = Confidence()

        self.notifications = []

        self.memory = Memory()

        