from enum import Enum
from Milestone import Milestone
from Task import Task
from Media import Media
import datetime

class ProjectStatus(Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"

class Project:
    def __init__(self, projectId, title, description, deadline):
        self.projectId = projectId
        self.title = title
        self.description = description
        self.deadline = deadline
        self.status = ProjectStatus.PLANNING
        self.progress = 0.0
        self.dateCreated = datetime.now()
        self.dateCompleted: datetime = None
        self.milestones: list[Milestone] = []
        self.tasks: list[Task] = []
        self.media: list[Media] = []

    def addTask(self, task: Task):
        self.tasks.append(task)

    def removeTask(self, taskId: int):
        for task in self.tasks:
            if task.taskId == taskId:
                self.tasks.remove(task)
                break
    
    def addMilestone(self, milestone: Milestone):
        self.milestones.append(milestone)
    
    def removeMilestone(self, milestoneId: int):
        for milestone in self.milestones:
            if milestone.milestoneId == milestoneId:
                self.milestones.remove(milestone)
                break
    
    def addMedia(self, media: Media):
        self.media.append(media)

    def removeMedia(self, mediaId: int):
        for media in self.media:
            if media.mediaId == mediaId:
                self.media.remove(media)
                break

    def editProject(self, title: str = None, description: str = None, deadline: datetime = None):
        if title: 
            self.title = title
        if description:
            self.description = description
        if deadline:
            self.deadline = deadline

    def getProgress(self) -> float:
        if not self.tasks:
            return 0.0
        
        tasksCompleted = 0

        for task in self.tasks:
            if task.dateCompleted:
                tasksCompleted += 1

        completed = (tasksCompleted / len(self.tasks)) * 100

        return completed 
    
    def completedTasks(self):
        completed = []

        for task in self.tasks:
            if task.dateCompleted:
                completed.append(task)

        return completed
    
    def pendingTasks(self):
        pending = []

        for task in self.tasks:
            if not task.dateCompleted:
                pending.append(task)
        
        return pending