# -*- coding: utf-8 -*-
"""
Anki Add-on: Deck Overview Stats Tooltip

Shows a tooltip on the main window deck browser page

Makes use of MiniTip (Dual licensed under the MIT and GPL licenses)
http://goldfirestudios.com/blog/81/miniTip-jQuery-Plugin
https://github.com/goldfire/minitip

Copyright:  (c) Steve AW 2013 <steveawa@gmail.com>
            (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

#

from aqt.qt import *
from anki.hooks import wrap
from anki.lang import _, ngettext
from anki.utils import ids2str, fmtTimeSpan
from aqt import mw
from aqt.deckbrowser import DeckBrowser


minitip_js = """
   /*!
 * miniTip v1.5.3
 *
 * Updated: July 15, 2012
 * Requires: jQuery v1.3+
 *
 * (c) 2011, James Simpson
 * http://goldfirestudios.com
 *
 * Dual licensed under the MIT and GPL
 *
 * Documentation found at:
 * http://goldfirestudios.com/blog/81/miniTip-jQuery-Plugin
*/
(function(e){e.fn.miniTip=function(t){var n={title:"",content:!1,delay:300,anchor:"n",event:"hover",fadeIn:200,fadeOut:200,aHide:!0,maxW:"250px",offset:5,stemOff:0,doHide:!1},r=e.extend(n,t);e("#miniTip")[0]||e("body").append('<div id="miniTip"><div id="miniTip_t"></div><div id="miniTip_c"></div><div id="miniTip_a"></div></div>');var i=e("#miniTip"),s=e("#miniTip_t"),o=e("#miniTip_c"),u=e("#miniTip_a");return r.doHide?(i.stop(!0,!0).fadeOut(r.fadeOut),!1):this.each(function(){var t=e(this),n=r.content?r.content:t.attr("title");if(n!=""&&typeof n!="undefined"){window.delay=!1;var a=!1,f=!0;r.content||t.removeAttr("title"),r.event=="hover"?(t.hover(function(){i.removeAttr("click"),f=!0,l.call(this)},function(){f=!1,c()}),r.aHide||i.hover(function(){a=!0},function(){a=!1,setTimeout(function(){!f&&!i.attr("click")&&c()},20)})):r.event=="click"&&(r.aHide=!0,t.click(function(){return i.attr("click","t"),i.data("last_target")!==t?l.call(this):i.css("display")=="none"?l.call(this):c(),i.data("last_target",t),e("html").unbind("click").click(function(t){i.css("display")=="block"&&!e(t.target).closest("#miniTip").length&&(e("html").unbind("click"),c())}),!1}));var l=function(){r.show&&r.show.call(this,r),r.content&&r.content!=""&&(n=r.content),o.html(n),r.title!=""?s.html(r.title).show():s.hide(),r.render&&r.render(i),u.removeAttr("class"),i.hide().width("").width(i.width()).css("max-width",r.maxW);var a=t.is("area");if(a){var f,l=[],c=[],h=t.attr("coords").split(",");function p(e,t){return e-t}for(f=0;f<h.length;f++)l.push(h[f++]),c.push(h[f]);var d=t.parent().attr("name"),v=e("img[usemap=\\#"+d+"]").offset(),m=parseInt(v.left,10)+parseInt((parseInt(l.sort(p)[0],10)+parseInt(l.sort(p)[l.length-1],10))/2,10),g=parseInt(v.top,10)+parseInt((parseInt(c.sort(p)[0],10)+parseInt(c.sort(p)[c.length-1],10))/2,10)}else var g=parseInt(t.offset().top,10),m=parseInt(t.offset().left,10);var y=a?0:parseInt(t.outerWidth(),10),b=a?0:parseInt(t.outerHeight(),10),w=i.outerWidth(),E=i.outerHeight(),S=Math.round(m+Math.round((y-w)/2)),x=Math.round(g+b+r.offset+8),T=Math.round(w-16)/2-parseInt(i.css("borderLeftWidth"),10),N=0,C=m+y+w+r.offset+8>parseInt(e(window).width(),10),k=w+r.offset+8>m,L=E+r.offset+8>g-e(window).scrollTop(),A=g+b+E+r.offset+8>parseInt(e(window).height()+e(window).scrollTop(),10),O=r.anchor;if(k||r.anchor=="e"&&!C){if(r.anchor=="w"||r.anchor=="e")O="e",N=Math.round(E/2-8-parseInt(i.css("borderRightWidth"),10)),T=-8-parseInt(i.css("borderRightWidth"),10),S=m+y+r.offset+8,x=Math.round(g+b/2-E/2)}else if(C||r.anchor=="w"&&!k)if(r.anchor=="w"||r.anchor=="e")O="w",N=Math.round(E/2-8-parseInt(i.css("borderLeftWidth"),10)),T=w-parseInt(i.css("borderLeftWidth"),10),S=m-w-r.offset-8,x=Math.round(g+b/2-E/2);if(A||r.anchor=="n"&&!L){if(r.anchor=="n"||r.anchor=="s")O="n",N=E-parseInt(i.css("borderTopWidth"),10),x=g-(E+r.offset+8)}else if(L||r.anchor=="s"&&!A)if(r.anchor=="n"||r.anchor=="s")O="s",N=-8-parseInt(i.css("borderBottomWidth"),10),x=g+b+r.offset+8;r.anchor=="n"||r.anchor=="s"?w/2>m?(S=S<0?T+S:T,T=0):m+w/2>parseInt(e(window).width(),10)&&(S-=T,T*=2):L?(x+=N,N=0):A&&(x-=N,N*=2),u.css({"margin-left":(T>0?T:T+parseInt(r.stemOff,10)/2)+"px","margin-top":N+"px"}).attr("class",O),delay&&clearTimeout(delay),delay=setTimeout(function(){i.css({"margin-left":S+"px","margin-top":x+"px"}).stop(!0,!0).fadeIn(r.fadeIn)},r.delay)},c=function(){if(!r.aHide&&!a||r.aHide)delay&&clearTimeout(delay),delay=setTimeout(function(){h()},r.delay)},h=function(){!r.aHide&&!a||r.aHide?(i.stop(!0,!0).fadeOut(r.fadeOut),r.hide&&r.hide.call(this)):setTimeout(function(){c()},200)}}})}})(jQuery)
"""

minitip_css = """
    /*! miniTip CSS - v1.5.3 */
#miniTip{background-color:#f8f5ca;border:4px solid #eae4b4;color:#000000;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;display:none;position:absolute;top:0;left:0;z-index:99999}#miniTip_t{background-color:#f5edc2;font-weight:700;padding:4px 6px}#miniTip_c{padding:4px 8px}#miniTip_a{width:0;height:0;position:absolute;top:0;left:0}#miniTip .n{border-left:8px solid transparent;border-right:8px solid transparent;border-top:8px solid #eae4b4;border-bottom:0}#miniTip .s{border-left:8px solid transparent;border-right:8px solid transparent;border-bottom:8px solid #eae4b4;border-top:0}#miniTip .e{border-bottom:8px solid transparent;border-top:8px solid transparent;border-right:8px solid #eae4b4;border-left:0}#miniTip .w{border-bottom:8px solid transparent;border-top:8px solid transparent;border-left:8px solid #eae4b4;border-right:0}"""


def _generate_jquery_scripts():
    """
    This generates a js function for each deck's row based on did
    I am guessing that only one function is needed, but I couldn't figure out how to do it
    Somehow the render function needs to keep a reference to the outer context this.id
    I don't know js or jquery well enough to do that.
    If you know, please let me know.
    """
    tip_script = "    $(function(){"
    template = """
    $('tr#%(id)s a').miniTip({
        content: 'Loading...', offset: 1, delay: 500, maxW: '500px',
		render: function(tt) {
        $('#miniTip_c').html(py_deck_inf.deck_information_for(%(id)s) );}});
        """
    for did in mw.col.decks.allIds():
        tip_script += (template % dict(id=did))
    tip_script += """
        });
        """
    return tip_script


class DeckInformation(QObject):
    """
    A single instance of the class is created and stored in the module's deck_info
    variable. This instance is then added as a javascript object to the deckbrowser's
    main frame. We then get callbacks from miniTip show functions requesting
    the html to display
    """

    def __init__(self):
        QObject.__init__(self)


    @pyqtSlot(str, result=str)
    def deck_information_for(self, did):
        return self.generate_tooltip_html(did)

    def generate_tooltip_html(self, did):
        return DeckReport(mw, did).generate_html()


deck_info = DeckInformation()


class DeckReport(object):
    """
    Generate and answer the html for the did deck's tooltip
    Instances are short lived, they are created for a single tooltip callback
    """

    def __init__(self, mw, did):
        object.__init__(self)
        self.mw = mw
        self.col = self.mw.col
        self.did = did
        self.deck = self.col.decks.get(did)
        self.deck_children = self.col.decks.children(did)
        self.deck_limit = ids2str([child_did for (child_name, child_did) in self.deck_children] + [self.did])
        self.html = ''

    def generate_html(self):
        self.html = "<table width=100%>"
        self.build_html()
        self.html += "</table>"
        return self.html

    def build_html(self):

        self.add_row("Name:", self.deck["name"])
        self.add_row("Options", self.col.decks.confForDid(self.did)["name"])

        (card_count, note_count) = mw.col.db.first("""
select count(id), count(distinct nid) from cards
where did in %s """ % self.deck_limit)
        self.add_row("Total notes:", note_count)
        self.add_row("Total cards:", card_count)

        suspended_count = mw.col.db.scalar("""
select count(id)from cards
where queue = -1 and did in %s """ % self.deck_limit)
        self.add_row("Suspended:", suspended_count)
        self.add_row("Did:", self.did)
        self.add_row("Today:", self.todayStats())

        #todo
        """
        Due tomorrow,next etc
        If you studied every day:	6.1 minutes/day
Average answer time:	17.5s (3 cards/minute)
        """

    def todayStats(self):
        """
        Copy and paste from CollectionStats.todayStats(self)
        Two changes made
        """
        #DeckInformation ... changed formatting
        b = ""
        #DeckInformation ... changed to use our deck limit
        lim = "cid in (select id from cards where did in %s)" % self.deck_limit
        if lim:
            lim = " and " + lim
        cards, thetime, failed, lrn, rev, relrn, filt = self.col.db.first("""
select count(), sum(time)/1000,
sum(case when ease = 1 then 1 else 0 end), /* failed */
sum(case when type = 0 then 1 else 0 end), /* learning */
sum(case when type = 1 then 1 else 0 end), /* review */
sum(case when type = 2 then 1 else 0 end), /* relearn */
sum(case when type = 3 then 1 else 0 end) /* filter */
from revlog where id > ? """ + lim, (self.col.sched.dayCutoff - 86400) * 1000)
        cards = cards or 0
        thetime = thetime or 0
        failed = failed or 0
        lrn = lrn or 0
        rev = rev or 0
        relrn = relrn or 0
        filt = filt or 0
        # studied
        def bold(s):
            return "<b>" + unicode(s) + "</b>"

        msgp1 = ngettext("<!--studied-->%d card", "<!--studied-->%d cards", cards) % cards
        b += _("Studied %(a)s in %(b)s today.") % dict(
            a=bold(msgp1), b=bold(fmtTimeSpan(thetime, unit=1)))
        # again/pass count
        b += "<br>" + _("Again count: %s") % bold(failed)
        if cards:
            b += " " + _("(%s correct)") % bold(
                "%0.1f%%" % ((1 - failed / float(cards)) * 100))
            # type breakdown
        b += "<br>"
        b += (_("Learn: %(a)s, Review: %(b)s, Relearn: %(c)s, Filtered: %(d)s")
              % dict(a=bold(lrn), b=bold(rev), c=bold(relrn), d=bold(filt)))
        # mature today
        mcnt, msum = self.col.db.first("""
select count(), sum(case when ease = 1 then 0 else 1 end) from revlog
where lastIvl >= 21 and id > ?""" + lim, (self.col.sched.dayCutoff - 86400) * 1000)
        b += "<br>"
        if mcnt:
            b += _("Correct answers on mature cards: %(a)d/%(b)d (%(c).1f%%)") % dict(
                a=msum, b=mcnt, c=(msum / float(mcnt) * 100))
        else:
            b += _("No mature cards were studied today.")
        return b

    def add_row(self, label, value):
        self.html += "<tr><td><b>%s</b></td><td>%s</td></tr>" % (label, value)


def add_tipjs_to_rendered_page(self, reuse=False):
    #add the minitip function
    self.web.page().mainFrame().evaluateJavaScript(minitip_js)
    #add the jquery functions for each deck
    self.web.page().mainFrame().evaluateJavaScript(_generate_jquery_scripts())
    #add the callback object
    self.web.page().mainFrame().addToJavaScriptWindowObject("py_deck_inf", deck_info)
    #insert the extra css
    self.web.page().mainFrame().findFirstElement("style").appendInside(minitip_css)


DeckBrowser._renderPage = wrap(DeckBrowser._renderPage, add_tipjs_to_rendered_page, "after")




