from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from qfluentwidgets import (
    BodyLabel, CardWidget, SubtitleLabel, TitleLabel, PrimaryPushButton, 
    HorizontalSeparator, IconWidget, InfoBar, InfoBarPosition, PushButton
)
from qfluentwidgets import FluentIcon as FIF
from components.widgets import createFeatureCard
from components.projectMessageBox import NewProjectDialog
from classes.Hobbyist import Hobbyist
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
    def __init__(self, hobbyist: Hobbyist):
        super().__init__()
        self.hobbyist = hobbyist
        self.setObjectName("projectPage")
        
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        outer.setContentsMargins(40, 0, 40, 0) 

        container = QWidget()
        container.setMaximumWidth(1000)
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        mainLayout = QVBoxLayout(container)
        mainLayout.setContentsMargins(40, 40, 40, 40)
        mainLayout.setSpacing(30)
        
        # Header row
        headerRow = QHBoxLayout()
        headerRow.addWidget(TitleLabel("Projects"))
        headerRow.addStretch() 
        btn = PrimaryPushButton("+ New Project")
        btn.clicked.connect(self.openNewProjectDialog)
        btn.setFixedWidth(150)
        btn.setFixedHeight(40)
        headerRow.addWidget(btn)
        mainLayout.addLayout(headerRow)

        # Swappable projects area ← this was missing
        self.projectsContainer = QVBoxLayout()
        self.projectsContainer.setSpacing(10)
        mainLayout.addLayout(self.projectsContainer)

        mainLayout.addStretch() 
        mainLayout.addWidget(HorizontalSeparator())

        self.featureRow = QHBoxLayout()
        self.featureRow.setSpacing(20)
        mainLayout.addLayout(self.featureRow)

        outer.addWidget(container)

        self.refreshProjects()  # must be after projectsContainer is defined

    def showEvent(self, event):
        super().showEvent(event)
        self.refreshFeatureCards()
    
    def openNewProjectDialog(self):
        dialog = NewProjectDialog(self.window())
        if dialog.exec():
            values = dialog.getValues()
            try:
                project = self.hobbyist.createProject(
                    values["title"],
                    values["description"],
                    values["deadline"]
                )
                self.refreshProjects()
            except Exception as e:
                InfoBar.warning(
                    title="Couldn't create project",
                    content=str(e),
                    parent=self,
                    duration=3000,
                    position=InfoBarPosition.TOP
                )

    def refreshProjects(self):
        while self.projectsContainer.count():
            item = self.projectsContainer.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.hobbyist.projects:
            self.projectsContainer.addWidget(self.createNpCard())
        else:
            for project in self.hobbyist.projects:
                self.projectsContainer.addWidget(self.createProjectCard(project))

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

    def createProjectCard(self, project):
        card = CardWidget()
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)

        textLayout = QVBoxLayout()
        title = SubtitleLabel(project.title.upper())
        desc = BodyLabel(project.description)
        desc.setWordWrap(True)
        textLayout.addWidget(title)
        textLayout.addWidget(desc)

        openBtn = PushButton("Open")
        openBtn.setFixedWidth(80)
        openBtn.clicked.connect(lambda checked=False, p=project: self.openProject(p))

        layout.addLayout(textLayout)
        layout.addStretch()
        layout.addWidget(openBtn, alignment=Qt.AlignmentFlag.AlignVCenter)

        return card

    def openProject(self, project):
        mainWindow = self.window()
        if hasattr(mainWindow, "projectViewPage"):
            mainWindow.projectViewPage.setProject(project)
            mainWindow.switchTo(mainWindow.projectViewPage)