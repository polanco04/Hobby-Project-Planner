from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from qfluentwidgets import SubtitleLabel, BodyLabel, CardWidget


class ProjectCard(CardWidget):
    clicked = pyqtSignal()

    def __init__(self, title, description="", parent=None):
        super().__init__(parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

        self.titleLabel = SubtitleLabel(title)
        layout.addWidget(self.titleLabel)

        self.descriptionLabel = BodyLabel(description)
        self.descriptionLabel.setWordWrap(True)
        layout.addWidget(self.descriptionLabel)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class projectPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("projectPage")

        # test data for now
        # leave this as [] if you want the page to look empty
        self.projects = [
            {"title": "Painting Project", "description": "Track painting progress and ideas."},
            {"title": "Woodworking Build", "description": "Keep materials, steps, and notes."},
            {"title": "Guitar Practice", "description": "Organize songs and practice goals."}
        ]

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 20, 30, 20)
        self.layout.setSpacing(16)

        self.label = SubtitleLabel("Projects")
        self.layout.addWidget(self.label)

        self.projectsContainer = QWidget()
        self.projectsLayout = QVBoxLayout()
        self.projectsLayout.setContentsMargins(0, 0, 0, 0)
        self.projectsLayout.setSpacing(12)
        self.projectsContainer.setLayout(self.projectsLayout)

        self.layout.addWidget(self.projectsContainer)
        self.layout.addStretch()

        self.setLayout(self.layout)

        self.loadProjects()

    def loadProjects(self):
        # clear old widgets first
        while self.projectsLayout.count():
            item = self.projectsLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # empty state
        if not self.projects:
            self.emptyLabel = BodyLabel("No projects yet.")
            self.emptyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.projectsLayout.addWidget(self.emptyLabel)
            return

        # project cards
        for project in self.projects:
            card = ProjectCard(
                project["title"],
                project["description"]
            )
            card.clicked.connect(lambda checked=False, p=project: self.openProject(p))
            self.projectsLayout.addWidget(card)

    def openProject(self, project):
        print("Project clicked:", project["title"])