from itertools import count
from typing import Union

import pygame
from pygame.event import Event


class EventHandler:
    """
    Core event handler, handles pygame and custom events.

    can be called as a function decorator to register a function as an event handler.
    """

    def __init__(self):
        self.handlers = {}
        self.events = []
        self.custom_event_ids = count(pygame.USEREVENT)
        self.custom_events = {}

    def register(self, event_type, handler):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def unregister(self, event_type, handler):
        if event_type in self.handlers:
            self.handlers[event_type].remove(handler)

    def handle(self, event: Union[str, int, Event], **event_data):
        if isinstance(event, str):
            event = self.custom_events[event]
        if isinstance(event, int):
            if len(event_data) > 0:
                event = pygame.event.Event(event, event_data)
            else:
                event = pygame.event.Event(event)
        if event.type in self.handlers:
            for handler in self.handlers[event.type]:
                handler(event)

    def handle_events(self, events):
        for event in events:
            if not isinstance(event, tuple):
                self.handle(event)
            else:
                self.handle(event[0], **event[1])

    def create_event(self, event_name: str):
        event_id = next(self.custom_event_ids)
        self.custom_events[event_name] = event_id
        self.handlers[event_id] = []
        print(f"Created custom event type {event_name} with id {event_id}")
        return event_name, event_id,

    def delete_event(self, event_name: str):
        del self.custom_events[event_name]
        del self.handlers[self.custom_events[event_name]]

    def get_event_name(self, event_id):
        for event_name, event_id_ in self.custom_events.items():
            if event_id_ == event_id:
                return event_name
        else:
            return pygame.event.event_name(event_id)

    def get_custom_event_id(self, event_name):
        if event_name in self.custom_events:
            return self.custom_events[event_name]
        else:
            return None

    def __call__(self, *event_types):
        def decorator(handler):
            for event_type in event_types:
                self.register(event_type, handler)
            return handler

        return decorator
