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

from typing import List
from .member import Member
from .utils import camel_to_snake
from .metadata.club import Club as ClubPayload

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
    members: List[`~.ClubMember`]
        A list consisting of `ClubMember` objects, representing the club's members.
    type: `str`
        The club's type (i.e. "Open"/"Invite Only"/"Closed").
    badge_id: `int`
        The club's badge ID.
    president: `~.ClubMember`
        A `ClubMember` object representing the club's president.
    """
    def __init__(self, data: dict):
        self.data = {camel_to_snake(key): value for key, value in data.items()}
        self.patch_data(self.data)

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r} tag={self.tag!r} members={len(self.members)}>"

    def __str__(self):
        return f"{self.name} ({self.tag})"

    def patch_data(self, payload: ClubPayload):
        self._name = payload["name"]
        self._tag = payload["tag"]
        self._description = payload["description"]
        self._trophies = payload["trophies"]
        self._required_trophies = payload["required_trophies"]
        self._type = payload["type"]
        self._badge_id = payload["badge_id"]


    @property
    def name(self) -> str:
        """`str`: The club's name."""
        return self._name

    @property
    def tag(self) -> str:
        """`str`: The club's tag."""
        return self._tag

    @property
    def description(self) -> str:
        """`str`: The club's description."""
        return self._description

    @property
    def trophies(self) -> int:
        """`int`: The club's current total trophies."""
        return self._trophies

    @property
    def required_trophies(self) -> int:
        """`int`: The trophies that are required for a new member to join."""
        return self._required_trophies

    @property
    def members(self) -> List[Member]:
        """List[`~.ClubMember`]: A list consisting of `ClubMember` objects, representing the club's members."""
        return [Member(member) for member in self.data["members"]]

    @property
    def type(self) -> str:
        """`str`: The club's type (i.e. "Open"/"Invite Only"/"Closed")."""
        return self._type.capitalize() if self._type.lower() != "inviteonly" else "Invite Only"

    @property
    def badge_id(self) -> int:
        """`int`: The club's badge ID."""
        return self._badge_id

    @property
    def president(self):
        """`~.ClubMember`: A `ClubMember` object representing the club's president."""
        for m in self.members:
            if m.role == "President":
                return m
