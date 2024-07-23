from .models import Event

def add_event(to: int, title: str, description: str, link: str):
    event = Event(
        to=to,
        title=title,
        description=description,
        link=link
    )
    event.save()
    
    return event