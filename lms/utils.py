from .models import Event

def add_event(to: int, title: str, description: str):
    event = Event(
        to=to,
        title=title,
        description=description,
    )
    event.save()
    
    return event