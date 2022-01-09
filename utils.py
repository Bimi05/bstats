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

import re

from urllib.parse import quote
from .errors import InvalidSuppliedTag, InappropriateFormat


def camel_to_snake(text: str) -> str:
    """
    Helper function to convert camelCase to snake_case.
        - e.g. ``bestBigBrawlerTime`` => ``best_big_brawler_time``

    Parameters
    ----------

    text: ``str``
        The text to restructure from camelCase to snake_case

    Returns
    -------
    ``str``
        The restructured snake_case text
    """
    return re.compile(r"(?<!^)(?=[A-Z])").sub("_", text).lower()


def format_tag(tag: str) -> str:
    """
    Format tag in the correct form to use API calls.
        - e.g. ``#80V2R98CQ`` => ``%2380V2R98CQ``

    This method also utilises and changes characters commonly mistaken
    for correct ones.
    - For example, ``OVRCC2O`` would return ``0VRCC20`` since O is invalid, but easily mistaken for 0
    - The same applies for ``B`` (would return ``8``) and so on


    Parameters
    ----------
    tag: ``str``
        The tag to format.

    Returns
    -------
    ``str``
        The formatted version of the provided tag.

    Raises
    ------
    `InappropriateFormat``
        The tag provided is less than 3 characters in length.
    `InvalidSuppliedTag``
        The tag contains invalid characters.
    """
    tag = tag.strip().strip("#").upper().replace("B", "8").replace("O", "0")
    if len(tag) < 3:
        raise InappropriateFormat(f"Could not format tag, tag less than 3 characters.")

    invalid = set((c for c in tag if c.upper() not in "0289PYLQGRJCUV"))
    if invalid:
        raise InvalidSuppliedTag(f"A tag with invalid characters has been passed. -> \"{', '.join(invalid)}\"")
    return quote(f"#{tag}")


def calculate_exp(exp_points: int, /) -> str:
    """
    A helper function that calcuates the experience the user is currently at
    and the experience needed for the next level.

    Parameters
    ----------

    exp_points: ``int``
        The total experience points that the user has gained.
        You can access this via the ``exp_points`` property of this class

    Returns
    -------

    ``str``
        A string following the format "current_exp/required_exp"
        - i.e. 1652/1760
    """
    required, total = 30, exp_points
    while total >= 0:
        required += 10
        total -= required

    if total < 0:
        total += required

    return f"{total}/{required}"
