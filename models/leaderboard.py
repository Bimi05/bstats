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

from typing import Optional
from ..utils import camel_to_snake


class LeaderboardEntry:
    """
    Represents a Brawl Stars leaderboard ranking entry.
    """
    def __init__(self, ranking: dict) -> None:
        self.ranking = {}
        for key in ranking:
            self.ranking[camel_to_snake(key)] = ranking[key]


class LeaderboardPlayerEntry(LeaderboardEntry):
    """
    Represents a Brawl Stars player leaderboard ranking entry.
    This is both used for the players leaderboard as well as the brawlers leaderboard

    Attributes
    ----------

    name: ``str``
        The player's name.
    tag: ``str``
        The player's unique tag.
    trophies: ``int``
        The player's current total trophies.
    rank: ``int``
        The player's leaderboard rank.
    color: ``str``
        The hex code representing the player's name colour.
    colour: ``str``
        An alias to ``LeaderboardPlayerEntry.color``.
    icon_id: ``int``
        The ID of the player's icon.
    club_name: Optional[``str``]
        The player's club's name, if in any.
    """

    def __repr__(self) -> str:
        return f"<LeaderboardPlayerEntry object name='{self.ranking['name']}' tag='{self.ranking['tag']}'>"

    def __str__(self) -> str:
        return f"{self.ranking['name']} ({self.ranking['tag']})"


    @property
    def name(self) -> str:
        """``str``: The player's name."""
        return self.ranking["name"]

    @property
    def tag(self) -> str:
        """``str``: The player's unique tag."""
        return self.ranking["tag"]

    @property
    def trophies(self) -> int:
        """``int``: The player's current total trophies."""
        return self.ranking["trophies"]

    @property
    def rank(self) -> int:
        """``int``: The player's leaderboard rank."""
        return self.ranking["rank"]

    @property
    def color(self) -> str:
        """``str``: The hex code representing the player's name colour."""
        return self.ranking["name_color"]

    @property
    def colour(self) -> str:
        """An alias to ``LeaderboardPlayerEntry.color``."""
        return self.color

    @property
    def icon_id(self) -> int:
        """``int``: The ID of the player's icon."""
        return self.ranking["icon"]["id"]

    @property
    def club_name(self) -> Optional[str]:
        """Optional[``str``]: The player's club's name, if in any."""
        try:
            return self.ranking["club"]["name"]
        except KeyError:
            return None

class LeaderboardClubEntry(LeaderboardEntry):
    """
    Represents a Brawl Stars club leaderboard ranking entry.

    Attributes
    ----------

    name: ``str``
        The club's name.
    tag: ``str``
        The club's unique tag.
    trophies: ``int``
        The club's current total trophies.
    rank: ``int``
        The club's leaderboard rank.
    member_count: ``int``
        The club's current amount of members.
    badge_id: ``int``
        The club's badge ID.
    """

    def __repr__(self) -> str:
        return f"<LeaderboardClubEntry name='{self.ranking['name']}' tag='{self.ranking['tag']}'>"

    def __str__(self) -> str:
        return f"{self.ranking['name']} ({self.ranking['tag']})"


    @property
    def name(self) -> str:
        """``str``: The club's name."""
        return self.ranking["name"]

    @property
    def tag(self) -> str:
        """``str``: The club's unique tag."""
        return self.ranking["tag"]

    @property
    def trophies(self) -> int:
        """``int``: The club's current total trophies."""
        return self.ranking["trophies"]

    @property
    def rank(self) -> int:
        """``int``: The club's leaderboard rank."""
        return self.ranking["rank"]

    @property
    def member_count(self) -> int:
        """``int``: The club's current amount of members."""
        return self.ranking["member_count"]

    @property
    def badge_id(self) -> int:
        """``int``: The club's badge ID."""
        return self.ranking["badge_id"]
