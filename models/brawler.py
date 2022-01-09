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
from ..utils import camel_to_snake

class Gadget:
    """
    Represents a Brawl Stars brawler's gadget.
    
    Attributes
    ----------

    name: ``str``
        The gadget's name.
    id: ``int``
        The gadget's unique ID.
    """
    def __init__(self, gadget: dict) -> None:
        self.gadget = gadget

    def __repr__(self) -> str:
        return f"<Gadget object name='{self.gadget['name'].title()}' id={self.gadget['id']}>"


    @property
    def name(self) -> str:
        """``str``: The gadget's name."""
        return self.gadget["name"]

    @property
    def id(self) -> int:
        """``int``: The gadget's unique ID."""
        return self.gadget["id"]

class StarPower:
    """
    Represents a Brawl Stars brawler's star power.

    Attributes
    ----------

    name: ``str``
        The star power's name.
    id: ``int``
        The star power's unique ID.
    """
    def __init__(self, sp: dict) -> None:
        self.star_power = sp

    def __repr__(self) -> str:
        return f"<StarPower object name='{self.star_power['name'].title()}' id={self.star_power['id']}>"


    @property
    def name(self) -> str:
        """``str``: The star power's name."""
        return self.star_power["name"]

    @property
    def id(self) -> int:
        """``int``: The star power's unique ID."""
        return self.star_power["id"]

class Gear:
    """
    Represents a Brawl Stars brawler's gear.

    Attributes
    ----------

    name: ``str``
        The gear's name.
    id: ``int``
        The gear's unique ID.
    level: ``int``
        The gear's level.
    """
    def __init__(self, gear: dict) -> None:
        self.gear = gear

    def __repr__(self) -> str:
        return f"<Gear object name='{self.gear['name']}' id={self.gear['id']} level={self.gear['level']}>"


    @property
    def name(self) -> str:
        """``str``: The gear's name."""
        return self.gear["name"]

    @property
    def id(self) -> int:
        """``int``: The gear's unique ID."""
        return self.gear["id"]

    @property
    def level(self) -> int:
        """``int``: The gear's level."""
        return self.gear["level"]



class Brawler:
    """
    Represents a Brawl Stars brawler.

    Attributes
    ----------

    name: ``int``
        The brawler's name.
    id: ``int``
        The brawler's unique ID.
    power: ``int``
        The brawler's power level.
    rank: ``int``
        The brawler's rank.
    trophies: ``int``
        The brawler's current trophies.
    highest_trophies: ``int``
        The brawler's highest trophies.
    gadgets: List[``Gadget``]
        A list of the brawler's unlocked gadgets.
    star_powers: List[``StarPower``]
        A list of the brawler's unlocked star powers.
    gears: List[``Gear``]
        A list of the brawler's unlocked gears.
    """
    def __init__(self, data: dict):
        self.data = {}
        for key in data:
            self.data[camel_to_snake(key)] = data[key]

    def __repr__(self):
        return f"<Brawler object name='{self.data['name'].title()}' id={self.data['id']} power={self.data['power']}>"

    def __str__(self) -> str:
        return f"'{self.data['name'].title()}' (Power {self.data['power']:02d}): Rank {self.data['rank']}"


    @property
    def name(self) -> str:
        """``str``: The brawler's name."""
        return self.data["name"].title()

    @property
    def id(self) -> int:
        """``int``: The brawler's unique ID."""
        return self.data["id"]

    @property
    def power(self) -> int:
        """``int``: The brawler's power level."""
        return self.data["power"]

    @property
    def rank(self) -> int:
        """``int``: The brawler's rank."""
        return self.data["rank"]

    @property
    def trophies(self) -> int:
        """``int``: The brawler's current trophies."""
        return self.data["trophies"]

    @property
    def highest_trophies(self) -> int:
        """``int``: The brawler's highest trophies."""
        return self.data["highest_trophies"]

    @property
    def gadgets(self) -> List[Gadget]:
        """List[``Gadget``]: A list of the brawler's unlocked gadgets."""
        return [Gadget(gadget) for gadget in self.data["gadgets"]]

    @property
    def star_powers(self) -> List[StarPower]:
        """List[``StarPower``]: A list of the brawler's unlocked star powers."""
        return [StarPower(sp) for sp in self.data["star_powers"]]

    @property
    def gears(self) -> List[Gear]:
        """List[``Gear``]: A list of the brawler's unlocked gears."""
        return [Gear(gear) for gear in self.data["gears"]]

