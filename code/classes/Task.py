# Task Class 

from dataclasses import dataclass
from typing import Any


VALID_PRIORITIES = {"Low", "Medium", "High"}

@dataclass
class Task:
    title: str
    description: str = ""
    priority: str = "Medium"
    completed: bool = False


    def __post_init__(self) -> None:
        self.title = self.title.strip()
        self.description = self.description.strip()
        self.priority = self.priority.strip().title()


        if not self.title:
            raise ValueError("Task title cannot be empty")
        
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority '{self.priority}'. Choose from: "
                f"{', '.join(sorted(VALID_PRIORITIES))}."
    
            )
    
    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False

    def update_details(
            self, 
            *,
            title: str | None = None,
            description: str | None = None,
            priority: str | None = None,
    ) -> None:
        
        if title is not None:
            self.description = description.strip()

        
        if priority is not None:
            cleaned_priority = priority.strip().title()
            if cleaned_priority not in VALID_PRIORITIES:
                raise ValueError (
                    f"Invalid priority '{cleaned_priority}'. Choose from: "
                    f"{', '.join(sorted(VALID_PRIORITIES))}."
                )
            self.priority = cleaned_priority

    
    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,

        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(
            title = str(data.get("title", "")),
            description = str(data.get("description", "")),
            priority = str(data.get("priority", "Medium")),
            completed = bool(data.get("completed", False)),
            
        )