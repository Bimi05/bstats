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

from ..utils import camel_to_snake
from typing import List, Tuple, Union

class BattlelogEntryBrawler:
    """
    Represents a Brawl Stars battle log entry brawler.
    
    Attributes
    ----------

    name: ``str``
        The brawler's name.
    id: ``int``
        The brawler's unique ID.
    power: ``int``
        The brawler's power level.
    trophies: ``int``
        The brawler's trophies at the time of the recorded entry.
    """
    def __init__(self, brawler: dict) -> None:
        self.brawler = brawler

    def __repr__(self) -> str:
        return f"<BattlelogEntryBrawler object name='{self.brawler['name'].title()}' id={self.brawler['id']}>"


    @property
    def name(self) -> str:
        """``str``: The brawler's name."""
        return self.brawler["name"].title()

    @property
    def id(self) -> int:
        """``int``: The brawler's unique ID."""
        return self.brawler["id"]

    @property
    def power(self) -> int:
        """``int``: The brawler's power level."""
        return self.brawler["power"]

    @property
    def trophies(self) -> int:
        """``int``: The brawler's trophies at the time of the recorded entry."""
        return self.brawler["trophies"]

class BattlelogEntryPlayer:
    """
    Represents a Brawl Stars battle log entry player.

    Attributes
    ----------

    name: ``str``
        The player's name.
    tag: ``str``
        The player's unique tag.
    brawler: ``BattlelogEntryBrawler``
        The player's brawler, represented by a ``BattlelogEntryBrawler`` object.
    """
    def __init__(self, player: dict) -> None:
        self.player = player

    def __repr__(self) -> str:
        return f"<BattlelogEntryPlayer name='{self.player['name']}' tag='{self.player['tag']}'>"

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
    def brawler(self) -> BattlelogEntryBrawler:
        """``BattlelogEntryBrawler``: The player's brawler, represented by a ``BattlelogEntryBrawler`` object."""
        return BattlelogEntryBrawler(self.player["brawler"])


class BattlelogEntry:
    """
    Represents a Brawl Stars battle log entry.

    Attributes
    ----------

    mode_name: ``str``
        The battle's gamemode name.
    mode_id: ``int``
        The battle's gamemode ID.
    mode_map: ``str``
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
        return f"<BattlelogEntry object mode_name='{self.mode_name}' result='{self.result}'>"


    @property
    def mode_name(self) -> str:
        """``str``: The battle's gamemode name."""
        name = self.data["event"]["mode"] or self.data["battle"]["mode"]
        return " ".join(char.capitalize() for char in camel_to_snake(name).split("_"))

    @property
    def mode_id(self) -> int:
        """``int``: The battle's gamemode ID."""
        return self.data["event"]["id"]

    @property
    def mode_map(self) -> str:
        """``str``: The battle's gamemode map."""
        return self.data["event"]["map"]

    @property
    def result(self) -> str:
        """``str``: The result of the battle (Defeat/Draw/Victory or the rank (1st, 2nd, ...) depending on the gamemode)."""
        try:
            return self.data["battle"]["result"].capitalize()
        except KeyError:
            return f"Rank {self.data['battle']['rank']}"

    @property
    def time(self) -> str:
        """``str``: A string representing the time at which the entry was recorded."""
        return datetime.datetime.strptime(self.data["battle_time"], "%Y%m%dT%H%M%S.%fZ").strftime("%d/%m/%Y - %H:%M:%S")

    @property
    def duration(self) -> Tuple[int, int]:
        """Tuple[``int``, ``int``]: A tuple representing how long the battle lasted (e.g. (2, 21) first number represents the minutes, second the seconds)."""
        return divmod(self.data["battle"]["duration"], 60)

    @property
    def trophy_change(self) -> int:
        """``int``: The amount of trophies the player won or lost from the battle"""
        try:
            return self.data["battle"]["trophy_change"]
        except KeyError: # the API returns camelCased keys; catch the issue in case it's not converted to snake_case
            return self.data["battle"]["trophyChange"]

    @property
    def star_player(self) -> BattlelogEntryPlayer:
        try:
            return BattlelogEntryPlayer(self.data["battle"]["star_player"])
        except KeyError: # the API returns camelCased keys; catch the issue in case it's not converted to snake_case
            return BattlelogEntryPlayer(self.data["battle"]["starPlayer"])

    @property
    def players(self) -> Union[List[BattlelogEntryPlayer], List[List[BattlelogEntryPlayer]]]:
        """Union[List[``BattlelogEntryPlayer``], List[List[``BattlelogEntryPlayer``]]]: The players that took part in the battle.
        - A single list of ``BattlelogEntryPlayer`` objects indicates the gamemode was solo showdown. 
            If the list is nested, it's either duo showdown or a 3vs3 gamemode.
        """
        try:
            players = self.data["battle"]["teams"]
        except KeyError: # only gets raised if mode is solo showdown
            players = self.data["battle"]["players"]

        if isinstance(players[0], list): # nested list meaning that the mode is anything but solo showdown
            return [[BattlelogEntryPlayer(player) for player in players[0]], [BattlelogEntryPlayer(player) for player in players[1]]]
        else:
            return [BattlelogEntryPlayer(player) for player in players]
