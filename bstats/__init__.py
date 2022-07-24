"""
## Brawl Stars API wrapper

A basic Brawl Stars API wrapper,
covering all endpoints with many features!

Copyright (c) 2022-present Bimi
"""

__title__ = "bstats"
__author__ = "Bimi"
__license__ = "MIT"
__version__ = "1.1.1"

from typing import NamedTuple

from . import utils
from .client import Client
from .errors import *
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

try:
    major, minor, micro = (int(num) for num in __version__.split("."))
    rlevel = "final"
except ValueError: # alpha/beta releases cover
    major, minor, micro = (int(num) for num in __version__[:-1].split("."))
    levels = {"a": "alpha", "b": "beta", "rc": "candidate release"}
    rlevel = levels[__version__[-1]]

version_info = VerInfo(major, minor, micro, level=rlevel, serial=0)
