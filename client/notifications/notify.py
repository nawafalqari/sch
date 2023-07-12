from notifypy import Notify

def notify(message: str, room_code: str):
    notf = Notify(
        default_notification_application_name="SCH",
        default_notification_icon="icon.ico",
    )

    notf.title = f"New message in room {room_code}"
    notf.message = message
    notf.send()
