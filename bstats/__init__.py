"""
## Brawl Stars API wrapper

A basic Brawl Stars API wrapper,
covering all endpoints with many features!

Copyright (c) 2022-present Bimi05
"""

__title__ = "bstats"
__author__ = "Bimi05"
__license__ = "MIT"
__version__ = "1.1.0a"

import logging
from typing import NamedTuple

from .client import Client
from .errors import *

from . import utils
from .profile import *
from .club import *
from .brawler import *
from .member import *
from .leaderboard import *
from .battlelog import *
from .rotation import *


class VerInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    level: str
    serial: int

major, minor, micro = (int(num) for num in __version__[:-1].split("."))
version_info = VerInfo(major, minor, micro, level="alpha", serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())
