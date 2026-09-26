from database.database import get_today_timetable
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from models.class_info import ClassInfo


IST = ZoneInfo("Asia/Kolkata")


def get_now(test_time=None):

    if test_time is not None:
        return test_time

    return datetime.now(IST)


def get_current_class(test_time=None):

    now = get_now(test_time)

    d = now.strftime("%A")
    t = now.strftime("%H:%M")

    l = get_today_timetable(d)

    for i in l:

        if i[1] <= t <= i[2]:
            return ClassInfo(
                subject=i[0],
                start=i[1],
                end=i[2]
            )

    return None


def get_next_class(test_time=None):

    now = get_now(test_time)

    d = now.strftime("%A")
    t = now.strftime("%H:%M")

    l = get_today_timetable(d)

    for i in l:

        if i[1] > t:
            return ClassInfo(
                subject=i[0],
                start=i[1],
                end=i[2]
            )

    return None


def time_until_next_class():

    now = get_now()

    next_class = get_next_class()

    if next_class is None:
        return None

    next_time = datetime.strptime(
        next_class.start,
        "%H:%M"
    ).time()

    next_time = datetime.combine(
        now.date(),
        next_time,
        tzinfo=IST
    )

    return round(
        (next_time - now).total_seconds() / 60
    )


def classes_remaining_today():

    now = get_now()

    d = now.strftime("%A")
    t = now.strftime("%H:%M")

    finished_classes = 0

    l = get_today_timetable(d)

    total_classes = len(l)

    for name, start, end in l:

        if t > end:
            finished_classes += 1

    return total_classes - finished_classes


def should_check_attendance():

    current = get_current_class()

    if current is None:
        return None

    now = get_now()

    start = datetime.strptime(
        current.start,
        "%H:%M"
    ).time()

    start = datetime.combine(
        now.date(),
        start,
        tzinfo=IST
    )

    if now >= start + timedelta(minutes=5):
        return current

    return None


def run(context):

    now = get_now()

    context.current_day = now.strftime("%A")
    context.current_time = now.strftime("%H:%M")

    context.current_class = get_current_class()
    context.next_class = get_next_class()
    context.time_until_next_class = time_until_next_class()
    context.remaining_classes = classes_remaining_today()

    return context