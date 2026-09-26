from services.notification_service import notify
from engines import memory_engine


def run(context):

    decision = context.confidence.decision

    if decision == "AUTO_LOG":

        notify(
            context,
            "CollegeOS",
            "Attendance logged automatically."
        )

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