from qfluentwidgets import FluentWindow, NavigationItemPosition, toggleTheme, NavigationToolButton
from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtWidgets import QApplication, QScrollArea, QWidget
from PyQt6.QtCore import Qt
from pages import homePage, projectPage, profilePage, projectViewPage
from classes.Hobbyist import Hobbyist
from classes.LocalStorage import LocalStorage

class MainWindow(FluentWindow):
    def __init__(self, isFirstTime=False):
        super().__init__()

        self.setWindowTitle("Hobby Project Planner")
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)

        screen = QApplication.primaryScreen().availableGeometry()
        frameGeo = self.frameGeometry()
        frameGeo.moveCenter(screen.center())
        frameGeo.setTop(max(frameGeo.top(), screen.top()))
        frameGeo.setLeft(max(frameGeo.left(), screen.left()))
        self.move(frameGeo.topLeft())

        self.storage = LocalStorage()
        self.hobbyist = self.storage.loadHobbyist()
        if self.hobbyist is None:
            self.hobbyist = Hobbyist("User")
            self.storage.saveHobbyist(self.hobbyist)

        self.homePage = homePage(self, self.hobbyist, isFirstTime)
        self.projectPage = projectPage(self.hobbyist, self.storage)
        self.profilePage = profilePage(self.hobbyist, self.storage)
        self.projectViewPage = projectViewPage(self.storage)

        self._homeScroll    = self.wrapScroll(self.homePage)
        self._projectScroll = self.wrapScroll(self.projectPage)
        self._profileScroll = self.wrapScroll(self.profilePage)
        self._viewScroll    = self.wrapScroll(self.projectViewPage)

        self.addSubInterface(self._homeScroll,    FIF.HOME,   "Home")
        self.addSubInterface(self._projectScroll, FIF.FOLDER, "Projects")
        self.addSubInterface(self._profileScroll, FIF.PEOPLE, "Profile")
        self.stackedWidget.addWidget(self._viewScroll)
        self.navigationInterface.setReturnButtonVisible(False)

        self.themeButton = NavigationToolButton(FIF.CONSTRACT, self)
        self.navigationInterface.addWidget(
            routeKey="themeToggle",
            widget=self.themeButton,
            position=NavigationItemPosition.BOTTOM,
        )
        self.themeButton.clicked.connect(self.toggleAppTheme)

    def wrapScroll(self, widget):
        scroll = QScrollArea()
        scroll.setObjectName(widget.objectName() + "_scroll")
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll.viewport().setStyleSheet("background: transparent;")
        return scroll

    def toggleAppTheme(self):
        toggleTheme(lazy=True)

    def closeEvent(self, event):
        self.storage.close()
        super().closeEvent(event)