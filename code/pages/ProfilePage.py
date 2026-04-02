from PyQt6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SubtitleLabel

class profilePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("profilePage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        self.label = SubtitleLabel("Profile")
        layout.addWidget(self.label)

        layout.addStretch()

        self.setLayout(layout)
