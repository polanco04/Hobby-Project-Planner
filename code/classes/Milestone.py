# Milestones class

from .Task import Task
from datetime import datetime

class Milestone:
    def __init__(self, name: str, deadline: datetime):
        self.milestoneId = None
        self.name = name.strip()
        self.createdAt = datetime.now()
        self.deadline = deadline
        self.tasks: list[Task] = []

    def getProgress(self):
        if not self.tasks:
            return 0.0
        
        tasksCompleted = 0

        for task in self.tasks:
            if task.dateCompleted:
                tasksCompleted += 1

        return (tasksCompleted / len(self.tasks)) * 100 
    
    def isReached(self):
        return self.getProgress() == 100.0
    
    def addTask(self, task: Task):
        if len(self.tasks) >= 3:
            raise Exception("Milestones cannot have more than 3 tasks")
        self.tasks.append(task)
    
    def markComplete(self):
        for task in self.tasks:
            if not task.dateCompleted:
                task.markComplete()