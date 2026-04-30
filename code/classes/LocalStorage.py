import sqlite3
import os
from datetime import datetime
from utils import getAppDataDir

class LocalStorage:
    def __init__(self):
        self.dbPath = os.path.join(getAppDataDir(), "data.db")
        os.makedirs(getAppDataDir(), exist_ok=True)
        self.conn = sqlite3.connect(self.dbPath)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.createTables()

    def createTables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS hobbyist (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                username TEXT NOT NULL,
                bio TEXT DEFAULT '',
                profilePicture TEXT,
                projectId INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS projects (
                projectId INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'planning',
                progress REAL DEFAULT 0.0,
                dateCreated TEXT,
                dateCompleted TEXT,
                deadline TEXT,
                taskId INTEGER DEFAULT 1,
                milestoneId INTEGER DEFAULT 1,
                mediaId INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS tasks (
                taskId INTEGER PRIMARY KEY,
                projectId INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                dateCreated TEXT,
                dateCompleted TEXT,
                deadline TEXT,
                estimatedTime INTEGER DEFAULT 0,
                FOREIGN KEY (projectId) REFERENCES projects(projectId) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS milestones (
                milestoneId INTEGER PRIMARY KEY,
                projectId INTEGER NOT NULL,
                name TEXT NOT NULL,
                createdAt TEXT,
                deadline TEXT,
                manuallyCompleted INTEGER DEFAULT 0,
                FOREIGN KEY (projectId) REFERENCES projects(projectId) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS milestone_tasks (
                milestoneId INTEGER NOT NULL,
                taskId INTEGER NOT NULL,
                PRIMARY KEY (milestoneId, taskId),
                FOREIGN KEY (milestoneId) REFERENCES milestones(milestoneId) ON DELETE CASCADE,
                FOREIGN KEY (taskId) REFERENCES tasks(taskId) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS media (
                mediaId INTEGER PRIMARY KEY,
                projectId INTEGER NOT NULL,
                filePath TEXT NOT NULL,
                description TEXT DEFAULT '',
                uploadedAt TEXT,
                FOREIGN KEY (projectId) REFERENCES projects(projectId) ON DELETE CASCADE
            );
        """)
        self.conn.commit()

    # ── Hobbyist ──────────────────────────────────────────────────────────────

    def saveHobbyist(self, hobbyist):
        self.conn.execute("""
            INSERT INTO hobbyist (id, username, bio, profilePicture, projectId)
            VALUES (1, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                username = excluded.username,
                bio = excluded.bio,
                profilePicture = excluded.profilePicture,
                projectId = excluded.projectId
        """, (
            hobbyist.username,
            hobbyist.bio,
            hobbyist.profilePicture,
            hobbyist.projectId
        ))
        self.conn.commit()

    def loadHobbyist(self):
        from classes.Hobbyist import Hobbyist
        row = self.conn.execute("SELECT * FROM hobbyist WHERE id = 1").fetchone()
        if not row:
            return None
        hobbyist = Hobbyist(row["username"])
        hobbyist.bio = row["bio"] or ""
        hobbyist.profilePicture = row["profilePicture"]
        hobbyist.projectId = row["projectId"]
        hobbyist.projects = self.loadProjects()
        return hobbyist

    # ── Projects ──────────────────────────────────────────────────────────────

    def saveProject(self, project):
        self.conn.execute("""
            INSERT INTO projects
                (projectId, title, description, status, progress,
                 dateCreated, dateCompleted, deadline, taskId, milestoneId, mediaId)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(projectId) DO UPDATE SET
                title = excluded.title,
                description = excluded.description,
                status = excluded.status,
                progress = excluded.progress,
                dateCreated = excluded.dateCreated,
                dateCompleted = excluded.dateCompleted,
                deadline = excluded.deadline,
                taskId = excluded.taskId,
                milestoneId = excluded.milestoneId,
                mediaId = excluded.mediaId
        """, (
            project.projectId,
            project.title,
            project.description,
            project.status.value,
            project.progress,
            project.dateCreated.isoformat(),
            project.dateCompleted.isoformat() if project.dateCompleted else None,
            project.deadline.isoformat() if hasattr(project.deadline, 'isoformat') else str(project.deadline),
            project.taskId,
            project.milestoneId,
            project.mediaId
        ))

        for task in project.tasks:
            self.saveTask(task, project.projectId)

        for milestone in project.milestones:
            self.saveMilestone(milestone, project.projectId)

        for media in project.media:
            self.saveMedia(media, project.projectId)

        self.conn.commit()

    def loadProjects(self):
        from classes.Project import Project, ProjectStatus
        rows = self.conn.execute("SELECT * FROM projects").fetchall()
        projects = []
        for row in rows:
            project = Project(
                row["projectId"],
                row["title"],
                row["description"],
                datetime.fromisoformat(row["deadline"])
            )
            project.status = ProjectStatus(row["status"])
            project.progress = row["progress"]
            project.dateCreated = datetime.fromisoformat(row["dateCreated"])
            project.dateCompleted = datetime.fromisoformat(row["dateCompleted"]) if row["dateCompleted"] else None
            project.taskId = row["taskId"]
            project.milestoneId = row["milestoneId"]
            project.mediaId = row["mediaId"]
            project.tasks = self.loadTasks(row["projectId"])
            project.milestones = self.loadMilestones(row["projectId"], project.tasks)
            project.media = self.loadMedia(row["projectId"])
            projects.append(project)
        return projects

    def deleteProject(self, projectId: int):
        self.conn.execute("DELETE FROM projects WHERE projectId = ?", (projectId,))
        self.conn.commit()

    # ── Tasks ─────────────────────────────────────────────────────────────────

    def saveTask(self, task, projectId: int):
        self.conn.execute("""
            INSERT INTO tasks
                (taskId, projectId, name, description, dateCreated, dateCompleted, deadline, estimatedTime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(taskId) DO UPDATE SET
                name = excluded.name,
                description = excluded.description,
                dateCreated = excluded.dateCreated,
                dateCompleted = excluded.dateCompleted,
                deadline = excluded.deadline,
                estimatedTime = excluded.estimatedTime
        """, (
            task.taskId,
            projectId,
            task.name,
            task.description,
            task.dateCreated.isoformat(),
            task.dateCompleted.isoformat() if task.dateCompleted else None,
            task.deadline.isoformat() if hasattr(task.deadline, 'isoformat') else str(task.deadline),
            task.estimatedTime
        ))

    def loadTasks(self, projectId: int):
        from classes.Task import Task
        rows = self.conn.execute(
            "SELECT * FROM tasks WHERE projectId = ?", (projectId,)
        ).fetchall()
        tasks = []
        for row in rows:
            task = Task(
                row["name"],
                row["description"],
                datetime.fromisoformat(row["deadline"]),
                row["estimatedTime"]
            )
            task.taskId = row["taskId"]
            task.dateCreated = datetime.fromisoformat(row["dateCreated"])
            task.dateCompleted = datetime.fromisoformat(row["dateCompleted"]) if row["dateCompleted"] else None
            tasks.append(task)
        return tasks

    def deleteTask(self, taskId: int):
        self.conn.execute("DELETE FROM tasks WHERE taskId = ?", (taskId,))
        self.conn.commit()

    # ── Milestones ────────────────────────────────────────────────────────────

    def saveMilestone(self, milestone, projectId: int):
        self.conn.execute("""
            INSERT INTO milestones
                (milestoneId, projectId, name, createdAt, deadline, manuallyCompleted)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(milestoneId) DO UPDATE SET
                name = excluded.name,
                createdAt = excluded.createdAt,
                deadline = excluded.deadline,
                manuallyCompleted = excluded.manuallyCompleted
        """, (
            milestone.milestoneId,
            projectId,
            milestone.name,
            milestone.createdAt.isoformat(),
            milestone.deadline.isoformat(),
            1 if milestone.manuallyCompleted else 0
        ))

        # save milestone-task links
        self.conn.execute(
            "DELETE FROM milestone_tasks WHERE milestoneId = ?", (milestone.milestoneId,)
        )
        for task in milestone.tasks:
            self.conn.execute(
                "INSERT OR IGNORE INTO milestone_tasks (milestoneId, taskId) VALUES (?, ?)",
                (milestone.milestoneId, task.taskId)
            )

    def loadMilestones(self, projectId: int, tasks: list):
        from classes.Milestone import Milestone
        rows = self.conn.execute(
            "SELECT * FROM milestones WHERE projectId = ?", (projectId,)
        ).fetchall()

        # build a taskId lookup so we can reuse the same task objects
        taskMap = {t.taskId: t for t in tasks}

        milestones = []
        for row in rows:
            milestone = Milestone(
                row["name"],
                datetime.fromisoformat(row["deadline"])
            )
            milestone.milestoneId = row["milestoneId"]
            milestone.createdAt = datetime.fromisoformat(row["createdAt"])
            milestone.manuallyCompleted = bool(row["manuallyCompleted"])

            # link tasks using the junction table
            linkedTaskIds = self.conn.execute(
                "SELECT taskId FROM milestone_tasks WHERE milestoneId = ?",
                (milestone.milestoneId,)
            ).fetchall()

            for taskRow in linkedTaskIds:
                task = taskMap.get(taskRow["taskId"])
                if task:
                    # use the class method to keep both sides in sync
                    if milestone not in task.milestones:
                        task.milestones.append(milestone)
                    if task not in milestone.tasks:
                        milestone.tasks.append(task)

            milestones.append(milestone)
        return milestones

    def deleteMilestone(self, milestoneId: int):
        self.conn.execute("DELETE FROM milestones WHERE milestoneId = ?", (milestoneId,))
        self.conn.commit()

    # ── Media ─────────────────────────────────────────────────────────────────

    def saveMedia(self, media, projectId: int):
        self.conn.execute("""
            INSERT INTO media
                (mediaId, projectId, filePath, description, uploadedAt)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(mediaId) DO UPDATE SET
                filePath = excluded.filePath,
                description = excluded.description,
                uploadedAt = excluded.uploadedAt
        """, (
            media.mediaId,
            projectId,
            media.filePath,
            media.description,
            media.uploadedAt.isoformat()
        ))

    def loadMedia(self, projectId: int):
        from classes.Media import Media
        rows = self.conn.execute(
            "SELECT * FROM media WHERE projectId = ?", (projectId,)
        ).fetchall()
        mediaList = []
        for row in rows:
            m = Media(row["filePath"], row["description"])
            m.mediaId = row["mediaId"]
            m.uploadedAt = datetime.fromisoformat(row["uploadedAt"])
            mediaList.append(m)
        return mediaList

    def deleteMedia(self, mediaId: int):
        self.conn.execute("DELETE FROM media WHERE mediaId = ?", (mediaId,))
        self.conn.commit()

    def close(self):
        self.conn.close()