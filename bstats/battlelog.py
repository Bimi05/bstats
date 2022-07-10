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

import datetime

from .utils import camel_to_snake
from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Union,
    TypeVar
)

class EntryBrawler:
    """
    # Do not manually initialise this.
    Represents a player's brawler in a Brawl Stars battle log entry.

    ### Attributes
    name: `str`
        The brawler's name.
    id: `int`
        The brawler's ID.
    power: `int`
        The brawler's power level (1-11 exclusive).
    trophies: `int`
        The brawler's trophies at the time of the entry.
    """
    def __init__(self, brawler: Any) -> None:
        self.push_data(brawler)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} id={self.id} power={self.power} trophies={self.trophies}>"

    def push_data(self, data: Any) -> None:
        self._name: str = data["name"]
        self._id: int = data["id"]
        self._power: int = data["power"]
        self._trophies: int = data["trophies"]


    @property
    def name(self) -> str:
        """`str`: The brawler's name."""
        return self._name.title()

    @property
    def id(self) -> int:
        """`int`: The brawler's ID."""
        return self._id

    @property
    def power(self) -> int:
        """`int`: The brawler's power level (1-11 exclusive)."""
        return self._power

    @property
    def trophies(self) -> int:
        """`int`: The brawler's trophies at the time of the entry."""
        return self._trophies

class EntryPlayer:
    """
    # Do not manually initialise this.
    Represents a player in a Brawl Stars battle log entry.

    ### Attributes
    name: `str`
        The player's name.
    tag: `str`
        The player's tag.
    brawler: `~.EntryBrawler`
        A `EntryBrawler` object representing the player's brawler.
    """
    def __init__(self, player: Any) -> None:
        self.push_data(player)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} tag={self.tag!r} brawler={self.brawler}>"

    def __str__(self) -> str:
        return f"{self._name} ({self._tag})"

    def push_data(self, data: Any) -> None:
        self._name: str = data["name"]
        self._tag: str = data["tag"]
        self._brawler: Any = data["brawler"]


    @property
    def name(self) -> str:
        """`str`: The player's name."""
        return self._name

    @property
    def tag(self) -> str:
        """`str`: The player's tag."""
        return self._tag

    @property
    def brawler(self) -> EntryBrawler:
        """`~.EntryBrawler`: A `EntryBrawler` object representing the player's brawler."""
        return EntryBrawler(self._brawler)


BE = TypeVar("BE", bound="BattlelogEntry")
class BattlelogEntry:
    """
    Represents a Brawl Stars battle log entry.

    ### Attributes
    name: `str`
        The mode's name.
    id: `int`
        The mode's ID.
    map: `str`
        The mode's map. If `None`, return "Community Map".
    result: `str`
        The result of the battle (Defeat/Draw/Victory in case of 3v3, the rank in case of showdown).
    time: `str`
        The time at which the entry was recorded.
    duration: Tuple[`int`, `int`]
        How long the battle lasted.
    trophy_change: `int`
        The amount of trophies the player gained or lost from the battle.
    players: List[`~.EntryPlayer`]
        The players that took part in the battle.
    star_player: `~.EntryPlayer`
        The star player of the battle.
    """
    def __init__(self: BE, data: Any) -> None:
        self.push_data({camel_to_snake(key): value for key, value in data.items()})

    def __repr__(self: BE) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} result={self.result!r}>"

    def push_data(self: BE, data: Any) -> None:
        self._name: str = data["event"]["mode"] or data["battle"]["mode"]
        self._id: int = data["event"]["id"]
        self._map: Optional[str] = data["event"].get("map")
        self._result: Union[int, str] = data["battle"]["result"] or data["battle"]["rank"]
        self._time: str = data["battle_time"]
        self._duration: int = data["battle"]["duration"]
        self._trophy_change: int = data["battle"]["trophyChange"]
        self._players: Union[List[List[Any]], List[Any]] = data["battle"]["teams"] or data["battle"]["players"]
        self._star_player: Any = data["battle"]["starPlayer"]


    @property
    def name(self: BE) -> str:
        """`str`: The mode's name."""
        name = " ".join([word.capitalize() for word in camel_to_snake(self._name).split("_")])
        return name

    @property
    def id(self: BE) -> int:
        """`int`: The mode's ID."""
        return self._id

    @property
    def map(self: BE) -> str:
        """`str`: The mode's map. If `None`, return "Community Map"."""
        if self._map:
            return self._map
        return "Community Map"

    @property
    def result(self: BE) -> str:
        """`str`: The result of the battle (Defeat/Draw/Victory in case of 3v3, the rank in case of showdown)."""
        if type(self._result) is int:
            return f"Rank {self._result}"
        return self._result.capitalize()

    @property
    def time(self: BE) -> datetime.datetime:
        """`str`: The time at which the entry was recorded."""
        return datetime.datetime.strptime(self._time, "%Y%m%dT%H%M%S.%fZ")

    @property
    def duration(self: BE) -> Tuple[int, int]:
        """Tuple[`int`, `int`]: How long the battle lasted."""
        return divmod(self._duration, 60)

    @property
    def trophy_change(self: BE) -> int:
        """`int`: The amount of trophies the player gained or lost from the battle."""
        return self._trophy_change

    @property
    def players(self: BE) -> List[EntryPlayer]:
        """List[`~.EntryPlayer`]: The players that took part in the battle."""
        try:
            getattr(self._players[0], "append")
        except AttributeError:
            return [EntryPlayer(player) for player in self._players]
        else:
            from functools import reduce
            return reduce(lambda x, y: x + y, self._players)

    @property
    def star_player(self: BE) -> EntryPlayer:
        """`~.EntryPlayer`: The star player of the battle."""
        return EntryPlayer(self._star_player)
