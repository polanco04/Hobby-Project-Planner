from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, LineEdit, TextEdit, 
    StrongBodyLabel, DatePicker
)

class NewProjectDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.titleLabel = SubtitleLabel("New Project")

        # Title field
        self.titleInput = LineEdit()
        self.titleInput.setPlaceholderText("Project title...")

        # Description field
        self.descInput = TextEdit()
        self.descInput.setPlaceholderText("What is this project about?")
        self.descInput.setFixedHeight(80)

        # Deadline field
        self.deadlinePicker = DatePicker()

        # Labels
        titleFieldLabel = StrongBodyLabel("Title")
        descFieldLabel = StrongBodyLabel("Description")
        deadlineFieldLabel = StrongBodyLabel("Deadline")

        # Add to the built-in viewLayout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addSpacing(10)
        self.viewLayout.addWidget(titleFieldLabel)
        self.viewLayout.addWidget(self.titleInput)
        self.viewLayout.addSpacing(8)
        self.viewLayout.addWidget(descFieldLabel)
        self.viewLayout.addWidget(self.descInput)
        self.viewLayout.addSpacing(8)
        self.viewLayout.addWidget(deadlineFieldLabel)
        self.viewLayout.addWidget(self.deadlinePicker)

        # Built-in buttons
        self.yesButton.setText("Create")
        self.cancelButton.setText("Cancel")

        self.widget.setMinimumWidth(400)

    def getValues(self):
        from datetime import date
        d = self.deadlinePicker.getDate()
        deadline = date(d.year(), d.month(), d.day())
        return {
            "title": self.titleInput.text().strip(),
            "description": self.descInput.toPlainText().strip(),
            "deadline": deadline
        }

    def validate(self) -> bool:
        # Called automatically when Create is clicked
        if not self.titleInput.text().strip():
            self.titleInput.setError(True)
            return False
        return True