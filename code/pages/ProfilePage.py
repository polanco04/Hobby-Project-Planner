import json
import shutil
from pathlib import Path

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor
from qfluentwidgets import (
    SubtitleLabel, StrongBodyLabel, BodyLabel,
    LineEdit, TextEdit, PrimaryPushButton, PushButton, CardWidget, FluentIcon as FIF
)

# Project-relative data directory: <repo root>/data/
_DATA_DIR = Path(__file__).parent.parent.parent / "data"
_PROFILE_JSON = _DATA_DIR / "profile.json"
_AVATAR_FILE = _DATA_DIR / "avatar.png"


def _load_profile() -> dict:
    # Start: read profile.json from disk and return its contents as a dict
    if _PROFILE_JSON.exists():
        try:
            return json.loads(_PROFILE_JSON.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"username": "", "bio": ""}
    # End: returns saved profile data, or empty defaults if file is missing or unreadable


def _save_profile(data: dict) -> None:
    # Start: write the profile dict to profile.json, creating the data folder if needed
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    _PROFILE_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")
    # End: profile.json is now updated on disk


class AvatarLabel(QLabel):
    """Circular avatar; clicking it opens a file picker when in edit mode."""

    def __init__(self, size=96, parent=None):
        # Start: set up the avatar widget with a fixed size and default arrow cursor
        super().__init__(parent)
        self._size = size
        self._pixmap = None
        self.edit_mode = False
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        # End: avatar widget is ready to display

    def setPixmap(self, pixmap):
        # Start: store the new pixmap and trigger a repaint
        self._pixmap = pixmap
        self.update()
        # End: avatar will redraw with the new image on the next paint cycle

    def setEditMode(self, enabled):
        # Start: switch the avatar between clickable (edit) and display-only (view) mode
        self.edit_mode = enabled
        self.setCursor(
            Qt.CursorShape.PointingHandCursor if enabled else Qt.CursorShape.ArrowCursor
        )
        # End: cursor now reflects whether the avatar is clickable

    def mousePressEvent(self, event):
        # Start: open a file picker when the avatar is clicked in edit mode
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
                # Notify the parent page so it can show the remove button
                page = self.parent().parent()
                if hasattr(page, "_updateRemoveBtn"):
                    page._updateRemoveBtn()
        # End: selected image is copied to the data folder and shown in the avatar

    def paintEvent(self, event):
        # Start: draw the avatar as a circle, either with the user's image or a default icon
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
        # End: avatar circle is fully painted to the screen


class profilePage(QWidget):
    def __init__(self):
        # Start: build the full profile page layout with view and edit modes
        super().__init__()
        self.setObjectName("profilePage")

        self._editing = False
        profile = _load_profile()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 20, 30, 20)
        outer.setSpacing(16)

        outer.addWidget(SubtitleLabel("Profile"))

        # ── Card ────────────────────────────────────────────────────────────
        card = CardWidget(self)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        cardLayout = QVBoxLayout(card)
        cardLayout.setContentsMargins(24, 20, 24, 20)
        cardLayout.setSpacing(12)

        cardLayout.addWidget(StrongBodyLabel("User Information"))

        # Avatar (centered) with remove button below it
        avatarRow = QVBoxLayout()
        avatarRow.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.avatar = AvatarLabel(96, card)
        if _AVATAR_FILE.exists():
            self.avatar.setPixmap(QPixmap(str(_AVATAR_FILE)))
        avatarRow.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._removePhotoBtn = PushButton("Remove Photo")
        self._removePhotoBtn.setFixedWidth(120)
        self._removePhotoBtn.clicked.connect(self._removePhoto)
        self._removePhotoBtn.hide()  # only shown in edit mode when a photo exists
        avatarRow.addWidget(self._removePhotoBtn, alignment=Qt.AlignmentFlag.AlignHCenter)
        cardLayout.addLayout(avatarRow)

        # ── View mode ────────────────────────────────────────────────────────
        self._viewWidget = QWidget()
        viewLayout = QVBoxLayout(self._viewWidget)
        viewLayout.setContentsMargins(0, 0, 0, 0)
        viewLayout.setSpacing(4)

        viewLayout.addWidget(StrongBodyLabel("Username"))
        self._usernameDisplay = BodyLabel(profile["username"])
        self._usernameDisplay.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        viewLayout.addWidget(self._usernameDisplay)

        viewLayout.addSpacing(8)
        viewLayout.addWidget(StrongBodyLabel("Bio"))
        self._bioDisplay = BodyLabel(profile["bio"])
        self._bioDisplay.setWordWrap(True)
        self._bioDisplay.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        viewLayout.addWidget(self._bioDisplay)

        # ── Edit mode ────────────────────────────────────────────────────────
        self._editWidget = QWidget()
        self._editWidget.hide()
        editLayout = QVBoxLayout(self._editWidget)
        editLayout.setContentsMargins(0, 0, 0, 0)
        editLayout.setSpacing(4)

        editLayout.addWidget(StrongBodyLabel("Username"))
        self._usernameEdit = LineEdit()
        self._usernameEdit.setPlaceholderText("Enter your username...")
        self._usernameEdit.setText(profile["username"])
        editLayout.addWidget(self._usernameEdit)

        editLayout.addSpacing(8)
        editLayout.addWidget(StrongBodyLabel("Bio"))
        self._bioEdit = TextEdit()
        self._bioEdit.setPlaceholderText("Tell us a bit about yourself...")
        self._bioEdit.setPlainText(profile["bio"])
        self._bioEdit.setFixedHeight(80)
        editLayout.addWidget(self._bioEdit)

        cardLayout.addWidget(self._viewWidget)
        cardLayout.addWidget(self._editWidget)

        self._editBtn = PrimaryPushButton("Edit Profile")
        self._editBtn.clicked.connect(self._toggleEdit)
        cardLayout.addWidget(self._editBtn)

        outer.addWidget(card)
        outer.addStretch()
        # End: profile page layout is fully constructed and ready to display

    def _toggleEdit(self):
        # Start: switch between view mode and edit mode when the button is clicked
        if not self._editing:
            self._editing = True
            self._usernameEdit.setText(self._usernameDisplay.text())
            self._bioEdit.setPlainText(self._bioDisplay.text())
            self.avatar.setEditMode(True)
            self._updateRemoveBtn()
            self._viewWidget.hide()
            self._editWidget.show()
            self._editBtn.setText("Save Profile")
        else:
            self._editing = False
            username = self._usernameEdit.text().strip()
            bio = self._bioEdit.toPlainText().strip()

            self._usernameDisplay.setText(username)
            self._bioDisplay.setText(bio)
            _save_profile({"username": username, "bio": bio})

            if _AVATAR_FILE.exists():
                self.avatar.setPixmap(QPixmap(str(_AVATAR_FILE)))

            self.avatar.setEditMode(False)
            self._removePhotoBtn.hide()
            self._editWidget.hide()
            self._viewWidget.show()
            self._editBtn.setText("Edit Profile")
        # End: page is now showing either edit inputs or the saved profile display

    def _updateRemoveBtn(self):
        # Start: show the remove button only when in edit mode and a photo exists
        self._removePhotoBtn.setVisible(_AVATAR_FILE.exists())
        # End: remove button visibility is now in sync with whether a photo is set

    def _removePhoto(self):
        # Start: delete the saved avatar file and reset the avatar to the default icon
        if _AVATAR_FILE.exists():
            _AVATAR_FILE.unlink()
        self.avatar._pixmap = None
        self.avatar.update()
        self._removePhotoBtn.hide()
        # End: avatar is cleared and the default placeholder icon is shown again
