from datetime import datetime
from typing import Any

class Task:
    """
    Name: __init__

    INPUT:
        name:           Name of the task (str)
        description:    Description of the task (str)
        deadline:       Deadline for the task (datetime)
        estimatedTime:  Estimated time to complete the task in minutes (int)

    RETURN:
        N/A

    DESCRIPTION:
        Initializes a Task with a stripped name and description, a creation timestamp,
        no completion date, the given deadline and estimated time, and empty lists
        for dependencies, and milestones. Raises ValueError if the name
        is empty or estimatedTime is negative.
    """
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
        self.milestones: list = [] 

    """
    Name: markComplete

    INPUT:
        N/A

    RETURN:
        N/A

    DESCRIPTION:
        Marks the task as completed by setting dateCompleted to the current time.
        Also checks each associated milestone and clears manuallyCompleted if all
        milestone tasks are now done.
    """
    def markComplete(self) -> None:
        self.dateCompleted = datetime.now()

        for milestone in self.milestones:
            if not milestone.manuallyCompleted and milestone.getProgress() == 100.0:
                milestone.manuallyCompleted = False

    """
    Name: unmarkComplete

    INPUT:
        N/A

    RETURN:
        N/A

    DESCRIPTION:
        Resets the task's dateCompleted to None, effectively un-completing
        the task without modifying any associated milestones or dependencies.
    """
    def unmarkComplete(self) -> None:
        self.dateCompleted = None

    """
    Name: updateDetails

    INPUT:
        name:           New name for the task (str)
        desc:           New description for the task (str)

    RETURN:
        N/A

    DESCRIPTION:
        Updates the task's name and description after stripping whitespace.
        Raises ValueError if the cleaned name is empty.
    """
    def updateDetails(self, name: str, desc: str) -> None:
        cleanedName = name.strip()

        if not cleanedName:
            raise ValueError("Task name cannot be empty.")

        self.name = cleanedName
        self.description = desc.strip()
