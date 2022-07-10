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

from .member import Member
from .utils import camel_to_snake

from typing import (
    List,
    Any,
    TypeVar
)

C = TypeVar("C", bound="Club")
class Club:
    """
    Represents a Brawl Stars club.

    ### Attributes
    name: `str`
        The club's name.
    tag: `str`
        The club's tag.
    description: `str`
        The club's description.
    trophies: `int`
        The club's current total trophies.
    required_trophies: `int`
        The trophies that are required for a new member to join.
    members: List[`~.Member`]
        A list consisting of `Member` objects, representing the club's members.
    type: `str`
        The club's type (i.e. "Open"/"Invite Only"/"Closed").
    badge_id: `int`
        The club's badge ID.
    president: `~.Member`
        A `Member` object representing the club's president.
    """
    def __init__(self: C, club: Any) -> None:
        self.push_data({camel_to_snake(key): value for key, value in club.items()})

    def __repr__(self: C) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} tag={self.tag!r} members={len(self.members)}>"

    def __str__(self: C) -> str:
        return f"{self.name} ({self.tag})"

    def push_data(self: C, data: Any) -> None:
        self._name: str = data["name"]
        self._tag: str = data["tag"]
        self._description: str = data["description"]
        self._trophies: int = data["trophies"]
        self._required_trophies: str = data["required_trophies"]
        self._type: str = data["type"]
        self._badge_id: int = data["badge_id"]
        self._members: Any = data["members"]


    @property
    def name(self: C) -> str:
        """`str`: The club's name."""
        return self._name

    @property
    def tag(self: C) -> str:
        """`str`: The club's tag."""
        return self._tag

    @property
    def description(self: C) -> str:
        """`str`: The club's description."""
        return self._description

    @property
    def trophies(self: C) -> int:
        """`int`: The club's current total trophies."""
        return self._trophies

    @property
    def required_trophies(self: C) -> int:
        """`int`: The trophies that are required for a new member to join."""
        return self._required_trophies

    @property
    def members(self: C) -> List[Member]:
        """List[`~.Member`]: A list consisting of `Member` objects, representing the club's members."""
        return [Member(member) for member in self._members]

    @property
    def type(self: C) -> str:
        """`str`: The club's type (i.e. "Open"/"Invite Only"/"Closed")."""
        if self._type.lower() != "inviteonly":
            return self._type.capitalize()
        return "Invite Only"

    @property
    def badge_id(self: C) -> int:
        """`int`: The club's badge ID."""
        return self._badge_id

    @property
    def president(self: C) -> Member:
        """`~.Member`: A `Member` object representing the club's president."""
        for m in self.members:
            if m.role == "President":
                return m
