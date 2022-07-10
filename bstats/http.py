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

import aiohttp
import asyncio
import json

from cachetools import TTLCache
from typing import Any, Callable, Mapping, Optional, Union

from .utils import format_tag
from .errors import Forbidden, NotFound, RateLimited, UnknownServerError, MaintenanceError

class APIRoute:
    """
    ## Initialise this manually only if another Base URL will be used.
    Represents an API endpoint route.

    ### Attributes
    url: `str`
        The full request URL.
    """
    BASE: str = "https://api.brawlstars.com/v1"
    def __init__(self, path: str) -> None:
        self.path = path

    @property
    def base_url(self):
        """`str`: The raw Base URL (without endpoints) for all API requests."""
        return self.BASE

    @base_url.setter
    def base_url(self, new_base: str):
        """
        Sets a new Base URL for API requests.
        
        ### Parameters
        new_base: `str`
            The new Base URL.
        """
        self.BASE = new_base

    @property
    def url(self) -> str:
        """`str`: The full request URL."""
        return self.BASE + self.path


# 300K items for 5 minutes
# this should be enough... right?

class HTTPClient:
    def __init__(self, session: aiohttp.ClientSession, *, headers: Mapping[str, str], timeout: int) -> None:
        self.__cache = TTLCache(maxsize=3000*1024, ttl=300)
        self.session: aiohttp.ClientSession = session
        self.headers: Mapping[str, str] = headers
        self.timeout: int = timeout


    async def _read_resp(self, response: aiohttp.ClientResponse) -> Union[Any, str]:
        if response.headers["Content-Type"][:16] == "application/json":
            return json.loads(await response.text())
        return await response.text()

    async def request(self, url: str, /) -> Callable[[aiohttp.ClientResponse], Optional[Union[Any, str]]]:
        """
        Perform a GET API request.

        ### Parameters
        url: `str`
            The URL to use for the request.
        """
        cache_res = self.__cache.get(url)
        if cache_res:
            return cache_res

        try:
            async with self.session.get(url, headers=self.headers, timeout=self.timeout) as response:
                data = await self._read_resp(response)
        except asyncio.TimeoutError:
            raise MaintenanceError(response, 503, "The API is down due to in-game maintenance. Please be patient and try again later.")

        # all good. data has been retrieved and API is functional
        code = response.status
        exc_mapping = {
            403: {"exc": Forbidden, "message": "The API token you supplied is invalid. Authorization failed."},
            404: {"exc": NotFound, "message": "The item requested has not been found."},
            429: {"exc": RateLimited, "message": "You are being rate-limited. Please retry in a few moments."},
            500: {"exc": UnknownServerError, "message": "An unexpected error has occurred.\n{}".format(data)},
            503: {"exc": MaintenanceError, "message": "The API is down due to in-game maintenance. Please be patient and try again later."}
        }

        if 200 <= code < 300:
            self.__cache[url] = data
            return data
        else:
            args = exc_mapping.get(code)
            if args:
                raise args["exc"](response, code, args["message"])


    async def _get_player(self, tag: str, /) -> Callable[[str], Optional[Union[Any, str]]]:
        return await self.request(APIRoute(f"/players/{format_tag(tag)}").url)

    async def _get_club(self, tag: str, /) -> Callable[[str], Optional[Union[Any, str]]]:
        return await self.request(APIRoute(f"/clubs/{format_tag(tag)}").url)

    async def _get_brawlers(self) -> Callable[[str], Optional[Union[Any, str]]]:
        return await self.request(APIRoute("/brawlers").url)

    async def _get_members(self, tag: str, /) -> Callable[[str], Optional[Union[Any, str]]]:
        return await self.request(APIRoute(f"/clubs/{format_tag(tag)}/members"))

    async def _get_battlelogs(self, tag: str, /) -> Callable[[str], Optional[Union[Any, str]]]:
        return await self.request(APIRoute(f"/players/{format_tag(tag)}/battlelog").url)

    async def _get_leaderboards(self, mode, region, limit, brawler) -> Callable[[str], Optional[Union[Any, str]]]:
        url = "/rankings/{region}/{mode}"
        if mode == "brawlers":
            url += "/{brawler}"
        if limit < 200:
            url += "?limit={limit}"

        return await self.request(APIRoute(url.format(region=region, mode=mode, brawler=brawler, limit=limit)).url)

    async def _get_event_rotation(self) -> Callable[[str], Optional[Union[Any, str]]]:
        return await self.request(APIRoute("/events/rotation").url)
