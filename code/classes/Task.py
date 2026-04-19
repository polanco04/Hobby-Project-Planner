from datetime import datetime
from typing import Any
from .Reminder import Reminder

class Task:
    def __init__(self, name: str, description: str, deadline: datetime, estimatedTime: int):
        name = name.strip()
        description = description.strip()

        if not name:
            raise ValueError("Task name cannot be empty.")

        if estimatedTime < 0:
            raise ValueError("Estimated time cannot be negative.")

        self.taskId = None
        self.name = name
        self.description = description
        self.dateCreated = datetime.now()
        self.dateCompleted: datetime | None = None
        self.deadline = deadline
        self.estimatedTime = estimatedTime
        self.reminders: list[Reminder] = []
        self.dependencies: list[Task] = []
        self.milestones: list = [] 

    def markComplete(self) -> None:
        if self.isBlocked():
            raise ValueError("Cannot complete a task while it is blocked by dependencies.")
        self.dateCompleted = datetime.now()

        for milestone in self.milestones:
            if not milestone.manuallyCompleted and milestone.getProgress() == 100.0:
                milestone.manuallyCompleted = False

    def unmarkComplete(self) -> None:
        self.dateCompleted = None

    def addDependency(self, task) -> None:
        if task is self:
            raise ValueError("A task cannot depend on itself.")

        if task in self.dependencies:
            return

        if self in task.dependencies:
            raise ValueError("This dependency would create a circular relationship.")

        self.dependencies.append(task)

    def removeDependency(self, task) -> None:
        if task in self.dependencies:
            self.dependencies.remove(task)

    def isBlocked(self) -> bool:
        for dependency in self.dependencies:
            if dependency.dateCompleted is None:
                return True
        return False

    def updateDetails(self, name: str, desc: str) -> None:
        cleanedName = name.strip()

        if not cleanedName:
            raise ValueError("Task name cannot be empty.")

        self.name = cleanedName
        self.description = desc.strip()

    def addReminder(self, reminder: Any) -> None:
        self.reminders.append(reminder)

    def toDict(self) -> dict[str, Any]:
        return {
            "taskId": self.taskId,
            "name": self.name,
            "description": self.description,
            "dateCreated": self.dateCreated,
            "dateCompleted": self.dateCompleted,
            "deadline": self.deadline,
            "estimatedTime": self.estimatedTime,
            "reminders": self.reminders,
            "milestones": [m.milestoneId for m in self.milestones],
            "dependencies": [dependency.taskId for dependency in self.dependencies],
        }
