# -*- coding: utf-8 -*-
"""
True Retention Add-on for Anki (extended)

Based on True Retention by Strider (?)
(https://ankiweb.net/shared/info/613684242)

Copyright: (c) 2016 Strider (?)
           (c) 2017 Glutanimate (https://github.com/Glutanimate)
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

import anki
from .utils import todayStats_new

anki.stats.CollectionStats.todayStats = todayStats_new
