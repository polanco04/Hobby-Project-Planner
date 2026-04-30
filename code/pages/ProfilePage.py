import shutil
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor
from qfluentwidgets import (
    SubtitleLabel, StrongBodyLabel, BodyLabel,
    LineEdit, TextEdit, PrimaryPushButton, PushButton, CardWidget, FluentIcon as FIF
)
from utils import getAppDataDir

_DATA_DIR = Path(getAppDataDir())
_AVATAR_FILE = _DATA_DIR / "avatar.png"


class AvatarLabel(QLabel):
    def __init__(self, size=96, parent=None):
        super().__init__(parent)
        self._size = size
        self._pixmap = None
        self.edit_mode = False
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self.update()

    def setEditMode(self, enabled):
        self.edit_mode = enabled
        self.setCursor(
            Qt.CursorShape.PointingHandCursor if enabled else Qt.CursorShape.ArrowCursor
        )

    def mousePressEvent(self, event):
        if self.edit_mode:
            path, _ = QFileDialog.getOpenFileName(
                self, "Choose Profile Picture", "",
                "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
            )
            if path:
                _DATA_DIR.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, _AVATAR_FILE)
                self._pixmap = QPixmap(str(_AVATAR_FILE))
                self.update()
                page = self.parent().parent()
                if hasattr(page, "updateRemoveBtn"):
                    page.updateRemoveBtn()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        size = self._size
        clip = QPainterPath()
        clip.addEllipse(0, 0, size, size)
        painter.setClipPath(clip)

        if self._pixmap and not self._pixmap.isNull():
            scaled = self._pixmap.scaled(
                size, size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (scaled.width() - size) // 2
            y = (scaled.height() - size) // 2
            painter.drawPixmap(-x, -y, scaled)
        else:
            painter.fillRect(0, 0, size, size, QColor("#e0e0e0"))
            icon = FIF.PEOPLE.icon()
            icon_size = size // 2
            offset = (size - icon_size) // 2
            icon.paint(painter, offset, offset, icon_size, icon_size)

        painter.end()


class profilePage(QWidget):
    def __init__(self, hobbyist=None, storage=None):
        super().__init__()
        self.setObjectName("profilePage")
        self.hobbyist = hobbyist
        self.storage = storage
        self._editing = False

        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 20, 30, 20)
        outer.setSpacing(16)

        outer.addWidget(SubtitleLabel("Profile"))

        card = CardWidget(self)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        cardLayout = QVBoxLayout(card)
        cardLayout.setContentsMargins(24, 20, 24, 20)
        cardLayout.setSpacing(12)

        cardLayout.addWidget(StrongBodyLabel("User Information"))

        avatarRow = QVBoxLayout()
        avatarRow.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.avatar = AvatarLabel(96, card)
        self.loadAvatar()
        avatarRow.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.removePhotoBtn = PushButton("Remove Photo")
        self.removePhotoBtn.setFixedWidth(120)
        self.removePhotoBtn.clicked.connect(self.removePhoto)
        self.removePhotoBtn.hide()
        avatarRow.addWidget(self.removePhotoBtn, alignment=Qt.AlignmentFlag.AlignHCenter)
        cardLayout.addLayout(avatarRow)

        self._viewWidget = QWidget()
        viewLayout = QVBoxLayout(self._viewWidget)
        viewLayout.setContentsMargins(0, 0, 0, 0)
        viewLayout.setSpacing(4)

        viewLayout.addWidget(StrongBodyLabel("Username"))
        self._usernameDisplay = BodyLabel(hobbyist.username if hobbyist else "")
        self._usernameDisplay.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        viewLayout.addWidget(self._usernameDisplay)

        viewLayout.addSpacing(8)
        viewLayout.addWidget(StrongBodyLabel("Bio"))
        self._bioDisplay = BodyLabel(hobbyist.bio if hobbyist else "")
        self._bioDisplay.setWordWrap(True)
        self._bioDisplay.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        viewLayout.addWidget(self._bioDisplay)

        self._editWidget = QWidget()
        self._editWidget.hide()
        editLayout = QVBoxLayout(self._editWidget)
        editLayout.setContentsMargins(0, 0, 0, 0)
        editLayout.setSpacing(4)

        editLayout.addWidget(StrongBodyLabel("Username"))
        self._usernameEdit = LineEdit()
        self._usernameEdit.setPlaceholderText("Enter your username...")
        self._usernameEdit.setText(hobbyist.username if hobbyist else "")
        editLayout.addWidget(self._usernameEdit)

        editLayout.addSpacing(8)
        editLayout.addWidget(StrongBodyLabel("Bio"))
        self._bioEdit = TextEdit()
        self._bioEdit.setPlaceholderText("Tell us a bit about yourself...")
        self._bioEdit.setPlainText(hobbyist.bio if hobbyist else "")
        self._bioEdit.setFixedHeight(80)
        editLayout.addWidget(self._bioEdit)

        cardLayout.addWidget(self._viewWidget)
        cardLayout.addWidget(self._editWidget)

        self._editBtn = PrimaryPushButton("Edit Profile")
        self._editBtn.clicked.connect(self.toggleEdit)
        cardLayout.addWidget(self._editBtn)

        outer.addWidget(card)
        outer.addStretch()

    def loadAvatar(self):
        if self.hobbyist and self.hobbyist.profilePicture:
            pixmap = QPixmap(self.hobbyist.profilePicture)
            if not pixmap.isNull():
                self.avatar.setPixmap(pixmap)
                return
        if _AVATAR_FILE.exists():
            self.avatar.setPixmap(QPixmap(str(_AVATAR_FILE)))

    def toggleEdit(self):
        if not self._editing:
            self._editing = True
            self._usernameEdit.setText(self._usernameDisplay.text())
            self._bioEdit.setPlainText(self._bioDisplay.text())
            self.avatar.setEditMode(True)
            self.updateRemoveBtn()
            self._viewWidget.hide()
            self._editWidget.show()
            self._editBtn.setText("Save Profile")
        else:
            self._editing = False
            username = self._usernameEdit.text().strip()
            bio = self._bioEdit.toPlainText().strip()

            if self.hobbyist:
                self.hobbyist.setUsername(username)
                self.hobbyist.setBio(bio)
                if _AVATAR_FILE.exists():
                    self.hobbyist.setProfilePicture(str(_AVATAR_FILE))
                if self.storage:
                    self.storage.saveHobbyist(self.hobbyist)  

            self._usernameDisplay.setText(username)
            self._bioDisplay.setText(bio)
            self.loadAvatar()
            self.avatar.setEditMode(False)
            self.removePhotoBtn.hide()
            self._editWidget.hide()
            self._viewWidget.show()
            self._editBtn.setText("Edit Profile")

    def updateRemoveBtn(self):
        self.removePhotoBtn.setVisible(_AVATAR_FILE.exists())

    def removePhoto(self):
        self.avatar._pixmap = None
        self.avatar.update()
        
        if _AVATAR_FILE.exists():
            try:
                _AVATAR_FILE.unlink()
            except PermissionError:
                _AVATAR_FILE.rename(_AVATAR_FILE.with_suffix(".bak"))
        
        if self.hobbyist:
            self.hobbyist.profilePicture = None
            if self.storage:
                self.storage.saveHobbyist(self.hobbyist)

        self.removePhotoBtn.hide()