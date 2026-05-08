from PyQt6.QtCore import QDate
from qfluentwidgets import (
    MessageBoxBase, SubtitleLabel, LineEdit, TextEdit,
    StrongBodyLabel, CalendarPicker, InfoBar, InfoBarPosition
)

class EditProjectDialog(MessageBoxBase):
    """
    Name: __init__

    INPUT:
        project:        The Project instance whose details are being edited (Project)
        parent:         Optional parent widget (QWidget)

    RETURN:
        N/A

    DESCRIPTION:
        Initializes the EditProjectDialog with input fields pre-populated with
        the given project's current title, description, and deadline. Sets up
        the dialog layout with labels, inputs, a calendar picker, and Save/Cancel buttons.
    """
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

    """
    Name: getValues

    INPUT:
        N/A

    RETURN:
        dict:           Dictionary with keys 'title', 'description', and 'deadline'

    DESCRIPTION:
        Reads and returns the current values from the dialog's input fields.
        If no deadline is selected in the picker, falls back to the project's
        existing deadline.
    """
    def getValues(self):
        d = self.deadlinePicker.getDate()
        return {
            "title": self.titleInput.text().strip(),
            "description": self.descInput.toPlainText().strip(),
            "deadline": d.toPyDate() if d else self.project.deadline
        }

    """
    Name: validate

    INPUT:
        N/A

    RETURN:
        bool:           True if all inputs are valid, False otherwise

    DESCRIPTION:
        Validates the dialog inputs before submission. Returns False and highlights
        the title field if it is empty. Returns False and shows a warning InfoBar
        if no deadline is selected or the selected date is in the past.
    """
    def validate(self) -> bool:
        if not self.titleInput.text().strip():
            self.titleInput.setError(True)
            return False

        d = self.deadlinePicker.getDate()
        if not d or d < QDate.currentDate():
            InfoBar.warning(
                title="Invalid Date",
                content="The deadline cannot be in the past.",
                parent=self.parent(),
                duration=3000,
                position=InfoBarPosition.TOP
            )
            return False

        return True