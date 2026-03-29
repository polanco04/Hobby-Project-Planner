import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (
    FluentWindow, BodyLabel, CardWidget, SubtitleLabel,
    NavigationItemPosition, toggleTheme, NavigationToolButton
)
from qfluentwidgets import FluentIcon as FIF


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

class ProjectPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("projectPage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        self.label = SubtitleLabel("Projects")
        layout.addWidget(self.label)

        layout.addStretch()

        self.setLayout(layout)

class profilePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("profilePage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        self.label = SubtitleLabel("Profile")
        layout.addWidget(self.label)

        layout.addStretch()

        self.setLayout(layout)


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hobby Project Planner")
        self.resize(600, 400)

        # Create pages
        self.homePage = HomePage()
        self.projectPage = ProjectPage()
        self.profilePage = profilePage()

        # Add to Fluent navigation
        self.addSubInterface(self.homePage, FIF.HOME, "Home")
        self.addSubInterface(self.projectPage, FIF.FOLDER, "Projects")
        self.addSubInterface(self.profilePage, FIF.PEOPLE, "Profile")
        self.navigationInterface.setReturnButtonVisible(False)

        # Add theme toggle — connect via signal only, no onClick param
        self.themeButton = NavigationToolButton(FIF.CONSTRACT, self)
        self.navigationInterface.addWidget(
            routeKey="themeToggle",
            widget=self.themeButton,
            position=NavigationItemPosition.BOTTOM,
        )
        self.themeButton.clicked.connect(self.toggleAppTheme)

    def toggleAppTheme(self):
        toggleTheme(lazy=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())