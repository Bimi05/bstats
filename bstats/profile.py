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

import asyncio

from .club import Club
from .brawler import Brawler

from .utils import camel_to_snake

from typing import (
    List,
    Any,
    TypeVar
)

P = TypeVar("P", bound="Profile")
class Profile:
    """
    Represents a Brawl Stars profile.
    You can access your profile by clicking the top left box
    which has your icon and name colour.

    ### Attributes
    name: `str`
        The player's in-game name.
    tag: `str`
        The player's in-game unique tag.
    trophies: `int`
        The player's current total amount of trophies.
    highest_trophies: `int`
        The player's highest total amount of trophies.
    colour: `str`
        The player's profile colour represented as a hex (#XXXXXX).
    color: `str`
        An alias to `.colour`.
    icon_id: `int`
        The player's icon ID.
    is_cc_qualified: `bool`
        Whether the player has qualified from a championship challenge (aka got 15 wins).
    level: `int`
        The player's current experience level.
    exp_points: `int`
        The player's lifetime gained experience points.
        - These are lifetime exp points, not the ones on the current level
        and/or the required ones to advance to the next level.
        To access the exp the player is on and the exp required for the next level,
        refer to `utils.calculate_exp()`

    x3vs3_victories: `int`
        The player's amount of 3vs3 victories. An alias exists, `.team_victories`.
    team_victories: `int`
        The player's amount of 3vs3 victories. An alias exists, `.x3vs3_victories`.
    solo_victories: `int`
        The player's amount of solo showdown victories.
    duo_victories: `int`
        The player's amount of duo showdown victories.
    club: `Club`
        A `Club` object representing the player's club.
    brawlers: List[`Brawler`]
        A list consisting of `Brawler` objects, representing the player's brawlers.
    """
    def __init__(self: P, data: Any) -> None:
        self.push_data({camel_to_snake(key): value for key, value in data.items()})

    def __repr__(self: P) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} tag={self.tag!r} brawlers={len(self.brawlers)}>"

    def __str__(self: P) -> str:
        return f"{self.name} ({self.tag})"

    def push_data(self: P, data: Any) -> None:
        self._name: str = data["name"]
        self._tag: str = data["tag"]
        self._trophies: int = data["trophies"]
        self._highest_trophies: int = data["highest_trophies"]
        self._colour: str = data["name_color"]
        self._icon_id: int = data["icon"]["id"]
        self._is_cc_qualified: bool = data["is_qualified_from_championship_challenge"]
        self._level: int = data["exp_level"]
        self._exp: int = data["exp_points"]
        self._x3vs3_victories: int = data["3vs3_victories"]
        self._solo_victories: int = data["solo_victories"]
        self._duo_victories: int = data["duo_victories"]
        self._club: Any = data["club"]
        self._brawlers: Any = data["brawlers"]


    @property
    def name(self: P) -> str:
        """`str`: The player's in-game name."""
        return self._name

    @property
    def tag(self: P) -> str:
        """`str`: The player's unique unique tag."""
        return self._tag

    @property
    def trophies(self: P) -> int:
        """`int`: The player's current total amount of trophies."""
        return self._trophies

    @property
    def highest_trophies(self: P) -> int:
        """`int`: The player's highest total amount of trophies."""
        return self._highest_trophies

    @property
    def colour(self: P) -> str:
        """`str`: The player's profile colour represented as a hex (#XXXXXX)."""
        return f"#{self._colour[4:]}"

    @property
    def color(self: P) -> str:
        """`str`: An alias to `.colour`."""
        return self.colour
    
    @property
    def icon_id(self: P) -> int:
        """`int`: The player's icon ID."""
        return self._icon_id


    def is_cc_qualified(self: P) -> bool:
        """`bool`: Whether the player has qualified from the championship challenge (aka got 15 wins)."""
        return self._is_cc_qualified

    @property
    def level(self: P) -> int:
        """`int`: The player's current experience level."""
        return self._level

    @property
    def experience(self: P) -> int:
        """`int`: The player's lifetime gained experience points."""
        return self._exp

    @property
    def exp(self: P) -> int:
        """`int`: An alias of `.experience`."""
        return self.experience

    @property
    def x3vs3_victories(self: P) -> int:
        """`int`: The player's amount of 3vs3 victories. An alias exists, `.team_victories`."""
        return self._x3vs3_victories

    @property
    def team_victories(self: P) -> int:
        """`int`: The player's amount of 3vs3 victories. An alias exists, `.x3vs3_victories`."""
        return self.x3vs3_victories

    @property
    def solo_victories(self: P) -> int:
        """`int`: The player's amount of solo showdown victories."""
        return self._solo_victories

    @property
    def duo_victories(self: P) -> int:
        """`int`: The player's amount of duo showdown victories."""
        return self._duo_victories

    @property
    def club(self: P) -> str:
        """`str`: The club's tag. Useful to easily access the club's info via `.get_club()`."""
        return self._club.pop("tag", None)

    @property
    def brawlers(self: P) -> List[Brawler]:
        """List[`Brawler`]: A list consisting of `Brawler` objects, representing the player's brawlers."""
        return [Brawler(brawler) for brawler in self._brawlers]

