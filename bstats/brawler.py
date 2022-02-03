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
from .utils import camel_to_snake

class Gadget:
    """
    Represents a Brawl Stars brawler gadget.

    ### Attributes
    name: `str`
        The gadget's name.
    id: `int`
        The gadget's ID.
    """
    def __init__(self, gadget: dict) -> None:
        self.gadget = gadget

    def __repr__(self) -> str:
        return f"<Gadget name={self.gadget['name'].title()!r} id={self.gadget['id']}>"


    @property
    def name(self) -> str:
        """`str`: The gadget's name."""
        return self.gadget["name"]

    @property
    def id(self) -> int:
        """`int`: The gadget's ID."""
        return self.gadget["id"]


class StarPower:
    """
    Represents a Brawl Stars brawler's star power.

    ### Attributes
    name: `str`
        The star power's name.
    id: `int`
        The star power's ID.
    """
    def __init__(self, sp: dict) -> None:
        self.star_power = sp

    def __repr__(self) -> str:
        return f"<StarPower name={self.star_power['name'].title()!r} id={self.star_power['id']}>"


    @property
    def name(self) -> str:
        """`str`: The star power's name."""
        return self.star_power["name"]

    @property
    def id(self) -> int:
        """`int`: The star power's ID."""
        return self.star_power["id"]


class Gear:
    """
    Represents a Brawl Stars brawler's gear.

    ### Attributes
    name: `str`
        The gear's name.
    id: `int`
        The gear's ID.
    level: `int`
        The gear's level.
    """
    def __init__(self, gear: dict) -> None:
        self.gear = gear

    def __repr__(self) -> str:
        return f"<Gear name={self.gear['name']!r} id={self.gear['id']} level={self.gear['level']}>"


    @property
    def name(self) -> str:
        """`str`: The gear's name."""
        return self.gear["name"]

    @property
    def id(self) -> int:
        """`int`: The gear's ID."""
        return self.gear["id"]

    @property
    def level(self) -> int:
        """`int`: The gear's level."""
        return self.gear["level"]


class Brawler:
    """
    Represents a Brawl Stars brawler.

    ### Attributes
    name: `int`
        The brawler's name.
    id: `int`
        The brawler's ID.
    power: `int`
        The brawler's power level (1-11 exclusive).
    rank: `int`
        The brawler's rank.
    trophies: `int`
        The brawler's current trophies.
    highest_trophies: `int`
        The brawler's highest trophies.
    gadgets: List[`~.Gadget`]
        A list of gadgets the brawler has unlocked.
    star_powers: List[`~.StarPower`]
        A list of star powers the brawler has unlocked.
    gears: List[`~.Gear`]
        A list of gears the brawler has crafted.
    """
    def __init__(self, data: dict):
        self.data = {camel_to_snake(key): value for key, value in data.items()}

    def __repr__(self):
        return f"<Brawler name={self.data['name'].title()!r} id={self.data['id']} power={self.data['power']}>"

    def __str__(self) -> str:
        return f"Rank {self.data['rank']} {self.data['name'].title()!r} (Power {self.data['power']:02d})"


    @property
    def name(self) -> str:
        """`str`: The brawler's name."""
        return self.data["name"].title()

    @property
    def id(self) -> int:
        """`int`: The brawler's ID."""
        return self.data["id"]

    @property
    def power(self) -> int:
        """`int`: The brawler's power level (1-11 exclusive)."""
        return self.data["power"]

    @property
    def rank(self) -> int:
        """`int`: The brawler's rank."""
        return self.data["rank"]

    @property
    def trophies(self) -> int:
        """`int`: The brawler's current trophies."""
        return self.data["trophies"]

    @property
    def highest_trophies(self) -> int:
        """`int`: The brawler's highest trophies."""
        return self.data["highest_trophies"]

    @property
    def gadgets(self) -> List[Gadget]:
        """List[`~.Gadget`]: A list of gadgets the brawler has unlocked."""
        return [Gadget(gadget) for gadget in self.data["gadgets"]]

    @property
    def star_powers(self) -> List[StarPower]:
        """List[`~.StarPower`]: A list of star powers the brawler has unlocked."""
        return [StarPower(sp) for sp in self.data["star_powers"]]

    @property
    def gears(self) -> List[Gear]:
        """List[`~.Gear`]: A list of gears the brawler has crafted."""
        return [Gear(gear) for gear in self.data["gears"]]

