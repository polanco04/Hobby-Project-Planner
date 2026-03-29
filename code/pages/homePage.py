from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (
    BodyLabel, CardWidget, SubtitleLabel
)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("homePage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        label = SubtitleLabel("Home")
        layout.addWidget(label)

        '''
        cardRow = QHBoxLayout()
        cardRow.setSpacing(12)

        card1 = self.createCard("Users", "124")
        card2 = self.createCard("Projects", "8")
        card3 = self.createCard("Milestones", "3")

        cardRow.addWidget(card1)
        cardRow.addWidget(card2)
        cardRow.addWidget(card3)

        layout.addLayout(cardRow)
        '''
        layout.addStretch()
        self.setLayout(layout)
'''
    def createCard(self, title, value):
        card = CardWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        layout.addWidget(BodyLabel(title))
        layout.addWidget(BodyLabel(value))

        card.setLayout(layout)
        return card
'''