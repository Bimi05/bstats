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

import asyncio
import aiohttp
import sys

from cachetools import TTLCache
from typing import List, Dict, Union, NoReturn, Literal, overload

from ..utils import format_tag
from ..http import APIRoute, AsyncHTTPClient
from ..errors import InappropriateFormat

from ..models.profile import Profile
from ..models.club import Club
from ..models.brawler import Brawler
from ..models.member import ClubMember
from ..models.battlelog import BattlelogEntry
from ..models.leaderboard import LeaderboardClubEntry, LeaderboardPlayerEntry
from ..models.rotation import Rotation

class AsyncClient:
    """
    Async Client to access the Brawl Stars API.

    Parameters
    ----------

    token: ``str``
        The API token to make requests with
        Get your own token from https://developer.brawlstars.com/ by making an account

    timeout: ``int``, optional
        How long to wait before terminating requests.
        By default, wait ``45`` seconds.

    loop: ``asyncio.AbstractEventLoop``, optional
        The event loop to use for all client operations.
        By default, the loop returned from ``asyncio.get_event_loop()`` is used.

    connector: ``aiohttp.TCPConnector``, optional
        Use a connector for the session. Must be an instance of ``aiohttp.TCPConnector``.
        By default ``None``.

    session: ``aiohttp.ClientSession``, optional
        Force the library to use a current or a new session.
        By default creates a fresh ``aiohttp.ClientSession()``.
    """
    def __init__(self, token, *, timeout=45, **options) -> None:
        try:
            timeout = int(timeout)
        except ValueError:
            raise TypeError(f"'timeout' must be convertible to int; {timeout.__class__.__name__!r} cannot be converted")
        else:
            self.timeout: int = timeout

        self.token: str = token
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"BStats/1.0.0 (Python {sys.version_info[0]}.{sys.version_info[1]})"
        }
        self.cache: TTLCache = TTLCache(3200*5, 60*5)

        # we'll need a loop and a connector for aiohttp so let's get those
        self.loop: asyncio.AbstractEventLoop = options.get("loop", asyncio.get_event_loop())
        self.connector: aiohttp.TCPConnector = options.get("connector")
        self.session: aiohttp.ClientSession = options.get("session") or aiohttp.ClientSession(connector=self.connector, loop=self.loop)

        # since all settings are ready
        # initialise async HTTP client for requests
        self.http_client: AsyncHTTPClient = AsyncHTTPClient(self.timeout, self.session, self.headers, self.cache)
        self.loop.create_task(self.__ainit__()) # create a background task to update the brawler dict asynchronously

    async def __ainit__(self):
        self.BRAWLERS = {brawler.name: brawler.id for brawler in await self.get_brawlers()}

    def __repr__(self):
        return f"<AsyncClient timeout={self.timeout} do_debug={self.do_debug} prevent_ratelimit={self.prevent_ratelimit}>"

    def __enter__(self) -> NoReturn:
        raise TypeError(f"{self.__class__.__name__!r} supports only async context management ('async with ...').")

    def __exit__(self, exc_type, exc, tb) -> None:
        # NOTE: __exit__() is paired with __enter__();
        # this is async, however, and __enter__() raises TypeError 
        # so this will never be actually executed
        pass

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.session.close()

    async def get_player(self, tag: str, *, use_cache: Literal[True, False] = True) -> Profile:
        """
        Get a player's profile and their stats

        Parameters
        ----------

        tag: ``str``
            The player to search for by the tag, must only contain valid characters.
            Valid characters: ``0289PYLQGRJCUV``

        use_cache: ``bool``, optional
            Whether to use the internal 5-minute cache for requests
            that may have already been made.
            By default, ``True``.

        Returns
        -------

        ``Profile``
            The ``Profile`` object associated with the profile
        """
        data = await self.http_client.request(APIRoute(f"/players/{format_tag(tag)}").url, use_cache=use_cache)
        return Profile(self, data)

    async def get_club(self, tag: str, *, use_cache: Literal[True, False] = True) -> Club:
        """
        Get a club's stats
        
        Parameters
        ----------

        tag: ``str``
            The club to search for by the tag, must only contain valid characters.
            Valid characters: ``0289PYLQGRJCUV``

        use_cache: ``bool``, optional
            Whether to use the internal 5-minute cache for requests
            that may have already been made.
            By default, ``True``.

        Returns
        -------

        ``Club``
            The ``Club`` object associated with the found club (if any)
        """
        data = await self.http_client.request(APIRoute(f"/clubs/{format_tag(tag)}").url, use_cache=use_cache)
        return Club(self, data)

    async def get_brawlers(self, *, use_cache: Literal[True, False] = True) -> List[Brawler]:
        """
        Get all the available brawlers and information about them.
        - These are NOT the brawlers a player has!
        
        Parameters
        ----------

        use_cache: ``bool``, optional
            Whether to use the internal 5-minute cache for requests
            that may have already been made.
            By default, ``True``.

        Returns
        -------

        List[``Brawler``]
            A list consisting of ``Brawler`` objects, representing the available in-game brawlers.
        """
        data = await self.http_client.request(APIRoute("/brawlers").url, use_cache=use_cache)
        return [Brawler(brawler) for brawler in data["items"]]

    async def get_members(self, tag: str, *, use_cache: Literal[True, False] = True) -> List[ClubMember]:
        """
        Get a club's members
        - Note: Each member does not have the attributes of the ``Player`` object,
        but some minimal ones that are viewable in the club tab in-game.
        
        Parameters
        ----------

        tag: ``str``
            The club to search for by the tag, must only contain valid characters.
            Valid characters: ``0289PYLQGRJCUV``

        use_cache: ``bool``, optional
            Whether to use the internal 5-minute cache for requests
            that may have already been made.
            By default, ``True``.

        Returns
        -------

        List[``ClubMember``]
            A list consisting of ``ClubMember`` objects, representing the club's members.
        """
        data = await self.http_client.request(APIRoute(f"/clubs/{format_tag(tag)}/members").url, use_cache=use_cache)
        return [ClubMember(member) for member in data["items"]]

    async def get_battlelogs(self, tag: str, *, use_cache: Literal[True, False] = True) -> List[BattlelogEntry]:
        """
        Get a player's battlelogs

        Parameters
        ----------

        tag: ``str``
            The player to search for by the tag, must only contain valid characters.
            Valid characters: ``0289PYLQGRJCUV``

        use_cache: ``bool``, optional
            Whether to use the internal 5-minute cache for requests
            that may have already been made.
            By default, ``True``.

        Returns
        -------

        List[``BattlelogEntry``]
            A list consisting of ``BattlelogEntry`` objects, representing the player's battlelogs
        """
        data = await self.http_client.request(APIRoute(f"/players/{format_tag(tag)}/battlelog").url, use_cache=use_cache)
        return [BattlelogEntry(battle) for battle in data["items"]]

    @overload
    async def get_leaderboards(
        self, 
        mode="players", 
        *, 
        country: str, 
        limit: int, 
        brawler: Union[int, str], 
        use_cache: Literal[True, False]
    ) -> List[LeaderboardPlayerEntry]:
        ...

    @overload
    async def get_leaderboards(
        self, 
        mode="clubs", 
        *, 
        country: str, 
        limit: int, 
        brawler: Union[int, str], 
        use_cache: Literal[True, False]
    ) -> List[LeaderboardClubEntry]:
        ...

    @overload
    async def get_leaderboards(
        self, 
        mode="brawlers", 
        *, 
        country: str, 
        limit: int, 
        brawler: Union[int, str], 
        use_cache: Literal[True, False]
    ) -> List[LeaderboardPlayerEntry]:
        ...


    async def get_leaderboards(
        self, 
        mode: Literal["players", "clubs", "brawlers"], 
        *, 
        country: str = "global", 
        limit: int = 200, 
        brawler: Union[int, str] = None, 
        use_cache: Literal[True, False] = True
    ) -> Union[List[LeaderboardPlayerEntry], List[LeaderboardClubEntry]]:
        """
        Get in-game leaderboard rankings for players, clubs or brawlers.

        Parameters
        ----------

        mode: ``str``
            The mode to get the rankings for.
            Must be "players", "clubs", or "brawlers".
        country: ``str``, optional
            The two-letter country code to use in order to search for local leaderboards.
            By default, ``global`` (this means that the global leaderboards will be returned).
        limit: ``int``, optional
            The amount of top players/clubs/players with a brawler to get the rankings with.
            Must be from 1-200, inclusive. By default, ``200``
        brawler: Union[``int``, ``str``], optional
            The brawler's name or ID to use. This only takes effect when the mode is set to "brawlers".
            By default, ``None``.
        use_cache: ``bool``, optional
            Whether to use the internal 5-minute cache for requests
            that may have already been made.
            By default, ``True``.

        Returns
        -------

        List[``bstats.LeaderboardEntry``]
            A list consisting of ``LeaderboardEntry`` objects, representing the leaderboard for the selected mode.

        Raises
        ------

        ``InappropriateFormat``
            - The mode provided isn't "players", "clubs" or "brawlers".
            - The brawler supplied is not an integer or a string.
            - The brawler supplied isn't valid.
            - The mode is set to "brawlers" but no brawler was supplied.
            - The given limit is not between 1 and 200.
        """
        mode = mode.lower()
        if mode not in {"players", "clubs", "brawlers"}:
            raise InappropriateFormat(f"'mode' cannot be of choice {mode!r}. The acceptable choices are players/clubs/brawlers")

        if not 0 < limit <= 200:
            raise InappropriateFormat(f"{limit} is not a valid limit choice. You must choose between 1-200.")

        if brawler:
            if isinstance(brawler, str):
                try:
                    brawler = self.BRAWLERS[brawler.title()]
                except KeyError:
                    raise InappropriateFormat(f"{brawler.title()!r} is not a valid brawler.")
            elif isinstance(brawler, int):
                if brawler not in self.BRAWLERS.values():
                    raise InappropriateFormat(f"Brawler with ID {brawler!r} is not a valid brawler.")
            else:
                raise InappropriateFormat(f"'brawler' must be int or str, not {brawler.__class__.__name__!r}")
        else:
            if mode == "brawlers":
                raise InappropriateFormat("You must supply a brawler name or ID if you want to get the 'brawlers' leaderboard rankings.")

        url = APIRoute(f"/rankings/{country}/{mode}?limit={limit}")
        if mode == "brawlers":
            url.modify_path(f"/rankings/{country}/{mode}/{brawler}?limit={limit}")

        data = await self.http_client.request(url.url, use_cache=use_cache)
        mapping = {
            "players": LeaderboardPlayerEntry,
            "clubs": LeaderboardClubEntry,
            "brawlers": LeaderboardPlayerEntry
        }

        for name, entry_type in mapping.items():
            if mode == name:
                return [entry_type(entry) for entry in data["items"]]

    async def get_event_rotation(self, use_cache: Literal[True, False] = True) -> List[Rotation]:
        """
        Get the current in-game ongoing event rotation.

        Parameters
        ----------

        use_cache: ``bool``, optional
            Whether to use the internal 5-minute cache for requests
            that may have already been made.
            By default, ``True``.

        Returns
        -------

        List[``Rotation``]
            A list consisting of ``Rotation`` objects, representing the current event rotation
        """
        data = await self.http_client.request(APIRoute("/events/rotation").url, use_cache=use_cache)
        return [Rotation(rotation) for rotation in data]
