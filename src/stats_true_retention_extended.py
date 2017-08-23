# -*- coding: utf-8 -*-

"""
True Retention Add-on for Anki (extended)

Based on True Retention by Strider (?)
(https://ankiweb.net/shared/info/613684242)

Copyright: (c) 2016 Strider (?)
           (c) 2017 Glutanimate (https://github.com/Glutanimate)
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

MATURE_IVL = 21 # mature card interval in days

##############  USER CONFIGURATION END  ##############

import anki.stats

from anki.utils import fmtTimeSpan
from anki.lang import _, ngettext
from anki import version as anki_version


# Types: 0 - new today; 1 - review; 2 - relearn; 3 - (cram?) [before the answer was pressed]
# "Learning" corresponds to New|Relearn. "Review" corresponds to Young|Mature.
# Ease: 1 - flunk button; 2 - second; 3 - third; 4 - fourth (easy) [which button was pressed]
# Intervals: -60 <1m -600 10m etc; otherwise days
def _line_now(self, i, a, b, bold=True):
    colon = _(":")
    if bold:
        i.append(("<tr><td align=right>%s%s</td><td><b>%s</b></td></tr>") % (a,colon,b))
    else:
        i.append(("<tr><td align=right>%s%s</td><td>%s</td></tr>") % (a,colon,b))

def _lineTbl_now(self, i):
    return "<table>" + "".join(i) + "</table>"

def statList(self, lim, span):
    yflunked, ypassed, mflunked, mpassed, learned, relearned = self.col.db.first("""
    select
    sum(case when lastIvl < %(i)d and ease = 1 and type == 1 then 1 else 0 end), /* flunked young */
    sum(case when lastIvl < %(i)d and ease > 1 and type == 1 then 1 else 0 end), /* passed young */
    sum(case when lastIvl >= %(i)d and ease = 1 and type == 1 then 1 else 0 end), /* flunked mature */
    sum(case when lastIvl >= %(i)d and ease > 1 and type == 1 then 1 else 0 end), /* passed mature */
    sum(case when ivl > 0 and type == 0 then 1 else 0 end), /* learned */
    sum(case when ivl > 0 and type == 2 then 1 else 0 end) /* relearned */
    from revlog where id > ? """ % dict(i=MATURE_IVL) +lim, span)
    yflunked, mflunked = yflunked or 0, mflunked or 0
    ypassed, mpassed = ypassed or 0, mpassed or 0
    learned, relearned = learned or 0, relearned or 0

    # True retention
    # young
    try:
        yret = "%0.1f%%" %(ypassed/float(ypassed+yflunked)*100)
    except ZeroDivisionError:
        yret = "N/A"
    # mature
    try:
        mret = "%0.1f%%" %(mpassed/float(mpassed+mflunked)*100)
    except ZeroDivisionError:
        mret = "N/A"
    # total
    try:
        tret = "%0.1f%%" %((ypassed+mpassed)/float(ypassed+mpassed+yflunked+mflunked)*100)
    except ZeroDivisionError:
        tret = "N/A"
    
    i = []
    i.append(u"""<style>tr.trsct>td{text-align: center; font-style: italic;
            padding-top:1em;padding-bottom:0.5em}</style>""")
    i.append(u"<tr class='trsct'><td colspan='2'>Young cards</center></td></tr>")
    _line_now(self, i, u"True retention", yret)
    _line_now(self, i, u"Passed reviews", ypassed)
    _line_now(self, i, u"Flunked reviews", yflunked)
    i.append(u"<tr class='trsct'><td colspan='2'>Mature cards (ivl≥%d)</td></tr>" % MATURE_IVL)
    _line_now(self, i, u"True retention", mret)
    _line_now(self, i, u"Passed reviews", mpassed)
    _line_now(self, i, u"Flunked reviews", mflunked)
    i.append(u"<tr class='trsct'><td colspan='2'>Total</center></td></tr>")
    _line_now(self, i, u"True retention", tret)
    _line_now(self, i, u"Passed reviews", ypassed+mpassed)
    _line_now(self, i, u"Flunked reviews", yflunked+mflunked)
    _line_now(self, i, u"New cards learned", learned)
    _line_now(self, i, u"Cards relearned", relearned)
    return _lineTbl_now(self, i)

def todayStats_new(self):
    lim = self._revlogLimit()
    if lim:
        lim = u" and " + lim
    
    pastDay = statList(self, lim, (self.col.sched.dayCutoff-86400)*1000)
    pastWeek = statList(self, lim, (self.col.sched.dayCutoff-86400*7)*1000)
    
    if self.type == 0:
        period = 31; name = u"<strong>Past month</strong>"
    elif self.type == 1:
        period = 365; name = u"<strong>Past year</strong>"
    elif self.type == 2:
        period = float('inf'); name = u"<strong>All time</strong>"
    
    pastPeriod = statList(self, lim, (self.col.sched.dayCutoff-86400*period)*1000)
    
    return todayStats_old(self) + u"<br><br><table style='text-align: center'><tr><td style='padding: 5px'>" \
        + u"<span><strong>Past day</strong></span>" + pastDay + u"</td><td style='padding: 5px'>" \
        + u"<span><strong>Past week</strong></span>" + pastWeek + u"</td><td style='padding: 5px'>" \
        + u"<span>" + name + u"</span>" + pastPeriod + u"</td></tr></table>"

def todayStats_old(self):
    """We need to overwrite the entire method to change the mature ivl"""
    b = self._title(_("Today"))
    # studied today
    lim = self._revlogLimit()
    if lim:
        lim = " and " + lim
    cards, thetime, failed, lrn, rev, relrn, filt = self.col.db.first("""
select count(), sum(time)/1000,
sum(case when ease = 1 then 1 else 0 end), /* failed */
sum(case when type = 0 then 1 else 0 end), /* learning */
sum(case when type = 1 then 1 else 0 end), /* review */
sum(case when type = 2 then 1 else 0 end), /* relearn */
sum(case when type = 3 then 1 else 0 end) /* filter */
from revlog where id > ? """+lim, (self.col.sched.dayCutoff-86400)*1000)
    cards = cards or 0
    thetime = thetime or 0
    failed = failed or 0
    lrn = lrn or 0
    rev = rev or 0
    relrn = relrn or 0
    filt = filt or 0
    # studied
    if anki_version.startswith("2.0."):
        def bold(s):
            return "<b>"+unicode(s)+"</b>"
    else:
        def bold(s):
            return "<b>"+str(s)+"</b>"
    msgp1 = ngettext("<!--studied-->%d card", "<!--studied-->%d cards", cards) % cards
    b += _("Studied %(a)s in %(b)s today.") % dict(
        a=bold(msgp1), b=bold(fmtTimeSpan(thetime, unit=1)))
    # again/pass count
    b += "<br>" + _("Again count: %s") % bold(failed)
    if cards:
        b += " " + _("(%s correct)") % bold(
            "%0.1f%%" %((1-failed/float(cards))*100))
    # type breakdown
    b += "<br>"
    b += (_("Learn: %(a)s, Review: %(b)s, Relearn: %(c)s, Filtered: %(d)s")
          % dict(a=bold(lrn), b=bold(rev), c=bold(relrn), d=bold(filt)))
    # mature today
    mcnt, msum = self.col.db.first("""
select count(), sum(case when ease = 1 then 0 else 1 end) from revlog
where lastIvl >= %d and id > ?""" % MATURE_IVL +lim, (self.col.sched.dayCutoff-86400)*1000)
    b += "<br>"
    if mcnt:
        b += _("Correct answers on mature cards: %(a)d/%(b)d (%(c).1f%%)") % dict(
            a=msum, b=mcnt, c=(msum / float(mcnt) * 100))
    else:
        b += _("No mature cards were studied today.")
    return b

anki.stats.CollectionStats.todayStats = todayStats_new
