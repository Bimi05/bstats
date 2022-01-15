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

import requests
import aiohttp
import asyncio
import json

from cachetools import TTLCache
from typing import Any, Callable, Dict, Literal, Optional, Union
from .errors import Forbidden, ItemNotFound, RateLimitReached, UnexpectedError, InternalServerError

class APIRoute:
    BASE: str = f"https://api.brawlstars.com/v1"

    def __init__(self, path: str) -> None:
        self.url: str = self.BASE + path

    def modify_path(self, new_path: str) -> None:
        self.url: str = self.BASE + new_path

class HTTPClient:
    def __init__(self, timeout, headers, cache) -> None:
        self.timeout: int = timeout
        self.headers: Dict[str, str] = headers
        self.cache: TTLCache = cache

    async def _return_data(self, response: aiohttp.ClientResponse):
        if response.headers["Content-Type"][:16] == "application/json":
            return json.loads(await response.text())
        return await response.text()

    async def request(self, url: str, /, *, use_cache: bool = True) -> Optional[Any]:
        cache_res = self.cache.get(url)
        if use_cache and cache_res:
            return cache_res

        try:
            async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as session:
                async with session.get(url, headers=self.headers, timeout=self.timeout, ssl=False) as response:
                    data = await self._return_data(response)
        except (requests.Timeout, asyncio.TimeoutError):
            raise InternalServerError(response, 503, "The API is down due to in-game maintenance. Please be patient and try again later.")

        # all good. data has been retrieved and API is functional
        code = response.status
        if 200 <= code < 300:
            if use_cache:
                self.cache[url] = data
            return data

        if code == 403:
            raise Forbidden(response, 403, "The API token you supplied is invalid. Authorization failed.")
        if code == 404:
            raise ItemNotFound(response, 404, "The item requested has not been found.")
        if code == 429:
            raise RateLimitReached(response, 429, "You are being rate-limited. Please retry in a few moments.")
        if code == 500:
            raise UnexpectedError(response, 500, "An unexpected error has occurred.\n{}".format(data))
        if code == 503:
            raise InternalServerError(response, 503, "The API is down due to in-game maintenance. Please be patient and try again later.")
