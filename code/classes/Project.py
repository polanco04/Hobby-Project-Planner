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
    def __init__(self, projectId: int, title: str, description: str, deadline: datetime):
        self.projectId = projectId
        self.title = title.strip()
        self.description = description.strip()
        self.deadline = deadline
        self.status = ProjectStatus.PLANNING
        self.progress = 0.0
        self.dateCreated = datetime.now()
        self.dateCompleted: datetime = None
        self.milestones: list[Milestone] = []
        self.tasks: list[Task] = []
        self.media: list[Media] = []

    def addTask(self, task: Task):
        # 15 tasks since theres only 5 milestones per project, 
        # and each milestone can only have 3 tasks per milestone
        if self.tasks >= 15:
            raise Exception("Cannot have more than 15 tasks")
        self.tasks.append(task)

    def removeTask(self, taskId: int):
        if self.tasks:
            for task in self.tasks:
                if task.taskId == taskId:
                    self.tasks.remove(task)
                    break
        else:
             raise Exception("You have no tasks") 
    
    def addMilestone(self, milestone: Milestone):
        if self.milestones >= 5:
            raise Exception("Cannot have more than 5 milestones")
        
        self.milestones.append(milestone)
    
    def removeMilestone(self, milestoneId: int):
        if self.milestones:
            for milestone in self.milestones:
                if milestone.milestoneId == milestoneId:
                    self.milestones.remove(milestone)
                    break
        else:
            raise Exception("You have no Milestones")
    
    def addMedia(self, media: Media):
        if self.media >= 3:
            raise Exception("Cannot have more than 3 photos")
        self.media.append(media)

    def removeMedia(self, mediaId: int):
        if self.media:
            for media in self.media:
                if media.mediaId == mediaId:
                    self.media.remove(media)
                    break
        else:
            raise Exception("You have no media")

    def editProject(self, title: str = None, description: str = None, deadline: datetime = None):
        if title: 
            self.title = title.strip()
        if description:
            self.description = description.strip()
        if deadline:
            self.deadline = deadline

    def getProgress(self) -> float:
        if not self.tasks:
            return 0.0
        
        tasksCompleted = 0

        for task in self.tasks:
            if task.dateCompleted:
                tasksCompleted += 1

        self.progress = (tasksCompleted / len(self.tasks)) * 100

        return self.progress 
    
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