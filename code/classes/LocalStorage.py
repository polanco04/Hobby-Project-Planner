import sqlite3
import os
from datetime import datetime
from utils import getAppDataDir
from classes.Hobbyist import Hobbyist
from classes.Project import Project, ProjectStatus
from classes.Task import Task
from classes.Milestone import Milestone
from classes.Media import Media

class LocalStorage:
    """
    Name: __init__

    INPUT:
        N/A

    RETURN:
        N/A

    DESCRIPTION:
        Initializes the LocalStorage instance by resolving the database path,
        ensuring the app data directory exists, opening a SQLite connection with
        row factory and foreign key support enabled, and calling createTables()
        to set up the schema.
    """
    def __init__(self):
        self.dbPath = os.path.join(getAppDataDir(), "data.db")
        os.makedirs(getAppDataDir(), exist_ok=True)
        self.conn = sqlite3.connect(self.dbPath)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.createTables()

    """
    Name: createTables

    INPUT:
        N/A

    RETURN:
        N/A

    DESCRIPTION:
        Executes a SQL script that creates all required tables (hobbyist, projects,
        tasks, milestones, milestone_tasks, media) if they do not already exist.
        Commits the transaction after execution.
    """
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

    """
    Name: saveHobbyist

    INPUT:
        hobbyist:       Hobbyist instance to persist (Hobbyist)

    RETURN:
        N/A

    DESCRIPTION:
        Inserts the hobbyist record into the database or updates it if a record
        with id=1 already exists. Commits the transaction after the upsert.
    """
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

    """
    Name: loadHobbyist

    INPUT:
        N/A

    RETURN:
        hobbyist:       Reconstructed Hobbyist instance, or None if no record exists

    DESCRIPTION:
        Fetches the single hobbyist row from the database, reconstructs a Hobbyist
        object with its bio, profile picture, projectId, and full project list
        loaded via loadProjects(). Returns None if no hobbyist has been saved.
    """
    def loadHobbyist(self):
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

    """
    Name: saveProject

    INPUT:
        project:        Project instance to persist (Project)

    RETURN:
        N/A

    DESCRIPTION:
        Inserts or updates the project record in the database, then iterates
        over and saves all associated tasks, milestones, and media items.
        Commits the full transaction after all inserts/updates.
    """
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

    """
    Name: loadProjects

    INPUT:
        N/A

    RETURN:
        projects:       List of all reconstructed Project instances

    DESCRIPTION:
        Fetches all project rows from the database and reconstructs each into
        a Project object, restoring its status, progress, dates, counters,
        and related tasks, milestones, and media via their respective load methods.
    """
    def loadProjects(self):
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

    """
    Name: deleteProject

    INPUT:
        projectId:      ID of the project to delete (int)

    RETURN:
        N/A

    DESCRIPTION:
        Deletes the project row with the given projectId from the database.
        Cascading deletes handle associated tasks, milestones, and media.
        Commits the transaction after deletion.
    """
    def deleteProject(self, projectId: int):
        self.conn.execute("DELETE FROM projects WHERE projectId = ?", (projectId,))
        self.conn.commit()

    # ── Tasks ─────────────────────────────────────────────────────────────────

    """
    Name: saveTask

    INPUT:
        task:           Task instance to persist (Task)
        projectId:      ID of the project this task belongs to (int)

    RETURN:
        N/A

    DESCRIPTION:
        Inserts or updates the task record in the database using an upsert.
        Does not commit — the caller is responsible for committing the transaction.
    """
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

    """
    Name: loadTasks

    INPUT:
        projectId:      ID of the project whose tasks should be loaded (int)

    RETURN:
        tasks:          List of reconstructed Task instances for the given project

    DESCRIPTION:
        Fetches all task rows associated with the given projectId and reconstructs
        each into a Task object, restoring its taskId, dateCreated, and dateCompleted.
    """
    def loadTasks(self, projectId: int):
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

    """
    Name: deleteTask

    INPUT:
        taskId:         ID of the task to delete (int)

    RETURN:
        N/A

    DESCRIPTION:
        Deletes the task row with the given taskId from the database and commits
        the transaction. Cascading deletes handle milestone_tasks join entries.
    """
    def deleteTask(self, taskId: int):
        self.conn.execute("DELETE FROM tasks WHERE taskId = ?", (taskId,))
        self.conn.commit()

    # ── Milestones ────────────────────────────────────────────────────────────

    """
    Name: saveMilestone

    INPUT:
        milestone:      Milestone instance to persist (Milestone)
        projectId:      ID of the project this milestone belongs to (int)

    RETURN:
        N/A

    DESCRIPTION:
        Inserts or updates the milestone record in the database. Clears and
        re-inserts all milestone_tasks join entries for the milestone's associated
        tasks. Does not commit — the caller is responsible for committing.
    """
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

        self.conn.execute(
            "DELETE FROM milestone_tasks WHERE milestoneId = ?", (milestone.milestoneId,)
        )
        for task in milestone.tasks:
            self.conn.execute(
                "INSERT OR IGNORE INTO milestone_tasks (milestoneId, taskId) VALUES (?, ?)",
                (milestone.milestoneId, task.taskId)
            )

    """
    Name: loadMilestones

    INPUT:
        projectId:      ID of the project whose milestones should be loaded (int)
        tasks:          List of already-loaded Task instances for the project (list)

    RETURN:
        milestones:     List of reconstructed Milestone instances for the given project

    DESCRIPTION:
        Fetches all milestone rows for the given projectId and reconstructs each
        into a Milestone object. Resolves associated tasks from the milestone_tasks
        join table using the provided task list, and links each task and milestone
        bidirectionally.
    """
    def loadMilestones(self, projectId: int, tasks: list):
        rows = self.conn.execute(
            "SELECT * FROM milestones WHERE projectId = ?", (projectId,)
        ).fetchall()

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

            linkedTaskIds = self.conn.execute(
                "SELECT taskId FROM milestone_tasks WHERE milestoneId = ?",
                (milestone.milestoneId,)
            ).fetchall()

            for taskRow in linkedTaskIds:
                task = taskMap.get(taskRow["taskId"])
                if task:
                    if milestone not in task.milestones:
                        task.milestones.append(milestone)
                    if task not in milestone.tasks:
                        milestone.tasks.append(task)

            milestones.append(milestone)
        return milestones

    """
    Name: deleteMilestone

    INPUT:
        milestoneId:    ID of the milestone to delete (int)

    RETURN:
        N/A

    DESCRIPTION:
        Deletes the milestone row with the given milestoneId from the database
        and commits the transaction. Cascading deletes handle milestone_tasks entries.
    """
    def deleteMilestone(self, milestoneId: int):
        self.conn.execute("DELETE FROM milestones WHERE milestoneId = ?", (milestoneId,))
        self.conn.commit()

    # ── Media ─────────────────────────────────────────────────────────────────

    """
    Name: saveMedia

    INPUT:
        media:          Media instance to persist (Media)
        projectId:      ID of the project this media belongs to (int)

    RETURN:
        N/A

    DESCRIPTION:
        Inserts or updates the media record in the database using an upsert.
        Does not commit — the caller is responsible for committing the transaction.
    """
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

    """
    Name: loadMedia

    INPUT:
        projectId:      ID of the project whose media should be loaded (int)

    RETURN:
        mediaList:      List of reconstructed Media instances for the given project

    DESCRIPTION:
        Fetches all media rows associated with the given projectId and reconstructs
        each into a Media object, restoring its mediaId and uploadedAt timestamp.
    """
    def loadMedia(self, projectId: int):
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

    """
    Name: deleteMedia

    INPUT:
        mediaId:        ID of the media item to delete (int)

    RETURN:
        N/A

    DESCRIPTION:
        Deletes the media row with the given mediaId from the database and commits
        the transaction. The associated file on disk is not removed here.
    """
    def deleteMedia(self, mediaId: int):
        self.conn.execute("DELETE FROM media WHERE mediaId = ?", (mediaId,))
        self.conn.commit()

    """
    Name: close

    INPUT:
        N/A

    RETURN:
        N/A

    DESCRIPTION:
        Closes the SQLite database connection. Should be called when the
        application is shutting down or the storage instance is no longer needed.
    """
    def close(self):
        self.conn.close()