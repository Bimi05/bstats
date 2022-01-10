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
from .member import ClubMember
from ..utils import camel_to_snake

class Club:
    """
    Represents a Brawl Stars club.

    Attributes
    ----------

    name: ``str``
        The club's name.
    tag: ``str``
        The club's unique tag.
    description: ``str``
        The club's clean (as it is/with no modification) description.
    trophies: ``int``
        The club's current total trophies.
    required_trophies: ``int``
        The club's required trophies for a new member to join.
    members: List[``ClubMember``]
        A list consisting of ``ClubMember`` objects, representing each of the club's members.
    type: ``str``
        The club's type (i.e. Open/Invite Only/Closed).
    badge_id: ``int``
        The club's badge ID.
    president: ``ClubMember``
        A ``ClubMember`` object representing the club's president.
    """
    def __init__(self, data):
        self.data = {}
        for key in data:
            self.data[camel_to_snake(key)] = data[key]

    def __repr__(self):
        return f"<Club object name='{self.data['name']}' tag='{self.data['tag']}' members={len(self.data['members'])}>"

    def __str__(self):
        return f"{self.data['name']} ({self.data['tag']})"


    @property
    def name(self) -> str:
        """``str``: The club's name."""
        return self.data["name"]

    @property
    def tag(self) -> str:
        """``str``: The club's unique tag."""
        return self.data["tag"]

    @property
    def description(self) -> str:
        """``str``: The club's clean (as it is/with no modification) description."""
        return self.data["description"]

    @property
    def trophies(self) -> int:
        """``int``: The club's current total trophies."""
        return self.data["trophies"]

    @property
    def required_trophies(self) -> int:
        """``int``: The club's required trophies for a new member to join."""
        return self.data["required_trophies"]

    @property
    def members(self) -> List[ClubMember]:
        """List[``ClubMember``]: A list consisting of ``ClubMember`` objects, representing each of the club's members."""
        return [ClubMember(member) for member in self.data["members"]]

    @property
    def type(self) -> str:
        """``str``: The club's type (i.e. Open/Invite Only/Closed)."""
        return self.data["type"].capitalize() if self.data["type"].lower() != "inviteonly" else "Invite Only"

    @property
    def badge_id(self) -> int:
        """``int``: The club's badge ID."""
        return self.data["badge_id"]

    @property
    def president(self):
        """``ClubMember``: A ``ClubMember`` object representing the club's president."""
        for cm in self.members:
            if cm.role == "President":
                return ClubMember(cm)

