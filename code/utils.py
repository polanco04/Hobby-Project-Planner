import os
import json

def getAppDataDir() -> str:
    appData = os.getenv("APPDATA") or os.path.expanduser("~")
    return os.path.join(appData, "HobbyProjectPlanner")

def hasOpenedBefore() -> bool:
    flagPath = os.path.join(getAppDataDir(), "opened.json")
    return os.path.exists(flagPath)

def markAsOpened():
    appDir = getAppDataDir()
    os.makedirs(appDir, exist_ok=True)
    flagPath = os.path.join(appDir, "opened.json")
    with open(flagPath, "w") as f:
        json.dump({"opened": True}, f)