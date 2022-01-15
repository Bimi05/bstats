"""
Brawl Stars API wrapper
~~~~~~~~~~~~~~~~~~~~~~~

A fundamental wrapper for the Brawl Stars API
covering all endpoints and including many features!

Copyright (c) 2022-present Bimi05
"""

__title__ = "bstats"
__author__ = "Bimi05"
__license__ = "MIT"
__version__ = "1.1.0"

from .clients import SyncClient, AsyncClient
from .client import APIClient  # 1.1.x
from .models import *
from .errors import *

