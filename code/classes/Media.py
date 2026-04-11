from datetime import datetime
import shutil
import os
from utils import getAppDataDir
from PyQt6.QtGui import QPixmap

class Media:
    def __init__(self, filePath: str, description: str = ""):
        self.mediaId = None
        self.filePath = filePath
        self.description = description
        self.uploadedAt = datetime.now()

    def upload(self, projectId: int) -> bool:
        if not os.path.exists(self.filePath):
            return False

        appDir = getAppDataDir()
        destinationFolder = os.path.join(appDir, "media", f"project_{projectId}")
        os.makedirs(destinationFolder, exist_ok=True)

        fileName = os.path.basename(self.filePath)
        destination = os.path.join(destinationFolder, fileName)
        shutil.copy2(self.filePath, destination)
        self.filePath = destination
        return True

    def delete(self):
        if os.path.exists(self.filePath):
            os.remove(self.filePath)

    def getPixmap(self):
        return QPixmap(self.filePath)