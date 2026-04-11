from __future__ import annotations

from datetime import datetime
from typing import Any


class Task:
    def __init__(
        self,
        taskId: int,
        name: str,
        description: str,
        deadline: datetime,
        estimatedTime: int,
    ):
        name = name.strip()
        description = description.strip()

        if not name:
            raise ValueError("Task name cannot be empty.")

        if estimatedTime < 0:
            raise ValueError("Estimated time cannot be negative.")

        self.taskId = taskId
        self.name = name
        self.description = description
        self.dateCreated = datetime.now()
        self.dateCompleted: datetime | None = None
        self.deadline = deadline
        self.estimatedTime = estimatedTime
        self.reminders: list[Any] = []
        self.dependencies: list[Task] = []

    def markComplete(self) -> None:
        if self.isBlocked():
            raise ValueError("Cannot complete a task while it is blocked by dependencies.")

        self.dateCompleted = datetime.now()

    def addDependency(self, task: Task) -> None:
        if task is self:
            raise ValueError("A task cannot depend on itself.")

        if task in self.dependencies:
            return

        if self in task.dependencies:
            raise ValueError("This dependency would create a circular relationship.")

        self.dependencies.append(task)

    def removeDependency(self, task: Task) -> None:
        if task in self.dependencies:
            self.dependencies.remove(task)

    def isBlocked(self) -> bool:
        for dependency in self.dependencies:
            if dependency.dateCompleted is None:
                return True
        return False

    def updateDetails(self, name: str, desc: str) -> None:
        cleaned_name = name.strip()
        cleaned_desc = desc.strip()

        if not cleaned_name:
            raise ValueError("Task name cannot be empty.")

        self.name = cleaned_name
        self.description = cleaned_desc

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
            "dependencies": [dependency.taskId for dependency in self.dependencies],
        }
