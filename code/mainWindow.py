from qfluentwidgets import FluentWindow, NavigationItemPosition, toggleTheme, NavigationToolButton
from qfluentwidgets import FluentIcon as FIF
from pages import homePage, projectPage, profilePage, projectViewPage
from classes.Hobbyist import Hobbyist
from classes.LocalStorage import LocalStorage

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hobby Project Planner")
        self.resize(600, 400)

        self.storage = LocalStorage()
        self.hobbyist = self.storage.loadHobbyist()
        if self.hobbyist is None:
            self.hobbyist = Hobbyist("User")
            self.storage.saveHobbyist(self.hobbyist)

        self.homePage = homePage(self, self.hobbyist)
        self.projectPage = projectPage(self.hobbyist, self.storage)
        self.profilePage = profilePage(self.hobbyist, self.storage)
        self.projectViewPage = projectViewPage(self.storage)

        self.addSubInterface(self.homePage, FIF.HOME, "Home")
        self.addSubInterface(self.projectPage, FIF.FOLDER, "Projects")
        self.addSubInterface(self.profilePage, FIF.PEOPLE, "Profile")
        self.stackedWidget.addWidget(self.projectViewPage)
        self.navigationInterface.setReturnButtonVisible(False)

        self.themeButton = NavigationToolButton(FIF.CONSTRACT, self)
        self.navigationInterface.addWidget(
            routeKey="themeToggle",
            widget=self.themeButton,
            position=NavigationItemPosition.BOTTOM,
        )
        self.themeButton.clicked.connect(self.toggleAppTheme)

    def toggleAppTheme(self):
        toggleTheme(lazy=True)

    def closeEvent(self, event):
        self.storage.close()
        super().closeEvent(event)