from datetime import datetime
import shutil
import os
from utils import getAppDataDir
from PyQt6.QtGui import QPixmap

class Media:
    """
    Name: __init__

    INPUT:
        filePath:       Path to the media file (str)
        description:    Optional description for the media (str)

    RETURN:
        N/A

    DESCRIPTION:
        Initializes a Media instance with a file path, optional description,
        a None mediaId, and an uploadedAt timestamp set to the current time.
    """
    def __init__(self, filePath: str, description: str = ""):
        self.mediaId = None
        self.filePath = filePath
        self.description = description
        self.uploadedAt = datetime.now()

    """
    Name: upload

    INPUT:
        projectId:      ID of the project this media belongs to (int)

    RETURN:
        bool:           True if the upload succeeded, False if the source file does not exist

    DESCRIPTION:
        Copies the media file into the app data directory under a project-specific
        subfolder. Updates self.filePath to the new destination path on success.
    """
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

    """
    Name: delete

    INPUT:
        N/A

    RETURN:
        N/A

    DESCRIPTION:
        Deletes the media file from disk if it exists at the stored file path.
    """
    def delete(self):
        if os.path.exists(self.filePath):
            os.remove(self.filePath)

    """
    Name: getPixmap

    INPUT:
        N/A

    RETURN:
        QPixmap:        A QPixmap object loaded from the media file path

    DESCRIPTION:
        Creates and returns a QPixmap from the stored file path, suitable
        for display in a PyQt6 UI.
    """
    def getPixmap(self):
        return QPixmap(self.filePath)