import os

def getAppDataDir() -> str:
    appData = os.getenv("APPDATA") or os.path.expanduser("~")
    return os.path.join(appData, "HobbyProjectPlanner")