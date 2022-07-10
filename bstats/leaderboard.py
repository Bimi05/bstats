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
    Optional,
    Any,
    TypeVar
)

LPE = TypeVar("LPE", bound="LeaderboardPlayerEntry")
class LeaderboardPlayerEntry:
    """
    Represents a Brawl Stars leaderboard ranking entry for players.

    ### Attributes
    name: `str`
        The player's name.
    tag: `str`
        The player's tag.
    trophies: `int`
        The player's current total trophies.
    rank: `int`
        The player's leaderboard rank.
    colour: `str`
        The hex code representing the player's name colour (#XXXXXX).
    color: `str`
        An alias of `.colour`.
    icon_id: `int`
        The ID of the player's icon.
    club_name: Optional[`str`]
        The player's club's name.
        `None` if the member is not in any club.
    """
    def __init__(self: LPE, ranking: Any) -> None:
        self.push_data({camel_to_snake(key): value for key, value in ranking.items()})

    def __repr__(self: LPE) -> str:
        return f"<{self.__class__.__name__} rank={self.rank} name={self.name!r} tag={self.tag!r}>"

    def __str__(self: LPE) -> str:
        return f"Rank {self.rank}: {self.name} ({self.tag})"

    def push_data(self: LPE, data: Any) -> None:
        self._name = data["name"]
        self._tag = data["tag"]
        self._trophies = data["trophies"]
        self._rank = data["rank"]
        self._colour = data["name_color"]
        self._icon_id = data["icon"]["id"]
        self._club = data.get("club")


    @property
    def name(self: LPE) -> str:
        """`str`: The player's name."""
        return self._name

    @property
    def tag(self: LPE) -> str:
        """`str`: The player's tag."""
        return self._tag

    @property
    def trophies(self: LPE) -> int:
        """`int`: The player's current total trophies."""
        return self._trophies

    @property
    def rank(self: LPE) -> int:
        """`int`: The player's leaderboard rank."""
        return self._rank

    @property
    def colour(self: LPE) -> str:
        """`str`: The hex code representing the player's name colour (#XXXXXX)."""
        return f"#{self._colour[4:]}"

    @property
    def color(self: LPE) -> str:
        """`str`: An alias of `.colour`."""
        return self.colour

    @property
    def icon_id(self: LPE) -> int:
        """`int`: The ID of the player's icon."""
        return self._icon_id

    @property
    def club_name(self: LPE) -> Optional[str]:
        """Optional[`str`]: The player's club's name. `None` if the member is not in any club."""
        if self._club:
            return self._club["name"]
        return None

LCE = TypeVar("LCE", bound="LeaderboardClubEntry")
class LeaderboardClubEntry:
    """
    Represents a Brawl Stars leaderboard ranking entry.

    ### Attributes
    name: `str`
        The club's name.
    tag: `str`
        The club's tag.
    trophies: `int`
        The club's current total trophies.
    rank: `int`
        The club's leaderboard rank.
    member_count: `int`
        The club's current amount of members.
    badge_id: `int`
        The club's badge ID.
    """
    def __init__(self: LCE, ranking: Any) -> None:
        self.push_data({camel_to_snake(key): value for key, value in ranking.items()})

    def __repr__(self: LCE) -> str:
        return f"<{self.__class__.__name__} rank={self.ranking['rank']} name={self.ranking['name']!r} tag={self.ranking['tag']!r}>"

    def __str__(self: LCE) -> str:
        return f"Rank {self.ranking['rank']}: {self.ranking['name']} ({self.ranking['tag']})"

    def push_data(self: LCE, data: Any) -> None:
        self._name = data["name"]
        self._tag = data["tag"]
        self._trophies = data["trophies"]
        self._rank = data["rank"]
        self._member_count = data["member_count"]
        self._badge_id = data["badge_id"]


    @property
    def name(self: LCE) -> str:
        """`str`: The club's name."""
        return self._name

    @property
    def tag(self: LCE) -> str:
        """`str`: The club's tag."""
        return self._tag

    @property
    def trophies(self: LCE) -> int:
        """`int`: The club's current total trophies."""
        return self._trophies

    @property
    def rank(self: LCE) -> int:
        """`int`: The club's leaderboard rank."""
        return self._rank

    @property
    def member_count(self: LCE) -> int:
        """`int`: The club's current amount of members."""
        return self._member_count

    @property
    def badge_id(self: LCE) -> int:
        """`int`: The club's badge ID."""
        return self._badge_id

