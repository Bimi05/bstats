"""
The MIT License (MIT)

Copyright (c) 2022-present Bimi

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import datetime
from .utils import camel_to_snake

from typing import (
    TypeVar,
    Any
)

class EventDetails:
    """
    Represents a Brawl Stars event slot details.

    ### Attributes
    mode: `str`
        The event slot's mode name.
    map: `str`
        The event slot's mode map.
    id: `int`
        The event slot's map ID.
    """
    def __init__(self, event: Any) -> None:
        self.push_data(event)

    def __repr__(self) -> str:
        return f"<Event object mode={self.mode!r} map={self.map!r}>"

    def push_data(self, data: Any) -> None:
        self._mode = data["mode"]
        self._map = data["map"]
        self._id = data["id"]


    @property
    def mode(self) -> str:
        """`str`: The event's mode name."""
        f = " ".join(camel_to_snake(self._mode).split("_"))
        return f.title()

    @property
    def map(self) -> str:
        """`str`: The event's mode map."""
        return self._map

    @property
    def id(self) -> int:
        """`int`: The event's map ID."""
        return self._id


ES = TypeVar("ES", bound="EventSlot")
class EventSlot:
    """
    Represents a Brawl Stars event slot.

    ### Attributes
    start: `datetime.datetime`
        The time that the event came into rotation.
    end: `datetime.datetime`
        The time that the event will come out of rotation.
    ends_in: `int`
        The amount of seconds left before the event comes out of rotation.
    event: `EventDetails`
        An `EventDetails` object representing the event's details.
    """
    def __init__(self: ES, rotation: Any) -> None:
        self.push_data({camel_to_snake(key): value for key, value in rotation.items()})

    def __repr__(self: ES) -> str:
        return f"<{self.__class__.__name__} mode={self.event.mode!r} map={self.event.map!r}>"

    def push_data(self: ES, data: Any) -> None:
        self._start = data["start_time"]
        self._end = data["end_time"]
        self._event = data["event"]


    @property
    def start(self: ES) -> datetime.datetime:
        """`datetime.datetime`: The time that the event came into rotation."""
        return datetime.datetime.strptime(self._start, "%Y%m%dT%H%M%S.%fZ")

    @property
    def end(self: ES) -> datetime.datetime:
        """`datetime.datetime`: The time that the event will come out of rotation."""
        return datetime.datetime.strptime(self._end, "%Y%m%dT%H%M%S.%fZ")

    @property
    def ends_in(self: ES) -> int:
        """`int`: The amount of seconds left before the event comes out of rotation."""
        return int((self.end - datetime.datetime.utcnow()).total_seconds())

    @property
    def event(self: ES) -> EventDetails:
        """`EventDetails`: An `EventDetails` object representing the event's details."""
        return EventDetails(self._event)
