from qfluentwidgets import (
    FluentWindow, NavigationItemPosition, toggleTheme, NavigationToolButton
)
from qfluentwidgets import FluentIcon as FIF
from pages import homePage, projectPage, profilePage, projectViewPage

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hobby Project Planner")
        self.resize(600, 400)

        # Create pages
        self.homePage = homePage(self)
        self.projectPage = projectPage()
        self.profilePage = profilePage()
        self.projectViewPage = projectViewPage()

        # Add to Fluent navigation
        self.addSubInterface(self.homePage, FIF.HOME, "Home")
        self.addSubInterface(self.projectPage, FIF.FOLDER, "Projects")
        self.addSubInterface(self.profilePage, FIF.PEOPLE, "Profile")
        self.addSubInterface(self.projectViewPage, FIF.PEOPLE, "Project View")
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