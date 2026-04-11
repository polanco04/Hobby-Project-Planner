from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from qfluentwidgets import (
    BodyLabel, CardWidget, SubtitleLabel, TitleLabel, PrimaryPushButton, 
    HorizontalSeparator, IconWidget
)
from qfluentwidgets import FluentIcon as FIF
from pages.widgets import createFeatureCard
import random

FEATURE_CARDS = {
    "Start a new project": [
        "projectImages/startProject1.jpg",
        "projectImages/startProject2.jpg",
        "projectImages/startProject3.jpg",
    ],
    "Stay organized": [
        "projectImages/organize1.jpg",
        "projectImages/organize2.jpg",
        "projectImages/organize3.jpg",
    ],
    "Bring ideas to life": [
        "projectImages/ideas1.jpg",
        "projectImages/ideas2.jpg",
        "projectImages/ideas3.jpg",
    ],
}

class projectPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("projectPage")
        
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        outer.setContentsMargins(40, 0, 40, 0) 

        container = QWidget()
        container.setMaximumWidth(1000)
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        headerRow = QHBoxLayout()
        headerRow.addWidget(TitleLabel("Projects"))
        headerRow.addStretch() 

        btn = PrimaryPushButton("+ New Project")
        btn.setFixedWidth(150)
        btn.setFixedHeight(40)
        headerRow.addWidget(btn)

        layout.addLayout(headerRow)
        layout.addWidget(self.createNpCard())
        layout.addStretch() 
        layout.addWidget(HorizontalSeparator())

        self.featureRow = QHBoxLayout()
        self.featureRow.setSpacing(20)

        layout.addLayout(self.featureRow)

        outer.addWidget(container)

    def showEvent(self, event):
        super().showEvent(event)
        self.refreshFeatureCards()

    def refreshFeatureCards(self):
        while self.featureRow.count():
            item = self.featureRow.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for caption, images in FEATURE_CARDS.items():
            image = random.choice(images)
            self.featureRow.addWidget(createFeatureCard(image, caption))

    def createNpCard(self):
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(10)

        iconWidget = IconWidget(FIF.FOLDER)
        iconWidget.setFixedSize(60, 60)

        iconRow = QHBoxLayout()
        iconRow.addStretch()
        iconRow.addWidget(iconWidget)
        iconRow.addStretch()

        title = SubtitleLabel("No projects yet")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        body = BodyLabel("Create your first project to get started!")
        body.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(iconRow)
        layout.addWidget(title)
        layout.addWidget(body)
        return card
