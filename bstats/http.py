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

import json
import logging
import aiohttp
import asyncio

from cachetools import TTLCache
from typing import Any, Callable, Mapping, Optional, Union

from .utils import camel_to_snake
from .errors import Forbidden, NotFound, RateLimited, APIServerError, APIMaintenanceError

_log = logging.getLogger(__name__)

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


class HTTPClient:
    def __init__(self, timeout: int, headers: Mapping[str, str], cache: TTLCache) -> None:
        self.timeout = timeout
        self.headers = headers
        self.cache = cache

    async def _return_data(self, response: aiohttp.ClientResponse) -> Union[Any, str]:
        if response.headers["Content-Type"][:16] == "application/json":
            return json.loads(await response.text())
        return await response.text()

    async def request(
        self, 
        url: str, 
        *, 
        use_cache: bool = True
    ) -> Callable[[aiohttp.ClientResponse], Optional[Union[Any, str]]]:
        """
        Perform a GET API request.

        ### Parameters
        url: `str`
            The URL to use for the request.
        use_cache (optional, defaults to `True`): `bool`
            Whether to use the internal 5-minute cache.
        """
        cache_res = self.cache.get(url)
        if use_cache and cache_res:
            return cache_res

        try:
            async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as session:
                async with session.get(url, headers=self.headers, timeout=self.timeout, ssl=False) as response:
                    data = await self._return_data(response)
        except asyncio.TimeoutError:
            raise APIMaintenanceError(response, 503, "The API is down due to in-game maintenance. Please be patient and try again later.")

        # all good. data has been retrieved and API is functional
        code = response.status
        if 200 <= code < 300:
            if use_cache:
                self.cache[url] = data
            return data

        exc_mapping = {
            403: {"exc": Forbidden, "message": "The API token you supplied is invalid. Authorization failed."},
            404: {"exc": NotFound, "message": "The item requested has not been found."},
            429: {"exc": RateLimited, "message": "You are being rate-limited. Please retry in a few moments."},
            500: {"exc": APIServerError, "message": "An unexpected error has occurred.\n{}".format(data)},
            503: {"exc": APIMaintenanceError, "message": "The API is down due to in-game maintenance. Please be patient and try again later."}
        }

        if code in exc_mapping:
            for exc_code, items in exc_mapping.items():
                if exc_code == code:
                    _log.error(f"{url} has returned {exc_code}: {' '.join(camel_to_snake(data['reason']).split('_')).title()}")
                    raise items["exc"](response, exc_code, items["message"])

