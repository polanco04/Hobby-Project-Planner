from .Task import Task
from datetime import datetime

class Milestone:
    def __init__(self, name: str, deadline: datetime):
        self.milestoneId = None
        self.name = name.strip()
        self.createdAt = datetime.now()
        self.deadline = deadline
        self.tasks: list[Task] = []
        self.manuallyCompleted: bool = False

    def getProgress(self):
        if not self.tasks:
            return 0.0
        
        tasksCompleted = 0

        for task in self.tasks:
            if task.dateCompleted:
                tasksCompleted += 1

        return (tasksCompleted / len(self.tasks)) * 100 
    
    def isReached(self):
        if self.manuallyCompleted:
            return True
        
        return self.getProgress() == 100.0
    
    def addTask(self, task: Task):
        if len(self.tasks) >= 3:
            raise Exception("Milestones cannot have more than 3 tasks")
        
        if task in self.tasks:
            return
        self.tasks.append(task)

        if self not in task.milestones:
            task.milestones.append(self)
    
    def removeTask(self, task):
        if task in self.tasks:
            self.tasks.remove(task)

        if self in task.milestones:
            task.milestones.remove(self)

    def markComplete(self):
        self.manuallyCompleted = True
        for task in self.tasks:
            if not task.dateCompleted:
                task.markComplete()

    def unmarkComplete(self):
        self.manuallyCompleted = False