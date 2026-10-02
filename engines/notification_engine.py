from datetime import datetime

from database.database import (
    get_subject_id,
    add_daily_logs,
    is_already_logged
)

from services.notification_service import notify, auto_log
from engines import memory_engine


def get_class_hours(context):

    start = datetime.strptime(
        context.current_class.start,
        "%H:%M"
    )

    end = datetime.strptime(
        context.current_class.end,
        "%H:%M"
    )

    return int((end - start).total_seconds() / 3600)


def log_attendance_automatically(context):

    if context.current_class is None:
        return False

    subject = context.current_class.subject

    sub_id = get_subject_id(subject)

    if sub_id is None:
        return False

    today = datetime.now().strftime("%Y-%m-%d")

    start_time = context.current_class.start
    end_time = context.current_class.end

    if is_already_logged(
        sub_id,
        today,
        start_time,
        end_time
    ):
        return False

    hours = get_class_hours(context)

    add_daily_logs(
        sub_id,
        today,
        "present",
        hours,
        start_time,
        end_time
    )

    return True


def run(context):

    decision = context.confidence.decision

    if decision == "AUTO_LOG":

        logged = log_attendance_automatically(context)

        if logged:
            auto_log(context)

    elif decision == "ASK_USER":

        already = memory_engine.already_notified(context)

        if already:
            return context

        success = notify(
            context,
            "CollegeOS",
            "Your class is running. Mark attendance?"
        )

        if success:
            memory_engine.mark_as_notified(context)

    return context