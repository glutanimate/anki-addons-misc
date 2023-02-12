# -*- coding: utf-8 -*-
#
# Entry point for the add-on into Anki
# Please do not edit this if you do not know what you are doing.
#
# Copyright: (c) 2017 Glutanimate <https://glutanimate.com/>
# License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>

from anki import version

if int(version.split(sep='.')[2]) <= 26:
    from . import stats_true_retention_extended_old
else:
    from . import stats_true_retention_extended
