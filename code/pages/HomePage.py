from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from qfluentwidgets import (
    BodyLabel, CardWidget, SubtitleLabel, TitleLabel, PrimaryPushButton, 
    HorizontalSeparator, CaptionLabel
)
class homePage(QWidget):
    def __init__(self, mainWindow=None):
        super().__init__()
        self.setObjectName("homePage")
        self.mainWindow = mainWindow
        # Outer layout just for centering
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        outer.setContentsMargins(40, 0, 40, 0)  # left/right margins give breathing room

        # Inner container with a fixed width
        container = QWidget()
        container.setMaximumWidth(1000)
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        layout.addWidget(TitleLabel("Welcome!"))
        layout.addWidget(BodyLabel("Enjoy and track your hobbies!"))
        layout.addWidget(self.createStCard())

        layout.addStretch() 

        layout.addWidget(HorizontalSeparator())

        featureRow = QHBoxLayout()
        featureRow.setSpacing(20)
        featureRow.addWidget(self.createFeatureCard("images/tasks.jpg", "Organize your tasks"))
        featureRow.addWidget(self.createFeatureCard("images/milestones.jpg", "Track milestones"))
        featureRow.addWidget(self.createFeatureCard("images/notes.jpg", "Document progress"))

        layout.addLayout(featureRow)

        outer.addWidget(container)

    def createStCard(self):
        card = CardWidget()
        layout = QVBoxLayout(card)
        title = SubtitleLabel("Get started")
        body = BodyLabel("You haven't created any projects yet. Start your first hobby project today!")
        btn = PrimaryPushButton("Go to Projects →")
        btn.setFixedWidth(300)
        btn.clicked.connect(lambda: self.mainWindow.switchTo(self.mainWindow.projectPage))

        layout.addWidget(title)
        layout.addSpacing(5)
        layout.addWidget(body)
        layout.addSpacing(15)
        layout.addWidget(btn)
        layout.setContentsMargins(40, 20, 20, 20)
        card.setLayout(layout)
        return card
    
    def createFeatureCard(self, imagePath, caption):
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
