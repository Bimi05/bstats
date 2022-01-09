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

from typing import Union


class BSException(Exception):
    """
    Base class for all exceptions raised by the wrapper.
    This class ideally catches all the errors that the library may throw
    """
    pass

class HTTPException(BSException):
    """
    Base class for all HTTP-related errors.
    This includes status codes such as:
    - ``403``: Invalid Authorization
    - ``404``: Item not Found
    - ``429``: Rate Limited
    - ``500``: Internal Server Error
    - ``503``: API is down
    """
    from requests import Response
    from aiohttp import ClientResponse

    def __init__(self, response: Union[Response, ClientResponse], code: int, message: str):
        super().__init__(f"{response.reason} (Status Code {code}): {message}")

class ProcessingException(BSException):
    """
    Base class for all processing errors
    - i.e. formatting a tag or receiving a bad request (status code: 400)
    """
    def __init__(self, message):
        super().__init__(f"An error occurred while processing the data: {message}")


class InvalidSuppliedTag(ProcessingException):
    """The supplied tag is invalid (less than 3 characters, contains invalid characters)."""
    pass


class InappropriateFormat(ProcessingException):
    """The received format is not proper for an API request."""
    pass


class Forbidden(HTTPException):
    """The supplied API token is invalid and/or the authorization has failed."""
    pass

class ItemNotFound(HTTPException):
    """The requested item (e.g. player, club) has not been found"""
    pass

class RateLimitReached(HTTPException):
    """The API rate-limit has been reached"""
    pass

class InternalAPIError(HTTPException):
    """An error has occurred during the processing of a request"""
    pass

class InternalServerError(HTTPException):
    """The API is temporarily unavailable due to in-game maintenance"""
    pass
