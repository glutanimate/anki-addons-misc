from aqt import mw

options = None
def readIfRequired():
    global options
    if options is None:
        options = mw.addonManager.getConfig(__name__) or dict()

def newConf(config):
    global options
    options = None

def getConfig(s = None, default = None):
    """Get the dictionnary of objects. If a name is given, return the
    object with this name if it exists.

    reads if required."""

    readIfRequired()
    if s is None:
        return options
    else:
        return options.get(s, default)

mw.addonManager.setConfigUpdatedAction(__name__,newConf)
