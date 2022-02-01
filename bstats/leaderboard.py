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
from .utils import camel_to_snake


class LeaderboardEntry:
    """
    Represents a Brawl Stars leaderboard ranking entry.
    
    Attributes for Players/Brawlers rankings
    ----------

    name: ``str``
        The player's or the club's name.
    tag: ``str``
        The player's or the club's unique tag.
    trophies: ``int``
        The player's or the club's current total trophies.
    rank: ``int``
        The player's or the club's leaderboard rank.
    color: Optional[``str``]
        The hex code representing the player's name colour. ``None`` if the current leaderboard rankings are focused on clubs.
    colour: Optional[``str``]
        An alias to ``LeaderboardPlayerEntry.color``. ``None`` if the current leaderboard rankings are focused on clubs.
    icon_id: Optional[``int``]
        The ID of the player's icon. ``None`` if the current leaderboard rankings are focused on clubs.
    club_name: Optional[``str``]
        The player's club's name, ``None`` if the current leaderboard rankings are focused on clubs or if the member is not in any club.
    member_count: Optional[``int``]
        The club's current amount of members. ``None`` if the current leaderboard rankings are focused on players.
    badge_id: Optional[``int``]
        The club's badge ID. ``None`` if the current leaderboard rankings are focused on players.
    """
    def __init__(self, ranking: dict) -> None:
        self.ranking = {}
        for key in ranking:
            self.ranking[camel_to_snake(key)] = ranking[key]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object rank={self.ranking['rank']} name='{self.ranking['name']}' tag='{self.ranking['tag']}'>"

    def __str__(self) -> str:
        return f"Rank {self.ranking['rank']}: {self.ranking['name']} ({self.ranking['tag']})"


    @property
    def name(self) -> str:
        """``str``: The player's or the club's name."""
        return self.ranking["name"]

    @property
    def tag(self) -> str:
        """``str``: The player's or the club's unique tag."""
        return self.ranking["tag"]

    @property
    def trophies(self) -> int:
        """``int``: The player's or the club's current total trophies."""
        return self.ranking["trophies"]

    @property
    def rank(self) -> int:
        """``int``: The player's or the club's leaderboard rank."""
        return self.ranking["rank"]

    @property
    def color(self) -> Optional[str]:
        """Optional[``str``]: The hex code representing the player's name colour. ``None`` if the current leaderboard rankings are focused on clubs."""
        try:
            return self.ranking["name_color"]
        except KeyError:
            return None

    @property
    def colour(self) -> Optional[str]:
        """An alias to ``LeaderboardPlayerEntry.color``."""
        return self.color

    @property
    def icon_id(self) -> Optional[int]:
        """Optional[``int``]: The ID of the player's icon. ``None`` if the current leaderboard rankings are focused on clubs."""
        try:
            return self.ranking["icon"]["id"]
        except KeyError:
            return None

    @property
    def club_name(self) -> Optional[str]:
        """Optional[``str``]: The player's club's name. ``None`` if the current leaderboard rankings are focused on clubs or if the member is not in any club."""
        try:
            return self.ranking["club"]["name"]
        except KeyError:
            return None

    @property
    def member_count(self) -> Optional[int]:
        """Optional[``int``]: The club's current amount of members. ``None`` if the current leaderboard rankings are focused on players."""
        try:
            return self.ranking["member_count"]
        except KeyError:
            return None

    @property
    def badge_id(self) -> Optional[int]:
        """Optional[``int``]: The club's badge ID. ``None`` if the current leaderboard rankings are focused on players."""
        try:
            return self.ranking["badge_id"]
        except KeyError:
            return None

