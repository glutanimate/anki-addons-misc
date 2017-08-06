# -*- coding: utf-8 -*-

"""
Anki Add-on: Batch Note Editing

Batch edit field in selected notes. Allows you to choose between
adding content to the field or replacing its contents entirely.

Commissioned by: /u/TryhardasaurusRex on Reddit

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

import os, tempfile

from aqt.qt import *
from aqt.utils import tooltip, askUser, getFile
from anki.hooks import addHook

class BatchEditDialog(QDialog):
    """Browser batch editing dialog"""
    def __init__(self, browser, nids):
        QDialog.__init__(self, parent=browser)
        self.browser = browser
        self.nids = nids
        self._setupUi()

    def _setupUi(self):
        tlabel = QLabel("Content to add to or replace with:")
        image_btn = QPushButton(clicked=self._insertMedia)
        image_btn.setIcon(QIcon(":/icons/mail-attachment.png"))
        image_btn.setToolTip("Insert a media file reference (e.g. to an image)")
        press_action = QAction(self, triggered=image_btn.animateClick)
        press_action.setShortcut(QKeySequence(_("Alt+i")))
        image_btn.addAction(press_action)
        top_hbox = QHBoxLayout()
        top_hbox.addWidget(tlabel)
        top_hbox.insertStretch(1, stretch=1)
        top_hbox.addWidget(image_btn)
        
        self.tedit = QPlainTextEdit()
        self.tedit.setTabChangesFocus(True)

        flabel = QLabel("In this field:")
        self.fsel = QComboBox()
        fields = self._getFields()
        self.fsel.addItems(fields)
        f_hbox = QHBoxLayout()
        f_hbox.addWidget(flabel)
        f_hbox.addWidget(self.fsel)
        f_hbox.setAlignment(Qt.AlignLeft)

        button_box = QDialogButtonBox(Qt.Horizontal, self)
        adda_btn = button_box.addButton("Add &after", 
            QDialogButtonBox.ActionRole)
        addb_btn = button_box.addButton("Add &before", 
            QDialogButtonBox.ActionRole)
        replace_btn = button_box.addButton("&Replace", 
            QDialogButtonBox.ActionRole)
        close_btn = button_box.addButton("&Cancel",
            QDialogButtonBox.RejectRole)
        adda_btn.setToolTip("Add after existing field contents")
        addb_btn.setToolTip("Add before existing field contents")
        replace_btn.setToolTip("Replace existing field contents")
        adda_btn.clicked.connect(lambda state, x="adda": self.onConfirm(x))
        addb_btn.clicked.connect(lambda state, x="addb": self.onConfirm(x))
        replace_btn.clicked.connect(lambda state, x="replace": self.onConfirm(x))
        close_btn.clicked.connect(self.close)

        self.cb_html = QCheckBox(self)
        self.cb_html.setText("Insert as HTML")
        self.cb_html.setChecked(False)
        s = QShortcut(QKeySequence(_("Alt+H")), 
            self, activated=lambda: self.cb_html.setChecked(True))


        bottom_hbox = QHBoxLayout()
        bottom_hbox.addWidget(self.cb_html)
        bottom_hbox.addWidget(button_box)

        vbox_main = QVBoxLayout()
        vbox_main.addLayout(top_hbox)
        vbox_main.addWidget(self.tedit)
        vbox_main.addLayout(f_hbox)
        vbox_main.addLayout(bottom_hbox)
        self.setLayout(vbox_main)
        self.tedit.setFocus()
        self.setMinimumWidth(540)
        self.setMinimumHeight(400)
        self.setWindowTitle("Batch Edit Selected Notes")

    def _getFields(self):
        nid = self.nids[0]
        mw = self.browser.mw
        model = mw.col.getNote(nid).model()
        fields = mw.col.models.fieldNames(model)
        return fields

    def _insertMedia(self):
        media_file = self._getClip()
        if not media_file:
            media_file = self._chooseFile()
        if not media_file:
            return
        html = self.browser.editor._addMedia(media_file, canDelete=True)
        # need to unescape images again:
        html = self.browser.mw.col.media.escapeImages(html, unescape=True)
        current = self.tedit.toPlainText()
        new = []
        if current:
            # avoid duplicate newlines
            new = current.strip('\n').split('\n') + [html]
            new = "\n".join(new)
        else:
            new = html
        self.tedit.setPlainText(new)

    def _chooseFile(self):
        key = (_("Media") +
               " (*.jpg *.png *.gif *.tiff *.svg *.tif *.jpeg "+
               "*.mp3 *.ogg *.wav *.avi *.ogv *.mpg *.mpeg *.mov *.mp4 " +
               "*.mkv *.ogx *.ogv *.oga *.flv *.swf *.flac)")
        return getFile(self, _("Add Media"), None, key, key="media")

    def _getClip(self):
        clip = QApplication.clipboard()
        if not clip or not clip.mimeData().imageData():
            return False
        handle, image_path = tempfile.mkstemp(suffix='.png')
        clip.image().save(image_path)
        clip.clear()
        if os.stat(image_path).st_size == 0:
            return False
        return unicode(image_path)
            
    def onConfirm(self, mode):
        browser = self.browser
        nids = self.nids
        fld = self.fsel.currentText()
        text = self.tedit.toPlainText()
        isHtml = self.cb_html.isChecked()
        if mode == "replace":
            q = (u"This will replace the contents of the <b>'{0}'</b> field "
                u"in <b>{1} selected note(s)</b>. Proceed?").format(fld, len(nids))
            if not askUser(q, parent=self):
                return
        batchEditNotes(browser, mode, nids, fld, text, isHtml=isHtml)
        self.close()
        

def batchEditNotes(browser, mode, nids, fld, html, isHtml=False):
    if not isHtml:
        # convert newlines to <br> elms
        html = html.replace('\n', '<br/>')
    mw = browser.mw
    mw.checkpoint("batch edit")
    mw.progress.start()
    browser.model.beginReset()
    cnt = 0
    for nid in nids:
        note = mw.col.getNote(nid)
        if fld in note:
            content = note[fld]
            if isHtml:
                spacer = "\n"
                breaks = (spacer)
            else:
                breaks = ("<div>", "</div>", "<br>", "<br/>")
                spacer = "<br/>"
            if mode == "adda":
                if content.endswith(breaks):
                    spacer = ""
                note[fld] += spacer + html
            elif mode == "addb":
                if content.startswith(breaks):
                    spacer = ""
                note[fld] = html + spacer + content
            elif mode == "replace":
                note[fld] = html
            cnt += 1
            note.flush()
    browser.model.endReset()
    mw.requireReset()
    mw.progress.finish()
    mw.reset()
    tooltip("<b>Updated</b> {0} notes.".format(cnt), parent=browser)


def onBatchEdit(browser):
    nids = browser.selectedNotes()
    if not nids:
        tooltip("No cards selected.")
        return
    dialog = BatchEditDialog(browser, nids)
    dialog.exec_()


def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Batch Edit...')
    a.setShortcut(QKeySequence("Ctrl+Alt+B"))
    a.triggered.connect(lambda _, b=browser: onBatchEdit(b))

addHook("browser.setupMenus", setupMenu)