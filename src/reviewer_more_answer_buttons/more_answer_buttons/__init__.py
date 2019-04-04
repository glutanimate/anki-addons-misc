# -*- coding: utf-8 -*-
#
# Entry point for the add-on into Anki
# Please do not edit this if you do not know what you are doing.
#
# Copyright: (c) 2017-2019 Glutanimate <https://glutanimate.com/>
#            (c) 2019 ijgnd
# License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>

from anki import version

anki20 = version.startswith("2.0")

if anki20:
    from . import reviewer_more_answer_buttons_for_20  # noqa: F401
else:
    from . import reviewer_more_answer_buttons_for_21  # noqa: F401
