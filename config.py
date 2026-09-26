COLLEGE_LOCATION = (
    28.6057146,
    77.0385629
)

CAMPUS_RADIUS = 80


ZONES = {
    "Academic Block": {
        "center": (0, 0),
        "radius": 40
    },

    "Canteen": {
        "center": (0, 0),
        "radius": 30
    },

    "Sports Complex": {
        "center": (0, 0),
        "radius": 45
    },

    "Garden": {
        "center": (0, 0),
        "radius": 35
    }
}


CLASS_RUNNING_SCORE = 50
INSIDE_CAMPUS_SCORE = 30
LOW_ATTENDANCE_SCORE = 20

CLASS_JUST_STARTED_SCORE = 20
CLASS_IN_PROGRESS_SCORE = 35
CLASS_FULLY_RUNNING_SCORE = 50

NEXT_CLASS_SOON_SCORE = 10
NEXT_CLASS_NEAR_SCORE = 20
NEXT_CLASS_IMMINENT_SCORE = 30


import os
from dotenv import load_dotenv

load_dotenv()


TOPIC = os.getenv("TOPIC")
API_URL = os.getenv("API_URL")
COLLEGEOS_TOKEN = os.getenv("COLLEGEOS_TOKEN")