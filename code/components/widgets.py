from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from qfluentwidgets import CaptionLabel, CardWidget
import sys, os

"""
Name: resource_path

INPUT:
    relative_path:      Relative file path to a resource (str)

RETURN:
    str:                Absolute path to the resource, accounting for PyInstaller bundling

DESCRIPTION:
    Resolves the absolute path to a resource file. When running as a PyInstaller
    executable, uses the temporary _MEIPASS directory; otherwise resolves relative
    to the current working directory.
"""
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

"""
Name: createFeatureCard

INPUT:
    imagePath:          Relative path to the card's image file (str)
    caption:            Caption text to display below the card (str)

RETURN:
    QWidget:            A widget containing a styled image card and caption label

DESCRIPTION:
    Builds and returns a centered card widget displaying a scaled image and a
    caption label beneath it. The image is scaled to 250x180 pixels while
    preserving aspect ratio. Uses CardWidget from qfluentwidgets for styling.
"""
def createFeatureCard(imagePath, caption):
    wrapper = QWidget()
    wrapperLayout = QVBoxLayout(wrapper)
    wrapperLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    card = CardWidget()
    card_layout = QVBoxLayout(card)
    
    img_label = QLabel()
    img_label.setPixmap(
        QPixmap(resource_path(imagePath)).scaled(250, 180, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
    )
    img_label.setFixedSize(250, 180)
    card_layout.addWidget(img_label)

    captionLabel = CaptionLabel(caption)
    captionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    wrapperLayout.addWidget(card)
    wrapperLayout.addWidget(captionLabel)

    return wrapper