from .Project import Project 
from datetime import datetime

class Hobbyist:
    """
    Name: __init__

    INPUT:
        username:       The hobbyist's display name (str)

    RETURN:
        N/A

    DESCRIPTION:
        Initializes a Hobbyist instance with a stripped username, empty bio,
        no profile picture, an empty project list, and a starting project ID of 1.
    """
    def __init__(self, username: str):
        self.username = username.strip()
        self.bio: str = ""
        self.profilePicture: str = None
        self.projects: list[Project] = []
        self.projectId = 1

    """
    Name: setUsername

    INPUT:
        username:       New username to assign to the hobbyist (str)

    RETURN:
        N/A

    DESCRIPTION:
        Strips whitespace from the provided username and assigns it
        to the hobbyist's username field.
    """
    def setUsername(self, username: str): 
        self.username = username.strip()

    """
    Name: setBio

    INPUT:
        bio:            Biography text to assign to the hobbyist (str)

    RETURN:
        N/A

    DESCRIPTION:
        Sets the hobbyist's bio to the provided string.
    """
    def setBio(self, bio: str): 
        self.bio = bio

    """
    Name: createProject

    INPUT:
        title:          Title of the new project (str)
        description:    Description of the new project (str)
        deadline:       Deadline for the new project (datetime)

    RETURN:
        project:        The newly created Project instance

    DESCRIPTION:
        Creates a new Project with the current projectId and appends it to the
        hobbyist's project list. Raises an exception if the hobbyist already
        has 3 projects. Increments projectId after creation.
    """
    def createProject(self, title: str, description: str, deadline: datetime) -> Project:
        if len(self.projects) >= 3:
            raise Exception("You can only have 3 projects at a time")
 
        project = Project(self.projectId, title, description, deadline)
        self.projects.append(project)
        self.projectId += 1
        return project

    """
    Name: deleteProject

    INPUT:
        projectId:      ID of the project to remove (int)

    RETURN:
        N/A

    DESCRIPTION:
        Searches the hobbyist's project list for a project matching the given
        projectId and removes it. Stops after the first match is found.
    """
    def deleteProject(self, projectId: int):
        for project in self.projects:
            if project.projectId == projectId:
                self.projects.remove(project)
                break

    """
    Name: setProfilePicture

    INPUT:
        filePath:       File path to the profile picture image (str)

    RETURN:
        N/A

    DESCRIPTION:
        Sets the hobbyist's profile picture to the provided file path.
    """
    def setProfilePicture(self, filePath: str):
        self.profilePicture = filePath

    """
    Name: allProjects

    INPUT:
        N/A

    RETURN:
        projects:       List of all Project instances belonging to the hobbyist

    DESCRIPTION:
        Returns the full list of projects associated with this hobbyist.
    """
    def allProjects(self) -> list[Project]:
        return self.projects