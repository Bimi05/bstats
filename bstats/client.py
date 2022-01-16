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

import sys
import asyncio
import aiohttp
import requests

from cachetools import TTLCache
from typing import Dict, List, Literal, Optional, Type, Union
from .utils import format_tag
from .http import APIRoute, HTTPClient
from .errors import InappropriateFormat

from .models.profile import Profile
from .models.club import Club
from .models.brawler import Brawler
from .models.member import ClubMember
from .models.battlelog import BattlelogEntry
from .models.leaderboard import LeaderboardEntry
from .models.rotation import Rotation

class APIClient:
    """
    Sync/Async Client to access the Brawl Stars API.

    Parameters
    ----------

    token: ``str``
        The API token to make requests with.
        Get your own token from https://developer.brawlstars.com/
        - You have to make an account before you can create an API token!

    asynchronous: ``bool``, optional
        Whether the client should be asynchronous (use ``async``/``await`` syntax).
        By default, ``False``.

    timeout: ``int``, optional
        How long to wait before terminating requests.
        By default, wait ``45`` seconds.
    """
    def __init__(self, token: str, *, asynchronous: bool = False, timeout: int = 45) -> None:
        try:
            timeout = int(timeout)
        except ValueError:
            raise TypeError(f"'timeout' must be convertible to int; {timeout.__class__.__name__!r} cannot be converted")
        else:
            self.timeout = timeout

        self.use_async = asynchronous
        self.token = token

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "BStats/1.1.0 (Python {0[0]}.{0[1]}, Aiohttp {1})".format(sys.version_info, aiohttp.__version__)
        }

        self.session = requests.Session()
        if self.use_async:
            self.session = aiohttp.ClientSession(loop=asyncio.get_event_loop())

        self.cache = TTLCache(3200*5, 60*5)
        self.http_client = HTTPClient(self.timeout, self.headers, self.cache)
        self.BRAWLERS = {brawler.name: brawler.id for brawler in self.get_brawlers()}

    def __repr__(self):
        return f"<{self.__class__.__name__} asynchronous={self.use_async} timeout={self.timeout}>"

    def __enter__(self):
        if not self.use_async:
            return self
        raise TypeError(f"Use 'async with {self.__class__.__name__} as ...:' instead")

    def __exit__(self, exc_type, exc, tb):
        self.session.close()

    async def __aenter__(self):
        if self.use_async:
            return self
        raise TypeError(f"Use 'with {self.__class__.__name__} as ...:' instead")

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    def get_player(self, tag: str, /, *, use_cache: bool = True) -> Profile:
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
        url = APIRoute(f"/players/{format_tag(tag)}").url
        loop = asyncio.get_event_loop()

        data = loop.run_until_complete(self.http_client.request(url, use_cache=use_cache))
        return Profile(self, data)

    def get_club(self, tag: str, /, *, use_cache: bool = True) -> Club:
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
        url = APIRoute(f"/clubs/{format_tag(tag)}").url
        loop = asyncio.get_event_loop()

        data = loop.run_until_complete(self.http_client.request(url, use_cache=use_cache))
        return Club(data)

    def get_brawlers(self, *, use_cache: bool = True) -> List[Brawler]:
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
        url = APIRoute("/brawlers").url
        loop = asyncio.get_event_loop()

        data = loop.run_until_complete(self.http_client.request(url, use_cache=use_cache))
        return [Brawler(brawler) for brawler in data["items"]]

    def get_members(self, tag: str, /, *, use_cache: bool = True) -> List[ClubMember]:
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
        url = APIRoute(f"/clubs/{format_tag(tag)}/members").url
        loop = asyncio.get_event_loop()

        data = loop.run_until_complete(self.http_client.request(url, use_cache=use_cache))
        return [ClubMember(member) for member in data["items"]]

    def get_battlelogs(self, tag: str, /, *, use_cache: bool = True) -> List[BattlelogEntry]:
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
        url = APIRoute(f"/players/{format_tag(tag)}/battlelog").url
        loop = asyncio.get_event_loop()

        data = loop.run_until_complete(self.http_client.request(url, use_cache=use_cache))
        return [BattlelogEntry(battle) for battle in data["items"]]

    def get_leaderboards(self, mode: Literal["players", "clubs", "brawlers"], /, **options) -> List[LeaderboardEntry]:
        """
        Get in-game leaderboard rankings for players, clubs or brawlers.

        Parameters
        ----------

        mode: ``str``
            The mode to get the rankings for.
            Must be "players", "clubs", or "brawlers".
        region: ``str``, optional
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

        List[``LeaderboardEntry``]
            A list consisting of ``LeaderboardEntry`` objects, representing the leaderboard rankings for the selected mode.
            - NOTE: ``LeaderboardEntry`` is a subclass of both ``LeaderboardPlayerEntry`` and ``LeaderboardClubEntry``.
                If mode is players or brawlers, refer to the attributes of ``LeaderboardPlayerEntry``.
                Otherwise, refer to the attributes of ``LeaderboardClubEntry``.

        Raises
        ------

        ``InappropriateFormat``
            - The mode provided isn't "players", "clubs" or "brawlers".
            - The brawler supplied is not an integer or a string.
            - The brawler supplied isn't valid.
            - The mode is set to "brawlers" but no brawler was supplied.
            - The given limit is not between 1 and 200.
        """
        # get and format all possible attributes
        mode: str = mode.lower()
        region: str = options.get("region", "global").lower()
        limit: int = options.get("limit", 200)
        brawler: Union[str, int] = options.get("brawler")
        use_cache: bool = options.get("use_cache", True)

        # check if every aspect is OK so we can proper request
        if mode not in {"players", "clubs", "brawlers"}:
            raise InappropriateFormat(f"'mode' cannot be of choice {mode!r}. The acceptable choices are players/clubs/brawlers")
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
                        brawler = self.BRAWLERS[brawler.title()]
                    except KeyError:
                        raise InappropriateFormat(f"{brawler.title()!r} is not a valid brawler.")
                else:
                    if brawler not in self.BRAWLERS.values():
                        raise InappropriateFormat(f"Brawler with ID {brawler!r} is not a valid brawler.")
            else:
                raise InappropriateFormat(f"'brawler' must be int or str, not {brawler.__class__.__name__!r}")
        else:
            if mode == "brawlers":
                raise InappropriateFormat("You must supply a brawler name or ID if you want to get the 'brawlers' leaderboard rankings.")

        url = APIRoute(f"/rankings/{region}/{mode}?limit={limit}")
        if mode == "brawlers":
            url.modify_path(f"/rankings/{region}/{mode}/{brawler}?limit={limit}")
        loop = asyncio.get_event_loop()

        data = loop.run_until_complete(self.http_client.request(url.url, use_cache=use_cache))
        return [LeaderboardEntry(entry) for entry in data["items"]]

    def get_event_rotation(self, *, use_cache: bool = True) -> List[Rotation]:
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
        url = APIRoute("/events/rotation").url
        loop = asyncio.get_event_loop()

        data = loop.run_until_complete(self.http_client.request(url, use_cache=use_cache))
        return [Rotation(rotation) for rotation in data]

