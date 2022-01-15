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

class BSException(Exception):
    """
    Base class for all exceptions raised by the wrapper.
    This class ideally catches all the errors that the library may throw
    """
    pass

class HTTPException(BSException):
    """
    Base class for all HTTP-related errors.
    This includes (but is not limited to) status codes such as:
    - ``403``: Invalid Authorization
    - ``404``: Item not Found
    - ``429``: User is Rate Limited
    - ``500``: Unexpected Error occurrence
    - ``503``: API is down
    """
    def __init__(self, response, code, message):
        super().__init__(f"{response.reason} (Status Code {code}): {message}")

class ProcessingError(BSException):
    """
    Base class for all processing errors.
    Any request that could lead to a 400 will be caught
    and have a subclass (of this error class) raised
    """
    def __init__(self, message):
        super().__init__(f"An error occurred while processing the supplied data: {message}")


class InvalidSuppliedTag(ProcessingError):
    """The supplied tag is invalid (less than 3 characters, contains invalid characters, ...)"""
    pass


class InappropriateFormat(ProcessingError):
    """The given data are not appropriate for an API call."""
    pass


class Forbidden(HTTPException):
    """The supplied API token is invalid"""
    pass

class ItemNotFound(HTTPException):
    """The requested item has not been found"""
    pass

class RateLimitReached(HTTPException):
    """The API rate-limit has been reached"""
    pass

class UnexpectedError(HTTPException):
    """An unknown error has occurred during the processing of the request"""
    pass

class InternalServerError(HTTPException):
    """The API is temporarily unavailable due to in-game maintenance"""
    pass
