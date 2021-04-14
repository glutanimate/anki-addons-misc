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
import pathlib

import aqt
from .utils import todayStats_new

root = pathlib.Path(__file__).parent.resolve()
assets_dir = root / "web"

INJECT_ASSETS = """
const injectAssets = (assets) => {
    assets.forEach((url) => {
        if (url.endsWith('.js')) {
            const script = document.createElement('script');
            script.src = url;
            script.async = true;
            document.head.appendChild(script);
        } else if (url.endsWith('.css')) {
            const link = document.createElement('link');
            link.href = url;
            link.rel = 'stylesheet';
            document.head.appendChild(link);
        }
    });
};
"""


def generate_run_function(func: str):
    import json
    html = todayStats_new(aqt.mw.col.stats())

    js = """
    ( async (stats) => {
    while(typeof setStats !== 'function') {
        await new Promise((resolve) => setTimeout(resolve, 100));
    }
    setStats(stats);
    })(%s);
""" % (json.dumps(html))

    return js


def generate_js() -> str:
    js = ""
    urls = []
    for file_path in sorted(assets_dir.glob("*.*")):
        if file_path.name.endswith((".css", ".js")):
            urls.append(f"/_addons/{root.name}/web/{file_path.name}")
    if urls:
        urls_string = ",".join(f'"{url}"' for url in urls)
        js = f"{INJECT_ASSETS}injectAssets([{urls_string}]);"
    return js


def onShowStats_new(webview: aqt.webview.AnkiWebView):

    if isinstance(webview.parent(), aqt.stats.NewDeckStats):
        js = generate_js()
        if js:
            webview.eval(js)
            webview.eval(generate_run_function('setStats'))
    #    print(json.dumps(html))


def onShowStats_old(statsDialog: aqt.stats.NewDeckStats):

    js = generate_js()
    if js:
        statsDialog.form.web.loadFinished.connect(lambda *_: statsDialog.form.web.eval(js))
        statsDialog.form.web.loadFinished.connect(
            lambda *_: statsDialog.form.web.eval(generate_run_function('setStats')))


aqt.mw.addonManager.setWebExports(__name__, r".+\.(css|js)")

try:
    aqt.gui_hooks.webview_did_inject_style_into_page.append(onShowStats_new)
except AttributeError:
    # for Anki 2.1.35 or earlier
    aqt.gui_hooks.stats_dialog_will_show.append(onShowStats_old)
