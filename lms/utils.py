from .models import Notification

def add_event(to: int, title: str, description: str, link: str):
    event = Notification(
        to=to,
        title=title,
        description=description,
        link=link
    )
    event.save()
    
    return event