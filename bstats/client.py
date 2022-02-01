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

import os
import re
import sys
import logging
import asyncio
import aiohttp
import requests

from cachetools import TTLCache
from typing import List, Literal, TypeVar, Union, overload

from .utils import format_tag
from .http import APIRoute, HTTPClient
from .errors import InappropriateFormat, NoSuppliedToken

from .profile import Profile
from .club import Club
from .brawler import Brawler
from .member import ClubMember
from .battlelog import BattlelogEntry
from .leaderboard import LeaderboardEntry
from .rotation import Rotation

T = TypeVar("T")
_log = logging.getLogger(__name__)

class Client:
    """
    ## You have to make an account before you can create an API token!
    Sync/Async Client to access the Brawl Stars API.
    
    ### Parameters
    token: `str`
        The API token from the [API website](https://developer.brawlstars.com/) to make requests with.
        If the token is invalid, then you will receive an exception (`~.errors.Forbidden`).
    asynchronous (optional, defaults to `False`): `bool`
        Whether the client should be asynchronous.
    timeout (optional, defaults to `45`): `int`
        How long to wait before terminating requests.
    """
    def __init__(self, token: str, *, asynchronous: bool = False, timeout: int = 45) -> None:
        with open(os.path.join(os.path.dirname(__file__), "__init__.py")) as file:
            self.VERSION = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", file.read(), re.MULTILINE).group(1)

        try:
            timeout = int(timeout)
        except ValueError:
            raise TypeError(f"'timeout' must be convertible to int; {timeout.__class__.__name__!r} cannot be converted.")
        else:
            self.timeout = timeout

        self.use_async = asynchronous

        if not token:
            raise NoSuppliedToken("You have to supply a token to access the API.")

        self.token = token
        self.headers = {
            "Authorization": "Bearer {}".format(self.token),
            "User-Agent": "BStats/{0} (Python {1[0]}.{1[1]}, Aiohttp {2})"\
                .format(self.VERSION, sys.version_info, aiohttp.__version__)
        }

        self.session = aiohttp.ClientSession(loop=self._make_loop()) if self.use_async else requests.Session()
        self.cache = TTLCache(3200 * 5, 60 * 5)
        self.http_client = HTTPClient(self.timeout, self.headers, self.cache)

    async def __ainit__(self) -> None:
        self.BRAWLERS = {brawler.name: brawler.id for brawler in await self.get_brawlers()}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} asynchronous={self.use_async} timeout={self.timeout}>"

    def __enter__(self):
        if not self.use_async:
            return self
        raise TypeError(f"Use 'async with {self.__class__.__name__} as ...:' instead")

    def __exit__(self, exc_type, exc, tb):
        # if the client is async, this never gets called because __enter__ raises an exception
        if self.session:
            self.session.close()

    async def __aenter__(self):
        if self.use_async:
            return self
        raise TypeError(f"Use 'with {self.__class__.__name__} as ...:' instead")

    async def __aexit__(self, exc_type, exc, tb):
        if not self.session.closed:
            await self.session.close()

    def _make_loop(self):
        if sys.version_info >= (3, 10):
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()
        return loop


    def _get_data(
        self, 
        route: APIRoute, 
        model: T, 
        *, 
        use_cache: bool = True
    ) -> Union[T, List[T]]:
        """
        Request the necessary data with the given URL
        and return the model supplied containing the data.
        Depending on what model is requested, there is:
        - either the model itself is returned.
        - or a list full of the model is returned.
        """
        data = self._make_loop().run_until_complete(self.http_client.request(route.url, use_cache=use_cache))

        try:
            return [model(item) for item in data["items"]]
        except KeyError:
            # this gets raised if the items key is not present.
            # if it's a list (battlelog entries, club members, ...)
            # then it is a dict with the keys "items" and "paging".
            # Otherwise, it's just the plain dict response with the data
            # which in any case, is what we need
            try:
                return model(data)
            except TypeError:
                return model(self, data) # Profile takes two arguments

    async def _aget_data(
        self, 
        route: APIRoute, 
        model: T, 
        *, 
        use_cache: bool = True
    ) -> Union[T, List[T]]:
        """
        Request the necessary data with the given URL
        and return the model supplied containing the data.
        Depending on what model is requested, there is:
        - either the model itself is returned.
        - or a list full of the model is returned.
        """
        data = await self.http_client.request(route.url, use_cache=use_cache)
        try:
            return [model(item) for item in data["items"]]
        except KeyError:
            # this gets raised if the items key is not present.
            # if it's a list (battlelog entries, club members, ...)
            # then it is a dict with the keys "items" and "paging".
            # Otherwise, it's just the plain dict response with the data
            # which in any case, is what we need
            try:
                return model(data)
            except TypeError:
                return model(self, data) # Profile takes two arguments


    @overload
    def get_player(self, tag: str, *, use_cache: Literal[True]) -> Profile:
        ...

    @overload
    def get_player(self, tag: str, *, use_cache: Literal[False]) -> Profile:
        ...

    def get_player(self, tag: str, *, use_cache: bool = True) -> Profile:
        """
        Get a player's profile and their statistics.

        ### Parameters
        tag: `str`
            The player's tag to use for the request.
            If a character other than `0289PYLQGRJCUV` is in the tag,
            then `~.InvalidSuppliedTag` is raised.
        use_cache (optional, defaults to `True`): `bool`
            Whether to use the internal 5-minute cache.

        ### Returns
        `~.Profile`
            A `Profile` object representing the player's profile.
        """
        if self.use_async:
            return self._aget_data(APIRoute(f"/players/{format_tag(tag)}"), Profile, use_cache=use_cache)
        return self._get_data(APIRoute(f"/players/{format_tag(tag)}"), Profile, use_cache=use_cache)


    @overload
    def get_club(self, tag: str, *, use_cache: Literal[True]) -> Club:
        ...

    @overload
    def get_club(self, tag: str, *, use_cache: Literal[False]) -> Club:
        ...

    def get_club(self, tag: str, *, use_cache: bool = True) -> Club:
        """
        Get a club and its statistics.
        
        ### Parameters
        tag: `str`
            The club's tag to use for the request.
            If a character other than `0289PYLQGRJCUV` is in the tag,
            then `~.errors.InvalidSuppliedTag` is raised.
        use_cache (optional, defaults to `True`): `bool`
            Whether to use the internal 5-minute cache.

        ### Returns
        `~.Club`
            A `Club` object representing the club.
        """
        return self._get_data(APIRoute(f"/clubs/{format_tag(tag)}").url, Club, use_cache=use_cache)


    @overload
    def get_brawlers(self, *, use_cache: Literal[True]) -> List[Brawler]:
        ...

    @overload
    def get_brawlers(self, *, use_cache: Literal[False]) -> List[Brawler]:
        ...

    def get_brawlers(self, *, use_cache: bool = True) -> List[Brawler]:
        """
        Get all the available brawlers and their details.
        - These are not the brawlers a player has!

        ### Parameters
        use_cache (optional, defaults to `True`): `bool`
            Whether to use the internal 5-minute cache.

        ### Returns
        List[`~.Brawler`]
            A list of `Brawler` objects representing the available in-game brawlers.
        """
        return self._get_data(APIRoute("/brawlers").url, Brawler, use_cache=use_cache)


    @overload
    def get_members(self, tag: str, *, use_cache: Literal[True]) -> List[ClubMember]:
        ...

    @overload
    def get_members(self, tag: str, *, use_cache: Literal[False]) -> List[ClubMember]:
        ...

    def get_members(self, tag: str, *, use_cache: bool = True) -> List[ClubMember]:
        """
        Get a club's members
        - Note: Each member has some minimal attributes,
        specifically what is viewable in the club tab in-game.
        To get a `Player` object of that member, use `~.get_player()`
        with the member's tag.

        ### Parameters
        tag: `str`
            The club's tag to use for the request.
            If a character other than `0289PYLQGRJCUV` is in the tag,
            then `~.InvalidSuppliedTag` is raised.
        use_cache (optional, defaults to `True`): `bool`
            Whether to use the internal 5-minute cache.

        ### Returns
        List[`~.ClubMember`]
            A list of `ClubMember` objects representing the club's members.
        """
        return self._get_data(APIRoute(f"/clubs/{format_tag(tag)}/members").url, ClubMember, use_cache=use_cache)


    @overload
    def get_battlelogs(self, tag: str, *, use_cache: Literal[True]) -> List[BattlelogEntry]:
        ...

    @overload
    def get_battlelogs(self, tag: str, *, use_cache: Literal[False]) -> List[BattlelogEntry]:
        ...

    def get_battlelogs(self, tag: str, *, use_cache: bool = True) -> List[BattlelogEntry]:
        """
        Get a player's battlelogs

        ### Parameters
        tag: `str`
            The player's tag to use for the request.
            If a character other than `0289PYLQGRJCUV` is in the tag,
            then `~.errors.InvalidSuppliedTag` is raised.
        use_cache (optional, defaults to `True`): `bool`
            Whether to use the internal 5-minute cache.

        ### Returns
        List[`~.BattlelogEntry`]
            A list of `BattlelogEntry` objects representing the player's battlelog entries
        """
        return self._get_data(APIRoute(f"/players/{format_tag(tag)}/battlelog").url, BattlelogEntry, use_cache=use_cache)


    @overload
    def get_leaderboards(self, mode="players", **options) -> List[LeaderboardEntry]:
        ...

    @overload
    def get_leaderboards(self, mode="clubs", **options) -> List[LeaderboardEntry]:
        ...

    @overload
    def get_leaderboards(self, mode="brawlers", **options) -> List[LeaderboardEntry]:
        ...

    def get_leaderboards(self, mode: Literal["players", "clubs", "brawlers"], **options) -> List[LeaderboardEntry]:
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
        use_cache (optional, defaults to `True`): `bool`
            Whether to use the internal 5-minute cache.

        ### Returns
        List[`~.LeaderboardEntry`]
            A list of `LeaderboardEntry` objects representing the leaderboard rankings.

        ### Raises
        `~.InappropriateFormat`
        - The mode provided isn't "players", "clubs" or "brawlers".
        - The brawler supplied is not an integer or a string.
        - The brawler supplied isn't valid.
        - The mode is set to "brawlers" but no brawler was supplied.
        - The given limit is not an integer or convertible to an integer.
        - The given limit is not between 1 and 200.
        """

        # get and format all possible attributes
        mode = mode.lower()
        region = options.get("region", "global").lower()
        limit = options.get("limit", 200)
        try:
            limit = int(limit)
        except ValueError:
            raise InappropriateFormat(f"'limit' must be convertible to int; {limit.__class__.__name__!r} cannot be converted.")
        brawler = options.get("brawler")
        use_cache = bool(options.get("use_cache", True))

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

        url = "/rankings/{}/{}"
        if mode == "brawlers":
            url += "/{}"
        if limit < 200:
            url += "?limit={}"

        return self._get_data(APIRoute(url.format(region, mode, brawler, limit)).url, LeaderboardEntry, use_cache=use_cache)


    @overload
    def get_event_rotation(self, *, use_cache: Literal[True]) -> List[Rotation]:
        ...

    @overload
    def get_event_rotation(self, *, use_cache: Literal[False]) -> List[Rotation]:
        ...

    def get_event_rotation(self, *, use_cache: bool = True) -> List[Rotation]:
        """
        Get the current in-game event rotation.

        ### Parameters
        use_cache: `bool`, optional
            Whether to use the internal 5-minute cache. By default, ``True``.

        ### Returns
        List[`~.Rotation`]
            A list of `Rotation` objects representing the current event rotation.
        """
        return self._get_data(APIRoute("/events/rotation").url, Rotation, use_cache=use_cache)

