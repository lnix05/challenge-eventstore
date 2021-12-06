#%%
from event_store import *

def test_event_class(event_id: int, event_type: str, timestamp: str):
    event = Event(event_id=event_id, event_type=event_type, timestamp=timestamp)
    if (event.event_id != event_id or event.event_type != event_type or event.timestamp != timestamp):
        print("Event broken!")
        return 1
    else:
        print("Success!!")
        return 0


def test_event_store(events: list):
    store = EventStore()
    for event in events:
        store.insert(event)

    ids = [event.event_id for event in events]

    error = 0
    for stored_event in store.stored_events:
        if stored_event["event_id"] in ids:
            continue
        else:
            error += 1

    if error != 0:
        print("Problem in storing events.")
        return 1
    else:
        print("Success!!")
        return 0


def test_remove_all(events: list, event_type: str):
    store = EventStore()
    for event in events:
        store.insert(event)

    store.remove_all(event_type)

    event_types = [stored_event["event_type"] for stored_event in store.stored_events]
    if event_type in event_types:
        print(f"Problem in removing event type {event_type}.")
        return 1
    else:
        print("Success!!")
        return 0


def test_event_iterator(store: EventStore, event_type: str, start_time: str, end_time: str):
    event_iterator = EventIterator(store, event_type, start_time, end_time)

    for event in event_iterator.iterator:
        if event["event_type"] != event_type:
            print("Problem in iterator.")
            return 1
        else:
            print("Success!!")
            return 0
    
    
def test_move_next(event_iterator: EventIterator):
    current_idx = event_iterator.iterator.index(event_iterator.current_event)
    next_event = event_iterator.iterator[current_idx + 1]

    event_iterator.move_next()
    if event_iterator.current_event != next_event:
        print("Problem in moving next.")
        return 1
    else:
        print("Success!")
        return 0        


def test_remove(event_iterator: EventIterator):
    current_event = event_iterator.current_event
    event_iterator.remove()
    if current_event in event_iterator.iterator:
        print("Problem in removing event.")
        return 1
    else:
        print("Success!")
        return 0

    
# %%
