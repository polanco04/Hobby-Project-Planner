from PyQt6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SubtitleLabel

class projectViewPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("projectViewPage")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        self.label = SubtitleLabel("Project View")
        layout.addWidget(self.label)

        layout.addStretch()

        self.setLayout(layout)