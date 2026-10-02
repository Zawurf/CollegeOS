from datetime import datetime
from database.database import get_subject_id, was_notified, mark_notified


def today():
    return datetime.now().strftime("%Y-%m-%d")


def get_notification_subject_id(context):

    if context.current_class is None:
        return None

    return get_subject_id(context.current_class.subject)


def already_notified(context):
    sub_id = get_notification_subject_id(context)

    if sub_id is None:
        return False

    return was_notified(
        sub_id,
        today(),
        context.current_class.start,
        context.current_class.end
    )


def mark_as_notified(context):
    sub_id = get_notification_subject_id(context)

    if sub_id is None:
        return

    mark_notified(
        sub_id,
        today(),
        context.current_class.start,
        context.current_class.end
    )