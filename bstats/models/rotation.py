"""
The MIT License (MIT)

Copyright (c) 2022-present Bimi05

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

from ..utils import camel_to_snake


class Event:
    """
    Represents a Brawl Stars event slot.

    Attributes
    ----------

    mode: ``str``
        The event's mode name.
    map: ``str``
        The event's mode map.
    id: ``int``
        The event's map ID.
    """
    def __init__(self, event: dict) -> None:
        self.event = event

    def __repr__(self) -> str:
        return f"<Event object mode='{self.mode}' map='{self.map}'>"


    @property
    def mode(self) -> str:
        """``str``: The event's mode name."""
        return " ".join(char.capitalize() for char in camel_to_snake(self.event["mode"]).split("_"))

    @property
    def map(self) -> str:
        """``str``: The event's mode map."""
        return self.event["map"]

    @property
    def id(self) -> int:
        """``int``: The event's map ID."""
        return self.event["id"]

class Rotation:
    """
    Represents a Brawl Stars event rotation.

    Attributes
    ----------

    start: ``str``
        The time that the event came into rotation.
        Follows this format: DD/MM/YY - HH:MM:SS
    end: ``str``
        The time that the event will come out of rotation.
        Follows this format: DD/MM/YY - HH:MM:SS
    event: ``Event``
        An ``Event`` object representing the event's details.
    """
    def __init__(self, rotation: dict) -> None:
        self.rotation = {}
        for key in rotation:
            self.rotation[camel_to_snake(key)] = rotation[key]

    def __repr__(self) -> str:
        return f"<Rotation object event_mode='{self.event.mode}' event_map='{self.event.map}'>"


    @property
    def start(self) -> str:
        """``str``: The time that the event came into rotation. Follows this format: DD/MM/YY - HH:MM:SS"""
        return datetime.datetime.strptime(self.rotation["start_time"], "%Y%m%dT%H%M%S.%fZ").strftime("%d/%m/%Y - %H:%M:%S")

    @property
    def end(self) -> str:
        """``str``: The time that the event will come out of rotation. Follows this format: DD/MM/YY - HH:MM:SS"""
        return datetime.datetime.strptime(self.rotation["end_time"], "%Y%m%dT%H%M%S.%fZ").strftime("%d/%m/%Y - %H:%M:%S")

    @property
    def event(self) -> Event:
        """``Event``: An ``Event`` object representing the event's details."""
        return Event(self.rotation["event"])
