from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from qfluentwidgets import (
    BodyLabel, CardWidget, SubtitleLabel, TitleLabel, PrimaryPushButton,
    HorizontalSeparator, IconWidget, InfoBar, InfoBarPosition, PushButton,
    MessageBox
)
from qfluentwidgets import FluentIcon as FIF
from components.widgets import createFeatureCard
from components.projectMessageBox import NewProjectDialog
from components.editProjectDialog import EditProjectDialog
from classes.Hobbyist import Hobbyist
from classes.Project import ProjectStatus
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

STATUS_COLORS = {
    "planning":    ("#1A6FA8", "#E8F0FA"),
    "in_progress": ("#B07D00", "#FFF8E1"),
    "completed":   ("#2E7D32", "#E8F5E9"),
    "on_hold":     ("#7B3F00", "#FBE9E7"),
}

class projectPage(QWidget):
    def __init__(self, hobbyist: Hobbyist, storage=None):
        super().__init__()
        self.hobbyist = hobbyist
        self.storage = storage
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

        headerRow = QHBoxLayout()
        headerRow.addWidget(TitleLabel("Projects"))
        headerRow.addStretch()
        btn = PrimaryPushButton("+ New Project")
        btn.clicked.connect(self.openNewProjectDialog)
        btn.setFixedWidth(150)
        btn.setFixedHeight(40)
        headerRow.addWidget(btn)
        mainLayout.addLayout(headerRow)

        self.projectsContainer = QVBoxLayout()
        self.projectsContainer.setSpacing(10)
        mainLayout.addLayout(self.projectsContainer)

        mainLayout.addStretch()
        mainLayout.addWidget(HorizontalSeparator())

        self.featureRow = QHBoxLayout()
        self.featureRow.setSpacing(20)
        mainLayout.addLayout(self.featureRow)

        outer.addWidget(container)
        self.refreshProjects()

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
                if self.storage:
                    self.storage.saveProject(project)
                    self.storage.saveHobbyist(self.hobbyist)
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
        title = SubtitleLabel(project.title)
        title.setFont(QFont("Segoe UI", 14))
        desc = BodyLabel(project.description)
        desc.setFont(QFont("Segoe UI", 11))
        desc.setWordWrap(True)
        textLayout.addWidget(title)
        textLayout.addWidget(desc)

        if hasattr(project, 'deadline') and project.deadline:
            dateLabel = BodyLabel(f"Deadline: {project.deadline}")
            dateLabel.setFont(QFont("Segoe UI", 10))
            dateLabel.setStyleSheet("color: gray;")
            textLayout.addWidget(dateLabel)

        # Status badge
        statusVal = project.status.value
        fg, bg = STATUS_COLORS.get(statusVal, ("#555555", "#EEEEEE"))
        statusLabel = QLabel(statusVal.replace("_", " ").title())
        statusLabel.setFont(QFont("Segoe UI", 9))
        statusLabel.setStyleSheet(
            f"color: {fg}; background: {bg}; border-radius: 8px; padding: 2px 8px;"
        )
        statusLabel.setFixedHeight(22)
        textLayout.addWidget(statusLabel)

        btnRow = QVBoxLayout()
        btnRow.setSpacing(6)

        openBtn = PushButton("Open")
        openBtn.setFixedWidth(80)
        openBtn.clicked.connect(lambda checked=False, p=project: self.openProject(p))

        editBtn = PushButton("Edit")
        editBtn.setFixedWidth(80)
        editBtn.clicked.connect(lambda checked=False, p=project: self.editProject(p))

        holdBtn = PushButton("On Hold" if project.status != ProjectStatus.ON_HOLD else "Resume")
        holdBtn.setFixedWidth(80)
        holdBtn.clicked.connect(lambda checked=False, p=project: self.toggleHold(p))

        deleteBtn = PushButton("Delete")
        deleteBtn.setFixedWidth(80)
        deleteBtn.setStyleSheet("""
            QPushButton {
                color: #CC4444;
                border: 1.5px solid #CC4444;
                border-radius: 8px;
                background: transparent;
            }
            QPushButton:hover { background: rgba(204,68,68,0.08); }
        """)
        deleteBtn.clicked.connect(lambda checked=False, p=project: self.deleteProject(p))

        btnRow.addWidget(openBtn)
        btnRow.addWidget(editBtn)
        btnRow.addWidget(holdBtn)
        btnRow.addWidget(deleteBtn)

        layout.addLayout(textLayout)
        layout.addStretch()
        layout.addLayout(btnRow)
        return card

    def openProject(self, project):
        mainWindow = self.window()
        if hasattr(mainWindow, "projectViewPage"):
            mainWindow.projectViewPage.setProject(project)
            mainWindow.switchTo(mainWindow.projectViewPage)

    def editProject(self, project):
        dialog = EditProjectDialog(project, self.window())
        if dialog.exec():
            values = dialog.getValues()
            project.editProject(
                title=values["title"],
                description=values["description"],
                deadline=values["deadline"]
            )
            if self.storage:
                self.storage.saveProject(project)
            self.refreshProjects()

    def toggleHold(self, project):
        if project.status == ProjectStatus.ON_HOLD:
            completed = sum(1 for t in project.tasks if t.dateCompleted)
            total = len(project.tasks)
            if total == 0:
                project.status = ProjectStatus.PLANNING
            elif completed == total:
                project.status = ProjectStatus.COMPLETED
            elif completed > 0:
                project.status = ProjectStatus.IN_PROGRESS
            else:
                project.status = ProjectStatus.PLANNING
        else:
            project.status = ProjectStatus.ON_HOLD

        if self.storage:
            self.storage.saveProject(project)
        self.refreshProjects()

    def deleteProject(self, project):
        dialog = MessageBox(
            "Delete Project",
            f"Are you sure you want to delete '{project.title}'? This cannot be undone.",
            self.window()
        )
        if dialog.exec():
            self.hobbyist.deleteProject(project.projectId)
            if self.storage:
                self.storage.deleteProject(project.projectId)
                self.storage.saveHobbyist(self.hobbyist)
            self.refreshProjects()