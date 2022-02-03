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

import datetime

from .utils import camel_to_snake
from typing import List, Tuple, Union

class EntryBrawler:
    """
    # Do not manually initialise this.
    Represents a player's brawler in a Brawl Stars battle log entry.

    ### Attributes
    name: `str`
        The brawler's name.
    id: `int`
        The brawler's unique ID.
    power: `int`
        The brawler's power level (1-11 exclusive).
    trophies: `int`
        The brawler's trophies at the time of the entry.
    """
    def __init__(self, brawler: dict) -> None:
        self.brawler = brawler

    def __repr__(self) -> str:
        return f"<BattlelogEntryBrawler object name={self.brawler['name'].title()!r} id={self.brawler['id']}>"


    @property
    def name(self) -> str:
        """`str`: The brawler's name."""
        return self.brawler["name"].title()

    @property
    def id(self) -> int:
        """`int`: The brawler's ID."""
        return self.brawler["id"]

    @property
    def power(self) -> int:
        """`int`: The brawler's power level (1-11 exclusive)."""
        return self.brawler["power"]

    @property
    def trophies(self) -> int:
        """`int`: The brawler's trophies at the time of the entry."""
        return self.brawler["trophies"]


class EntryPlayer:
    """
    Represents a player in a Brawl Stars battle log entry.

    ### Attributes
    name: `str`
        The player's name.
    tag: `str`
        The player's unique tag.
    brawler: `~.EntryBrawler`
        A `EntryBrawler` object representing the player's brawler.
    """
    def __init__(self, player: dict) -> None:
        self.player = player

    def __repr__(self) -> str:
        return f"<BattlelogEntryPlayer name={self.player['name']!r} tag='{self.player['tag']}'>"

    def __str__(self) -> str:
        return f"{self.player['name']} ({self.player['tag']})"


    @property
    def name(self) -> str:
        """``str``: The player's name."""
        return self.player["name"]

    @property
    def tag(self) -> str:
        """``str``: The player's unique tag."""
        return self.player["tag"]

    @property
    def brawler(self) -> EntryBrawler:
        """`EntryBrawler`: A `EntryBrawler` object representing the player's brawler."""
        return EntryBrawler(self.player["brawler"])


class BattlelogEntry:
    """
    Represents a Brawl Stars battle log entry.

    ### Attributes
    name: `str`
        The battle's gamemode name.
    id: `int`
        The battle's gamemode ID.
    map: `str`
        The battle's gamemode map.
    result: ``str``
        The result of the battle (Defeat/Draw/Victory or the rank (1st, 2nd, ...) depending on the gamemode).
    time: ``str``
        A string representing the time at which the entry was recorded.
    duration: Tuple[``int``, ``int``]
        A tuple representing how long the battle lasted (e.g. (2, 21) first number are the minutes, second are the seconds).
    trophy_change: ``int``
        The amount of trophies the player won or lost from the battle
    players: Union[List[``BattlelogEntryPlayer``], List[List[``BattlelogEntryPlayer``]]]
        The players that took part in the battle.
        .. note:: A single list of ``BattlelogEntryPlayer`` objects indicates the gamemode was solo showdown. 
            If the list is nested, it's either duo showdown or a 3vs3 gamemode.
    """
    def __init__(self, data: dict) -> None:
        self.data = {}
        for key in data:
            self.data[camel_to_snake(key)] = data[key]

    def __repr__(self) -> str:
        return f"<BattlelogEntry object mode_name={self.name!r} result={self.result!r}>"


    @property
    def name(self) -> str:
        """`str`: The mode's name."""
        try:
            name = self.data["event"]["mode"] 
        except KeyError:
            name = self.data["battle"]["mode"]
        return " ".join(char.capitalize() for char in camel_to_snake(name).split("_"))

    @property
    def id(self) -> int:
        """`int`: The mode's ID."""
        return self.data["event"]["id"]

    @property
    def map(self) -> str:
        """`str`: The mode's map. If `None`, return "Community Map"."""
        m = self.data["event"]["map"]
        if m:
            return m
        return "Community Map"

    @property
    def result(self) -> str:
        """`str`: The result of the battle (Defeat/Draw/Victory in case of 3v3, the rank in case of showdown)."""
        try:
            return self.data["battle"]["result"].capitalize()
        except KeyError:
            return f"Rank {self.data['battle']['rank']}"

    @property
    def time(self) -> str:
        """`str`: The time at which the entry was recorded."""
        return datetime.datetime.strptime(self.data["battle_time"], "%Y%m%dT%H%M%S.%fZ").strftime("%d/%m/%Y - %H:%M:%S")

    @property
    def duration(self) -> Tuple[int, int]:
        """Tuple[`int`, `int`]: How long the battle lasted."""
        return divmod(self.data["battle"]["duration"], 60)

    @property
    def trophy_change(self) -> int:
        """`int`: The amount of trophies the player gained or lost from the battle."""
        try:
            return self.data["battle"]["trophy_change"]
        except KeyError: # the API returns camelCased keys; catch the issue in case it's not converted to snake_case
            return self.data["battle"]["trophyChange"]

    @property
    def star_player(self) -> EntryPlayer:
        """`~.EntryPlayer`: The star player of the battle."""
        try:
            return EntryPlayer(self.data["battle"]["star_player"])
        except KeyError: # the API returns camelCased keys; catch the issue in case it's not converted to snake_case
            return EntryPlayer(self.data["battle"]["starPlayer"])

    @property
    def players(self) -> List[EntryPlayer]:
        """List[`~.EntryPlayer`]: The players that took part in the battle."""
        try:
            players = self.data["battle"]["teams"]
        except KeyError: # only gets raised if mode is solo showdown
            players = self.data["battle"]["players"]

        if isinstance(players[0], list): # nested list meaning that the mode is anything but solo showdown
            players = [EntryPlayer(player) for player in players[0]]
            for player in players[1]:
                players.append(EntryPlayer(player))
            return players
        else:
            return [EntryPlayer(player) for player in players]
