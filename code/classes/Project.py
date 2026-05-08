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
    """
    Name: __init__

    INPUT:
        projectId:      Unique identifier for the project (int)
        title:          Title of the project (str)
        description:    Description of the project (str)
        deadline:       Deadline for the project (datetime)

    RETURN:
        N/A

    DESCRIPTION:
        Initializes a Project with the given ID, stripped title and description,
        deadline, default status of PLANNING, 0.0 progress, a creation timestamp,
        and empty lists for milestones, tasks, and media.
    """
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

    """
    Name: addTask

    INPUT:
        task:           Task instance to add to the project (Task)

    RETURN:
        N/A

    DESCRIPTION:
        Assigns a unique taskId to the task (based on projectId and internal counter),
        appends it to the project's task list, and increments the taskId counter.
        Raises an exception if the project already has 15 tasks.
    """
    def addTask(self, task: Task):
        # 15 tasks since theres only 5 milestones per project, 
        # and each milestone can only have 3 tasks per milestone
        if len(self.tasks) >= 15:
            raise Exception("Cannot have more than 15 tasks")
        
        task.taskId = self.projectId * 1000 + self.taskId
        self.taskId += 1
        self.tasks.append(task)

    """
    Name: removeTask

    INPUT:
        taskId:         ID of the task to remove (int)

    RETURN:
        N/A

    DESCRIPTION:
        Searches the project's task list for a task matching the given taskId
        and removes it. Raises an exception if no matching task is found.
    """
    def removeTask(self, taskId: int):
        for task in self.tasks:
            if task.taskId == taskId:
                self.tasks.remove(task)
                return
            
        raise Exception(f"Task {taskId} not found")
    
    """
    Name: addMilestone

    INPUT:
        milestone:      Milestone instance to add to the project (Milestone)

    RETURN:
        N/A

    DESCRIPTION:
        Assigns a unique milestoneId to the milestone (based on projectId and
        internal counter), appends it to the project's milestone list, and
        increments the milestoneId counter. Raises an exception if the project
        already has 5 milestones.
    """
    def addMilestone(self, milestone: Milestone):
        if len(self.milestones) >= 5:
            raise Exception("Cannot have more than 5 milestones")
        
        milestone.milestoneId = self.projectId * 1000 + self.milestoneId
        self.milestoneId += 1
        self.milestones.append(milestone)
    
    """
    Name: removeMilestone

    INPUT:
        milestoneId:    ID of the milestone to remove (int)

    RETURN:
        N/A

    DESCRIPTION:
        Searches the project's milestone list for a milestone matching the given
        milestoneId and removes it. Raises an exception if no match is found.
    """
    def removeMilestone(self, milestoneId: int):
        for milestone in self.milestones:
            if milestone.milestoneId == milestoneId:
                self.milestones.remove(milestone)
                return
        raise Exception(f"Milestone {milestoneId} not found")
    
    """
    Name: addMedia

    INPUT:
        media:          Media instance to add to the project (Media)

    RETURN:
        N/A

    DESCRIPTION:
        Assigns a unique mediaId to the media item (based on projectId and
        internal counter), appends it to the project's media list, and
        increments the mediaId counter. Raises an exception if the project
        already has 6 media items.
    """
    def addMedia(self, media: Media):
        if len(self.media) >= 6:
            raise Exception("Cannot have more than 6 photos")
        
        media.mediaId = self.projectId * 1000 + self.mediaId
        self.mediaId += 1
        self.media.append(media)

    """
    Name: removeMedia

    INPUT:
        mediaId:        ID of the media item to remove (int)

    RETURN:
        N/A

    DESCRIPTION:
        Searches the project's media list for an item matching the given mediaId
        and removes it. Raises an exception if no matching media is found.
    """
    def removeMedia(self, mediaId: int):
        for media in self.media:
            if media.mediaId == mediaId:
                self.media.remove(media)
                return
        raise Exception(f"Media {mediaId} not found")

    """
    Name: editProject

    INPUT:
        title:          New title for the project, optional (str)
        description:    New description for the project, optional (str)
        deadline:       New deadline for the project, optional (datetime)

    RETURN:
        N/A

    DESCRIPTION:
        Updates any combination of the project's title, description, and deadline.
        Only fields provided with truthy values are updated; others remain unchanged.
    """
    def editProject(self, title: str = None, description: str = None, deadline: datetime = None):
        if title: 
            self.title = title.strip()
        if description:
            self.description = description.strip()
        if deadline:
            self.deadline = deadline

    """
    Name: getProgress

    INPUT:
        N/A

    RETURN:
        float:          Percentage of completed tasks (0.0 to 100.0)

    DESCRIPTION:
        Calculates project progress as a percentage of completed tasks.
        Also updates the project's status based on progress — COMPLETED at 100%,
        IN_PROGRESS above 0%, or PLANNING otherwise. Sets dateCompleted on first
        completion. Does not change status if the project is ON_HOLD.
    """
    def getProgress(self) -> float:
        if not self.tasks:
            return 0.0
        
        tasksCompleted = sum(1 for t in self.tasks if t.dateCompleted)
        self.progress = (tasksCompleted / len(self.tasks)) * 100

        if self.status != ProjectStatus.ON_HOLD:
            if self.progress == 100:
                self.status = ProjectStatus.COMPLETED
                if not self.dateCompleted:
                    self.dateCompleted = datetime.now()
            elif self.progress > 0:
                self.status = ProjectStatus.IN_PROGRESS
            else:
                self.status = ProjectStatus.PLANNING

        return self.progress
    
    """
    Name: completedTasks

    INPUT:
        N/A

    RETURN:
        completed:      List of Task instances that have been completed

    DESCRIPTION:
        Iterates over the project's task list and returns only those tasks
        that have a non-None dateCompleted value.
    """
    def completedTasks(self):
        completed = []

        for task in self.tasks:
            if task.dateCompleted:
                completed.append(task)

        return completed
    
  