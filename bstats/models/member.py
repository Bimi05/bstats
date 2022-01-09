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

from ..utils import camel_to_snake

class ClubMember:
    """
    Represents a Brawl Stars club member.

    Attributes
    ----------

    name: ``str``
        The member's name.
    tag: ``str``
        The member's unique in-game tag.
    color: ``str``
        The hex code for the member's name colour.
    colour: ``str``
        An alias of ``ClubMember.color``.
    role: ``str``
        The member's role in the club (i.e. Member/Senior/Vice President/President)
    trophies: ``int``
        The member's current total trophies.
    icon_id: ``int``
        The member's icon ID.
    """
    def __init__(self, data: dict) -> None:
        self.data = {}
        for key in data:
            self.data[camel_to_snake(key)] = data[key]

    def __repr__(self) -> str:
        return f"<ClubMember object name='{self.data['name']}' tag='{self.data['tag']}'>"

    def __str__(self) -> str:
        return f"{self.data['name']} ({self.data['tag']}): {self.role}"


    @property
    def name(self) -> str:
        """``str``: The member's name."""
        return self.data["name"]

    @property
    def tag(self) -> str:
        """``str``: The member's unique in-game tag."""
        return self.data["tag"]

    @property
    def color(self) -> str:
        """``str``: The hex code for the member's name colour."""
        return self.data["name_color"]

    @property
    def colour(self) -> str:
        """``str``: An alias of ``ClubMember.color``."""
        return self.color

    @property
    def role(self) -> str:
        """``str``: The member's role in the club (i.e. Member/Senior/Vice President/President)"""
        return self.data["role"].title() if self.data["role"].lower() != "vicepresident" else "Vice President"

    @property
    def trophies(self) -> int:
        """``int``: The member's current total trophies."""
        return self.data["trophies"]

    @property
    def icon_id(self) -> int:
        """``int``: The member's icon ID."""
        return self.data["icon"]["id"]

