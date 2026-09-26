from database.database import (
    create_table,
    add_subject,
    add_timetable
)
from dataset import semester2_tt


def seed_database():

    create_table()

    subjects = [
        "DS",
        "EVS",
        "C++",
        "PC",
        "Graphic Design",
        "FIT INDIA",
        "GE2",
        "VAC-II",
        "MM",
    ]

    for subject in subjects:
        add_subject(subject, 67)

    for subject, day, start, end in semester2_tt:
        add_timetable(subject, day, start, end)


if __name__ == "__main__":
    seed_database()


#python -m database.seed