from PyQt6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SubtitleLabel

class ProjectPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("projectPage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        self.label = SubtitleLabel("Projects")
        layout.addWidget(self.label)

        layout.addStretch()

        self.setLayout(layout)