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
import aiohttp
import re
import os
import sys

from .http import HTTPClient
from .errors import InappropriateFormat, NoSuppliedToken

from .profile import Profile
from .club import Club
from .brawler import Brawler
from .member import Member
from .battlelog import BattlelogEntry
from .leaderboard import LeaderboardPlayerEntry, LeaderboardClubEntry
from .rotation import EventSlot

from typing import (
    List,
    TypeVar,
    Union,
    overload
)

C = TypeVar("C", bound="Client")
class Client:
    """
    ## You have to make an account before you can create an API token!
    Asynchronous Client to access the Brawl Stars API.
    
    ### Parameters
    token: `str`
        The API token from the [API website](https://developer.brawlstars.com/) to make requests with.
        If the token is invalid, then you will receive an exception (`errors.Forbidden`).
    timeout (optional, defaults to `45`): `int`
        How long to wait before terminating requests.
    """
    def __init__(self: C, token: str, *, timeout: int = 45) -> None:
        with open(os.path.join(os.path.dirname(__file__), "__init__.py")) as file:
            self.VERSION = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", file.read(), re.MULTILINE).group(1)

        if not token:
            raise NoSuppliedToken("You must supply a token to access the API.")

        self.token = token
        try:
            timeout = int(timeout)
        except ValueError:
            raise TypeError(f"timeout type {timeout.__class__.__name__!r} cannot be converted to int.")
        else:
            self.timeout = timeout

        self.headers = {
            "Authorization": "Bearer {}".format(self.token),
            "User-Agent": "BStats/{v} (Python {pv[0]}.{pv[1]}, Aiohttp {av})"\
                .format(v=self.VERSION, pv=sys.version_info, av=aiohttp.__version__)
        }

        self.session = aiohttp.ClientSession(loop=self._make_loop())
        self.http = HTTPClient(self.session, headers=self.headers, timeout=self.timeout)

    async def __ainit__(self: C) -> None:
        self.BRAWLERS = {brawler.name: brawler.id for brawler in await self.get_brawlers()}

    def __repr__(self: C) -> str:
        return f"<{self.__class__.__name__} timeout={self.timeout}>"

    def _make_loop(self: C) -> asyncio.AbstractEventLoop:
        if sys.version_info >= (3, 10):
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()
        return loop


    async def get_player(self: C, tag: str, /) -> Profile:
        """
        Get a player's profile and their statistics.

        ### Parameters
        tag: `str`
            The player's tag to use for the request.
            If a character other than `0289PYLQGRJCUV` is in the tag,
            then `errors.InvalidSuppliedTag` is raised.

        ### Returns
        `~.Profile`
            A `Profile` object representing the player's profile.
        """
        data = await self.http._get_player(tag)
        return Profile(data)


    async def get_club(self: C, tag: str, /) -> Club:
        """
        Get a club and its statistics.
        
        ### Parameters
        tag: `str`
            The club's tag to use for the request.
            If a character other than `0289PYLQGRJCUV` is in the tag,
            then `errors.InvalidSuppliedTag` is raised.

        ### Returns
        `~.Club`
            A `Club` object representing the club.
        """
        data = await self.http._get_club(tag)
        return Club(data)


    async def get_brawlers(self: C) -> List[Brawler]:
        """
        Get all the available brawlers and their details.
        - These are not the brawlers a player has!

        ### Returns
        List[`Brawler`]
            A list of `Brawler` objects representing the available in-game brawlers.
        """

        data = await self.http._get_brawlers()
        return [Brawler(brawler) for brawler in data["items"]]


    async def get_members(self: C, tag: str, /) -> List[Member]:
        """
        Get a club's members
        - Note: Each member has some minimal attributes,
        specifically what is viewable in the club tab in-game.
        To get a `Player` object of that member, use `.get_player()`
        with the member's tag.

        ### Parameters
        tag: `str`
            The club's tag to use for the request.
            If a character other than `0289PYLQGRJCUV` is in the tag,
            then `errors.InvalidSuppliedTag` is raised.

        ### Returns
        List[`Member`]
            A list of `Member` objects representing the club's members.
        """
        data = await self.http._get_members(tag)
        return [Member(member) for member in data["items"]]


    async def get_battlelogs(self: C, tag: str, /) -> List[BattlelogEntry]:
        """
        Get a player's battlelogs

        ### Parameters
        tag: `str`
            The player's tag to use for the request.
            If a character other than `0289PYLQGRJCUV` is in the tag,
            then `errors.InvalidSuppliedTag` is raised.

        ### Returns
        List[`BattlelogEntry`]
            A list of `BattlelogEntry` objects representing the player's battlelog entries
        """
        data = await self.http._get_battlelogs(tag)
        return [BattlelogEntry(entry) for entry in data["items"]]


    @overload
    async def get_leaderboards(self: C, mode: str = "players", **options) -> List[LeaderboardPlayerEntry]:
        ...

    @overload
    async def get_leaderboards(self: C, mode: str = "clubs", **options) -> List[LeaderboardClubEntry]:
        ...

    @overload
    async def get_leaderboards(self: C, mode: str = "brawlers", **options) -> List[LeaderboardPlayerEntry]:
        ...

    async def get_leaderboards(self: C, mode: str, **options) -> Union[List[LeaderboardPlayerEntry], List[LeaderboardClubEntry]]:
        """
        Get in-game leaderboard rankings for players, clubs or brawlers.

        ### Parameters
        mode: `str`
            The mode to get the rankings for. Must be one of: "players", "clubs", or "brawlers".
        region (optional, defaults to `global`): `str`
            The two-letter country code to use in order to search for local leaderboards.
        limit (optional, defaults to `200`): `int`
            The amount of top players/clubs/players with a brawler to get the rankings with.
            Must be from 1-200, inclusive.
        brawler (optional, defaults to `None`): Union[`int`, `str`]
            The brawler's name or ID to use. This only takes effect when the mode is set to "brawlers".

        ### Returns
        List[`LeaderboardPlayerEntry`] | List[`LeaderboardClubEntry`]
            A list of `LeaderboardPlayerEntry` or `LeaderboardClubEntry` objects.
            - `LeaderboardPlayerEntry` objects are returned when the leaderboard mode is set to "players" or "brawlers".
            - `LeaderboardClubEntry` objects are return when the leaderboard mode is set to "clubs".

        ### Raises
        `InappropriateFormat`
        - The mode provided isn't "players", "clubs" or "brawlers".
        - The brawler supplied is not an integer or a string.
        - The brawler supplied isn't valid.
        - The mode is set to "brawlers" but no brawler was supplied.
        - The given limit is not an integer and is not convertible to an integer.
        - The given limit is not between 1 and 200.
        """

        mode = mode.lower()
        region = options.pop("region", "global").lower()
        limit = options.pop("limit", 200)
        try:
            limit = int(limit)
        except ValueError:
            raise InappropriateFormat(f"'limit' must be int or convertible to int,  {limit.__class__.__name__!r}.")
        brawler = options.pop("brawler", None)
        if brawler:
            brawler = brawler.title()

        # check if every aspect is OK so we can proper request
        if not 0 < limit <= 200:
            raise InappropriateFormat(f"{limit} is not a valid limit choice. You must choose between 1-200.")
        if region != "global" and len(region) > 2:
            raise InappropriateFormat(f"{region!r} is not a valid region. Regions must be passed in as their two-letter representative.")
        if brawler:
            if isinstance(brawler, (str, int)):
                try:
                    brawler = int(brawler)
                except ValueError:
                    try:
                        brawler = self.BRAWLERS[brawler]
                    except KeyError:
                        raise InappropriateFormat(f"{brawler!r} is not a valid brawler.")
                else:
                    if brawler not in self.BRAWLERS.values():
                        raise InappropriateFormat(f"Brawler with ID {brawler!r} is not a valid brawler.")
            else:
                raise InappropriateFormat(f"'brawler' must be int or str, not {brawler.__class__.__name__!r}")
        else:
            if mode == "brawlers":
                raise InappropriateFormat("You must supply a brawler name or ID if you want to get the 'brawlers' leaderboard rankings.")

        m = {
            "players": LeaderboardPlayerEntry,
            "clubs": LeaderboardClubEntry,
            "brawlers": LeaderboardPlayerEntry
        }

        try:
            return_type = m[mode]
        except KeyError:
            raise InappropriateFormat(f"'mode' must either be 'players', 'clubs' or 'brawlers', not {mode!r}.")
        else:
            data = await self.http._get_leaderboards(mode, region, limit, brawler)
            return [return_type(entry) for entry in data["items"]]


    async def get_event_rotation(self) -> List[EventSlot]:
        """
        Get the current in-game event rotation.

        ### Returns
        List[`Rotation`]
            A list of `Rotation` objects representing the current event rotation.
        """
        data = await self.http._get_event_rotation()
        return [EventSlot(event) for event in data]
