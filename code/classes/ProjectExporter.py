from .Project import Project

class ProjectExporter:
    def createProjectSummary(self, project: Project) -> str:
        return (
            f"Project: {project.title}\n"
            f"Description: {project.description}\n"
            f"Status: {project.status.value}\n"
            f"Progress: {project.getProgress():.1f}%\n"
            f"Deadline: {project.deadline}\n"
            f"Tasks: {len(project.completedTasks())}/{len(project.tasks)} completed\n"
            f"Milestones: {len(project.milestones)}"
        )

    def exportProjectToPDF(self, project: Project):
        pass  # implement later 

    def exportProjectToImage(self, project: Project):
        pass  # implement later