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

from .club import Club
from .brawler import Brawler

from typing import List
from ..http import HTTPClient, APIRoute
from ..utils import camel_to_snake, format_tag

class Profile:
    """
    Represents a Brawl Stars profile.

    Attributes
    ----------

    name: ``str``
        The player's in-game name.
    tag: ``str``
        The player's in-game tag.
    trophies: ``int``
        The player's current total amount of trophies.
    highest_trophies: ``int``
        The player's highest total amount of trophies.
    is_cc_qualified: ``bool``
        Whether the player has qualified from a championship challenge (aka got 15 wins).
    level: ``int``
        The player's current experience level.
    exp_points: ``int``
        The player's lifetime gained experience points.
        .. note::
            These are lifetime exp points, not the ones on the current level
            and/or the required ones to advance to the next level.
            To access the exp the player is on and the exp required for the next level,
            refer to :meth:`utils.calculate_exp()`
    x3vs3_victories: ``int``
        The player's amount of 3vs3 victories.
    team_victories: ``int``
        An alias of ``x3vs3_victories``.
    solo_victories: ``int``
        The player's amount of solo showdown victories.
    duo_victories: ``int``
        The player's amount of duo showdown victories.
    club: ``Club``
        A ``Club`` object representing the player's club.
    brawlers: List[``Brawler``]
        A list consisting of ``Brawler`` objects, representing the player's brawlers.
    """
    def __init__(self, client, data: dict) -> None:
        self.client = client
        self.data = {}
        for key in data:
            self.data[camel_to_snake(key)] = data[key]

    def __repr__(self) -> str:
        return f"<Player object name='{self.data['name']}' tag='{self.data['tag']}' brawlers={len(self.data['brawlers'])}>"

    def __str__(self) -> str:
        return f"{self.data['name']} ({self.data['tag']})"


    @property
    def name(self) -> str:
        """``str``: The player's in-game name."""
        return self.data["name"]

    @property
    def tag(self) -> str:
        """``str``: The player's unique tag."""
        return self.data["tag"]

    @property
    def trophies(self) -> int:
        """``int``: The player's current total amount of trophies."""
        return self.data["trophies"]

    @property
    def highest_trophies(self) -> int:
        """``int``: The player's highest total amount of trophies."""
        return self.data["highest_trophies"]

    def is_cc_qualified(self) -> bool:
        """``bool``: Whether the player has qualified from the championship challenge (aka got 15 wins)."""
        return self.data["is_qualified_from_championship_challenge"]

    @property
    def level(self) -> int:
        """``int``: The player's current experience level."""
        return self.data["exp_level"]

    @property
    def exp_points(self) -> int:
        """``int``: The player's lifetime gained experience points."""
        return self.data["exp_points"]

    @property
    def x3vs3_victories(self) -> int:
        """``int``: The player's amount of 3vs3 victories."""
        return self.data["3vs3_victories"]

    @property
    def team_victories(self) -> int:
        """``int``: An alias of ``x3vs3_victories``."""
        return self.x3vs3_victories

    @property
    def solo_victories(self) -> int:
        """``int``: The player's amount of solo showdown victories."""
        return self.data["solo_victories"]

    @property
    def duo_victories(self) -> int:
        """``int``: The player's amount of duo showdown victories."""
        return self.data["duo_victories"]

    @property
    def club(self) -> Club:
        """``Club``: A ``Club`` object representing the player's club."""
        return Club(self.client, HTTPClient(self.client.timeout, self.client.session, self.client.headers, self.client.cache).request(APIRoute(f"/clubs/{format_tag(self.data['club']['tag'])}").url, use_cache=True))

    @property
    def brawlers(self) -> List[Brawler]:
        """List[``Brawler``]: A list consisting of ``Brawler`` objects, representing the player's brawlers."""
        return [Brawler(brawler) for brawler in self.data["brawlers"]]

