# -*- coding: utf-8 -*-
"""
Anki Add-on: Progress Bar

Shows progress in the Reviewer in terms of passed cards per session.

Copyright:  (c) Unknown author (nest0r/Ja-Dark?) 2017
            (c) SebastienGllmt 2017 <https://github.com/SebastienGllmt/>
            (c) liuzikai 2018-2020 <https://github.com/liuzikai>
            (c) Glutanimate 2017-2018 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

# Do not modify the following lines
from __future__ import unicode_literals
from typing import Optional

from anki.hooks import addHook, wrap
from anki import version as anki_version

from aqt.utils import showInfo

from aqt.qt import *
from aqt import mw

__version__ = '2.0.1'

############## USER CONFIGURATION START ##############

# CARD TALLY CALCULATION

# Which queues to include in the progress calculation (all True by default)
includeNew = True
includeRev = True
includeLrn = True

# Only include new cards once reviews are exhausted.
includeNewAfterRevs = True

# Calculation weights
#
#   Setting proper weights will make the progress bar goes smoothly and reasonably.
#
#   For example, if all weight are 1, and you set 2 steps for a new card in your desk config, you will convey
#   one 'new' into two 'learning' card if you press 'again' at the first time, which will increase remaining
#   count and cause the bar to move backward.
#
#   In this case, it's probably a good idea to set newWeight to 2, and remaining count will be calculated as
#   new * 2 + learn + review. Now pressing 'again' will just make it stop going forward, but not backward. If
#   you press 'easy' at first, the progress will go twice as fast, which is still reasonable.
#
#   However, if you press 'good' followed by 'again', there will be another two learning card again, and the
#   progress still needs to go backward. It may not be a big deal, but if you want the progress never goes
#   backward strictly, enable forceForward below.
#
#   Weights should be integers. It's their relative sizes that matters, not absolute values.
#
#   Another example that make the progress goes unstably is 'bury related new cards to next day.' If you have
#   three new cards in a note, there will be 3 new cards at the beginning of your review, but another two will
#   disappear instantly after you learn one of them. However, all three cards will be regarded as 'completed,'
#   so your progress may go three times as fast.

newWeight = 2
revWeight = 1
lrnWeight = 1

# If enabled, the progress will freeze if remaining count has to increase to prevent moving backward,
#   and wait until your correct answers 'make up' this additional part.
#   NOTE: This will not stop the progress from moving backward if you add cards or toggle suspended.
forceForward = False

# PROGRESS BAR APPEARANCE

showPercent = False  # Show the progress text percentage or not.
showNumber = False  # Show the progress text as a fraction

qtxt = "aliceblue"  # Percentage color, if text visible.
qbg = "rgba(0, 0, 0, 0)"  # Background color of progress bar.
qfg = "#3399cc"  # Foreground color of progress bar.
qbr = 0  # Border radius (> 0 for rounded corners).

# optionally restricts progress bar width
maxWidth = "5px"  # (e.g. "5px". default: "")

scrollingBarWhenEditing = True  # Make the progress bar 'scrolling' when waiting to resume.

orientationHV = Qt.Horizontal  # Show bar horizontally (side to side). Use with top/bottom dockArea.
# orientationHV = Qt.Vertical # Show bar vertically (up and down). Use with right/left dockArea.

invertTF = False  # If set to True, inverts and goes from right to left or top to bottom.

dockArea = Qt.TopDockWidgetArea  # Shows bar at the top. Use with horizontal orientation.
# dockArea = Qt.BottomDockWidgetArea # Shows bar at the bottom. Use with horizontal orientation.
# dockArea = Qt.RightDockWidgetArea # Shows bar at right. Use with vertical orientation.
# dockArea = Qt.LeftDockWidgetArea # Shows bar at left. Use with vertical orientation.

pbStyle = ""  # Stylesheet used only if blank. Else uses QPalette + theme style.
'''pbStyle options (insert a quoted word above):
    -- "plastique", "windowsxp", "windows", "windowsvista", "motif", "cde", "cleanlooks"
    -- "macintosh", "gtk", or "fusion" might also work
    -- "windowsvista" unfortunately ignores custom colors, due to animation?
    -- Some styles don't reset bar appearance fully on undo. An annoyance.
    -- Themes gallery: http://doc.qt.io/qt-4.8/gallery.html'''

##############  USER CONFIGURATION END  ##############

# Set up variables

remainCount = {}  # {did: remaining count (weighted) of the deck}
doneCount = {}  # {did: done count (weighted) of the deck}, calculated as total - remain when showing next question
totalCount = {}  # {did: max total count (weighted) that was seen}, calculated as remain + done after state change
# NOTE: did stands for 'deck id'
# For old API of deckDueList(), these counts don't include cards in children decks. For new deck_due_tree(), they do.


currDID: Optional[int] = None  # current deck id (None means at the deck browser)

nmStyleApplied = 0
nmUnavailable = 0
progressBar: Optional[QProgressBar] = None

pbdStyle = QStyleFactory.create("%s" % pbStyle)  # Don't touch.

# Defining palette in case needed for custom colors with themes.
palette = QPalette()
palette.setColor(QPalette.Base, QColor(qbg))
palette.setColor(QPalette.Highlight, QColor(qfg))
palette.setColor(QPalette.Button, QColor(qbg))
palette.setColor(QPalette.WindowText, QColor(qtxt))
palette.setColor(QPalette.Window, QColor(qbg))

if maxWidth:
    if orientationHV == Qt.Horizontal:
        restrictSize = "max-height: %s;" % maxWidth
    else:
        restrictSize = "max-width: %s;" % maxWidth
else:
    restrictSize = ""

try:
    # Remove that annoying separator strip if we have Night Mode, avoiding conflicts with this add-on.
    import Night_Mode

    Night_Mode.nm_css_menu \
        += Night_Mode.nm_css_menu \
           + '''
        QMainWindow::separator
    {
        width: 0px;
        height: 0px;
    }
    '''
except ImportError:
    nmUnavailable = 1

useOldAnkiAPI = anki_version.startswith("2.0.") or (
            anki_version.startswith("2.1.") and int(anki_version.split(".")[-1]) < 28)


def initPB() -> None:
    """Initialize and set parameters for progress bar, adding it to the dock."""
    global progressBar
    progressBar = QProgressBar()
    progressBar.setTextVisible(showPercent or showNumber)
    progressBar.setInvertedAppearance(invertTF)
    progressBar.setOrientation(orientationHV)
    if pbdStyle is None:
        progressBar.setStyleSheet(
            '''
                QProgressBar
                {
                    text-align:center;
                    color:%s;
                    background-color: %s;
                    border-radius: %dpx;
                    %s
                }
                QProgressBar::chunk
                {
                    background-color: %s;
                    margin: 0px;
                    border-radius: %dpx;
                }
                ''' % (qtxt, qbg, qbr, restrictSize, qfg, qbr))
    else:
        progressBar.setStyle(pbdStyle)
        progressBar.setPalette(palette)
    _dock(progressBar)


def _dock(pb: QProgressBar) -> QDockWidget:
    """Dock for the progress bar. Giving it a blank title bar,
        making sure to set focus back to the reviewer."""
    dock = QDockWidget()
    tWidget = QWidget()
    dock.setObjectName("pbDock")
    dock.setWidget(pb)
    dock.setTitleBarWidget(tWidget)

    # Note: if there is another widget already in this dock position, we have to add ourself to the list

    # first check existing widgets
    existing_widgets = [widget for widget in mw.findChildren(QDockWidget) if mw.dockWidgetArea(widget) == dockArea]

    # then add ourselves
    mw.addDockWidget(dockArea, dock)

    # stack with any existing widgets
    if len(existing_widgets) > 0:
        mw.setDockNestingEnabled(True)

        if dockArea == Qt.TopDockWidgetArea or dockArea == Qt.BottomDockWidgetArea:
            stack_method = Qt.Vertical
        if dockArea == Qt.LeftDockWidgetArea or dockArea == Qt.RightDockWidgetArea:
            stack_method = Qt.Horizontal
        mw.splitDockWidget(existing_widgets[0], dock, stack_method)

    if qbr > 0 or pbdStyle is not None:
        # Matches background for round corners.
        # Also handles background for themes' percentage text.
        mw.setPalette(palette)
    mw.web.setFocus()
    return dock


def updatePB() -> None:
    """Update progress bar range and value with currDID, totalCount[] and doneCount[]"""
    if useOldAnkiAPI:
        # With old API, counts don't include cards in child decks
        if currDID:  # in a specific deck
            deckName = mw.col.decks.name(currDID)
            pbMax = pbValue = 0
            # Sum up all children decks
            for deckProp in mw.col.sched.deckDueList():
                name = deckProp[0]
                did = deckProp[1]
                if name.startswith(deckName):
                    pbMax += totalCount[did]
                    pbValue += doneCount[did]
        else:  # at desk browser
            pbMax = sum(totalCount.values())
            pbValue = sum(doneCount.values())
    else:
        # With new API, counts include cards in child decks
        if currDID:  # in a specific deck
            pbMax = totalCount[currDID]
            pbValue = doneCount[currDID]
        else:  # at desk browser
            pbMax = pbValue = 0
            # Sum top-level decks
            for node in mw.col.sched.deck_due_tree().children:
                pbMax += totalCount[node.deck_id]
                pbValue += doneCount[node.deck_id]

    # showInfo("pbMax = %d, pbValue = %d" % (pbMax, pbValue))

    if pbMax == 0:  # 100%
        progressBar.setRange(0, 1)
        progressBar.setValue(1)
    else:
        progressBar.setRange(0, pbMax)
        progressBar.setValue(pbValue)

    if showNumber:
        if showPercent:
            percent = 100 if pbMax == 0 else int(100 * pbValue / pbMax)
            progressBar.setFormat("%d / %d (%d%%)" % (pbValue, pbMax, percent))
        else:
            progressBar.setFormat("%d / %d" % (pbValue, pbMax))
    nmApplyStyle()


def setScrollingPB() -> None:
    """Make progress bar in waiting style if the state is resetRequired (happened after editing cards.)"""
    progressBar.setRange(0, 0)
    if showNumber:
        progressBar.setFormat("Waiting...")
    nmApplyStyle()


def nmApplyStyle() -> None:
    """Checks whether Night_Mode is disabled:
        if so, we remove the separator here."""
    global nmStyleApplied
    if not nmUnavailable:
        nmStyleApplied = Night_Mode.nm_state_on
    if not nmStyleApplied:
        mw.setStyleSheet(
            '''
        QMainWindow::separator
    {
        width: 0px;
        height: 0px;
    }
    ''')


def calcProgress(rev: int, lrn: int, new: int) -> int:
    """Calculate progress using weights and card counts from the sched."""
    ret = 0
    if includeRev:
        ret += rev * revWeight
    if includeLrn:
        ret += lrn * lrnWeight
    if includeNew or (includeNewAfterRevs and rev == 0):
        ret += new * newWeight
    return ret


def updateCountsForAllDecks(updateTotal: bool) -> None:
    """
    Update counts.

    After adding, editing or deleting cards (afterStateChange hook), updateTotal should be set to True to update
    totalCount[] based on doneCount[] and remainCount[]. No card should have been answered before this hook is
    triggered, so the change in remainCount[] should be caused by editing collection and therefore goes into
    totalCount[].

    When the user answer a card (showQuestion hook), updateTotal should be set to False to update doneCount[] based on
    totalCount[] and remainCount[]. No change to collection should have been made before this hook is
    triggered, so the change in remainCount[] should be caused by answering cards and therefore goes into
    doneCount[].

    In the later case, remainCount[] may still increase based on the weights of New, Lrn and Rev cards (see comments
    of "Calculation weights" above), in which case totalCount[] may still get updated based on forceForward setting.

    :param updateTotal: True for afterStateChange hook, False for showQuestion hook
    """

    if useOldAnkiAPI:
        for deckProp in mw.col.sched.deckDueList():
            did = deckProp[1]
            remain = calcProgress(deckProp[2], deckProp[3], deckProp[4])
            updateCountsForDeck(did, remain, updateTotal)
    else:
        for node in mw.col.sched.deck_due_tree().children:
            updateCountsForTree(node, updateTotal)


def updateCountsForTree(node, updateTotal: bool) -> None:
    did = node.deck_id
    remain = calcProgress(node.review_count, node.learn_count, node.new_count)

    updateCountsForDeck(did, remain, updateTotal)

    for child in node.children:
        updateCountsForTree(child, updateTotal)


def updateCountsForDeck(did: int, remain: int, updateTotal: bool):
    if did not in totalCount.keys():
        totalCount[did] = remainCount[did] = remain
        doneCount[did] = 0
    else:
        remainCount[did] = remain
        if updateTotal:
            totalCount[did] = doneCount[did] + remainCount[did]
        else:
            if remainCount[did] + doneCount[did] > totalCount[did]:
                # This may happen if you press 'again' followed by 'good' for a new card, as stated in comments
                # "Calculation weights,' or when you undo a card, making remaining count increases.

                if forceForward:
                    pass  # give up changing counts, until the remainCount decrease.
                else:
                    totalCount[did] = doneCount[did] + remainCount[did]
            else:
                doneCount[did] = totalCount[did] - remainCount[did]


def afterStateChangeCallBack(state: str, oldState: str) -> None:
    global currDID

    if state == "resetRequired":
        if scrollingBarWhenEditing:
            setScrollingPB()
        return
    elif state == "deckBrowser":
        # initPB() has to be here, since objects are not prepared yet when the add-on is loaded.
        if not progressBar:
            initPB()
            updateCountsForAllDecks(True)
        currDID = None
    else:  # "overview" or "review"
        # showInfo("mw.col.decks.current()['id'])= %d" % mw.col.decks.current()['id'])
        currDID = mw.col.decks.current()['id']

    # showInfo("updateCountsForAllDecks(True), currDID = %d" % (currDID if currDID else 0))
    updateCountsForAllDecks(True)  # see comments at updateCountsForAllDecks()
    updatePB()


def showQuestionCallBack() -> None:
    # showInfo("updateCountsForAllDecks(False), currDID = %d" % (currDID if currDID else 0))
    updateCountsForAllDecks(False)  # see comments at updateCountsForAllDecks()
    updatePB()


addHook("afterStateChange", afterStateChangeCallBack)
addHook("showQuestion", showQuestionCallBack)

if anki_version.startswith("2.0.x"):
    """Workaround for QSS issue in EditCurrent,
    only necessary on Anki 2.0.x"""

    from aqt.editcurrent import EditCurrent


    def changeStylesheet(*args):
        mw.setStyleSheet('''
            QMainWindow::separator
        {
            width: 0px;
            height: 0px;
        }
        ''')


    def restoreStylesheet(*args):
        mw.setStyleSheet("")


    EditCurrent.__init__ = wrap(
        EditCurrent.__init__, restoreStylesheet, "after")
    EditCurrent.onReset = wrap(
        EditCurrent.onReset, changeStylesheet, "after")
    EditCurrent.onSave = wrap(
        EditCurrent.onSave, changeStylesheet, "after")
