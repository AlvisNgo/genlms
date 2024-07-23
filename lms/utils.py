from .models import Notification

def add_notification(to: int, title: str, description: str, link: str):
    notification = Notification(
        to=to,
        title=title,
        description=description,
        link=link
    )
    notification.save()
    
    return notification