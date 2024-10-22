class Event:
    """
    zhihu event
    """
    def __init__(self, event_type: str, event_time: str):
        self.event_type = event_type
        self.event_time = event_time
        
    def to_dict(self):
        return {"event_type": self.event_type, "event_time": self.event_time}
    
    def __str__(self):
        return f"Event(event_type={self.event_type}, event_time={self.event_time})"
