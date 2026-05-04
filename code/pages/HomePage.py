from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QEvent, QTimer
from qfluentwidgets import (
    CardWidget, PrimaryPushButton,
    HorizontalSeparator, CaptionLabel, PushButton, SubtitleLabel,
    TitleLabel, BodyLabel, isDarkTheme, StrongBodyLabel
)
from PyQt6.QtWidgets import QApplication
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

FIRST_TIME_SUBTITLES = [
    "Let's get started on something great.",
    "Your hobby journey starts here.",
    "Time to turn your passions into progress.",
    "Every expert was once a beginner.",
]

WELCOME_BACK_SUBTITLES = [
    "Small progress is still progress.",
    "Keep the momentum going.",
    "Every step counts.",
    "You're doing great. Keep it up.",
    "Back at it — let's make today count.",
]

IN_SESSION_SUBTITLES = [
    "What would you like to work on?",
    "Your projects are waiting.",
    "Pick up where you left off.",
    "Stay focused, stay creative.",
    "Every hobby deserves attention.",
]

class homePage(QWidget):
    def __init__(self, mainWindow=None, hobbyist=None, isFirstTime=False):
        super().__init__()
        self.setObjectName("homePage")
        self.mainWindow = mainWindow
        self.hobbyist = hobbyist
        self.isFirstTime = isFirstTime
        self._shownThisSession = False

        self._firstTimeSubtitle = random.choice(FIRST_TIME_SUBTITLES)
        self._welcomeBackSubtitle = random.choice(WELCOME_BACK_SUBTITLES)
        self._inSessionSubtitle = random.choice(IN_SESSION_SUBTITLES)

        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        outer.setContentsMargins(40, 0, 40, 0)

        container = QWidget()
        container.setMaximumWidth(1000)
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.mainLayout = QVBoxLayout(container)
        self.mainLayout.setContentsMargins(40, 40, 40, 40)
        self.mainLayout.setSpacing(30)

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

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.Type.PaletteChange, QEvent.Type.StyleChange):
            self.refreshHome()

    def _getGreeting(self):
        username = self.hobbyist.username if self.hobbyist and self.hobbyist.username else ""
        nameStr = f", {username}" if username and username != "User" else ""

        if not self.hobbyist or not self.hobbyist.projects:
            return "Welcome!", self._firstTimeSubtitle

        if self.isFirstTime and not self._shownThisSession:
            return "Welcome!", self._firstTimeSubtitle
        elif not self._shownThisSession:
            return f"Welcome back{nameStr}!", self._welcomeBackSubtitle
        else:
            return "Hobby Project Planner", self._inSessionSubtitle

    def refreshHome(self):
        self.topWidget.deleteLater()
        self.topWidget = QWidget()
        topLayout = QVBoxLayout(self.topWidget)
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setSpacing(16)
        self.mainLayout.insertWidget(0, self.topWidget)

        title, subtitle = self._getGreeting()

        titleLabel = TitleLabel(title)
        subtitleLabel = BodyLabel(subtitle)
        subtitleLabel.setStyleSheet("color: #888888;")

        topLayout.addWidget(titleLabel)
        topLayout.addWidget(subtitleLabel)

        if not self.hobbyist or not self.hobbyist.projects:
            topLayout.addWidget(self.createStCard())
        else:
            topLayout.addWidget(self.createContinueCard())

            otherProjects = self.hobbyist.projects[:-1]
            if otherProjects:
                otherLabel = StrongBodyLabel("Other Projects")
                topLayout.addWidget(otherLabel)

                otherRow = QHBoxLayout()
                otherRow.setSpacing(16)
                for project in otherProjects:
                    otherRow.addWidget(self.createOtherProjectCard(project))
                otherRow.addStretch()
                topLayout.addLayout(otherRow)

        self._shownThisSession = True

    def createStCard(self):
        card = CardWidget()
        card.setStyleSheet("CardWidget { border-radius: 14px; }")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(8)

        title = StrongBodyLabel("Get started")
        body = BodyLabel("You haven't created any projects yet. Start your first hobby project today!")
        body.setStyleSheet("color: #888888;")
        body.setWordWrap(True)

        btn = PrimaryPushButton("Go to Projects →")
        btn.setFixedWidth(180)
        btn.setFixedHeight(36)
        btn.clicked.connect(lambda: self.mainWindow.switchTo(self.mainWindow.projectPage))

        layout.addWidget(title)
        layout.addWidget(body)
        layout.addSpacing(8)
        layout.addWidget(btn)
        return card

    def createContinueCard(self):
        project = self.hobbyist.projects[-1]
        card = CardWidget()
        card.setStyleSheet("CardWidget { border-radius: 14px; }")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(10)

        headerLabel = CaptionLabel("Continue where you left off")
        headerLabel.setStyleSheet("color: #888888;")
        layout.addWidget(headerLabel)

        bottomRow = QHBoxLayout()
        textLayout = QVBoxLayout()
        textLayout.setSpacing(4)

        title = SubtitleLabel(project.title.upper())
        desc = BodyLabel(project.description)
        desc.setStyleSheet("color: #888888;")
        desc.setWordWrap(True)

        textLayout.addWidget(title)
        textLayout.addWidget(desc)

        continueBtn = PrimaryPushButton("Continue →")
        continueBtn.setFixedWidth(120)
        continueBtn.setFixedHeight(36)
        continueBtn.clicked.connect(lambda checked=False, p=project: self.openProject(p))

        bottomRow.addLayout(textLayout)
        bottomRow.addStretch()
        bottomRow.addWidget(continueBtn, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addLayout(bottomRow)
        return card

    def createOtherProjectCard(self, project):
        card = CardWidget()
        card.setStyleSheet("CardWidget { border-radius: 14px; }")
        card.setFixedWidth(300)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(6)

        title = StrongBodyLabel(project.title.upper())
        desc = CaptionLabel(project.description)
        desc.setStyleSheet("color: #888888;")
        desc.setWordWrap(True)

        openBtn = PushButton("Open")
        openBtn.setFixedHeight(32)
        openBtn.setStyleSheet("""
            QPushButton {
                border: 1.5px solid #CCCCCC;
                border-radius: 8px;
                font-weight: 500;
                background: transparent;
            }
            QPushButton:hover { background: rgba(0,0,0,0.05); }
        """)
        openBtn.clicked.connect(lambda checked=False, p=project: self.openProject(p))

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(6)
        layout.addWidget(openBtn)
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
        wrapperLayout.setSpacing(8)

        card = CardWidget()
        card.setStyleSheet("CardWidget { border-radius: 12px; }")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)

        img_label = QLabel()
        img_label.setPixmap(
            QPixmap(imagePath).scaled(
                250, 180,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        img_label.setFixedSize(250, 180)
        card_layout.addWidget(img_label)

        captionLabel = CaptionLabel(caption)
        captionLabel.setStyleSheet("color: #888888;")
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