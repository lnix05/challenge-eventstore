class Event(object):
    """
    Basic event object.
    """

    def __init__(self, event_id: int, event_type: str, timestamp: str):
        """
        Creates and instantiates an Event.

        Arguments:
        - event_id (int): unique id of the event
        - event_type (str): type of the event
        - timestamp (str): time in which the event ocurred
        """
        self.event_id = event_id
        self.event_type = event_type
        self.timestamp = timestamp


class EventStore(object):
    """
    Basic event store object.
    """

    def __init__(self):
        """
        Creates and instantiates an EventStore.
        """
        self.stored_events = []

    def insert(self, event: Event):
        """
        Inserts an Event into an EventStore.

        Arguments:
        - event (Event): an Event object
        """
        event_dict = event.__dict__
        self.stored_events.append(event_dict)

    def remove_all(self, event_type: str):
        """
        Removes all events of a given type.

        Arguments:
        - event_type (str): type of the event
        """
        self.stored_events = [
            d for d in self.stored_events if d["event_type"] != event_type
        ]
    

class EventIterator(object):
    """
    Basic iterator to use with event stores.
    """
    

    def __init__(self, store: EventStore, event_type: str, start_time: str, end_time: str):
        """
        Creates and instantiates an EventIterator.

        Arguments:
        - store (EventStore): event store object
        - event_type (str): type of an event
        - start_time (str): first event time to look for
        - end_time (str): last event time to look for
        """
        self.store = store
        self.type = event_type
        self.start_time = start_time
        self.end_time = end_time
        
        self.iterator = [
            d for d in store.stored_events if d["event_type"] == event_type and d["timestamp"] >= start_time and d["timestamp"] <= end_time   
        ]
        self.current_event = self.iterator[0]
        self._called_move_next = False
        self._reached_end = False

    def move_next(self):
        """
        Move to next event.

        Returns True if end of list is not reached yet and False otherwise.
        """
        self._called_move_next = True 
        current_index = self.iterator.index(self.current_event)
        if current_index < len(self.iterator):
            self.current_event = self.iterator[current_index + 1]
            return True
        else:
            self._reached_end = True
            return False

    def current(self):
        """
        Get current event.

        Returns current_event (Event).
        """
        if self._called_move_next and not self._reached_end:
            return self.current_event
        else:
            raise ValueError("Illegal state")

    def remove(self):
        """
        Remove current event from event store.
        """
        if self._called_move_next and not self._reached_end:
            event_id = self.current_event["event_id"]
            self.store = [
                d for d in self.store.stored_events if d["event_id"] != event_id
            ]
        else:
            raise ValueError("Illegal state")

