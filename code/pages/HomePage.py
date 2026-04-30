from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from qfluentwidgets import (
    BodyLabel, CardWidget, SubtitleLabel, TitleLabel, PrimaryPushButton,
    HorizontalSeparator, CaptionLabel, PushButton
)
import random

FEATURE_CARDS = {
    "Organize your tasks": [
        "homeImages/tasks1.jpg",
        "homeImages/tasks2.jpg",
        "homeImages/tasks3.jpg",
    ],
    "Track milestones": [
        "homeImages/milestones1.jpg",
        "homeImages/milestones2.jpg",
        "homeImages/milestones3.jpg",
    ],
    "Document progress": [
        "homeImages/notes1.jpg",
        "homeImages/notes2.jpg",
        "homeImages/notes3.jpg",
    ],
}

class homePage(QWidget):
    def __init__(self, mainWindow=None, hobbyist=None):
        super().__init__()
        self.setObjectName("homePage")
        self.mainWindow = mainWindow
        self.hobbyist = hobbyist

        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        outer.setContentsMargins(40, 0, 40, 0)

        container = QWidget()
        container.setMaximumWidth(1000)
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.mainLayout = QVBoxLayout(container)
        self.mainLayout.setContentsMargins(40, 40, 40, 40)
        self.mainLayout.setSpacing(30)

        # Swappable top area
        self.topWidget = QWidget()
        self.mainLayout.addWidget(self.topWidget)

        self.mainLayout.addStretch()
        self.mainLayout.addWidget(HorizontalSeparator())

        self.featureRow = QHBoxLayout()
        self.featureRow.setSpacing(20)
        self.mainLayout.addLayout(self.featureRow)

        outer.addWidget(container)

        self.refreshHome()

    def showEvent(self, event):
        super().showEvent(event)
        self.refreshHome()
        self.refreshFeatureCards()

    def refreshHome(self):
        self.topWidget.deleteLater()
        self.topWidget = QWidget()
        topLayout = QVBoxLayout(self.topWidget)
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setSpacing(16)
        self.mainLayout.insertWidget(0, self.topWidget)

        if not self.hobbyist or not self.hobbyist.projects:
            topLayout.addWidget(TitleLabel("Welcome!"))
            topLayout.addWidget(BodyLabel("Enjoy and track your hobbies!"))
            topLayout.addWidget(self.createStCard())
        else:
            topLayout.addWidget(TitleLabel("Welcome back"))
            topLayout.addWidget(BodyLabel("Small progress is still progress."))
            topLayout.addWidget(self.createContinueCard())

            otherProjects = self.hobbyist.projects[:-1]
            if otherProjects:
                topLayout.addWidget(SubtitleLabel("Other Projects"))
                otherRow = QHBoxLayout()
                otherRow.setSpacing(16)
                for project in otherProjects:
                    otherRow.addWidget(self.createOtherProjectCard(project))
                otherRow.addStretch()
                topLayout.addLayout(otherRow)

    def createStCard(self):
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 20, 20, 20)
        layout.setSpacing(5)

        title = SubtitleLabel("Get started")
        body = BodyLabel("You haven't created any projects yet. Start your first hobby project today!")
        btn = PrimaryPushButton("Go to Projects →")
        btn.setFixedWidth(300)
        btn.clicked.connect(lambda: self.mainWindow.switchTo(self.mainWindow.projectPage))

        layout.addWidget(title)
        layout.addSpacing(5)
        layout.addWidget(body)
        layout.addSpacing(15)
        layout.addWidget(btn)
        return card

    def createContinueCard(self):
        project = self.hobbyist.projects[-1]
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        layout.addWidget(BodyLabel("Continue where you left off"))

        bottomRow = QHBoxLayout()
        textLayout = QVBoxLayout()
        title = SubtitleLabel(project.title)
        desc = BodyLabel(project.description)
        desc.setWordWrap(True)
        textLayout.addWidget(title)
        textLayout.addWidget(desc)

        continueBtn = PrimaryPushButton("Continue →")
        continueBtn.setFixedWidth(120)
        continueBtn.clicked.connect(lambda checked=False, p=project: self.openProject(p))

        bottomRow.addLayout(textLayout)
        bottomRow.addStretch()
        bottomRow.addWidget(continueBtn, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addLayout(bottomRow)
        return card

    def createOtherProjectCard(self, project):
        card = CardWidget()
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)

        textLayout = QVBoxLayout()
        title = SubtitleLabel(project.title)
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

    def createFeatureCard(self, imagePath, caption):
        wrapper = QWidget()
        wrapperLayout = QVBoxLayout(wrapper)
        wrapperLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        card = CardWidget()
        card_layout = QVBoxLayout(card)

        img_label = QLabel()
        img_label.setPixmap(
            QPixmap(imagePath).scaled(250, 180, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        )
        img_label.setFixedSize(250, 180)
        card_layout.addWidget(img_label)

        captionLabel = CaptionLabel(caption)
        captionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        wrapperLayout.addWidget(card)
        wrapperLayout.addWidget(captionLabel)
        return wrapper
    
    def refreshFeatureCards(self):
        while self.featureRow.count():
            item = self.featureRow.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for caption, images in FEATURE_CARDS.items():
            image = random.choice(images)
            self.featureRow.addWidget(self.createFeatureCard(image, caption))