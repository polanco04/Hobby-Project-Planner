from .Task import Task
from datetime import datetime

class Milestone:
    """
    Name: __init__

    INPUT:
        name:           Name of the milestone (str)
        deadline:       Deadline for the milestone (datetime)

    RETURN:
        N/A

    DESCRIPTION:
        Initializes a Milestone with a stripped name, a creation timestamp,
        a deadline, an empty task list, a None milestoneId, and
        manuallyCompleted set to False.
    """
    def __init__(self, name: str, deadline: datetime):
        self.milestoneId = None
        self.name = name.strip()
        self.createdAt = datetime.now()
        self.deadline = deadline
        self.tasks: list[Task] = []
        self.manuallyCompleted: bool = False

    """
    Name: getProgress

    INPUT:
        N/A

    RETURN:
        float:          Percentage of completed tasks (0.0 to 100.0)

    DESCRIPTION:
        Calculates and returns the completion percentage of the milestone
        based on how many of its associated tasks have a dateCompleted value.
        Returns 0.0 if there are no tasks.
    """
    def getProgress(self):
        if not self.tasks:
            return 0.0
        
        tasksCompleted = 0

        for task in self.tasks:
            if task.dateCompleted:
                tasksCompleted += 1

        return (tasksCompleted / len(self.tasks)) * 100 
    
    """
    Name: isReached

    INPUT:
        N/A

    RETURN:
        bool:           True if the milestone is reached, False otherwise

    DESCRIPTION:
        Returns True if the milestone has been manually marked complete,
        or if all associated tasks are completed (progress == 100%).
    """
    def isReached(self):
        if self.manuallyCompleted:
            return True
        
        return self.getProgress() == 100.0
    
    """
    Name: addTask

    INPUT:
        task:           Task instance to associate with this milestone (Task)

    RETURN:
        N/A

    DESCRIPTION:
        Adds a task to the milestone's task list (max 3 tasks allowed).
        Also adds this milestone to the task's milestones list if not already
        present. Raises an exception if the milestone already has 3 tasks.
    """
    def addTask(self, task: Task):
        if len(self.tasks) >= 3:
            raise Exception("Milestones cannot have more than 3 tasks")
        
        if task in self.tasks:
            return
        self.tasks.append(task)

        if self not in task.milestones:
            task.milestones.append(self)
    
    """
    Name: removeTask

    INPUT:
        task:           Task instance to disassociate from this milestone (Task)

    RETURN:
        N/A

    DESCRIPTION:
        Removes the task from the milestone's task list and removes this
        milestone from the task's milestones list, if present in each.
    """
    def removeTask(self, task):
        if task in self.tasks:
            self.tasks.remove(task)

        if self in task.milestones:
            task.milestones.remove(self)

    """
    Name: markComplete

    INPUT:
        N/A

    RETURN:
        N/A

    DESCRIPTION:
        Marks the milestone as manually completed and calls markComplete()
        on any associated tasks that have not yet been completed.
    """
    def markComplete(self):
        self.manuallyCompleted = True
        for task in self.tasks:
            if not task.dateCompleted:
                task.markComplete()

    """
    Name: unmarkComplete

    INPUT:
        N/A

    RETURN:
        N/A

    DESCRIPTION:
        Resets the milestone's manuallyCompleted flag to False, effectively
        un-completing the milestone without affecting its tasks.
    """
    def unmarkComplete(self):
        self.manuallyCompleted = False