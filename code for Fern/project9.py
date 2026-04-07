from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import SubtitleLabel, BodyLabel, CardWidget, ComboBox


class TaskCard(CardWidget):
    def __init__(self, title, priority, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        self.titleLabel = SubtitleLabel(title)
        self.priorityLabel = BodyLabel(f"Priority: {priority}")

        layout.addWidget(self.titleLabel)
        layout.addWidget(self.priorityLabel)


class TasksTab(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("tasksTab")

        # example tasks
        self.tasks = [
            {"title": "Buy supplies", "priority": "Medium"},
            {"title": "Finish sketch", "priority": "High"},
            {"title": "Clean workspace", "priority": "Low"},
            {"title": "Add final details", "priority": "High"},
        ]

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 20, 30, 20)
        self.layout.setSpacing(16)

        self.titleLabel = SubtitleLabel("Tasks")
        self.layout.addWidget(self.titleLabel)

        # sort row
        self.sortRow = QHBoxLayout()
        self.sortLabel = BodyLabel("Sort by:")
        self.sortCombo = ComboBox()
        self.sortCombo.addItems([
            "Priority",
            "Alphabetical (A-Z)",
            "Alphabetical (Z-A)"
        ])
        self.sortCombo.currentTextChanged.connect(self.sortTasks)

        self.sortRow.addWidget(self.sortLabel)
        self.sortRow.addWidget(self.sortCombo)
        self.sortRow.addStretch()

        self.layout.addLayout(self.sortRow)

        # container for task cards
        self.taskListWidget = QWidget()
        self.taskListLayout = QVBoxLayout()
        self.taskListLayout.setContentsMargins(0, 0, 0, 0)
        self.taskListLayout.setSpacing(12)

        self.taskListWidget.setLayout(self.taskListLayout)
        self.layout.addWidget(self.taskListWidget)
        self.layout.addStretch()

        self.setLayout(self.layout)

        self.loadTasks()

    def loadTasks(self):
        while self.taskListLayout.count():
            item = self.taskListLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not self.tasks:
            self.taskListLayout.addWidget(BodyLabel("No tasks yet."))
            return

        for task in self.tasks:
            card = TaskCard(task["title"], task["priority"])
            self.taskListLayout.addWidget(card)

    def sortTasks(self, sortType):
        if sortType == "Priority":
            priorityOrder = {"High": 0, "Medium": 1, "Low": 2}
            self.tasks.sort(key=lambda task: priorityOrder.get(task["priority"], 99))

        elif sortType == "Alphabetical (A-Z)":
            self.tasks.sort(key=lambda task: task["title"].lower())

        elif sortType == "Alphabetical (Z-A)":
            self.tasks.sort(key=lambda task: task["title"].lower(), reverse=True)

        self.loadTasks()