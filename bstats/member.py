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

from .utils import camel_to_snake

from typing import (
    Any,
    TypeVar
)

M = TypeVar("M", bound="Member")
class Member:
    """
    Represents a Brawl Stars club member.

    ### Attributes
    name: `str`
        The member's name.
    tag: `str`
        The member's tag.
    color: `str`
        The hex code for the member's name color. An alias exists, `.colour`.
    colour: `str`
        The hex code for the member's name colour. An alias exists, `.color`.
    role: `str`
        The member's club role (i.e. "Member"/"Senior"/"Vice President"/"President")
    trophies: `int`
        The member's current total trophies.
    icon_id: `int`
        The member's icon ID.
    """
    def __init__(self: M, member: Any) -> None:
        self.push_data({camel_to_snake(key): value for key, value in member.items()})

    def __repr__(self: M) -> str:
        return f"<Member name={self.name!r} tag={self.tag!r} trophies={self.trophies} role={self.role}>"

    def __str__(self: M) -> str:
        return f"{self.name} ({self.tag}): {self.role}"

    def push_data(self: M, data: Any) -> None:
        self._name: str = data["name"]
        self._tag: str = data["tag"]
        self._colour: str = data["name_color"]
        self._role: str = data["role"]
        self._trophies: int = data["trophies"]
        self._icon_id: int = data["icon"]["id"]


    @property
    def name(self: M) -> str:
        """`str`: The member's name."""
        return self._name

    @property
    def tag(self: M) -> str:
        """`str`: The member's unique in-game tag."""
        return self._tag

    @property
    def color(self: M) -> str:
        """`str`: The hex code for the member's name colour (#XXXXXX)."""
        return f"#{self._colour[4:]}"

    @property
    def colour(self: M) -> str:
        """`str`: An alias of `.color`."""
        return self._color

    @property
    def role(self: M) -> str:
        """`str`: The member's role in the club (i.e. Member/Senior/Vice President/President)"""
        if self._role.lower() != "vicepresident":
            return self._role.title()
        return "Vice President"

    @property
    def trophies(self: M) -> int:
        """`int`: The member's current total trophies."""
        return self._trophies

    @property
    def icon_id(self: M) -> int:
        """`int`: The member's icon ID."""
        return self._icon_id

