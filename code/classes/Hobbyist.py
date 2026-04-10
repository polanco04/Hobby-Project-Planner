from Project import Project 
import datetime

class Hobbyist:
    def __init__(self, username: str):
        self.username = username
        self.bio: str = ""
        self.profilePicture: str = None
        self.projects: list[Project] = []

    def setUsername(self, username: str): 
        self.username = username

    def setBio(self, bio: str): 
        self.bio = bio

    def createProject(self, title: str, description: str, deadline: datetime) -> Project:
        if len(self.projects) >= 3:
            raise Exception("You can only have 3 projects at a time")

        projectId = len(self.projects) + 1 
        project = Project(projectId, title, description, deadline)
        self.projects.append(project)
        return project

    def deleteProject(self, projectId: int):
        for project in self.projects:
            if project.projectId == projectId:
                self.projects.remove(project)
                break

    def shareProject(self, project: Project):
        pass  # implement sharing logic later

    def allProjects(self) -> list[Project]:
        return self.projects