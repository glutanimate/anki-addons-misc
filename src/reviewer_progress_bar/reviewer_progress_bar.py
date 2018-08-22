# -*- coding: utf-8 -*-
"""
Anki Add-on: Progress Bar

Shows progress in the Reviewer in terms of passed cards per session.

Copyright:  (c) Unknown author (nest0r/Ja-Dark?) 2017
            (c) SebastienGllmt 2017 <https://github.com/SebastienGllmt/>
            (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

# Do not modify the following lines
from __future__ import unicode_literals

from anki.hooks import addHook, wrap
from anki import version as anki_version

from aqt.utils import showInfo

from aqt.qt import *
from aqt import mw

__version__ = '2.0.0'

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
#   Setting proper weights will make the progress bar goes smoothly and decrease the chance of going backwards.
#
#   For example, if all weight are 1, and you set 2 steps for a new card in your desk config, you will convey
#   one 'new' into two 'learning' card if you press 'again' at the first time, which will increase remaining
#   count and cause the bar to move backward.
#
#   In this case, it's not a bad idea to set newWeight to 2, and remaining count will be calculated as
#   new * 2 + learn + review.Now pressing 'again' will just make it stop going forward, but not backward. If
#   you press 'esay' at first, the progress will go twice as fast, which is still reasonable.
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
#
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
qbg = "#ececec"  # Background color of progress bar.
qfg = "#3399cc"  # Foreground color of progress bar.
qbr = 0  # Border radius (> 0 for rounded corners).

# optionally restricts progress bar width
maxWidth = "5px"  # (e.g. "5px". default: "")

floatingBarWhenEditing = True # Make the progress bar 'floating' when waiting to resume.

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

## Set up variables

remainCount = {}  # {did: remaining count (weighted) of the deck}, calculated with data from Anki col and sched
doneCount = {}  # {did: done count (weighted) of the deck}, calculated as total - remain when showing next question
totalCount = {}  # {did: max total count (weighted) that was seen}, calculated as remain + done after state change
# NOTE: did stands for 'deck id'
# See comments on updateCounts() for further usage.


currDID = None  # current deck id (None means at the deck browser)

nmStyleApplied = 0
nmUnavailable = 0
progressBar = None

pbdStyle = QStyleFactory.create("%s" % (pbStyle))  # Don't touch.

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


def initPB():
    """Initialize and set parameters for progress bar, adding it to the dock."""
    global progressBar
    progressBar = QProgressBar()
    progressBar.setTextVisible(showPercent or showNumber)
    progressBar.setInvertedAppearance(invertTF)
    progressBar.setOrientation(orientationHV)
    if pbdStyle == None:
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


def _dock(pb):
    """Dock for the progress bar. Giving it a blank title bar,
        making sure to set focus back to the reviewer."""
    dock = QDockWidget()
    tWidget = QWidget()
    dock.setObjectName("pbDock")
    dock.setWidget(pb)
    dock.setTitleBarWidget(tWidget)

    ## Note: if there is another widget already in this dock position, we have to add ourself to the list

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

    if qbr > 0 or pbdStyle != None:
        # Matches background for round corners.
        # Also handles background for themes' percentage text.
        mw.setPalette(palette)
    mw.web.setFocus()
    return dock


def updatePB():
    """Update progress bar range and value with currDID, totalCount[] and doneCount[]"""
    if currDID:
        # In a specific deck
        deckName = mw.col.decks.name(currDID)
        pbMax = pbValue = 0
        # Sum up all children decks
        for deckProp in mw.col.sched.deckDueList():
            name = deckProp[0]
            did = deckProp[1]
            if name.startswith(deckName):
                pbMax += totalCount[did]
                pbValue += doneCount[did]
    else:
        # At desk browser
        pbMax = sum(totalCount.values())
        pbValue = sum(doneCount.values())
    # showInfo("pbMax = %d, pbValue = %d" % (pbMax, pbValue))

    if pbMax == 0:
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


def setFloatingPB():
    """Make progress bar in waiting style if the state is resetRequired (happened after editing cards.)"""
    progressBar.setRange(0, 0)
    if showNumber:
        progressBar.setFormat("Waiting...")
    nmApplyStyle()


def nmApplyStyle():
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


def calcCount(revRaw, lrnRaw, newRaw):
    """Calculate count with weights with raw values from the sched."""
    rev = lrn = new = 0
    if includeRev:
        rev = revRaw * revWeight
    if includeLrn:
        lrn = lrnRaw * lrnWeight
    if includeNew or (includeNewAfterRevs and rev == 0):
        new = newRaw * newWeight
    return rev + lrn + new


def initCounts():
    """Iterate decks and initialize totalCount[], remainCount[] and doneCount[]."""
    for deckProp in mw.col.sched.deckDueList():
        _initCounts(deckProp[1], calcCount(deckProp[2], deckProp[3], deckProp[4]))


def _initCounts(did, remain):
    totalCount[did] = remainCount[did] = remain
    doneCount[did] = 0


# When state change (happens after adding, editing or deleting cards), forceUpdateTotal = True,
#   totalCount = doneCount + remainCount. User doesn't answer questions during this process, so doneCount should not
#   change. Changes in remainCount are caused by user's adding, editing or deleting, so totalCount should be
#   re-evaluated based on doneCount + remainCount.
# When 'showQuestion' is triggered, forceUpdateTotal = False, doneCount = totalCount - remainCount. The changes in
#    remainCount are expected to be caused by answering questions, so the changed parts should be regarded as 'done.'


def updateCounts(forceUpdateTotal):
    """Update totalCount[], remainCount[] and doneCount[].
       If forceUpdateTotal, update totalCount based on doneCount and remainCount.
       If not, update doneCount based on remainCount and totalCount, and increase totalCount only if needed."""
    # if currDID:
    #     # When in reviewer, to get correct card count, we have to use the following codes.
    #     # Excerpted from Anki reviewer
    #     if mw.reviewer.hadCardQueue:
    #         counts = list(mw.col.sched.counts())
    #     else:
    #         counts = list(mw.col.sched.counts(mw.reviewer.card))
    #
    #     _updateCounts(currDID, calcCount(counts[2], counts[1], counts[0]), forceUpdateTotal)
    # else:
    availableDID = []  # record exist deck ids, for cleaning up
    for deckProp in mw.col.sched.deckDueList():
        did = deckProp[1]
        availableDID.append(did)
        remain = calcCount(deckProp[2], deckProp[3], deckProp[4])
        if did not in totalCount.keys():
            _initCounts(did, remain)
            # showInfo("New inited deck %s, remain = %d" % (deckProp[0], remain))
        else:
            _updateCounts(did, remain, forceUpdateTotal)

    # delete counts of unavailable decks
    for did in totalCount.keys():
        if did not in availableDID:
            del totalCount[did], remainCount[did], doneCount[did]


def _updateCounts(did, remain, forceUpdateTotal):
    remainCount[did] = remain

    if forceUpdateTotal:
        totalCount[did] = doneCount[did] + remainCount[did]  # See comments above updateCounts() for explanation.
    else:
        if remainCount[did] + doneCount[did] > totalCount[did]:
            if forceForward:
                return  # Give up changing counts, until the remainCount decrease.
            else:
                # This may happen if you press 'again' followed by 'good' for a new card, as stated in comments
                #    'Calculation weights,' or when you undo a card, making remaining count increases.

                # showInfo("Not forced update total from %d to %d" % (totalCount[did], doneCount[did] + remainCount[did]))
                totalCount[did] = doneCount[did] + remainCount[did]
        # showInfo("Confirm doneCount changes, did %d" % did)
        doneCount[did] = totalCount[did] - remainCount[did]  # See comments above updateCounts() for explanation.


def afterStateChangeCallBack(state, oldState):
    global currDID

    if state == "resetRequired":
        if floatingBarWhenEditing:
            setFloatingPB()
        return
    elif state == "deckBrowser":
        # initPB() has to be here, since objects are not prepared yet when the add-on is loaded.
        if not progressBar:
            initPB()
            initCounts()
        currDID = None
    else:  # "overview" or "review"
        # showInfo("mw.col.decks.current()['id'])= %d" % mw.col.decks.current()['id'])
        currDID = mw.col.decks.current()['id']

    # showInfo("updateCounts(False) 0, currDID = %d" % (currDID if currDID else 0))
    updateCounts(True)  # See comments above updateCounts() for explanation.
    updatePB()


def showQuestionCallBack():
    # showInfo("updateCounts(False) 1, currDID = %d" % (currDID if currDID else 0))
    updateCounts(False)  # See comments above updateCounts() for explanation.
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
