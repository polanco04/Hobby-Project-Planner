import os
import json

"""
Name: getAppDataDir

INPUT:
    N/A

RETURN:
    str:                Absolute path to the application's data directory

DESCRIPTION:
    Returns the path to the app's data directory by joining the APPDATA environment
    variable (or the user's home directory as a fallback) with the app folder name.
"""
def getAppDataDir() -> str:
    appData = os.getenv("APPDATA") or os.path.expanduser("~")
    return os.path.join(appData, "HobbyProjectPlanner")

"""
Name: hasOpenedBefore

INPUT:
    N/A

RETURN:
    bool:               True if the app has been launched before, False otherwise

DESCRIPTION:
    Checks whether the app has previously been opened by looking for the
    existence of an 'opened.json' flag file in the app data directory.
"""
def hasOpenedBefore() -> bool:
    flagPath = os.path.join(getAppDataDir(), "opened.json")
    return os.path.exists(flagPath)

"""
Name: markAsOpened

INPUT:
    N/A

RETURN:
    N/A

DESCRIPTION:
    Creates the app data directory if it doesn't exist, then writes an
    'opened.json' flag file to record that the app has been launched at least once.
"""
def markAsOpened():
    appDir = getAppDataDir()
    os.makedirs(appDir, exist_ok=True)
    flagPath = os.path.join(appDir, "opened.json")
    with open(flagPath, "w") as f:
        json.dump({"opened": True}, f)