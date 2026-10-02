from database.database import (
    get_official_data,
    get_daily_logs,
    get_min_attendance,
    get_subject_id
)
from models.attendance_stats import AttendanceStats


def calculate_attendance(sub_id):

    data = get_official_data(sub_id)

    if data is None:
        return None

    official_total, official_attended, _ = data

    logs = get_daily_logs(sub_id)

    total_logs = 0
    attended_logs = 0

    for log in logs:

        status = log[0]
        hours = log[1]

        if status != "cancelled":
            total_logs += hours

        if status in ["proxy", "present", "free"]:
            attended_logs += hours

    final_total_class = official_total + total_logs
    final_attended_class = official_attended + attended_logs

    if final_total_class == 0:
        return None

    min_att = get_min_attendance(sub_id)

    if min_att is None:
        return None

    safe_bunk = 0

    while (
        (final_attended_class /
         (final_total_class + safe_bunk + 1)) * 100
        >= min_att
    ):
        safe_bunk += 1

    need_to_attend = 0

    while (
        ((final_attended_class + need_to_attend) /
         (final_total_class + need_to_attend)) * 100
        < min_att
    ):
        need_to_attend += 1

    return AttendanceStats(
        total=final_total_class,
        attended=final_attended_class,
        safe_bunks=safe_bunk,
        need_to_attend=need_to_attend,
        min_attendance=min_att
    )


def run(context):

    if context.current_class is None:
        return context

    subject = context.current_class.subject

    sub_id = get_subject_id(subject)

    if sub_id is None:
        return context

    attendance = calculate_attendance(sub_id)

    if attendance is None:
        return context

    if attendance.total > 0:
        percentage = round(
            (attendance.attended / attendance.total) * 100,
            2
        )
    else:
        percentage = None

    context.attendance.percentage = percentage
    context.attendance.safe_bunks = attendance.safe_bunks
    context.attendance.need_to_attend = attendance.need_to_attend
    context.attendance.decision = None

    return context