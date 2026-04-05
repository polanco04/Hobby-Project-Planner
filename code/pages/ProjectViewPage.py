## Project View Page 
## This page will show the details of a specific project when selected within the
## Projects pages.
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget, QVBoxLayout
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QFont
from qfluentwidgets import SubtitleLabel, isDarkTheme



class projectViewPage(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set the object name for styling purposes
        self.setObjectName("projectViewPage")

        # Set up the layout and widgets for the project view page
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        # Top-left section with back button, title, and description
        topLayout = QHBoxLayout()
        topLayout.setSpacing(12)

        self.backButton = QLabel("←")
        self.backButton.setToolTip("Back to Projects")
        
        backFont = QFont()
        backFont.setPointSize(14)
        backFont.setBold(True)
        self.backButton.setFont(backFont)
        self.backButton.setFixedWidth(24)

        textLayout = QVBoxLayout()
        textLayout.setSpacing(4)
        textLayout.setContentsMargins(0, 0, 0, 0)

        self.projectTitle = SubtitleLabel("Project Title")
        self.projectDescription = QLabel("Project Description")
        descriptionFont = QFont()
        descriptionFont.setPointSize(11)
        descriptionFont.setBold(True)
        self.projectDescription.setFont(descriptionFont)
        self.projectDescription.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        textLayout.addWidget(self.projectTitle)
        textLayout.addWidget(self.projectDescription)

        topLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignTop)
        topLayout.addLayout(textLayout)
        topLayout.addStretch()

        # Add the top layout to the main layout
        layout.addLayout(topLayout)
        layout.addStretch()

        self.setLayout(layout)

        # Apply theme-aware colors after layout is set
        self._applyThemeColors()       
        
    def _applyThemeColors(self):
        if isDarkTheme():
            self.backButton.setStyleSheet("color: #FFFFFF;")
            self.projectDescription.setStyleSheet("color: #FFFFFF;")
        else:
            self.backButton.setStyleSheet("color: #202020;")
            self.projectDescription.setStyleSheet("color: #404040;")

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.Type.PaletteChange, QEvent.Type.StyleChange):
            self._applyThemeColors()

    def showEvent(self, event):
        super().showEvent(event)
        self._applyThemeColors()

    
