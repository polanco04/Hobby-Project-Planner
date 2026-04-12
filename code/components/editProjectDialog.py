from PyQt6.QtCore import Qt
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, LineEdit, TextEdit,
    StrongBodyLabel, CalendarPicker
)

class EditProjectDialog(MessageBoxBase):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project

        self.titleLabel = SubtitleLabel("Edit Project")

        titleFieldLabel = StrongBodyLabel("Title")
        self.titleInput = LineEdit()
        self.titleInput.setText(project.title)

        descFieldLabel = StrongBodyLabel("Description")
        self.descInput = TextEdit()
        self.descInput.setPlainText(project.description)
        self.descInput.setFixedHeight(80)

        deadlineFieldLabel = StrongBodyLabel("Deadline")
        self.deadlinePicker = CalendarPicker()

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

        self.yesButton.setText("Save")
        self.cancelButton.setText("Cancel")
        self.widget.setMinimumWidth(400)

    def getValues(self):
        d = self.deadlinePicker.getDate()
        return {
            "title": self.titleInput.text().strip(),
            "description": self.descInput.toPlainText().strip(),
            "deadline": d.toPyDate() if d else self.project.deadline
        }

    def validate(self) -> bool:
        if not self.titleInput.text().strip():
            self.titleInput.setError(True)
            return False
        return True