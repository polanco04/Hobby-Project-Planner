from qfluentwidgets import FluentWindow, NavigationItemPosition, toggleTheme, NavigationToolButton
from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtWidgets import QApplication, QScrollArea, QWidget
from PyQt6.QtCore import Qt
from pages import homePage, projectPage, profilePage, projectViewPage
from classes.Hobbyist import Hobbyist
from classes.LocalStorage import LocalStorage

class MainWindow(FluentWindow):
    """
    Name: __init__

    INPUT:
        isFirstTime:    Whether this is the user's first time launching the app (bool)

    RETURN:
        N/A

    DESCRIPTION:
        Initializes the main application window. Sets the title, size, and centers
        it on screen. Loads or creates the hobbyist profile from local storage.
        Instantiates and registers all pages wrapped in scroll areas, sets up
        navigation icons, and adds a theme toggle button to the bottom of the nav bar.
    """
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
        self.projectScroll = self.wrapScroll(self.projectPage)
        self._profileScroll = self.wrapScroll(self.profilePage)
        self.viewScroll    = self.wrapScroll(self.projectViewPage)

        self.addSubInterface(self._homeScroll,    FIF.HOME,   "Home")
        self.addSubInterface(self.projectScroll, FIF.FOLDER, "Projects")
        self.addSubInterface(self._profileScroll, FIF.PEOPLE, "Profile")
        self.stackedWidget.addWidget(self.viewScroll)
        self.navigationInterface.setReturnButtonVisible(False)

        self.themeButton = NavigationToolButton(FIF.CONSTRACT, self)
        self.navigationInterface.addWidget(
            routeKey="themeToggle",
            widget=self.themeButton,
            position=NavigationItemPosition.BOTTOM,
        )
        self.themeButton.clicked.connect(self.toggleAppTheme)

    """
    Name: wrapScroll

    INPUT:
        widget:         The page widget to wrap in a scroll area (QWidget)

    RETURN:
        QScrollArea:    A configured scroll area containing the given widget

    DESCRIPTION:
        Wraps a page widget in a QScrollArea with resizable content, no horizontal
        scrollbar, and a transparent borderless background. The scroll area's object
        name is derived from the wrapped widget's object name.
    """
    def wrapScroll(self, widget):
        scroll = QScrollArea()
        scroll.setObjectName(widget.objectName() + "_scroll")
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll.viewport().setStyleSheet("background: transparent;")
        return scroll

    """
    Name: toggleAppTheme

    INPUT:
        N/A

    RETURN:
        N/A

    DESCRIPTION:
        Toggles the application's visual theme between light and dark mode
        using qfluentwidgets' lazy theme toggle.
    """
    def toggleAppTheme(self):
        toggleTheme(lazy=True)

    """
    Name: closeEvent

    INPUT:
        event:          The close event triggered when the window is closed (QCloseEvent)

    RETURN:
        N/A

    DESCRIPTION:
        Handles the window close event by closing the local storage database
        connection before passing the event to the parent class for default handling.
    """
    def closeEvent(self, event):
        self.storage.close()
        super().closeEvent(event)