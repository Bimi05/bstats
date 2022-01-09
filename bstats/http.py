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
from typing import Any, Dict, Literal, Optional, Union
from .errors import Forbidden, ItemNotFound, RateLimitReached, InternalAPIError, InternalServerError

class APIRoute:
    BASE: str = f"https://api.brawlstars.com/v1"

    def __init__(self, path: str) -> None:
        self.url: str = self.BASE + path

    def modify_path(self, new_path: str) -> None:
        self.url: str = self.BASE + new_path

class HTTPClient:
    def __init__(self, timeout, session, headers, cache) -> None:
        self.timeout: int = timeout
        self.session: requests.Session = session
        self.headers: Dict[str, str] = headers
        self.cache: TTLCache = cache

    def get_from_cache(self, url: APIRoute) -> Optional[Any]:
        return self.cache.get(url)

    def request(self, url: APIRoute, *, use_cache: Literal[True, False] = True) -> Optional[Union[Any, str]]:
        if use_cache and self.get_from_cache(url) is not None:
            return self.get_from_cache(url)

        try:
            with self.session.get(url, headers=self.headers, timeout=self.timeout) as resp:
                try:
                    data = json.loads(resp.text)
                except json.JSONDecodeError:
                    data = resp.text

                code = resp.status_code
                if code == 403:
                    raise Forbidden(resp, 403, "The API token you supplied is invalid. Authorization failed.")
                if code == 404:
                    raise ItemNotFound(resp, 404, "The item requested has not been found.")
                if code == 429:
                    raise RateLimitReached(resp, 429, "You are being rate-limited. Please retry in a few moments.")
                if code == 500:
                    raise InternalAPIError(resp, 500, "An unexpected error has occurred.\n{}".format(data))
                if code == 503:
                    raise InternalServerError(resp, 503, "The API is down due to in-game maintenance. Please be patient and try again later.")
        except requests.Timeout:
            raise InternalServerError(resp, 503, "The API is down due to in-game maintenance. Please be patient and try again later.")
        else:
            if 200 <= code < 300:
                self.cache[url] = data
                return data

class AsyncHTTPClient:
    def __init__(self, timeout, session, headers, cache) -> None:
        self.timeout: int = timeout
        self.session: aiohttp.ClientSession = session
        self.headers: Dict[str, str] = headers
        self.cache: TTLCache = cache

    def get_from_cache(self, url: APIRoute) -> Optional[Any]:
        return self.cache.get(url)

    async def request(self, url: APIRoute, *, use_cache: Literal[True, False] = True) -> Optional[Union[Any, str]]:
        if use_cache and self.get_from_cache(url) is not None:
            return self.get_from_cache(url)

        try:
            async with self.session.get(url, headers=self.headers, timeout=self.timeout) as resp:
                try:
                    data = json.loads(await resp.text())
                except json.JSONDecodeError:
                    data = await resp.text()

                code = resp.status
                if code == 403:
                    raise Forbidden(resp, 403, "The API token you supplied is invalid. Authorization failed.")
                if code == 404:
                    raise ItemNotFound(resp, 404, "The item requested has not been found.")
                if code == 429:
                    raise RateLimitReached(resp, 429, "You are being rate-limited. Please retry in a few moments.")
                if code == 500:
                    raise InternalAPIError(resp, 500, "An unexpected error has occurred.\n{}".format(data))
                if code == 503:
                    raise InternalServerError(resp, 503, "The API is down due to in-game maintenance. Please be patient and try again later.")
        except asyncio.TimeoutError:
            raise InternalServerError(resp, 503, "The API is down due to in-game maintenance. Please be patient and try again later.")
        else:
            if 200 <= code < 300:
                self.cache[url] = data
                return data
