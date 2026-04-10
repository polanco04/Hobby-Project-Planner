from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from qfluentwidgets import CaptionLabel, CardWidget

def createFeatureCard(imagePath, caption):
    wrapper = QWidget()
    wrapperLayout = QVBoxLayout(wrapper)
    wrapperLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    card = CardWidget()
    card_layout = QVBoxLayout(card)
    
    img_label = QLabel()
    img_label.setPixmap(
        QPixmap(imagePath).scaled(250, 180, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
    )
    img_label.setFixedSize(250, 180)
    card_layout.addWidget(img_label)

    captionLabel = CaptionLabel(caption)
    captionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    wrapperLayout.addWidget(card)
    wrapperLayout.addWidget(captionLabel)

    return wrapper