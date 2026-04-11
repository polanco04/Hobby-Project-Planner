from enum import Enum
from .Milestone import Milestone
from .Task import Task
from .Media import Media
from datetime import datetime

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
        self.taskId = 1
        self.milestoneId = 1
        self.mediaId = 1
        self.milestones: list[Milestone] = []
        self.tasks: list[Task] = []
        self.media: list[Media] = []

    def addTask(self, task: Task):
        # 15 tasks since theres only 5 milestones per project, 
        # and each milestone can only have 3 tasks per milestone
        if len(self.tasks) >= 15:
            raise Exception("Cannot have more than 15 tasks")
        
        task.taskId = self.taskId
        self.taskId += 1
        self.tasks.append(task)

    def removeTask(self, taskId: int):
        for task in self.tasks:
            if task.taskId == taskId:
                self.tasks.remove(task)
                return
            
        raise Exception(f"Task {taskId} not found")
    
    def addMilestone(self, milestone: Milestone):
        if len(self.milestones) >= 5:
            raise Exception("Cannot have more than 5 milestones")
        
        milestone.milestoneId = self.milestoneId
        self.milestoneId += 1
        self.milestones.append(milestone)
    
    def removeMilestone(self, milestoneId: int):
        for milestone in self.milestones:
            if milestone.milestoneId == milestoneId:
                self.milestones.remove(milestone)
                return
        raise Exception(f"Milestone {milestoneId} not found")
    
    def addMedia(self, media: Media):
        if len(self.media) >= 3:
            raise Exception("Cannot have more than 3 photos")
        
        media.mediaId = self.mediaId
        self.mediaId += 1
        self.media.append(media)

    def removeMedia(self, mediaId: int):
        for media in self.media:
            if media.mediaId == mediaId:
                self.media.remove(media)
                return
        raise Exception(f"Media {mediaId} not found")

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