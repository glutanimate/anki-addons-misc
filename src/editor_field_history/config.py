from aqt import mw
import sys

userOption = None

def getUserOption(key = None, default = None):
    #print(f"getUserOption(key = {key}, default = {default})")
    global userOption
    if userOption is None:
        userOption = mw.addonManager.getConfig(__name__)
        #debug("userOption read from the file and is {userOption}")
    if key is None:
        #debug("return {userOption}")
        return userOption
    if key in userOption:
        #debug("key in userOption. Returning {userOption[key]}")
        return userOption[key]
    else:
        #debug("key not in userOption. Returning default.")
        return default

def writeConfig():
    mw.addonManager.writeConfig(__name__,userOption)

def update(_):
    global userOption, fromName
    userOption = None
    fromName = None

mw.addonManager.setConfigUpdatedAction(__name__,update)
