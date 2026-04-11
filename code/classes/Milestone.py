from Task import Task
import datetime

class Milestone:
    def __init__(self, milestoneId: int, name: str, deadline: datetime):
        self.milestoneId = milestoneId
        self.name = name.strip()
        self.progress = 0.0
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

        self.progress = (tasksCompleted / len(self.tasks)) * 100

        return self.progress 
    
    def isReached(self):
        if self.progress == 100:
            return True
        
        return False
    
    def addTask(self, task: Task):
        if len(self.tasks) >= 3:
            raise Exception("Milestones cannot have more than 3 tasks")
        self.tasks.append(task)
    
    def markComplete(self):
        # this would be some GUI thing i think
        return
