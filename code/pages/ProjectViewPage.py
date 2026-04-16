### Project View Page 
## This page will show the details of a specific project when selected within the
## Projects pages.

## NOTE: Comments are not done, still need documentation
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QWidgetItem,
)
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QFont
from qfluentwidgets import SubtitleLabel, isDarkTheme

class projectViewPage(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set the object name for styling purposes
        self.setObjectName("projectViewPage")

        # Set up the layout and widgets for the project view page
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        # Top-left section with back button, title, and description
        topLayout = QHBoxLayout()
        topLayout.setSpacing(12)


        # Adding functionality to the back button
        self.backButton = QPushButton("←") 
        self.backButton.setToolTip("Back to Projects")
        self.backButton.clicked.connect(self._goBackToProjects) # Placeholder for actual back navigation logic
        
        backFont = QFont()
        backFont.setPointSize(14)
        backFont.setBold(True)
        self.backButton.setFont(backFont)
        self.backButton.setFixedWidth(24)
        self.backButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backButton.setFlat(True) # Remove button borders for cleaner look

        textLayout = QVBoxLayout()
        textLayout.setSpacing(4)
        textLayout.setContentsMargins(0, 0, 0, 0)

        self.projectTitle = SubtitleLabel("Project Title")
        self.projectDescription = QLabel("Project Description")
        descriptionFont = QFont()
        descriptionFont.setPointSize(11)
        descriptionFont.setBold(True)
        self.projectDescription.setFont(descriptionFont)
        self.projectDescription.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        textLayout.addWidget(self.projectTitle)
        textLayout.addWidget(self.projectDescription)

        topLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignTop)
        topLayout.addLayout(textLayout)
        topLayout.addStretch()
        

        # Add the top layout to the main layout
        layout.addLayout(topLayout)

        # Tabs container for Tasks, Milestones, Images and Export
        self.tabsWidget = QFrame()
        self.tabsWidget.setObjectName("tabsWidget")
        self.tabsLayout = QHBoxLayout(self.tabsWidget)
        self.tabsLayout.setSpacing(10)
        self.tabsLayout.setContentsMargins(8, 8, 8, 8)

        

        # Four functional tab buttons
        self.taskTab = QPushButton("Tasks")
        self.milestonesTab = QPushButton("Milestones")
        self.imagesTab = QPushButton("Images")
        self.exportTab = QPushButton("Export")

        self.tabButtons = [
            self.taskTab,
            self.milestonesTab,
            self.imagesTab,
            self.exportTab,
        ]

        for button in self.tabButtons:
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(42)
            self.tabsLayout.addWidget(button)

        layout.addWidget(self.tabsWidget)

        # Content area that changes with the selected tab
        self.contentStack = QStackedWidget()

        self.taskPage = self._createTasksPage()
       
        self.milestonesPage = self._createPlaceholderPage("Milestones section")
        self.imagesPage = self._createPlaceholderPage("Images section")
        self.exportPage = self._createPlaceholderPage("Export section")

        self.contentStack.addWidget(self.tasksPage)
        self.contentStack.addWidget(self.milestonesPage)
        self.contentStack.addWidget(self.imagesPage)
        self.contentStack.addWidget(self.exportPage)

        layout.addWidget(self.contentStack)
        layout.addStretch()

        # Tab functionality
        self.taskTab.clicked.connect(lambda: self._setActiveTab(0))
        self.milestonesTab.clicked.connect(lambda: self._setActiveTab(1))
        self.imagesTab.clicked.connect(lambda: self._setActiveTab(2))
        self.exportTab.clicked.connect(lambda: self._setActiveTab(3))

        self.setLayout(layout)

        # Apply theme-aware colors after layout is set
        self._applyThemeColors()       
        self._setActiveTab(0)

    def _applyThemeColors(self):
        if isDarkTheme():
            self.backButton.setStyleSheet(
                "QPushButton { color: #FFFFFF; border: none; background: transparent; }"
                "QPushButton:hover { color: #CFCFCF; }"
            )
            self.projectDescription.setStyleSheet("color: #FFFFFF;")
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget {"
                "background-color: #3A3A3A;"
                "border-radius: 18px;"
                "padding: 2px;"
                "}"
            )
            inactive_color = "#F0F0F0"
            active_text = "#FFFFFF"
            active_bg = "#5A5A5A"
        else:
            self.backButton.setStyleSheet(
                "QPushButton { color: #202020; border: none; background: transparent; }"
                "QPushButton:hover { color: #606060; }"
            )
            self.projectDescription.setStyleSheet("color: #404040;")
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget {"
                "background-color: #E7E7E7;"
                "border-radius: 18px;"
                "padding: 2px;"
                "}"
            )
            inactive_color = "#202020"
            active_text = "#202020"
            active_bg = "#FFFFFF"

        for button in self.tabButtons:
            if button.isChecked():
                button.setStyleSheet(
                    "QPushButton {"
                    f"color: {active_text};"
                    f"background-color: {active_bg};"
                    "border: none;"
                    "border-radius: 16px;"
                    "font-weight: 600;"
                    "padding: 8px 18px;"
                    "}"
                )
            else:
                button.setStyleSheet(
                    "QPushButton {"
                    f"color: {inactive_color};"
                    "background-color: transparent;"
                    "border: none;"
                    "border-radius: 16px;"
                    "font-weight: 600;"
                    "padding: 8px 18px;"
                    "}"
                    "QPushButton:hover { background-color: rgba(255, 255, 255, 0.10); }"
                )

    def _createPlaceholderPage(self, title):
        page = QFrame()
        page.setObjectName("contentFrame")

        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(10)

        titleLabel = QLabel(title)
        titleFont = QFont()
        titleFont.setPointSize(13)
        titleFont.setBold(True)
        titleLabel.setFont(titleFont)

        helpLabel = QLabel()
        helpLabel.setWordWrap(True)

        pageLayout.addWidget(titleLabel)
        pageLayout.addWidget(helpLabel)
        pageLayout.addStretch()

        if isDarkTheme():
            page.setStyleSheet(
                "QFrame#contentFrame { background-color: #2F2F2F; border-radius: 20px; }"
                "QLabel { color: #FFFFFF; }"
            )
        else:
            page.setStyleSheet(
                "QFrame#contentFrame { background-color: #FFFFFF; border-radius: 20px; }"
                "QLabel { color: #202020; }"
            )

        return page
    
    def _createTasksPage(self):
        page = QFrame()
        page.setObjectName("contentFrame")

        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        self.taskInputWidget = QFrame()
        self.taskInputWidget.setObjectName("taskInputWidget")
        inputLayout = QHBoxLayout(self.taskInputWidget)
        inputLayout.setContentsMargins(0, 0, 0, 0)
        inputLayout.setSpacing(8)

        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Add a new task...")

        self.addTaskButton = QPushButton("Add Task")

        inputLayout.addWidget(self.taskInput)
        inputLayout.addWidget(self.addTaskButton)

        




    def _setActiveTab(self, index):
        self.contentStack.setCurrentIndex(index)

        for i, button in enumerate(self.tabButtons):
            button.setChecked(i == index)

        self._applyThemeColors()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.Type.PaletteChange, QEvent.Type.StyleChange):
            self._applyThemeColors()
            current_index = self.contentStack.currentIndex() if hasattr(self, "contentStack") else 0
            if hasattr(self, "contentStack"):
                self.contentStack.widget(0).setStyleSheet(
                    "QFrame#contentFrame { background-color: #2F2F2F; border-radius: 20px; } QLabel { color: #FFFFFF; }"
                    if isDarkTheme()
                    else "QFrame#contentFrame { background-color: #FFFFFF; border-radius: 20px; } QLabel { color: #202020; }"
                )
                self.contentStack.widget(1).setStyleSheet(
                    "QFrame#contentFrame { background-color: #2F2F2F; border-radius: 20px; } QLabel { color: #FFFFFF; }"
                    if isDarkTheme()
                    else "QFrame#contentFrame { background-color: #FFFFFF; border-radius: 20px; } QLabel { color: #202020; }"
                )
                self.contentStack.widget(2).setStyleSheet(
                    "QFrame#contentFrame { background-color: #2F2F2F; border-radius: 20px; } QLabel { color: #FFFFFF; }"
                    if isDarkTheme()
                    else "QFrame#contentFrame { background-color: #FFFFFF; border-radius: 20px; } QLabel { color: #202020; }"
                )
                self.contentStack.widget(3).setStyleSheet(
                    "QFrame#contentFrame { background-color: #2F2F2F; border-radius: 20px; } QLabel { color: #FFFFFF; }"
                    if isDarkTheme()
                    else "QFrame#contentFrame { background-color: #FFFFFF; border-radius: 20px; } QLabel { color: #202020; }"
                )
                self._setActiveTab(current_index)

    def showEvent(self, event):
        super().showEvent(event)
        self._applyThemeColors()

    # Function to go back to projects 
    def _goBackToProjects(self):
        mainWindow = self.window()
        if hasattr(mainWindow, "switchTo") and hasattr(mainWindow, "projectPage"):
            mainWindow.switchTo(mainWindow.projectPage)

    def setProject(self, project):
        self.project = project
        self.projectTitle.setText(project.title)
        self.projectDescription.setText(project.description)