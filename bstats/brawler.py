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
    List,
    TypeVar
)

class Gadget:
    """
    # Do not manually initialise this.
    Represents a Brawl Stars brawler gadget.

    ### Attributes
    name: `str`
        The gadget's name.
    id: `int`
        The gadget's ID.
    """
    def __init__(self, gadget: Any) -> None:
        self.push_data(gadget)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} id={self.id}>"

    def push_data(self, data: Any) -> None:
        self._name: str = data["name"]
        self._id: int = data["id"]


    @property
    def name(self) -> str:
        """`str`: The gadget's name."""
        return self._name.title()

    @property
    def id(self) -> int:
        """`int`: The gadget's ID."""
        return self._id

class StarPower:
    """
    # Do not manually initialise this.
    Represents a Brawl Stars brawler's star power.

    ### Attributes
    name: `str`
        The star power's name.
    id: `int`
        The star power's ID.
    """
    def __init__(self, sp: Any) -> None:
        self.push_data(sp)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} id={self.id}>"

    def push_data(self, data: Any) -> None:
        self._name: str = data["name"]
        self._id: int = data["id"]


    @property
    def name(self) -> str:
        """`str`: The star power's name."""
        return self._name.title()

    @property
    def id(self) -> int:
        """`int`: The star power's ID."""
        return self._id

class Gear:
    """
    # Do not manually initialise this.
    Represents a Brawl Stars brawler's gear.

    ### Attributes
    name: `str`
        The gear's name.
    id: `int`
        The gear's ID.
    level: `int`
        The gear's level.
    """
    def __init__(self, gear: Any) -> None:
        self.push_data(gear)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} id={self.id} level={self.level}>"

    def push_data(self, data: Any) -> None:
        self._name: str = data["name"]
        self._id: int = data["id"]
        self._level: int = data["level"]


    @property
    def name(self) -> str:
        """`str`: The gear's name."""
        return self._name.title()

    @property
    def id(self) -> int:
        """`int`: The gear's ID."""
        return self._id

    @property
    def level(self) -> int:
        """`int`: The gear's level."""
        return self._level


B = TypeVar("B", bound="Brawler")
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
    def __init__(self: B, data: Any):
        self.push_data({camel_to_snake(key): value for key, value in data.items()})

    def __repr__(self: B):
        return f"<{self.__class__.__name__} name={self.name!r} id={self.id} power={self.power} trophies={self.trophies}>"

    def __str__(self: B) -> str:
        return f"Rank {self.rank} {self.name!r} (Power {self.power:02d})"

    def push_data(self: B, data: Any) -> None:
        self._name: str = data["name"]
        self._id: int = data["id"]
        self._power: int = data.get("power")
        self._rank: int = data.get("rank")
        self._trophies: int = data.get("trophies")
        self._highest_trophies: int = data.get("highest_trophies")
        self._gadgets: Any = data["gadgets"]
        self._star_powers: Any = data["star_powers"]
        self._gears: Any = data["gears"]


    @property
    def name(self: B) -> str:
        """`str`: The brawler's name."""
        return self._name.title()

    @property
    def id(self: B) -> int:
        """`int`: The brawler's ID."""
        return self._id

    @property
    def power(self: B) -> int:
        """`int`: The brawler's power level (1-11 exclusive)."""
        return self._power

    @property
    def rank(self: B) -> int:
        """`int`: The brawler's rank."""
        return self._rank

    @property
    def trophies(self: B) -> int:
        """`int`: The brawler's current trophies."""
        return self._trophies

    @property
    def highest_trophies(self: B) -> int:
        """`int`: The brawler's highest trophies."""
        return self._highest_trophies

    @property
    def gadgets(self: B) -> List[Gadget]:
        """List[`~.Gadget`]: A list of gadgets the brawler has unlocked."""
        return [Gadget(gadget) for gadget in self._gadgets]

    @property
    def star_powers(self: B) -> List[StarPower]:
        """List[`~.StarPower`]: A list of star powers the brawler has unlocked."""
        return [StarPower(sp) for sp in self._star_powers]

    @property
    def gears(self: B) -> List[Gear]:
        """List[`~.Gear`]: A list of gears the brawler has crafted."""
        return [Gear(gear) for gear in self._gears]

