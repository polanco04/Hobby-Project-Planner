from .Project import Project 
from datetime import datetime

class Hobbyist:
    def __init__(self, username: str):
        self.username = username.strip()
        self.bio: str = ""
        self.profilePicture: str = None
        self.projects: list[Project] = []
        self.projectId = 1

    def setUsername(self, username: str): 
        self.username = username.strip()

    def setBio(self, bio: str): 
        self.bio = bio

    def createProject(self, title: str, description: str, deadline: datetime) -> Project:
        if len(self.projects) >= 3:
            raise Exception("You can only have 3 projects at a time")
 
        project = Project(self.projectId, title, description, deadline)
        self.projects.append(project)
        self.projectId += 1
        return project

    def deleteProject(self, projectId: int):
        for project in self.projects:
            if project.projectId == projectId:
                self.projects.remove(project)
                break

    def setProfilePicture(self, filePath: str):
        self.profilePicture = filePath

    def allProjects(self) -> list[Project]:
        return self.projects