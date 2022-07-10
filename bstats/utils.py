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

import re

from urllib.parse import quote
from .errors import InvalidSuppliedTag


def camel_to_snake(text: str) -> str:
    """
    A helper function to convert `camelCase` to `snake_case`.
    - e.g. `bestBigBrawlerTime` -> `best_big_brawler_time`

    ### Parameters
    text: `str`
        The text to restructure from `camelCase` to `snake_case`.

    ### Returns
    `str`
        The restructured `snake_case` text.
    """
    return re.compile(r"(?<!^)(?=[A-Z])").sub("_", text).lower()


def format_tag(tag: str) -> str:
    """
    A helper function to format the tag in the correct format for API calls.
    - e.g. `#80v2r98cq` -> `%2380V2R98CQ`

    ### Parameters
    tag: `str`
        The tag to format.

    ### Returns
    `str`
        The formatted version of the provided tag.

    ### Raises
    `~.InvalidSuppliedTag`
        - The tag provided is less than 3 characters in length.
        - The tag provided contains invalid characters.
    """
    tag = tag.strip("# ").upper()
    if len(tag) < 3:
        raise InvalidSuppliedTag("Could not format tag, tag less than 3 characters.")

    invalid = tuple(dict.fromkeys([c for c in tag if c not in set("0289PYLQGRJCUV")]))
    if invalid:
        raise InvalidSuppliedTag("A tag with invalid characters has been supplied.\nInvalid character(s): {}".format(", ".join(invalid)))
    return quote(f"#{tag}")


def calculate_exp(exp_points: int, /) -> str:
    """
    A helper function that calcuates the experience the user is currently at
    and the experience needed for the next level.

    ### Parameters
    exp_points: `int`
        The total experience points that the user has gained.

    ### Returns
    `str`
        A string following the format: "current_exp/required_exp"
        - i.e. 1652/1760

    ### Raises
    `TypeError`
        `exp_points` is not an integer and is not convertible to an integer.
    """
    try: 
        exp_points = int(exp_points)
    except ValueError:
        raise TypeError(f"'exp_points' must be int or convertible to int; got {exp_points.__class__.__name__!r} instead.")

    required, total = 30, exp_points
    while total >= 0:
        required += 10
        total -= required

    if total < 0:
        total += required
    return f"{total}/{required}"
