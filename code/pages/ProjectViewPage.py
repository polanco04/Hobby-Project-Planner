### Project View Page 
## This page will show the details of a specific project when selected within the
## Projects pages.
'''
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
        
        self.setObjectName("projectViewPage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        topLayout = QHBoxLayout()
        topLayout.setSpacing(12)

        self.backButton = QPushButton("←") 
        self.backButton.setToolTip("Back to Projects")
        self.backButton.clicked.connect(self.goBackToProjects)
        
        backFont = QFont()
        backFont.setPointSize(14)
        backFont.setBold(True)
        self.backButton.setFont(backFont)
        self.backButton.setFixedWidth(24)
        self.backButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backButton.setFlat(True)

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

        layout.addLayout(topLayout)

        self.tabsWidget = QFrame()
        self.tabsWidget.setObjectName("tabsWidget")
        self.tabsLayout = QHBoxLayout(self.tabsWidget)
        self.tabsLayout.setSpacing(10)
        self.tabsLayout.setContentsMargins(8, 8, 8, 8)

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

        self.contentStack = QStackedWidget()

        self.taskPage = self.createTasksTab()
        self.milestonesPage = self.createMilestonesTab()
        self.imagesPage = self.createImagesTab()
        self.exportPage = self.createExportTab()

        self.contentStack.addWidget(self.taskPage)
        self.contentStack.addWidget(self.milestonesPage)
        self.contentStack.addWidget(self.imagesPage)
        self.contentStack.addWidget(self.exportPage)

        layout.addWidget(self.contentStack)
        layout.addStretch()

        self.taskTab.clicked.connect(lambda: self.setActiveTab(0))
        self.milestonesTab.clicked.connect(lambda: self.setActiveTab(1))
        self.imagesTab.clicked.connect(lambda: self.setActiveTab(2))
        self.exportTab.clicked.connect(lambda: self.setActiveTab(3))

        self.setLayout(layout)

        self.applyThemeColors()       
        self.setActiveTab(0)

    def applyThemeColors(self):
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
            inactiveColor = "#F0F0F0"
            activeText = "#FFFFFF"
            activeBG = "#5A5A5A"
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
            inactiveColor = "#202020"
            activeText = "#202020"
            activeBG = "#FFFFFF"

        for button in self.tabButtons:
            if button.isChecked():
                button.setStyleSheet(
                    "QPushButton {"
                    f"color: {activeText};"
                    f"background-color: {activeBG};"
                    "border: none;"
                    "border-radius: 16px;"
                    "font-weight: 600;"
                    "padding: 8px 18px;"
                    "}"
                )
            else:
                button.setStyleSheet(
                    "QPushButton {"
                    f"color: {inactiveColor};"
                    "background-color: transparent;"
                    "border: none;"
                    "border-radius: 16px;"
                    "font-weight: 600;"
                    "padding: 8px 18px;"
                    "}"
                    "QPushButton:hover { background-color: rgba(255, 255, 255, 0.10); }"
                )

    def createTasksTab(self):
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

        pageLayout.addWidget(self.taskInputWidget)
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
    
    def createMilestonesTab(self):
        page = QFrame()
        page.setObjectName("contentFrame")

        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        self.milestoneInputWidget = QFrame()
        self.milestoneInputWidget.setObjectName("milestoneInputWidget")
        inputLayout = QHBoxLayout(self.taskInputWidget)
        inputLayout.setContentsMargins(0, 0, 0, 0)
        inputLayout.setSpacing(8)

        self.milestoneInput = QLineEdit()
        self.milestoneInput.setPlaceholderText("Add a new milestone...")

        self.addMilestoneButton = QPushButton("Add Milestone")

        inputLayout.addWidget(self.taskInput)
        inputLayout.addWidget(self.addMilestoneButton)

        pageLayout.addWidget(self.milestoneInputWidget)
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

    def createImagesTab(self):
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

        pageLayout.addWidget(self.taskInputWidget)
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
    
    def createExportTab(self):
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

        pageLayout.addWidget(self.taskInputWidget)
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
    
    def setActiveTab(self, index):
        self.contentStack.setCurrentIndex(index)

        for i, button in enumerate(self.tabButtons):
            button.setChecked(i == index)

        self.applyThemeColors()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.Type.PaletteChange, QEvent.Type.StyleChange):
            self.applyThemeColors()
            currentIndex = self.contentStack.currentIndex() if hasattr(self, "contentStack") else 0
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
                self.setActiveTab(currentIndex)

    def showEvent(self, event):
        super().showEvent(event)
        self.applyThemeColors()

    def goBackToProjects(self):
        mainWindow = self.window()
        if hasattr(mainWindow, "switchTo") and hasattr(mainWindow, "projectPage"):
            mainWindow.switchTo(mainWindow.projectPage)

    def setProject(self, project):
        self.project = project
        self.projectTitle.setText(project.title)
        self.projectDescription.setText(project.description)
'''
'''

### Project View Page 
## This page will show the details of a specific project when selected within the
## Projects pages.

## NOTE: Comments are not done, still need documentation
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
)
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QFont
from qfluentwidgets import (
    SubtitleLabel,
    BodyLabel,
    CardWidget,
    PushButton,
    LineEdit,
    isDarkTheme,
)

class projectViewPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setObjectName("projectViewPage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        topLayout = QHBoxLayout()
        topLayout.setSpacing(12)

        self.backButton = QPushButton("←") 
        self.backButton.setToolTip("Back to Projects")
        self.backButton.clicked.connect(self.goBackToProjects)
        
        backFont = QFont()
        backFont.setPointSize(14)
        backFont.setBold(True)
        self.backButton.setFont(backFont)
        self.backButton.setFixedWidth(24)
        self.backButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backButton.setFlat(True)

        textLayout = QVBoxLayout()
        textLayout.setSpacing(4)
        textLayout.setContentsMargins(0, 0, 0, 0)

        self.projectTitle = SubtitleLabel("Project Title")
        self.projectDescription = BodyLabel("Project Description")
        self.projectDescription.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        textLayout.addWidget(self.projectTitle)
        textLayout.addWidget(self.projectDescription)

        topLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignTop)
        topLayout.addLayout(textLayout)
        topLayout.addStretch()

        layout.addLayout(topLayout)

        self.tabsWidget = QFrame()
        self.tabsWidget.setObjectName("tabsWidget")
        self.tabsLayout = QHBoxLayout(self.tabsWidget)
        self.tabsLayout.setSpacing(10)
        self.tabsLayout.setContentsMargins(8, 8, 8, 8)

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

        self.contentStack = QStackedWidget()

        self.taskPage = self.createTasksTab()
        self.milestonesPage = self.createMilestonesTab()
        self.imagesPage = self.createPlaceholderTab("Images coming soon")
        self.exportPage = self.createPlaceholderTab("Export coming soon")

        self.contentStack.addWidget(self.taskPage)
        self.contentStack.addWidget(self.milestonesPage)
        self.contentStack.addWidget(self.imagesPage)
        self.contentStack.addWidget(self.exportPage)

        layout.addWidget(self.contentStack)
        layout.addStretch()

        self.taskTab.clicked.connect(lambda: self.setActiveTab(0))
        self.milestonesTab.clicked.connect(lambda: self.setActiveTab(1))
        self.imagesTab.clicked.connect(lambda: self.setActiveTab(2))
        self.exportTab.clicked.connect(lambda: self.setActiveTab(3))

        self.setLayout(layout)

        self.applyThemeColors()       
        self.setActiveTab(0)

    def applyThemeColors(self):
        if isDarkTheme():
            self.backButton.setStyleSheet(
                "QPushButton { color: #FFFFFF; border: none; background: transparent; }"
                "QPushButton:hover { color: #CFCFCF; }"
            )
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget {"
                "background-color: #3A3A3A;"
                "border-radius: 18px;"
                "padding: 2px;"
                "}"
            )
            inactiveColor = "#F0F0F0"
            activeText = "#FFFFFF"
            activeBG = "#5A5A5A"
        else:
            self.backButton.setStyleSheet(
                "QPushButton { color: #202020; border: none; background: transparent; }"
                "QPushButton:hover { color: #606060; }"
            )
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget {"
                "background-color: #E7E7E7;"
                "border-radius: 18px;"
                "padding: 2px;"
                "}"
            )
            inactiveColor = "#202020"
            activeText = "#202020"
            activeBG = "#FFFFFF"

        for button in self.tabButtons:
            if button.isChecked():
                button.setStyleSheet(
                    "QPushButton {"
                    f"color: {activeText};"
                    f"background-color: {activeBG};"
                    "border: none;"
                    "border-radius: 16px;"
                    "font-weight: 600;"
                    "padding: 8px 18px;"
                    "}"
                )
            else:
                button.setStyleSheet(
                    "QPushButton {"
                    f"color: {inactiveColor};"
                    "background-color: transparent;"
                    "border: none;"
                    "border-radius: 16px;"
                    "font-weight: 600;"
                    "padding: 8px 18px;"
                    "}"
                    "QPushButton:hover { background-color: rgba(255, 255, 255, 0.10); }"
                )

    def createTasksTab(self):
        page = CardWidget()

        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        # Input row
        inputLayout = QHBoxLayout()
        inputLayout.setContentsMargins(0, 0, 0, 0)
        inputLayout.setSpacing(8)

        self.taskInput = LineEdit()
        self.taskInput.setPlaceholderText("Add a new task...")
        self.taskInput.returnPressed.connect(self.addTask)

        self.addTaskButton = PushButton("Add Task")
        self.addTaskButton.clicked.connect(self.addTask)

        inputLayout.addWidget(self.taskInput)
        inputLayout.addWidget(self.addTaskButton)

        # Task list
        self.taskList = QListWidget()
        self.taskList.setSpacing(4)
        self.taskList.setStyleSheet(
            "QListWidget { border: none; background: transparent; }"
            "QListWidgetItem { padding: 8px; }"
        )

        pageLayout.addLayout(inputLayout)
        pageLayout.addWidget(self.taskList)

        return page

    def addTask(self):
        text = self.taskInput.text().strip()
        if not text:
            return

        item = QListWidgetItem()
        self.taskList.addItem(item)

        # Row widget with checkbox label and delete button
        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        rowLayout.setContentsMargins(4, 4, 4, 4)
        rowLayout.setSpacing(8)

        taskLabel = QLabel(text)
        taskFont = QFont()
        taskFont.setPointSize(10)
        taskLabel.setFont(taskFont)

        deleteButton = QPushButton("✕")
        deleteButton.setFixedSize(24, 24)
        deleteButton.setFlat(True)
        deleteButton.setCursor(Qt.CursorShape.PointingHandCursor)
        deleteButton.setStyleSheet(
            "QPushButton { color: #888; border: none; background: transparent; font-size: 12px; }"
            "QPushButton:hover { color: #FF5555; }"
        )

        # Capture item reference for deletion
        def makeDeleteHandler(i):
            def handler():
                row = self.taskList.row(i)
                self.taskList.takeItem(row)
            return handler

        deleteButton.clicked.connect(makeDeleteHandler(item))

        rowLayout.addWidget(taskLabel)
        rowLayout.addStretch()
        rowLayout.addWidget(deleteButton)

        item.setSizeHint(rowWidget.sizeHint())
        self.taskList.setItemWidget(item, rowWidget)

        self.taskInput.clear()

    def createMilestonesTab(self):
        page = CardWidget()

        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        inputLayout = QHBoxLayout()
        inputLayout.setContentsMargins(0, 0, 0, 0)
        inputLayout.setSpacing(8)

        self.milestoneInput = LineEdit()
        self.milestoneInput.setPlaceholderText("Add a new milestone...")

        self.addMilestoneButton = PushButton("Add Milestone")

        inputLayout.addWidget(self.milestoneInput)
        inputLayout.addWidget(self.addMilestoneButton)

        self.milestoneList = QListWidget()
        self.milestoneList.setSpacing(4)
        self.milestoneList.setStyleSheet(
            "QListWidget { border: none; background: transparent; }"
        )

        pageLayout.addLayout(inputLayout)
        pageLayout.addWidget(self.milestoneList)

        return page

    def createPlaceholderTab(self, message):
        page = CardWidget()

        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(10)

        label = BodyLabel(message)
        pageLayout.addWidget(label)
        pageLayout.addStretch()

        return page

    def setActiveTab(self, index):
        self.contentStack.setCurrentIndex(index)
        for i, button in enumerate(self.tabButtons):
            button.setChecked(i == index)
        self.applyThemeColors()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.Type.PaletteChange, QEvent.Type.StyleChange):
            if hasattr(self, "contentStack"):
                currentIndex = self.contentStack.currentIndex()
                self.applyThemeColors()
                self.setActiveTab(currentIndex)

    def showEvent(self, event):
        super().showEvent(event)
        self.applyThemeColors()

    def goBackToProjects(self):
        mainWindow = self.window()
        if hasattr(mainWindow, "switchTo") and hasattr(mainWindow, "projectPage"):
            mainWindow.switchTo(mainWindow.projectPage)

    def setProject(self, project):
        self.project = project
        self.projectTitle.setText(project.title)
        self.projectDescription.setText(project.description)
'''
'''
### Project View Page 
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QCheckBox,
    QFileDialog,
    QGridLayout,
    QScrollArea,
    QDateEdit,
    QLineEdit,
)
from PyQt6.QtCore import QEvent, Qt, QDate
from PyQt6.QtGui import QFont, QPixmap
from qfluentwidgets import (
    SubtitleLabel,
    BodyLabel,
    StrongBodyLabel,
    CardWidget,
    PushButton,
    PrimaryPushButton,
    LineEdit,
    isDarkTheme,
)

class projectViewPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("projectViewPage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        # Top section
        topLayout = QHBoxLayout()
        topLayout.setSpacing(12)

        self.backButton = QPushButton("←")
        self.backButton.setToolTip("Back to Projects")
        self.backButton.clicked.connect(self.goBackToProjects)

        backFont = QFont()
        backFont.setPointSize(14)
        backFont.setBold(True)
        self.backButton.setFont(backFont)
        self.backButton.setFixedWidth(24)
        self.backButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backButton.setFlat(True)

        textLayout = QVBoxLayout()
        textLayout.setSpacing(4)
        textLayout.setContentsMargins(0, 0, 0, 0)

        self.projectTitle = SubtitleLabel("Project Title")
        self.projectDescription = BodyLabel("Project Description")
        self.projectDescription.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        textLayout.addWidget(self.projectTitle)
        textLayout.addWidget(self.projectDescription)

        topLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignTop)
        topLayout.addLayout(textLayout)
        topLayout.addStretch()

        layout.addLayout(topLayout)

        # Tab bar
        self.tabsWidget = QFrame()
        self.tabsWidget.setObjectName("tabsWidget")
        self.tabsLayout = QHBoxLayout(self.tabsWidget)
        self.tabsLayout.setSpacing(10)
        self.tabsLayout.setContentsMargins(8, 8, 8, 8)

        self.taskTab = QPushButton("Tasks")
        self.milestonesTab = QPushButton("Milestones")
        self.imagesTab = QPushButton("Images")
        self.exportTab = QPushButton("Export")

        self.tabButtons = [self.taskTab, self.milestonesTab, self.imagesTab, self.exportTab]

        for button in self.tabButtons:
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(42)
            self.tabsLayout.addWidget(button)

        layout.addWidget(self.tabsWidget)

        # Content stack
        self.contentStack = QStackedWidget()

        self.taskPage = self.createTasksTab()
        self.milestonesPage = self.createMilestonesTab()
        self.imagesPage = self.createImagesTab()
        self.exportPage = self.createExportTab()

        self.contentStack.addWidget(self.taskPage)
        self.contentStack.addWidget(self.milestonesPage)
        self.contentStack.addWidget(self.imagesPage)
        self.contentStack.addWidget(self.exportPage)

        layout.addWidget(self.contentStack)
        layout.addStretch()

        self.taskTab.clicked.connect(lambda: self.setActiveTab(0))
        self.milestonesTab.clicked.connect(lambda: self.setActiveTab(1))
        self.imagesTab.clicked.connect(lambda: self.setActiveTab(2))
        self.exportTab.clicked.connect(lambda: self.setActiveTab(3))

        self.setLayout(layout)
        self.applyThemeColors()
        self.setActiveTab(0)

    # ─── Theme ────────────────────────────────────────────────────────────────

    def applyThemeColors(self):
        if isDarkTheme():
            self.backButton.setStyleSheet(
                "QPushButton { color: #FFFFFF; border: none; background: transparent; }"
                "QPushButton:hover { color: #CFCFCF; }"
            )
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget { background-color: #3A3A3A; border-radius: 18px; padding: 2px; }"
            )
            inactiveColor = "#F0F0F0"
            activeText = "#FFFFFF"
            activeBG = "#5A5A5A"
        else:
            self.backButton.setStyleSheet(
                "QPushButton { color: #202020; border: none; background: transparent; }"
                "QPushButton:hover { color: #606060; }"
            )
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget { background-color: #E7E7E7; border-radius: 18px; padding: 2px; }"
            )
            inactiveColor = "#202020"
            activeText = "#202020"
            activeBG = "#FFFFFF"

        for button in self.tabButtons:
            if button.isChecked():
                button.setStyleSheet(
                    f"QPushButton {{ color: {activeText}; background-color: {activeBG}; border: none;"
                    "border-radius: 16px; font-weight: 600; padding: 8px 18px; }"
                )
            else:
                button.setStyleSheet(
                    f"QPushButton {{ color: {inactiveColor}; background-color: transparent; border: none;"
                    "border-radius: 16px; font-weight: 600; padding: 8px 18px; }"
                    "QPushButton:hover { background-color: rgba(255, 255, 255, 0.10); }"
                )

    # ─── Tasks Tab ────────────────────────────────────────────────────────────

    def createTasksTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        # Input row
        inputLayout = QHBoxLayout()
        inputLayout.setSpacing(8)

        self.taskInput = LineEdit()
        self.taskInput.setPlaceholderText("Add a new task...")
        self.taskInput.returnPressed.connect(self.addTask)

        self.addTaskButton = PrimaryPushButton("+")
        self.addTaskButton.setFixedSize(40, 40)
        self.addTaskButton.clicked.connect(self.addTask)

        inputLayout.addWidget(self.taskInput)
        inputLayout.addWidget(self.addTaskButton)

        # Task list
        self.taskList = QListWidget()
        self.taskList.setSpacing(6)
        self.taskList.setStyleSheet(
            "QListWidget { border: none; background: transparent; }"
        )

        pageLayout.addLayout(inputLayout)
        pageLayout.addWidget(self.taskList)

        return page

    def addTask(self):
        text = self.taskInput.text().strip()
        if not text:
            return

        item = QListWidgetItem()
        self.taskList.addItem(item)

        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        rowLayout.setContentsMargins(4, 4, 4, 4)
        rowLayout.setSpacing(10)

        checkbox = QCheckBox(text)
        checkFont = QFont()
        checkFont.setPointSize(10)
        checkbox.setFont(checkFont)

        # Strike through text when checked
        def onChecked(state, cb=checkbox):
            font = cb.font()
            font.setStrikeOut(state == Qt.CheckState.Checked.value)
            cb.setFont(font)

        checkbox.stateChanged.connect(onChecked)

        rowLayout.addWidget(checkbox)
        rowLayout.addStretch()

        item.setSizeHint(rowWidget.sizeHint())
        self.taskList.setItemWidget(item, rowWidget)
        self.taskInput.clear()

    # ─── Milestones Tab ───────────────────────────────────────────────────────

    def createMilestonesTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        inputLayout = QHBoxLayout()
        inputLayout.setSpacing(8)

        self.milestoneInput = LineEdit()
        self.milestoneInput.setPlaceholderText("Milestone title...")
        self.milestoneInput.returnPressed.connect(self.addMilestone)

        self.milestoneDateInput = QDateEdit()
        self.milestoneDateInput.setCalendarPopup(True)
        self.milestoneDateInput.setDate(QDate.currentDate())
        self.milestoneDateInput.setDisplayFormat("MM/dd/yyyy")
        self.milestoneDateInput.setFixedWidth(160)
        self.milestoneDateInput.setStyleSheet(
            "QDateEdit { border: 1px solid #CCCCCC; border-radius: 6px; padding: 6px 10px; font-size: 13px; }"
        )

        self.addMilestoneButton = PrimaryPushButton("+")
        self.addMilestoneButton.setFixedSize(40, 40)
        self.addMilestoneButton.clicked.connect(self.addMilestone)

        inputLayout.addWidget(self.milestoneInput)
        inputLayout.addWidget(self.milestoneDateInput)
        inputLayout.addWidget(self.addMilestoneButton)

        self.milestoneList = QListWidget()
        self.milestoneList.setSpacing(6)
        self.milestoneList.setStyleSheet(
            "QListWidget { border: none; background: transparent; }"
        )

        pageLayout.addLayout(inputLayout)
        pageLayout.addWidget(self.milestoneList)

        return page

    def addMilestone(self):
        text = self.milestoneInput.text().strip()
        if not text:
            return

        date = self.milestoneDateInput.date().toString("yyyy-MM-dd")

        item = QListWidgetItem()
        self.milestoneList.addItem(item)

        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        rowLayout.setContentsMargins(4, 4, 4, 4)
        rowLayout.setSpacing(10)

        checkbox = QCheckBox()

        infoLayout = QVBoxLayout()
        infoLayout.setSpacing(2)

        titleLabel = BodyLabel(text)
        dateLabel = BodyLabel(date)
        dateFont = QFont()
        dateFont.setPointSize(9)
        dateLabel.setFont(dateFont)

        infoLayout.addWidget(titleLabel)
        infoLayout.addWidget(dateLabel)

        rowLayout.addWidget(checkbox)
        rowLayout.addLayout(infoLayout)
        rowLayout.addStretch()

        item.setSizeHint(rowWidget.sizeHint())
        self.milestoneList.setItemWidget(item, rowWidget)
        self.milestoneInput.clear()

    # ─── Images Tab ───────────────────────────────────────────────────────────

    def createImagesTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        # Upload button styled as dashed box
        self.uploadButton = QPushButton("↑\nClick to upload an image")
        self.uploadButton.setFixedSize(180, 120)
        self.uploadButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.uploadButton.setStyleSheet(
            "QPushButton {"
            "border: 2px dashed #AAAAAA;"
            "border-radius: 10px;"
            "color: #888888;"
            "font-size: 12px;"
            "background: transparent;"
            "}"
            "QPushButton:hover { border-color: #555555; color: #555555; }"
        )
        self.uploadButton.clicked.connect(self.uploadImage)

        # Scroll area for the image grid
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.imageGridContainer = QWidget()
        self.imageGrid = QGridLayout(self.imageGridContainer)
        self.imageGrid.setSpacing(16)
        self.imageGrid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Place upload button as first grid cell
        self.imageGrid.addWidget(self.uploadButton, 0, 0)
        self.imageGridCol = 1  # next column to place image
        self.imageGridRow = 0

        scrollArea.setWidget(self.imageGridContainer)

        pageLayout.addWidget(scrollArea)

        self.imagePaths = []

        return page

    def uploadImage(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if not filePath:
            return

        # Ask user for a description
        descDialog = QWidget(self, Qt.WindowType.Dialog)
        descDialog.setWindowTitle("Image Description")
        descDialog.setFixedSize(340, 120)
        dialogLayout = QVBoxLayout(descDialog)

        descInput = QLineEdit()
        descInput.setPlaceholderText("Enter a description for this image...")

        confirmBtn = QPushButton("Add")
        confirmBtn.clicked.connect(lambda: self.confirmImageUpload(filePath, descInput.text().strip(), descDialog))

        dialogLayout.addWidget(QLabel("Description:"))
        dialogLayout.addWidget(descInput)
        dialogLayout.addWidget(confirmBtn)
        descDialog.show()

    def confirmImageUpload(self, filePath, description, dialog):
        dialog.close()

        label = description if description else filePath.split("/")[-1]

        # Thumbnail
        pixmap = QPixmap(filePath).scaled(180, 140, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        cellWidget = QWidget()
        cellLayout = QVBoxLayout(cellWidget)
        cellLayout.setContentsMargins(0, 0, 0, 0)
        cellLayout.setSpacing(6)

        imgLabel = QLabel()
        imgLabel.setPixmap(pixmap)
        imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        nameLabel = BodyLabel(label)
        nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nameLabel.setWordWrap(True)
        nameLabel.setMaximumWidth(180)

        cellLayout.addWidget(imgLabel)
        cellLayout.addWidget(nameLabel)

        # Place in grid (3 columns, upload button always stays at 0,0)
        cols = 3
        pos = len(self.imagePaths) + 1  # offset by 1 for upload button
        row = pos // cols
        col = pos % cols

        self.imageGrid.addWidget(cellWidget, row, col)
        self.imagePaths.append(filePath)

    # ─── Export Tab ───────────────────────────────────────────────────────────

    def createExportTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(20)

        titleLabel = StrongBodyLabel("Project Summary")

        # Summary card
        summaryCard = QFrame()
        summaryCard.setStyleSheet(
            "QFrame { background-color: #EFEFEF; border-radius: 10px; }"
            if not isDarkTheme() else
            "QFrame { background-color: #3A3A3A; border-radius: 10px; }"
        )
        summaryLayout = QVBoxLayout(summaryCard)
        summaryLayout.setContentsMargins(16, 16, 16, 16)
        summaryLayout.setSpacing(8)

        self.summaryProjectLabel = BodyLabel("Project: —")
        self.summaryDescLabel = BodyLabel("Description: —")
        self.summaryTasksLabel = BodyLabel("Tasks: —")
        self.summaryMilestonesLabel = BodyLabel("Milestones: —")
        self.summaryImagesLabel = BodyLabel("Images: —")

        for lbl in [
            self.summaryProjectLabel,
            self.summaryDescLabel,
            self.summaryTasksLabel,
            self.summaryMilestonesLabel,
            self.summaryImagesLabel,
        ]:
            summaryLayout.addWidget(lbl)

        exportLabel = StrongBodyLabel("Export Options")

        self.exportPdfButton = PrimaryPushButton("  Export as PDF")
        self.exportPdfButton.setMinimumHeight(44)
        self.exportPdfButton.clicked.connect(self.exportAsPdf)

        pageLayout.addWidget(titleLabel)
        pageLayout.addWidget(summaryCard)
        pageLayout.addWidget(exportLabel)
        pageLayout.addWidget(self.exportPdfButton)
        pageLayout.addStretch()

        return page

    def refreshExportSummary(self):
        if not hasattr(self, "project"):
            return

        taskCount = self.taskList.count()
        checkedTasks = sum(
            1 for i in range(taskCount)
            if (w := self.taskList.itemWidget(self.taskList.item(i))) and
               w.findChild(QCheckBox) and w.findChild(QCheckBox).isChecked()
        )

        milestoneCount = self.milestoneList.count()
        checkedMilestones = sum(
            1 for i in range(milestoneCount)
            if (w := self.milestoneList.itemWidget(self.milestoneList.item(i))) and
               w.findChild(QCheckBox) and w.findChild(QCheckBox).isChecked()
        )

        imageCount = len(self.imagePaths)

        self.summaryProjectLabel.setText(f"Project: {self.project.title}")
        self.summaryDescLabel.setText(f"Description: {self.project.description}")
        self.summaryTasksLabel.setText(f"Tasks: {checkedTasks} / {taskCount} completed")
        self.summaryMilestonesLabel.setText(f"Milestones: {checkedMilestones} / {milestoneCount} achieved")
        self.summaryImagesLabel.setText(f"Images: {imageCount}")

    def exportAsPdf(self):
        if not hasattr(self, "project"):
            return

        filePath, _ = QFileDialog.getSaveFileName(self, "Export as PDF", f"{self.project.title}.pdf", "PDF Files (*.pdf)")
        if not filePath:
            return

        from PyQt6.QtGui import QPainter, QPageSize
        from PyQt6.QtPrintSupport import QPrinter

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(filePath)
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))

        painter = QPainter(printer)
        self.exportPage.render(painter)
        painter.end()

    # ─── Tab switching ────────────────────────────────────────────────────────

    def setActiveTab(self, index):
        self.contentStack.setCurrentIndex(index)
        for i, button in enumerate(self.tabButtons):
            button.setChecked(i == index)
        if index == 3:
            self.refreshExportSummary()
        self.applyThemeColors()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.Type.PaletteChange, QEvent.Type.StyleChange):
            if hasattr(self, "contentStack"):
                currentIndex = self.contentStack.currentIndex()
                self.applyThemeColors()
                self.setActiveTab(currentIndex)

    def showEvent(self, event):
        super().showEvent(event)
        self.applyThemeColors()

    # ─── Navigation / project binding ─────────────────────────────────────────

    def goBackToProjects(self):
        mainWindow = self.window()
        if hasattr(mainWindow, "switchTo") and hasattr(mainWindow, "projectPage"):
            mainWindow.switchTo(mainWindow.projectPage)

    def setProject(self, project):
        self.project = project
        self.projectTitle.setText(project.title)
        self.projectDescription.setText(project.description)

        # Clear tasks
        self.taskList.clear()

        # Clear milestones
        self.milestoneList.clear()

        # Clear images
        self.imagePaths = []
        # Remove all grid items except the upload button (index 0)
        while self.imageGrid.count() > 1:
            item = self.imageGrid.takeAt(1)
            if item.widget():
                item.widget().deleteLater()

        # Reset export summary
        self.summaryProjectLabel.setText(f"Project: {project.title}")
        self.summaryDescLabel.setText(f"Description: {project.description}")
        self.summaryTasksLabel.setText("Tasks: 0 / 0 completed")
        self.summaryMilestonesLabel.setText("Milestones: 0 / 0 achieved")
        self.summaryImagesLabel.setText("Images: 0")
'''
'''
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QCheckBox,
    QFileDialog,
    QGridLayout,
    QScrollArea,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QLineEdit,
)

from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import QEvent, Qt, QDate
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPageSize
from qfluentwidgets import (
    SubtitleLabel,
    BodyLabel,
    StrongBodyLabel,
    CardWidget,
    PushButton,
    PrimaryPushButton,
    LineEdit,
    InfoBar,
    InfoBarPosition,
    isDarkTheme,
)
from classes.Task import Task
from classes.Milestone import Milestone
from classes.Media import Media
from datetime import datetime


class projectViewPage(QWidget):
    def __init__(self):
        super().__init__()

        self.project = None
        self.setObjectName("projectViewPage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        # Top section
        topLayout = QHBoxLayout()
        topLayout.setSpacing(12)

        self.backButton = QPushButton("←")
        self.backButton.setToolTip("Back to Projects")
        self.backButton.clicked.connect(self.goBackToProjects)

        backFont = QFont()
        backFont.setPointSize(14)
        backFont.setBold(True)
        self.backButton.setFont(backFont)
        self.backButton.setFixedWidth(24)
        self.backButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backButton.setFlat(True)

        textLayout = QVBoxLayout()
        textLayout.setSpacing(4)
        textLayout.setContentsMargins(0, 0, 0, 0)

        self.projectTitle = SubtitleLabel("Project Title")
        self.projectDescription = BodyLabel("Project Description")
        self.projectDescription.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        textLayout.addWidget(self.projectTitle)
        textLayout.addWidget(self.projectDescription)

        topLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignTop)
        topLayout.addLayout(textLayout)
        topLayout.addStretch()
        layout.addLayout(topLayout)

        # Tab bar
        self.tabsWidget = QFrame()
        self.tabsWidget.setObjectName("tabsWidget")
        self.tabsLayout = QHBoxLayout(self.tabsWidget)
        self.tabsLayout.setSpacing(10)
        self.tabsLayout.setContentsMargins(8, 8, 8, 8)

        self.taskTab = QPushButton("Tasks")
        self.milestonesTab = QPushButton("Milestones")
        self.imagesTab = QPushButton("Images")
        self.exportTab = QPushButton("Export")

        self.tabButtons = [self.taskTab, self.milestonesTab, self.imagesTab, self.exportTab]

        for button in self.tabButtons:
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(42)
            self.tabsLayout.addWidget(button)

        layout.addWidget(self.tabsWidget)

        # Content stack
        self.contentStack = QStackedWidget()

        self.taskPage = self.createTasksTab()
        self.milestonesPage = self.createMilestonesTab()
        self.imagesPage = self.createImagesTab()
        self.exportPage = self.createExportTab()

        self.contentStack.addWidget(self.taskPage)
        self.contentStack.addWidget(self.milestonesPage)
        self.contentStack.addWidget(self.imagesPage)
        self.contentStack.addWidget(self.exportPage)

        layout.addWidget(self.contentStack)
        layout.addStretch()

        self.taskTab.clicked.connect(lambda: self.setActiveTab(0))
        self.milestonesTab.clicked.connect(lambda: self.setActiveTab(1))
        self.imagesTab.clicked.connect(lambda: self.setActiveTab(2))
        self.exportTab.clicked.connect(lambda: self.setActiveTab(3))

        self.setLayout(layout)
        self.applyThemeColors()
        self.setActiveTab(0)

    def applyThemeColors(self):
        if isDarkTheme():
            self.backButton.setStyleSheet(
                "QPushButton { color: #FFFFFF; border: none; background: transparent; }"
                "QPushButton:hover { color: #CFCFCF; }"
            )
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget { background-color: #3A3A3A; border-radius: 18px; padding: 2px; }"
            )
            inactiveColor = "#F0F0F0"
            activeText = "#FFFFFF"
            activeBG = "#5A5A5A"
        else:
            self.backButton.setStyleSheet(
                "QPushButton { color: #202020; border: none; background: transparent; }"
                "QPushButton:hover { color: #606060; }"
            )
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget { background-color: #E7E7E7; border-radius: 18px; padding: 2px; }"
            )
            inactiveColor = "#202020"
            activeText = "#202020"
            activeBG = "#FFFFFF"

        for button in self.tabButtons:
            if button.isChecked():
                button.setStyleSheet(
                    f"QPushButton {{ color: {activeText}; background-color: {activeBG}; border: none;"
                    "border-radius: 16px; font-weight: 600; padding: 8px 18px; }"
                )
            else:
                button.setStyleSheet(
                    f"QPushButton {{ color: {inactiveColor}; background-color: transparent; border: none;"
                    "border-radius: 16px; font-weight: 600; padding: 8px 18px; }"
                    "QPushButton:hover { background-color: rgba(255, 255, 255, 0.10); }"
                )
        if hasattr(self, "summaryCard"):
            self.summaryCard.setStyleSheet(
                "QFrame { background-color: #3A3A3A; border-radius: 10px; }"
                if isDarkTheme() else
                "QFrame { background-color: #EFEFEF; border-radius: 10px; }"
            )

    def createTasksTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        inputLayout = QHBoxLayout()
        inputLayout.setSpacing(8)

        self.taskInput = LineEdit()
        self.taskInput.setPlaceholderText("Add a new task...")
        self.taskInput.returnPressed.connect(self.addTask)

        self.addTaskButton = PrimaryPushButton("+")
        self.addTaskButton.setFixedSize(40, 40)
        self.addTaskButton.clicked.connect(self.addTask)

        inputLayout.addWidget(self.taskInput)
        inputLayout.addWidget(self.addTaskButton)

        self.taskList = QListWidget()
        self.taskList.setSpacing(6)
        self.taskList.setStyleSheet("QListWidget { border: none; background: transparent; }")

        pageLayout.addLayout(inputLayout)
        pageLayout.addWidget(self.taskList)

        return page

    def addTask(self):
        if not self.project:
            return

        text = self.taskInput.text().strip()
        if not text:
            return

        try:
            task = Task(
                name=text,
                description="",
                deadline=self.project.deadline,
                estimatedTime=0,
            )
            self.project.addTask(task)
            self.renderTask(task)
            self.taskInput.clear()
        except Exception as e:
            InfoBar.warning(
                title="Couldn't add task",
                content=str(e),
                parent=self,
                duration=3000,
                position=InfoBarPosition.TOP,
            )

    def renderTask(self, task: Task):
        item = QListWidgetItem()
        self.taskList.addItem(item)

        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        rowLayout.setContentsMargins(4, 4, 4, 4)
        rowLayout.setSpacing(10)

        checkbox = QCheckBox(task.name)
        checkFont = QFont()
        checkFont.setPointSize(10)
        checkbox.setFont(checkFont)
        checkbox.setChecked(task.dateCompleted is not None)

        def onChecked(state, t=task, cb=checkbox):
            font = cb.font()
            if state == Qt.CheckState.Checked.value:
                t.markComplete()
                font.setStrikeOut(True)
            else:
                t.dateCompleted = None
                font.setStrikeOut(False)
            cb.setFont(font)

        checkbox.stateChanged.connect(onChecked)

        if task.dateCompleted:
            font = checkbox.font()
            font.setStrikeOut(True)
            checkbox.setFont(font)

        rowLayout.addWidget(checkbox)
        rowLayout.addStretch()

        item.setSizeHint(rowWidget.sizeHint())
        self.taskList.setItemWidget(item, rowWidget)


    def createMilestonesTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        inputLayout = QHBoxLayout()
        inputLayout.setSpacing(8)

        self.milestoneInput = LineEdit()
        self.milestoneInput.setPlaceholderText("Milestone title...")
        self.milestoneInput.returnPressed.connect(self.addMilestone)

        self.milestoneDateInput = QDateEdit()
        self.milestoneDateInput.setCalendarPopup(True)
        self.milestoneDateInput.setDate(QDate.currentDate())
        self.milestoneDateInput.setDisplayFormat("MM/dd/yyyy")
        self.milestoneDateInput.setFixedWidth(160)
        self.milestoneDateInput.setStyleSheet(
            "QDateEdit { border: 1px solid #CCCCCC; border-radius: 6px; padding: 6px 10px; font-size: 13px; }"
        )

        self.addMilestoneButton = PrimaryPushButton("+")
        self.addMilestoneButton.setFixedSize(40, 40)
        self.addMilestoneButton.clicked.connect(self.addMilestone)

        inputLayout.addWidget(self.milestoneInput)
        inputLayout.addWidget(self.milestoneDateInput)
        inputLayout.addWidget(self.addMilestoneButton)

        self.milestoneList = QListWidget()
        self.milestoneList.setSpacing(6)
        self.milestoneList.setStyleSheet("QListWidget { border: none; background: transparent; }")

        pageLayout.addLayout(inputLayout)
        pageLayout.addWidget(self.milestoneList)

        return page

    def addMilestone(self):
        if not self.project:
            return

        text = self.milestoneInput.text().strip()
        if not text:
            return

        qdate = self.milestoneDateInput.date()
        deadline = datetime(qdate.year(), qdate.month(), qdate.day())

        try:
            milestone = Milestone(name=text, deadline=deadline)
            self.project.addMilestone(milestone)
            self.renderMilestone(milestone)
            self.milestoneInput.clear()
        except Exception as e:
            InfoBar.warning(
                title="Couldn't add milestone",
                content=str(e),
                parent=self,
                duration=3000,
                position=InfoBarPosition.TOP,
            )

    def renderMilestone(self, milestone: Milestone):
        item = QListWidgetItem()
        self.milestoneList.addItem(item)

        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        rowLayout.setContentsMargins(4, 4, 4, 4)
        rowLayout.setSpacing(10)

        checkbox = QCheckBox()
        checkbox.setChecked(milestone.isReached())

        def onChecked(state, m=milestone):
            if state == Qt.CheckState.Checked.value:
                m.markComplete()

        checkbox.stateChanged.connect(onChecked)

        infoLayout = QVBoxLayout()
        infoLayout.setSpacing(2)

        titleLabel = BodyLabel(milestone.name)
        dateLabel = BodyLabel(milestone.deadline.strftime("%Y-%m-%d"))
        smallFont = QFont()
        smallFont.setPointSize(9)
        dateLabel.setFont(smallFont)

        infoLayout.addWidget(titleLabel)
        infoLayout.addWidget(dateLabel)

        rowLayout.addWidget(checkbox)
        rowLayout.addLayout(infoLayout)
        rowLayout.addStretch()

        item.setSizeHint(rowWidget.sizeHint())
        self.milestoneList.setItemWidget(item, rowWidget)

    def createImagesTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        self.uploadButton = QPushButton("↑\nClick to upload an image")
        self.uploadButton.setFixedSize(180, 120)
        self.uploadButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.uploadButton.setStyleSheet(
            "QPushButton { border: 2px dashed #AAAAAA; border-radius: 10px;"
            "color: #888888; font-size: 12px; background: transparent; }"
            "QPushButton:hover { border-color: #555555; color: #555555; }"
        )
        self.uploadButton.clicked.connect(self.uploadImage)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.imageGridContainer = QWidget()
        self.imageGrid = QGridLayout(self.imageGridContainer)
        self.imageGrid.setSpacing(16)
        self.imageGrid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.imageGrid.addWidget(self.uploadButton, 0, 0)

        scrollArea.setWidget(self.imageGridContainer)
        pageLayout.addWidget(scrollArea)

        return page

    def uploadImage(self):
        if not self.project:
            return

        filePath, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if not filePath:
            return

        # Description dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Image Description")
        dialog.setFixedSize(360, 130)
        dialogLayout = QVBoxLayout(dialog)

        descInput = QLineEdit()
        descInput.setPlaceholderText("Enter a description for this image...")

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        dialogLayout.addWidget(QLabel("Description (optional):"))
        dialogLayout.addWidget(descInput)
        dialogLayout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        description = descInput.text().strip()

        try:
            media = Media(filePath=filePath, description=description)
            media.upload(self.project.projectId)
            self.project.addMedia(media)
            self.renderImage(media)
        except Exception as e:
            InfoBar.warning(
                title="Couldn't add image",
                content=str(e),
                parent=self,
                duration=3000,
                position=InfoBarPosition.TOP,
            )

    def renderImage(self, media: Media):
        pixmap = media.getPixmap().scaled(
            180, 140,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        cellWidget = QWidget()
        cellLayout = QVBoxLayout(cellWidget)
        cellLayout.setContentsMargins(0, 0, 0, 0)
        cellLayout.setSpacing(6)

        imgLabel = QLabel()
        imgLabel.setPixmap(pixmap)
        imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = media.description if media.description else media.filePath.split("/")[-1]
        nameLabel = BodyLabel(label)
        nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nameLabel.setWordWrap(True)
        nameLabel.setMaximumWidth(180)

        cellLayout.addWidget(imgLabel)
        cellLayout.addWidget(nameLabel)

        # Position after upload button (slot 0)
        count = len(self.project.media)
        cols = 3
        pos = count  # media was already appended, so count = index + 1
        row = pos // cols
        col = pos % cols

        # Shift upload button if it collides
        if row == 0 and col == 0:
            col = 0  # upload button stays at 0,0; offset images by 1
        
        # Always offset by 1 to account for upload button at 0,0
        totalPos = count  # 1-based after upload button
        gridRow = totalPos // cols
        gridCol = totalPos % cols

        self.imageGrid.addWidget(cellWidget, gridRow, gridCol)

    # ─── Export Tab ───────────────────────────────────────────────────────────

    def createExportTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(20)

        titleLabel = StrongBodyLabel("Project Summary")

        self.summaryCard = QFrame()
        self.summaryCard.setStyleSheet(
            "QFrame { background-color: #3A3A3A; border-radius: 10px; }"
            if isDarkTheme() else
            "QFrame { background-color: #EFEFEF; border-radius: 10px; }"
        )
        summaryLayout = QVBoxLayout(self.summaryCard)
        summaryLayout.setContentsMargins(16, 16, 16, 16)
        summaryLayout.setSpacing(8)

        self.summaryProjectLabel = BodyLabel("Project: —")
        self.summaryDescLabel = BodyLabel("Description: —")
        self.summaryTasksLabel = BodyLabel("Tasks: —")
        self.summaryMilestonesLabel = BodyLabel("Milestones: —")
        self.summaryImagesLabel = BodyLabel("Images: —")

        for lbl in [
            self.summaryProjectLabel,
            self.summaryDescLabel,
            self.summaryTasksLabel,
            self.summaryMilestonesLabel,
            self.summaryImagesLabel,
        ]:
            summaryLayout.addWidget(lbl)

        exportLabel = StrongBodyLabel("Export Options")

        self.exportPdfButton = PrimaryPushButton("  Export as PDF")
        self.exportPdfButton.setMinimumHeight(44)
        self.exportPdfButton.clicked.connect(self.exportAsPdf)

        pageLayout.addWidget(titleLabel)
        pageLayout.addWidget(self.summaryCard)
        pageLayout.addWidget(exportLabel)
        pageLayout.addWidget(self.exportPdfButton)
        pageLayout.addStretch()

        return page

    def refreshExportSummary(self):
        if not self.project:
            return

        completedTasks = len(self.project.completedTasks())
        totalTasks = len(self.project.tasks)
        completedMilestones = sum(1 for m in self.project.milestones if m.isReached())
        totalMilestones = len(self.project.milestones)
        totalImages = len(self.project.media)

        self.summaryProjectLabel.setText(f"Project: {self.project.title}")
        self.summaryDescLabel.setText(f"Description: {self.project.description}")
        self.summaryTasksLabel.setText(f"Tasks: {completedTasks} / {totalTasks} completed")
        self.summaryMilestonesLabel.setText(f"Milestones: {completedMilestones} / {totalMilestones} achieved")
        self.summaryImagesLabel.setText(f"Images: {totalImages}")

    def exportAsPdf(self):
        if not self.project:
            return

        filePath, _ = QFileDialog.getSaveFileName(
            self, "Export as PDF", f"{self.project.title}.pdf", "PDF Files (*.pdf)"
        )
        if not filePath:
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(filePath)
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))

        painter = QPainter(printer)
        self.exportPage.render(painter)
        painter.end()

    def setActiveTab(self, index):
        self.contentStack.setCurrentIndex(index)
        for i, button in enumerate(self.tabButtons):
            button.setChecked(i == index)
        if index == 3:
            self.refreshExportSummary()
        self.applyThemeColors()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.Type.PaletteChange, QEvent.Type.StyleChange):
            if hasattr(self, "contentStack"):
                currentIndex = self.contentStack.currentIndex()
                self.applyThemeColors()
                self.setActiveTab(currentIndex)

    def showEvent(self, event):
        super().showEvent(event)
        self.applyThemeColors()

    def goBackToProjects(self):
        mainWindow = self.window()
        if hasattr(mainWindow, "switchTo") and hasattr(mainWindow, "projectPage"):
            mainWindow.switchTo(mainWindow.projectPage)

    def setProject(self, project):
        self.project = project
        self.projectTitle.setText(project.title)
        self.projectDescription.setText(project.description)

        # Reload tasks from model
        self.taskList.clear()
        for task in project.tasks:
            self.renderTask(task)

        # Reload milestones from model
        self.milestoneList.clear()
        for milestone in project.milestones:
            self.renderMilestone(milestone)

        # Reload images from model
        while self.imageGrid.count() > 1:
            item = self.imageGrid.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        for media in project.media:
            self.renderImage(media)

        # Reset to tasks tab
        self.setActiveTab(0)
'''
### Project View Page
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QStackedWidget, QWidget, QVBoxLayout,
    QCheckBox, QFileDialog, QGridLayout, QScrollArea, QDateEdit,
    QDialog, QDialogButtonBox, QLineEdit, QListView,
)
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import QEvent, Qt, QDate
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPageSize
from qfluentwidgets import (
    SubtitleLabel, BodyLabel, StrongBodyLabel, CardWidget,
    PushButton, PrimaryPushButton, LineEdit, InfoBar, InfoBarPosition, isDarkTheme,
)
from classes.Task import Task
from classes.Milestone import Milestone
from classes.Media import Media
from datetime import datetime


class projectViewPage(QWidget):
    def __init__(self):
        super().__init__()

        self.project = None
        self.setObjectName("projectViewPage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        topLayout = QHBoxLayout()
        topLayout.setSpacing(12)

        self.backButton = QPushButton("←")
        self.backButton.setToolTip("Back to Projects")
        self.backButton.clicked.connect(self.goBackToProjects)
        backFont = QFont()
        backFont.setPointSize(14)
        backFont.setBold(True)
        self.backButton.setFont(backFont)
        self.backButton.setFixedWidth(24)
        self.backButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backButton.setFlat(True)

        textLayout = QVBoxLayout()
        textLayout.setSpacing(4)
        textLayout.setContentsMargins(0, 0, 0, 0)

        self.projectTitle = SubtitleLabel("Project Title")
        self.projectDescription = BodyLabel("Project Description")
        self.projectDescription.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        textLayout.addWidget(self.projectTitle)
        textLayout.addWidget(self.projectDescription)

        topLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignTop)
        topLayout.addLayout(textLayout)
        topLayout.addStretch()
        layout.addLayout(topLayout)

        self.tabsWidget = QFrame()
        self.tabsWidget.setObjectName("tabsWidget")
        self.tabsLayout = QHBoxLayout(self.tabsWidget)
        self.tabsLayout.setSpacing(10)
        self.tabsLayout.setContentsMargins(8, 8, 8, 8)

        self.taskTab = QPushButton("Tasks")
        self.milestonesTab = QPushButton("Milestones")
        self.imagesTab = QPushButton("Images")
        self.exportTab = QPushButton("Export")
        self.tabButtons = [self.taskTab, self.milestonesTab, self.imagesTab, self.exportTab]

        for button in self.tabButtons:
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(42)
            self.tabsLayout.addWidget(button)

        layout.addWidget(self.tabsWidget)

        self.contentStack = QStackedWidget()
        self.taskPage = self.createTasksTab()
        self.milestonesPage = self.createMilestonesTab()
        self.imagesPage = self.createImagesTab()
        self.exportPage = self.createExportTab()

        self.contentStack.addWidget(self.taskPage)
        self.contentStack.addWidget(self.milestonesPage)
        self.contentStack.addWidget(self.imagesPage)
        self.contentStack.addWidget(self.exportPage)

        layout.addWidget(self.contentStack)
        layout.addStretch()

        self.taskTab.clicked.connect(lambda: self.setActiveTab(0))
        self.milestonesTab.clicked.connect(lambda: self.setActiveTab(1))
        self.imagesTab.clicked.connect(lambda: self.setActiveTab(2))
        self.exportTab.clicked.connect(lambda: self.setActiveTab(3))

        self.setLayout(layout)
        self.applyThemeColors()
        self.setActiveTab(0)

    # ─── Theme ────────────────────────────────────────────────────────────────

    def applyThemeColors(self):
        if isDarkTheme():
            self.backButton.setStyleSheet(
                "QPushButton { color: #FFFFFF; border: none; background: transparent; }"
                "QPushButton:hover { color: #CFCFCF; }"
            )
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget { background-color: #3A3A3A; border-radius: 18px; padding: 2px; }"
            )
            inactiveColor = "#F0F0F0"
            activeText = "#FFFFFF"
            activeBG = "#5A5A5A"
        else:
            self.backButton.setStyleSheet(
                "QPushButton { color: #202020; border: none; background: transparent; }"
                "QPushButton:hover { color: #606060; }"
            )
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget { background-color: #E7E7E7; border-radius: 18px; padding: 2px; }"
            )
            inactiveColor = "#202020"
            activeText = "#202020"
            activeBG = "#FFFFFF"

        for button in self.tabButtons:
            if button.isChecked():
                button.setStyleSheet(
                    f"QPushButton {{ color: {activeText}; background-color: {activeBG}; border: none;"
                    "border-radius: 16px; font-weight: 600; padding: 8px 18px; }"
                )
            else:
                button.setStyleSheet(
                    f"QPushButton {{ color: {inactiveColor}; background-color: transparent; border: none;"
                    "border-radius: 16px; font-weight: 600; padding: 8px 18px; }"
                    "QPushButton:hover { background-color: rgba(255, 255, 255, 0.10); }"
                )

        if hasattr(self, "summaryCard"):
            self.summaryCard.setStyleSheet(
                "QFrame { background-color: #3A3A3A; border-radius: 10px; }"
                if isDarkTheme() else
                "QFrame { background-color: #EFEFEF; border-radius: 10px; }"
            )

    # ─── Tasks Tab ────────────────────────────────────────────────────────────

    def createTasksTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        inputLayout = QHBoxLayout()
        inputLayout.setSpacing(8)

        self.taskInput = LineEdit()
        self.taskInput.setPlaceholderText("Add a new task...")
        self.taskInput.returnPressed.connect(self.addTask)

        self.addTaskButton = PrimaryPushButton("+")
        self.addTaskButton.setFixedSize(40, 40)
        self.addTaskButton.clicked.connect(self.addTask)

        inputLayout.addWidget(self.taskInput)
        inputLayout.addWidget(self.addTaskButton)

        self.taskList = QListWidget()
        self.taskList.setSpacing(6)
        self.taskList.setStyleSheet("QListWidget { border: none; background: transparent; }")

        pageLayout.addLayout(inputLayout)
        pageLayout.addWidget(self.taskList)

        return page

    def addTask(self):
        if not self.project:
            return
        text = self.taskInput.text().strip()
        if not text:
            return
        try:
            task = Task(name=text, description="", deadline=self.project.deadline, estimatedTime=0)
            self.project.addTask(task)
            self.renderTask(task)
            self.taskInput.clear()
        except Exception as e:
            InfoBar.warning(title="Couldn't add task", content=str(e), parent=self,
                            duration=3000, position=InfoBarPosition.TOP)

    def renderTask(self, task: Task):
        item = QListWidgetItem()
        self.taskList.addItem(item)

        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        rowLayout.setContentsMargins(4, 4, 4, 4)
        rowLayout.setSpacing(10)

        checkbox = QCheckBox(task.name)
        checkFont = QFont()
        checkFont.setPointSize(10)
        checkbox.setFont(checkFont)
        checkbox.setChecked(task.dateCompleted is not None)
        if task.dateCompleted:
            font = checkbox.font()
            font.setStrikeOut(True)
            checkbox.setFont(font)

        def onChecked(state, t=task, cb=checkbox):
            font = cb.font()
            try:
                if state == Qt.CheckState.Checked.value:
                    t.markComplete()
                    font.setStrikeOut(True)
                else:
                    t.unmarkComplete()
                    font.setStrikeOut(False)
                cb.setFont(font)
                # Refresh milestones in case any auto-completed
                self.refreshMilestoneList()
            except Exception as e:
                InfoBar.warning(title="Couldn't update task", content=str(e), parent=self,
                                duration=3000, position=InfoBarPosition.TOP)
                cb.blockSignals(True)
                cb.setChecked(not cb.isChecked())
                cb.blockSignals(False)

        checkbox.stateChanged.connect(onChecked)

        # Assign to milestone button
        assignBtn = QPushButton("+ Milestone")
        assignBtn.setFixedHeight(28)
        assignBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        assignBtn.setStyleSheet(
            "QPushButton { border: 1px solid #AAAAAA; border-radius: 6px; padding: 2px 8px; font-size: 11px; background: transparent; }"
            "QPushButton:hover { background: rgba(0,0,0,0.05); }"
        )
        assignBtn.clicked.connect(lambda checked=False, t=task: self.showAssignToMilestoneDialog(t))

        # Show which milestones this task belongs to
        self.taskMilestoneLabel = QLabel()
        self.updateTaskMilestoneLabel(task, self.taskMilestoneLabel)
        self.taskMilestoneLabel.setStyleSheet("color: #888888; font-size: 10px;")

        rightLayout = QVBoxLayout()
        rightLayout.setSpacing(2)
        rightLayout.addWidget(assignBtn)
        rightLayout.addWidget(self.taskMilestoneLabel)

        # Store label ref on task for later refresh
        task._milestoneLabel = self.taskMilestoneLabel

        rowLayout.addWidget(checkbox)
        rowLayout.addStretch()
        rowLayout.addLayout(rightLayout)

        item.setSizeHint(rowWidget.sizeHint())
        self.taskList.setItemWidget(item, rowWidget)

    def updateTaskMilestoneLabel(self, task: Task, label: QLabel):
        if task.milestones:
            names = ", ".join(m.name for m in task.milestones)
            label.setText(f"→ {names}")
        else:
            label.setText("")

    def showAssignToMilestoneDialog(self, task: Task):
        if not self.project.milestones:
            InfoBar.warning(title="No milestones", content="Add a milestone first.",
                            parent=self, duration=3000, position=InfoBarPosition.TOP)
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Assign to Milestone")
        dialog.setFixedSize(320, 300)
        layout = QVBoxLayout(dialog)

        layout.addWidget(QLabel(f"Assign '{task.name}' to:"))

        listWidget = QListWidget()
        for milestone in self.project.milestones:
            item = QListWidgetItem(
                f"{'✓ ' if milestone in task.milestones else ''}{milestone.name} "
                f"({len(milestone.tasks)}/3 tasks)"
            )
            item.setData(Qt.ItemDataRole.UserRole, milestone)
            listWidget.addItem(item)

        layout.addWidget(listWidget)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        selected = listWidget.currentItem()
        if not selected:
            return

        milestone = selected.data(Qt.ItemDataRole.UserRole)

        try:
            if milestone in task.milestones:
                # Already assigned — unassign
                milestone.removeTask(task)
            else:
                milestone.addTask(task)

            # Update the label on the task row
            if hasattr(task, "_milestoneLabel"):
                self.updateTaskMilestoneLabel(task, task._milestoneLabel)

            self.refreshMilestoneList()
        except Exception as e:
            InfoBar.warning(title="Couldn't assign task", content=str(e), parent=self,
                            duration=3000, position=InfoBarPosition.TOP)

    # ─── Milestones Tab ───────────────────────────────────────────────────────

    def createMilestonesTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        inputLayout = QHBoxLayout()
        inputLayout.setSpacing(8)

        self.milestoneInput = LineEdit()
        self.milestoneInput.setPlaceholderText("Milestone title...")
        self.milestoneInput.returnPressed.connect(self.addMilestone)

        self.milestoneDateInput = QDateEdit()
        self.milestoneDateInput.setCalendarPopup(True)
        self.milestoneDateInput.setDate(QDate.currentDate())
        self.milestoneDateInput.setDisplayFormat("MM/dd/yyyy")
        self.milestoneDateInput.setFixedWidth(160)
        self.milestoneDateInput.setStyleSheet(
            "QDateEdit { border: 1px solid #CCCCCC; border-radius: 6px; padding: 6px 10px; font-size: 13px; }"
        )

        self.addMilestoneButton = PrimaryPushButton("+")
        self.addMilestoneButton.setFixedSize(40, 40)
        self.addMilestoneButton.clicked.connect(self.addMilestone)

        inputLayout.addWidget(self.milestoneInput)
        inputLayout.addWidget(self.milestoneDateInput)
        inputLayout.addWidget(self.addMilestoneButton)

        self.milestoneList = QListWidget()
        self.milestoneList.setSpacing(6)
        self.milestoneList.setStyleSheet("QListWidget { border: none; background: transparent; }")

        pageLayout.addLayout(inputLayout)
        pageLayout.addWidget(self.milestoneList)

        return page

    def addMilestone(self):
        if not self.project:
            return
        text = self.milestoneInput.text().strip()
        if not text:
            return
        qdate = self.milestoneDateInput.date()
        deadline = datetime(qdate.year(), qdate.month(), qdate.day())
        try:
            milestone = Milestone(name=text, deadline=deadline)
            self.project.addMilestone(milestone)
            self.renderMilestone(milestone)
            self.milestoneInput.clear()
        except Exception as e:
            InfoBar.warning(title="Couldn't add milestone", content=str(e), parent=self,
                            duration=3000, position=InfoBarPosition.TOP)

    def renderMilestone(self, milestone: Milestone):
        item = QListWidgetItem()
        self.milestoneList.addItem(item)

        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        rowLayout.setContentsMargins(4, 4, 4, 4)
        rowLayout.setSpacing(10)

        checkbox = QCheckBox()
        checkbox.setChecked(milestone.isReached())

        def onChecked(state, m=milestone):
            if state == Qt.CheckState.Checked.value:
                m.markComplete()
            else:
                m.unmarkComplete()
            self.refreshMilestoneList()

        checkbox.stateChanged.connect(onChecked)

        infoLayout = QVBoxLayout()
        infoLayout.setSpacing(2)

        titleLabel = BodyLabel(milestone.name)
        dateLabel = BodyLabel(milestone.deadline.strftime("%Y-%m-%d"))
        smallFont = QFont()
        smallFont.setPointSize(9)
        dateLabel.setFont(smallFont)

        # Show linked tasks
        taskNames = ", ".join(t.name for t in milestone.tasks) if milestone.tasks else "No tasks linked"
        tasksLabel = QLabel(f"Tasks: {taskNames}")
        tasksLabel.setStyleSheet("color: #888888; font-size: 10px;")

        # Progress
        progressLabel = QLabel(f"{milestone.getProgress():.0f}% complete")
        progressLabel.setStyleSheet("color: #888888; font-size: 10px;")

        infoLayout.addWidget(titleLabel)
        infoLayout.addWidget(dateLabel)
        infoLayout.addWidget(tasksLabel)
        infoLayout.addWidget(progressLabel)

        # Assign tasks button
        assignBtn = QPushButton("+ Tasks")
        assignBtn.setFixedHeight(28)
        assignBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        assignBtn.setStyleSheet(
            "QPushButton { border: 1px solid #AAAAAA; border-radius: 6px; padding: 2px 8px; font-size: 11px; background: transparent; }"
            "QPushButton:hover { background: rgba(0,0,0,0.05); }"
        )
        assignBtn.clicked.connect(lambda checked=False, m=milestone: self.showAssignTasksDialog(m))

        rowLayout.addWidget(checkbox)
        rowLayout.addLayout(infoLayout)
        rowLayout.addStretch()
        rowLayout.addWidget(assignBtn, alignment=Qt.AlignmentFlag.AlignTop)

        item.setSizeHint(rowWidget.sizeHint())
        self.milestoneList.setItemWidget(item, rowWidget)

    def showAssignTasksDialog(self, milestone: Milestone):
        if not self.project.tasks:
            InfoBar.warning(title="No tasks", content="Add tasks first.",
                            parent=self, duration=3000, position=InfoBarPosition.TOP)
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Assign Tasks to Milestone")
        dialog.setFixedSize(360, 320)
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(f"Select tasks for '{milestone.name}' (max 3):"))

        checkboxes = []
        for task in self.project.tasks:
            cb = QCheckBox(task.name)
            cb.setChecked(task in milestone.tasks)
            cb.setProperty("task", task)
            checkboxes.append(cb)
            layout.addWidget(cb)

        layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        # Apply changes
        for cb in checkboxes:
            task = cb.property("task")
            shouldBeLinked = cb.isChecked()
            isLinked = task in milestone.tasks

            try:
                if shouldBeLinked and not isLinked:
                    milestone.addTask(task)
                elif not shouldBeLinked and isLinked:
                    milestone.removeTask(task)
            except Exception as e:
                InfoBar.warning(title="Couldn't update", content=str(e), parent=self,
                                duration=3000, position=InfoBarPosition.TOP)

        # Refresh both lists so labels update everywhere
        self.refreshMilestoneList()
        self.refreshTaskList()

    def refreshMilestoneList(self):
        self.milestoneList.clear()
        if self.project:
            for milestone in self.project.milestones:
                self.renderMilestone(milestone)

    def refreshTaskList(self):
        self.taskList.clear()
        if self.project:
            for task in self.project.tasks:
                self.renderTask(task)

    # ─── Images Tab ───────────────────────────────────────────────────────────

    def createImagesTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        self.uploadButton = QPushButton("↑\nClick to upload an image")
        self.uploadButton.setFixedSize(180, 120)
        self.uploadButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.uploadButton.setStyleSheet(
            "QPushButton { border: 2px dashed #AAAAAA; border-radius: 10px;"
            "color: #888888; font-size: 12px; background: transparent; }"
            "QPushButton:hover { border-color: #555555; color: #555555; }"
        )
        self.uploadButton.clicked.connect(self.uploadImage)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.imageGridContainer = QWidget()
        self.imageGrid = QGridLayout(self.imageGridContainer)
        self.imageGrid.setSpacing(16)
        self.imageGrid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.imageGrid.addWidget(self.uploadButton, 0, 0)

        scrollArea.setWidget(self.imageGridContainer)
        pageLayout.addWidget(scrollArea)

        return page

    def uploadImage(self):
        if not self.project:
            return
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if not filePath:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Image Description")
        dialog.setFixedSize(360, 130)
        dialogLayout = QVBoxLayout(dialog)
        descInput = QLineEdit()
        descInput.setPlaceholderText("Enter a description for this image...")
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialogLayout.addWidget(QLabel("Description (optional):"))
        dialogLayout.addWidget(descInput)
        dialogLayout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            media = Media(filePath=filePath, description=descInput.text().strip())
            media.upload(self.project.projectId)
            self.project.addMedia(media)
            self.renderImage(media)
        except Exception as e:
            InfoBar.warning(title="Couldn't add image", content=str(e), parent=self,
                            duration=3000, position=InfoBarPosition.TOP)

    def renderImage(self, media: Media):
        pixmap = media.getPixmap().scaled(180, 140, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
        cellWidget = QWidget()
        cellLayout = QVBoxLayout(cellWidget)
        cellLayout.setContentsMargins(0, 0, 0, 0)
        cellLayout.setSpacing(6)

        imgLabel = QLabel()
        imgLabel.setPixmap(pixmap)
        imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = media.description if media.description else media.filePath.split("/")[-1]
        nameLabel = BodyLabel(label)
        nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nameLabel.setWordWrap(True)
        nameLabel.setMaximumWidth(180)

        cellLayout.addWidget(imgLabel)
        cellLayout.addWidget(nameLabel)

        count = len(self.project.media)
        cols = 3
        gridRow = count // cols
        gridCol = count % cols
        self.imageGrid.addWidget(cellWidget, gridRow, gridCol)

    # ─── Export Tab ───────────────────────────────────────────────────────────

    def createExportTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(20)

        titleLabel = StrongBodyLabel("Project Summary")

        self.summaryCard = QFrame()
        self.summaryCard.setStyleSheet(
            "QFrame { background-color: #3A3A3A; border-radius: 10px; }"
            if isDarkTheme() else
            "QFrame { background-color: #EFEFEF; border-radius: 10px; }"
        )
        summaryLayout = QVBoxLayout(self.summaryCard)
        summaryLayout.setContentsMargins(16, 16, 16, 16)
        summaryLayout.setSpacing(8)

        self.summaryProjectLabel = BodyLabel("Project: —")
        self.summaryDescLabel = BodyLabel("Description: —")
        self.summaryTasksLabel = BodyLabel("Tasks: —")
        self.summaryMilestonesLabel = BodyLabel("Milestones: —")
        self.summaryImagesLabel = BodyLabel("Images: —")

        for lbl in [self.summaryProjectLabel, self.summaryDescLabel,
                    self.summaryTasksLabel, self.summaryMilestonesLabel, self.summaryImagesLabel]:
            summaryLayout.addWidget(lbl)

        exportLabel = StrongBodyLabel("Export Options")
        self.exportPdfButton = PrimaryPushButton("  Export as PDF")
        self.exportPdfButton.setMinimumHeight(44)
        self.exportPdfButton.clicked.connect(self.exportAsPdf)

        pageLayout.addWidget(titleLabel)
        pageLayout.addWidget(self.summaryCard)
        pageLayout.addWidget(exportLabel)
        pageLayout.addWidget(self.exportPdfButton)
        pageLayout.addStretch()

        return page

    def refreshExportSummary(self):
        if not self.project:
            return
        self.summaryProjectLabel.setText(f"Project: {self.project.title}")
        self.summaryDescLabel.setText(f"Description: {self.project.description}")
        self.summaryTasksLabel.setText(
            f"Tasks: {len(self.project.completedTasks())} / {len(self.project.tasks)} completed"
        )
        self.summaryMilestonesLabel.setText(
            f"Milestones: {sum(1 for m in self.project.milestones if m.isReached())} / {len(self.project.milestones)} achieved"
        )
        self.summaryImagesLabel.setText(f"Images: {len(self.project.media)}")

    def exportAsPdf(self):
        if not self.project:
            return
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Export as PDF", f"{self.project.title}.pdf", "PDF Files (*.pdf)"
        )
        if not filePath:
            return
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(filePath)
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        painter = QPainter(printer)
        self.exportPage.render(painter)
        painter.end()

    # ─── Tab switching ────────────────────────────────────────────────────────

    def setActiveTab(self, index):
        self.contentStack.setCurrentIndex(index)
        for i, button in enumerate(self.tabButtons):
            button.setChecked(i == index)
        if index == 3:
            self.refreshExportSummary()
        self.applyThemeColors()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.Type.PaletteChange, QEvent.Type.StyleChange):
            if hasattr(self, "contentStack"):
                currentIndex = self.contentStack.currentIndex()
                self.applyThemeColors()
                self.setActiveTab(currentIndex)

    def showEvent(self, event):
        super().showEvent(event)
        self.applyThemeColors()

    # ─── Navigation ───────────────────────────────────────────────────────────

    def goBackToProjects(self):
        mainWindow = self.window()
        if hasattr(mainWindow, "switchTo") and hasattr(mainWindow, "projectPage"):
            mainWindow.switchTo(mainWindow.projectPage)

    def setProject(self, project):
        self.project = project
        self.projectTitle.setText(project.title)
        self.projectDescription.setText(project.description)

        self.taskList.clear()
        for task in project.tasks:
            self.renderTask(task)

        self.milestoneList.clear()
        for milestone in project.milestones:
            self.renderMilestone(milestone)

        while self.imageGrid.count() > 1:
            item = self.imageGrid.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        for media in project.media:
            self.renderImage(media)

        self.setActiveTab(0)