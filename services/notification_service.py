import requests
from datetime import datetime
from config import TOPIC, API_URL, COLLEGEOS_TOKEN


def notify(context, title, message, priority=3, tags="books"):

    try:

        if context.current_class is None:
            return False

        subject = context.current_class.subject
        start = datetime.strptime(
            context.current_class.start,
            "%H:%M"
        )

        end = datetime.strptime(
            context.current_class.end,
            "%H:%M"
        )

        hours = int((end - start).total_seconds() / 3600)

        attendance_url = f"{API_URL}/attendance-response"

        print("ATTENDANCE ACTION URL:", attendance_url)

        payload = {
            "topic": TOPIC,
            "title": title,
            "message": message,
            "priority": priority,
            "tags": [tags],

            "actions": [
                {
                    "action": "http",
                    "label": "Yes",
                    "url": attendance_url,
                    "method": "POST",

                    "headers": {
                        "X-CollegeOS-Token": COLLEGEOS_TOKEN,
                        "Content-Type": "application/json"
                    },

                    "body": f'{{"subject":"{subject}","response":"YES","hours":{hours},"start_time":"{context.current_class.start}","end_time":"{context.current_class.end}"}}',
                    "clear": True
                },

                {
                    "action": "http",
                    "label": "No",
                    "url": attendance_url,
                    "method": "POST",

                    "headers": {
                        "X-CollegeOS-Token": COLLEGEOS_TOKEN,
                        "Content-Type": "application/json"
                    },

                    "body": f'{{"subject":"{subject}","response":"NO","hours":{hours},"start_time":"{context.current_class.start}","end_time":"{context.current_class.end}"}}',
                    "clear": True
                }
            ]
        }

        response = requests.post(
            "https://ntfy.sh/",
            json=payload,
            timeout=5
        )

        response.raise_for_status()

        context.notifications.append(message)

        return True

    except requests.RequestException as e:

        print(f"Notification failed: {e}")

        return False


def auto_log(context):

    context.notifications.append("Attendance auto logged.")

    requests.post(
        "https://ntfy.sh/",
        json={
            "topic": TOPIC,
            "message": "Attendance logged automatically."
        }
    )