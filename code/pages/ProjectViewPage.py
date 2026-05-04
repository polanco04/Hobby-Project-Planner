### Project View Page 
## This page will show the details of a specific project when selected within the
## Projects pages.
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QStackedWidget, QWidget, QVBoxLayout,
    QCheckBox, QFileDialog, QGridLayout, QDateEdit,
    QDialog, QDialogButtonBox, QLineEdit, QLayout
)
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import QEvent, Qt, QDate, QRectF, QSizeF, QMarginsF, QPointF 
from PyQt6.QtGui import (
    QFont, QPixmap, QPainter, QPageSize, QColor, 
    QPainterPath, QPen, QImage, QPageSize, QPolygonF 
    )
from PyQt6.QtPrintSupport import QPrinter
from qfluentwidgets import (
    SubtitleLabel, BodyLabel, StrongBodyLabel, CardWidget,
    PrimaryPushButton, LineEdit, InfoBar, InfoBarPosition, isDarkTheme,
    CheckBox, ScrollArea, qconfig 
)
from classes.Task import Task
from classes.Milestone import Milestone
from classes.Media import Media
from datetime import datetime
from pathlib import Path
from utils import getAppDataDir

class projectViewPage(QWidget):
    def __init__(self, storage=None):
        super().__init__()

        self.project = None
        self.storage = storage
        self.setObjectName("projectViewPage")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        topLayout = QHBoxLayout()
        topLayout.setSpacing(12)

        self.backButton = QPushButton("←")
        self.backButton.setToolTip("Back to Projects")
        self.backButton.clicked.connect(self.goBackToProjects)
        backFont = QFont()
        backFont.setPointSize(14)
        backFont.setBold(True)
        self.backButton.setFont(backFont)
        self.backButton.setFixedWidth(24)
        self.backButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.backButton.setFlat(True)

        textLayout = QVBoxLayout()
        textLayout.setSpacing(4)
        textLayout.setContentsMargins(0, 0, 0, 0)

        self.projectTitle = SubtitleLabel("Project Title")
        self.projectDescription = BodyLabel("Project Description")
        self.projectDescription.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        textLayout.addWidget(self.projectTitle)
        textLayout.addWidget(self.projectDescription)

        topLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignTop)
        topLayout.addLayout(textLayout)
        topLayout.addStretch()
        layout.addLayout(topLayout)

        self.tabsWidget = QFrame()
        self.tabsWidget.setObjectName("tabsWidget")
        self.tabsLayout = QHBoxLayout(self.tabsWidget)
        self.tabsLayout.setSpacing(10)
        self.tabsLayout.setContentsMargins(8, 8, 8, 8)

        self.taskTab = QPushButton("Tasks")
        self.milestonesTab = QPushButton("Milestones")
        self.imagesTab = QPushButton("Images")
        self.exportTab = QPushButton("Export")
        self.tabButtons = [self.taskTab, self.milestonesTab, self.imagesTab, self.exportTab]

        for button in self.tabButtons:
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(42)
            self.tabsLayout.addWidget(button)

        layout.addWidget(self.tabsWidget)

        self.contentStack = QStackedWidget()
        self.taskPage = self.createTasksTab()
        self.milestonesPage = self.createMilestonesTab()
        self.imagesPage = self.createImagesTab()
        self.exportPage = self.createExportTab()

        self.contentStack.addWidget(self.taskPage)
        self.contentStack.addWidget(self.milestonesPage)
        self.contentStack.addWidget(self.imagesPage)
        self.contentStack.addWidget(self.exportPage)

        layout.addWidget(self.contentStack, 1) 

        self.taskTab.clicked.connect(lambda: self.setActiveTab(0))
        self.milestonesTab.clicked.connect(lambda: self.setActiveTab(1))
        self.imagesTab.clicked.connect(lambda: self.setActiveTab(2))
        self.exportTab.clicked.connect(lambda: self.setActiveTab(3))

        self.setLayout(layout)
        self.applyThemeColors()
        self.setActiveTab(0)

    # ─── Theme ────────────────────────────────────────────────────────────────

    def assignBtnStyle(self):
        if isDarkTheme():
            return (
                "QPushButton { color: #FFFFFF; border: 1px solid #CFCFCF; border-radius: 6px;"
                "padding: 2px 8px; font-size: 11px; background: transparent; }"
                "QPushButton:hover { background: rgba(255,255,255,0.10); }"
            )
        else:
            return (
                "QPushButton { color: #202020; border: 1px solid #909090; border-radius: 6px;"
                "padding: 2px 8px; font-size: 11px; background: transparent; }"
                "QPushButton:hover { background: rgba(32,32,32,0.08); }"
            )

    def deleteBtnStyle(self):
        return (
            "QPushButton { color: #CC4444; border: 1px solid #CC4444; border-radius: 6px;"
            "font-size: 11px; background: transparent; }"
            "QPushButton:hover { background: rgba(204,68,68,0.10); }"
        )

    def applyThemeColors(self):
        if isDarkTheme():
            self.backButton.setStyleSheet(
                "QPushButton { color: #FFFFFF; border: none; background: transparent; }"
                "QPushButton:hover { color: #CFCFCF; }"
            )
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget { background-color: #3A3A3A; border-radius: 18px; padding: 2px; }"
            )
            inactiveColor = "#F0F0F0"
            activeText = "#FFFFFF"
            activeBG = "#5A5A5A"
        else:
            self.backButton.setStyleSheet(
                "QPushButton { color: #202020; border: none; background: transparent; }"
                "QPushButton:hover { color: #606060; }"
            )
            self.tabsWidget.setStyleSheet(
                "QFrame#tabsWidget { background-color: #E7E7E7; border-radius: 18px; padding: 2px; }"
            )
            inactiveColor = "#202020"
            activeText = "#202020"
            activeBG = "#FFFFFF"

        for button in self.tabButtons:
            if button.isChecked():
                button.setStyleSheet(
                    f"QPushButton {{ color: {activeText}; background-color: {activeBG}; border: none;"
                    "border-radius: 16px; font-weight: 600; padding: 8px 18px; }"
                )
            else:
                button.setStyleSheet(
                    f"QPushButton {{ color: {inactiveColor}; background-color: transparent; border: none;"
                    "border-radius: 16px; font-weight: 600; padding: 8px 18px; }"
                    "QPushButton:hover { background-color: rgba(255, 255, 255, 0.10); }"
                )

        if hasattr(self, "summaryCard"):
            self.summaryCard.setStyleSheet(
                "QFrame { background-color: #3A3A3A; border-radius: 10px; }"
                if isDarkTheme() else
                "QFrame { background-color: #EFEFEF; border-radius: 10px; }"
            )

        if hasattr(self, "addTaskButton"):
            if isDarkTheme():
                self.addTaskButton.setStyleSheet(
                    "QPushButton { background-color: transparent; color: #FFFFFF; border: 1px solid #FFFFFF; border-radius: 6px; font-size: 14px; }"
                    "QPushButton:hover { background-color: rgba(255, 255, 255, 0.10); }"
                )
                self.taskList.setStyleSheet(
                    "QListWidget { border: none; background: transparent; color: #FFFFFF; }"
                )
            else:
                self.addTaskButton.setStyleSheet(
                    "QPushButton { background-color: transparent; color: #202020; border: 1px solid #202020; border-radius: 6px; font-size: 14px; }"
                    "QPushButton:hover { background-color: rgba(32, 32, 32, 0.10); }"
                )
                self.taskList.setStyleSheet(
                    "QListWidget { border: none; background: transparent; color: #202020; }"
                )

        if hasattr(self, "milestoneDateInput"):
            self.styleDateInput()

    # ─── Tasks Tab ────────────────────────────────────────────────────────────

    def createTasksTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(28, 28, 28, 28)
        pageLayout.setSpacing(20)

        inputLayout = QHBoxLayout()
        inputLayout.setSpacing(8)

        self.taskInput = LineEdit()
        self.taskInput.setPlaceholderText("Add a new task...")
        self.taskInput.returnPressed.connect(self.addTask)

        self.addTaskButton = PrimaryPushButton("+")
        self.addTaskButton.setFixedSize(40, 40)
        self.addTaskButton.clicked.connect(self.addTask)

        inputLayout.addWidget(self.taskInput)
        inputLayout.addWidget(self.addTaskButton)

        self.taskList = QListWidget()
        self.taskList.setSpacing(10)
        self.taskList.setStyleSheet("QListWidget { border: none; background: transparent; }")

        pageLayout.addLayout(inputLayout)
        pageLayout.addWidget(self.taskList)

        return page

    def addTask(self):
        if not self.project:
            return
        text = self.taskInput.text().strip()
        if not text:
            return
        try:
            task = Task(name=text, description="", deadline=self.project.deadline, estimatedTime=0)
            self.project.addTask(task)
            self.save()
            self.renderTask(task)
            self.taskInput.clear()
            self.syncProjectStatus()
        except Exception as e:
            InfoBar.warning(title="Couldn't add task", content=str(e), parent=self,
                            duration=3000, position=InfoBarPosition.TOP)

    def renderTask(self, task: Task):
        item = QListWidgetItem()
        self.taskList.addItem(item)

        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        rowLayout.setContentsMargins(4, 4, 4, 4)
        rowLayout.setSpacing(10)

        checkbox = CheckBox(task.name)
        checkFont = QFont()
        checkFont.setPointSize(10)
        checkbox.setFont(checkFont)
        checkbox.setChecked(task.dateCompleted is not None)

        if task.dateCompleted:
            font = checkbox.font()
            font.setStrikeOut(True)
            checkbox.setFont(font)

        def onChecked(state, t=task, cb=checkbox):
            font = cb.font()
            try:
                if state == Qt.CheckState.Checked.value:
                    t.markComplete()
                    font.setStrikeOut(True)
                else:
                    t.unmarkComplete()
                    font.setStrikeOut(False)
                cb.setFont(font)
                self.save()
                self.refreshMilestoneList()
                self.syncProjectStatus()  
            except Exception as e:
                InfoBar.warning(title="Couldn't update task", content=str(e), parent=self,
                                duration=3000, position=InfoBarPosition.TOP)
                cb.blockSignals(True)
                cb.setChecked(not cb.isChecked())
                cb.blockSignals(False)

        checkbox.stateChanged.connect(onChecked)

        assignBtn = QPushButton("+ Milestone")
        assignBtn.setFixedHeight(28)
        assignBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        assignBtn.setStyleSheet(self.assignBtnStyle())
        assignBtn.clicked.connect(lambda checked=False, t=task: self.showAssignToMilestoneDialog(t))

        editBtn = QPushButton("✎")
        editBtn.setFixedSize(28, 28)
        editBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        editBtn.setStyleSheet(self.assignBtnStyle())
        editBtn.clicked.connect(lambda checked=False, t=task: self.editTask(t))

        deleteBtn = QPushButton("✕")
        deleteBtn.setFixedSize(28, 28)
        deleteBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        deleteBtn.setStyleSheet(self.deleteBtnStyle())
        deleteBtn.clicked.connect(lambda checked=False, t=task: self.deleteTask(t))

        milestoneLabel = QLabel()
        self.updateTaskMilestoneLabel(task, milestoneLabel)
        milestoneLabel.setStyleSheet(
            f"color: {'#C0C0C0' if isDarkTheme() else '#606060'}; font-size: 10px;"
        )
        task._milestoneLabel = milestoneLabel

        btnRow = QHBoxLayout()
        btnRow.setSpacing(4)
        btnRow.addWidget(assignBtn)
        btnRow.addWidget(editBtn)
        btnRow.addWidget(deleteBtn)

        rightLayout = QVBoxLayout()
        rightLayout.setSpacing(4)
        rightLayout.addLayout(btnRow)
        rightLayout.addWidget(milestoneLabel)

        rowLayout.addWidget(checkbox)
        rowLayout.addStretch()
        rowLayout.addLayout(rightLayout)

        item.setSizeHint(rowWidget.sizeHint())
        self.taskList.setItemWidget(item, rowWidget)

    def editTask(self, task: Task):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Task")
        dialog.setFixedSize(360, 120)
        layout = QVBoxLayout(dialog)

        nameInput = QLineEdit(task.name)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addWidget(QLabel("Task name:"))
        layout.addWidget(nameInput)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        newName = nameInput.text().strip()
        if newName:
            task.updateDetails(newName, task.description)
            self.save()
            self.refreshTaskList()

    def deleteTask(self, task: Task):
        try:
            for milestone in self.project.milestones:
                if task in milestone.tasks:
                    milestone.removeTask(task)
            self.project.removeTask(task.taskId)
            self.save()
            self.refreshTaskList()
            self.refreshMilestoneList()
            self.syncProjectStatus()
        except Exception as e:
            InfoBar.warning(title="Couldn't delete task", content=str(e),
                            parent=self, duration=3000, position=InfoBarPosition.TOP)

    def updateTaskMilestoneLabel(self, task: Task, label: QLabel):
        if task.milestones:
            names = ", ".join(m.name for m in task.milestones)
            label.setText(f"→ {names}")
        else:
            label.setText("")

    def showAssignToMilestoneDialog(self, task: Task):
        if not self.project.milestones:
            InfoBar.warning(title="No milestones", content="Add a milestone first.",
                            parent=self, duration=3000, position=InfoBarPosition.TOP)
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Assign to Milestone")
        dialog.setFixedSize(320, 300)
        layout = QVBoxLayout(dialog)

        layout.addWidget(QLabel(f"Assign '{task.name}' to:"))

        listWidget = QListWidget()
        for milestone in self.project.milestones:
            item = QListWidgetItem(
                f"{'✓ ' if milestone in task.milestones else ''}{milestone.name} "
                f"({len(milestone.tasks)}/3 tasks)"
            )
            item.setData(Qt.ItemDataRole.UserRole, milestone)
            listWidget.addItem(item)

        layout.addWidget(listWidget)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        selected = listWidget.currentItem()
        if not selected:
            return

        milestone = selected.data(Qt.ItemDataRole.UserRole)

        try:
            if milestone in task.milestones:
                milestone.removeTask(task)
            else:
                milestone.addTask(task)

            if hasattr(task, "_milestoneLabel"):
                self.updateTaskMilestoneLabel(task, task._milestoneLabel)

            self.refreshMilestoneList()
            self.save()

        except Exception as e:
            InfoBar.warning(title="Couldn't assign task", content=str(e), parent=self,
                            duration=3000, position=InfoBarPosition.TOP)

    # ─── Milestones Tab ───────────────────────────────────────────────────────

    def createMilestonesTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(28, 28, 28, 28)
        pageLayout.setSpacing(20)

        inputLayout = QHBoxLayout()
        inputLayout.setSpacing(8)

        self.milestoneInput = LineEdit()
        self.milestoneInput.setPlaceholderText("Milestone title...")
        self.milestoneInput.returnPressed.connect(self.addMilestone)

        self.milestoneDateInput = QDateEdit()
        self.milestoneDateInput.setCalendarPopup(True)
        self.milestoneDateInput.setDate(QDate.currentDate())
        self.milestoneDateInput.setMinimumDate(QDate.currentDate())
        self.milestoneDateInput.setDisplayFormat("MM/dd/yyyy")
        self.milestoneDateInput.setFixedWidth(160)
        self.styleDateInput()

        self.addMilestoneButton = PrimaryPushButton("+")
        self.addMilestoneButton.setFixedSize(40, 40)
        self.addMilestoneButton.clicked.connect(self.addMilestone)

        inputLayout.addWidget(self.milestoneInput)
        inputLayout.addWidget(self.milestoneDateInput)
        inputLayout.addWidget(self.addMilestoneButton)

        self.milestoneList = QListWidget()
        self.milestoneList.setSpacing(10)
        self.milestoneList.setStyleSheet("QListWidget { border: none; background: transparent; }")

        pageLayout.addLayout(inputLayout)
        pageLayout.addWidget(self.milestoneList)

        return page

    def addMilestone(self):
        if not self.project:
            return
        text = self.milestoneInput.text().strip()
        if not text:
            return
        qdate = self.milestoneDateInput.date()
        deadline = datetime(qdate.year(), qdate.month(), qdate.day())
        try:
            milestone = Milestone(name=text, deadline=deadline)
            self.project.addMilestone(milestone)
            self.save()
            self.renderMilestone(milestone)
            self.milestoneInput.clear()
        except Exception as e:
            InfoBar.warning(title="Couldn't add milestone", content=str(e), parent=self,
                            duration=3000, position=InfoBarPosition.TOP)

    def renderMilestone(self, milestone: Milestone):
        item = QListWidgetItem()
        self.milestoneList.addItem(item)

        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        rowLayout.setContentsMargins(4, 4, 4, 4)
        rowLayout.setSpacing(10)

        statusDot = QLabel("●")
        statusDot.setFont(QFont("Segoe UI", 14))
        statusDot.setStyleSheet(
            f"color: {'#2E7D32' if milestone.isReached() else '#AAAAAA'};"
        )

        infoLayout = QVBoxLayout()
        infoLayout.setSpacing(2)

        titleLabel = BodyLabel(milestone.name)
        if milestone.isReached():
            f = titleLabel.font()
            f.setStrikeOut(True)
            titleLabel.setFont(f)

        dateLabel = BodyLabel(milestone.deadline.strftime("%Y-%m-%d"))
        smallFont = QFont()
        smallFont.setPointSize(9)
        dateLabel.setFont(smallFont)

        taskNames = ", ".join(t.name for t in milestone.tasks) if milestone.tasks else "No tasks linked"
        tasksLabel = QLabel(f"Tasks: {taskNames}")
        progressLabel = QLabel(f"{milestone.getProgress():.0f}% complete")

        if isDarkTheme():
            tasksLabel.setStyleSheet("color: #C0C0C0; font-size: 10px;")
            progressLabel.setStyleSheet("color: #C0C0C0; font-size: 10px;")
        else:
            tasksLabel.setStyleSheet("color: #606060; font-size: 10px;")
            progressLabel.setStyleSheet("color: #606060; font-size: 10px;")

        infoLayout.addWidget(titleLabel)
        infoLayout.addWidget(dateLabel)
        infoLayout.addWidget(tasksLabel)
        infoLayout.addWidget(progressLabel)

        assignBtn = QPushButton("+ Tasks")
        assignBtn.setFixedHeight(28)
        assignBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        assignBtn.setStyleSheet(self.assignBtnStyle())
        assignBtn.clicked.connect(lambda checked=False, m=milestone: self.showAssignTasksDialog(m))

        editBtn = QPushButton("✎")
        editBtn.setFixedSize(28, 28)
        editBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        editBtn.setStyleSheet(self.assignBtnStyle())
        editBtn.clicked.connect(lambda checked=False, m=milestone: self.editMilestone(m))

        deleteBtn = QPushButton("✕")
        deleteBtn.setFixedSize(28, 28)
        deleteBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        deleteBtn.setStyleSheet(self.deleteBtnStyle())
        deleteBtn.clicked.connect(lambda checked=False, m=milestone: self.deleteMilestone(m))

        btnRow = QHBoxLayout()
        btnRow.setSpacing(4)
        btnRow.addWidget(assignBtn)
        btnRow.addWidget(editBtn)
        btnRow.addWidget(deleteBtn)

        btnCol = QVBoxLayout()
        btnCol.setSpacing(4)
        btnCol.addLayout(btnRow)

        rowLayout.addWidget(statusDot)
        rowLayout.addLayout(infoLayout)
        rowLayout.addStretch()
        rowLayout.addLayout(btnCol)

        item.setSizeHint(rowWidget.sizeHint())
        self.milestoneList.setItemWidget(item, rowWidget)

    def editMilestone(self, milestone: Milestone):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Milestone")
        dialog.setFixedSize(360, 180)
        layout = QVBoxLayout(dialog)

        nameInput = QLineEdit(milestone.name)

        dateEdit = QDateEdit()
        dateEdit.setCalendarPopup(True)
        dateEdit.setDisplayFormat("MM/dd/yyyy")
        dateEdit.setMinimumDate(QDate.currentDate())
        dateEdit.setDate(QDate(
            milestone.deadline.year,
            milestone.deadline.month,
            milestone.deadline.day
        ))

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(nameInput)
        layout.addWidget(QLabel("Deadline:"))
        layout.addWidget(dateEdit)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        newName = nameInput.text().strip()
        if newName:
            milestone.name = newName
        qdate = dateEdit.date()
        milestone.deadline = datetime(qdate.year(), qdate.month(), qdate.day())
        self.save()
        self.refreshMilestoneList()

    def deleteMilestone(self, milestone: Milestone):
        try:
            for task in list(milestone.tasks):
                milestone.removeTask(task)
            self.project.removeMilestone(milestone.milestoneId)
            self.save()
            self.refreshMilestoneList()
            self.refreshTaskList()
        except Exception as e:
            InfoBar.warning(title="Couldn't delete milestone", content=str(e),
                            parent=self, duration=3000, position=InfoBarPosition.TOP)

    def showAssignTasksDialog(self, milestone: Milestone):
        if not self.project.tasks:
            InfoBar.warning(title="No tasks", content="Add tasks first.",
                            parent=self, duration=3000, position=InfoBarPosition.TOP)
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Assign Tasks to Milestone")
        dialog.setFixedSize(360, 320)
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(f"Select tasks for '{milestone.name}' (max 3):"))

        checkboxes = []
        for task in self.project.tasks:
            cb = QCheckBox(task.name)
            cb.setChecked(task in milestone.tasks)
            cb.setProperty("task", task)
            checkboxes.append(cb)
            layout.addWidget(cb)

        layout.addStretch()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        for cb in checkboxes:
            task = cb.property("task")
            shouldBeLinked = cb.isChecked()
            isLinked = task in milestone.tasks

            try:
                if shouldBeLinked and not isLinked:
                    milestone.addTask(task)
                elif not shouldBeLinked and isLinked:
                    milestone.removeTask(task)
            except Exception as e:
                InfoBar.warning(title="Couldn't update", content=str(e), parent=self,
                                duration=3000, position=InfoBarPosition.TOP)

        self.refreshMilestoneList()
        self.refreshTaskList()
        self.save()

    def refreshMilestoneList(self):
        self.milestoneList.clear()
        if self.project:
            for milestone in self.project.milestones:
                self.renderMilestone(milestone)

    def refreshTaskList(self):
        self.taskList.clear()
        if self.project:
            for task in self.project.tasks:
                self.renderTask(task)

    def styleDateInput(self):
        if isDarkTheme():
            self.milestoneDateInput.setStyleSheet("""
                QDateEdit {
                    background-color: #3A3A3A;
                    color: white;
                    border: 1px solid #666666;
                    border-radius: 6px;
                    padding: 6px;
                }

                QDateEdit::drop-down {
                    background-color: #3A3A3A;
                    border: none;
                    width: 22px;
                }

                QDateEdit QLineEdit {
                    background-color: #3A3A3A;
                    color: white;
                    border: none;
                }
            """)
        else:
            self.milestoneDateInput.setStyleSheet("""
                QDateEdit {
                    background-color: white;
                    color: #202020;
                    border: 1px solid #CCCCCC;
                    border-radius: 6px;
                    padding: 6px;
                }

                QDateEdit::drop-down {
                    background-color: white;
                    border: none;
                    width: 22px;
                }

                QDateEdit QLineEdit {
                    background-color: white;
                    color: #202020;
                    border: none;
                }
            """)

    # ─── Images Tab ───────────────────────────────────────────────────────────

    def createImagesTab(self):
        page = CardWidget()
        page.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(0, 0, 0, 0)

        scrollArea = ScrollArea(page)
        scrollArea.setWidgetResizable(True)
        scrollArea.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scrollArea.setStyleSheet("background: transparent; border: none;")

        self.imageGridContainer = QWidget()
        self.imageGridContainer.setStyleSheet("background: transparent;")
        self.imageGridContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.imageGrid = QGridLayout(self.imageGridContainer)
        self.imageGrid.setSpacing(30)
        self.imageGrid.setContentsMargins(24, 24, 24, 24)
        self.imageGrid.setColumnStretch(0, 1)
        self.imageGrid.setColumnStretch(1, 1)
        self.imageGrid.setColumnStretch(2, 1)
        self.imageGrid.setRowStretch(999, 1) 

        self.uploadButton = QPushButton("↑\nClick to upload an image")
        self.uploadButton.setFixedSize(280, 200)
        self.uploadButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.uploadButton.setStyleSheet(
            "QPushButton { border: 2px dashed #AAAAAA; border-radius: 10px;"
            "color: #888888; font-size: 12px; background: transparent; }"
            "QPushButton:hover { border-color: #555555; color: #555555; }"
        )
        self.uploadButton.clicked.connect(self.uploadImage)
        self.imageGrid.addWidget(
            self.uploadButton, 0, 0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        scrollArea.setWidget(self.imageGridContainer)
        pageLayout.addWidget(scrollArea)

        return page

    def uploadImage(self):
        if not self.project:
            return
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if not filePath:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Image Description")
        dialog.setFixedSize(360, 130)
        dialogLayout = QVBoxLayout(dialog)
        descInput = QLineEdit()
        descInput.setPlaceholderText("Enter a description for this image...")
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialogLayout.addWidget(QLabel("Description (optional):"))
        dialogLayout.addWidget(descInput)
        dialogLayout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            media = Media(filePath=filePath, description=descInput.text().strip())
            media.upload(self.project.projectId)
            self.project.addMedia(media)
            self.save()
            self.renderImage(media)
        except Exception as e:
            InfoBar.warning(title="Couldn't add image", content=str(e), parent=self,
                            duration=3000, position=InfoBarPosition.TOP)

    def renderImage(self, media: Media):
        IMG_W = 280
        IMG_H = 200

        pixmap = media.getPixmap()
        if pixmap is None or pixmap.isNull():
            return 
        
        pixmap = pixmap.scaled(
            IMG_W, IMG_H,
            Qt.AspectRatioMode.KeepAspectRatio,  
            Qt.TransformationMode.SmoothTransformation
        )

        cellWidget = QWidget()
        cellWidget.setFixedWidth(IMG_W)
        cellWidget.setStyleSheet("background: transparent;")
        
        cellLayout = QVBoxLayout(cellWidget)
        cellLayout.setContentsMargins(0, 0, 0, 0)
        cellLayout.setSpacing(8)
        cellLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        imgContainer = QWidget()
        imgContainer.setFixedSize(IMG_W, IMG_H)
        imgContainer.setStyleSheet("background: transparent;")
        
        imgContainerLayout = QVBoxLayout(imgContainer)
        imgContainerLayout.setContentsMargins(0, 0, 0, 0)

        imgLabel = QLabel()
        imgLabel.setPixmap(pixmap)
        imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imgLabel.setStyleSheet("background: transparent;")
        imgLabel.setCursor(Qt.CursorShape.PointingHandCursor)
        imgLabel.mousePressEvent = lambda e, m=media: self.showFullImage(m)
        
        imgContainerLayout.addWidget(imgLabel)

        deleteBtn = QPushButton("✕", imgContainer)
        deleteBtn.setFixedSize(26, 26)
        deleteBtn.move(IMG_W - 30, 4)
        deleteBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        deleteBtn.setStyleSheet(
            "QPushButton { color: #CC4444; border: 1px solid #CC4444; border-radius: 6px;"
            "font-size: 11px; background: rgba(255,255,255,0.9); font-weight: bold; }"
            "QPushButton:hover { background: rgba(204,68,68,0.15); }"
        )
        deleteBtn.clicked.connect(lambda checked=False, m=media: self.deleteImage(m))
        deleteBtn.raise_()

        label = media.description if media.description else ""
        nameLabel = QLabel(label)
        nameLabel.setFont(QFont("Segoe UI", 10))
        nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nameLabel.setWordWrap(True)
        nameLabel.setFixedWidth(IMG_W)

        def updateNameLabelColor():
            nameLabel.setStyleSheet(
                f"color: {'#CCCCCC' if isDarkTheme() else '#555555'}; background: transparent;"
            )

        def disconnectNameLabel():
            try:
                qconfig.themeChanged.disconnect(updateNameLabelColor)
            except RuntimeError:
                pass

        updateNameLabelColor()

        qconfig.themeChanged.connect(updateNameLabelColor)
        nameLabel.destroyed.connect(disconnectNameLabel)

        cellLayout.addWidget(imgContainer)
        cellLayout.addWidget(nameLabel)

        cellWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        count = self.imageGrid.count()
        cols = 3
        gridRow = count // cols
        gridCol = count % cols
        
        self.imageGrid.addWidget(cellWidget, gridRow, gridCol, Qt.AlignmentFlag.AlignTop)

    def deleteImage(self, media: Media):
        try:
            mediaId = media.mediaId
            self.project.removeMedia(mediaId)
            if self.storage:
                self.storage.deleteMedia(mediaId)
            media.delete()
            self.save()

            while self.imageGrid.count() > 1:
                item = self.imageGrid.takeAt(1)
                if item.widget():
                    item.widget().deleteLater()
            for m in self.project.media:
                self.renderImage(m)
        except Exception as e:
            InfoBar.warning(title="Couldn't delete image", content=str(e),
                            parent=self, duration=3000, position=InfoBarPosition.TOP)

    def showFullImage(self, media: Media):
        dialog = QDialog(self)
        dialog.setWindowTitle(media.description or "Image")
        dialog.setMinimumSize(600, 500)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)

        imgLabel = QLabel()
        fullPixmap = media.getPixmap().scaled(
            800, 600,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        imgLabel.setPixmap(fullPixmap)
        imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if media.description:
            descLabel = QLabel(media.description)
            descLabel.setFont(QFont("Segoe UI", 11))
            descLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            descLabel.setStyleSheet("color: #555555;")
            layout.addWidget(descLabel)

        layout.addWidget(imgLabel)
        dialog.exec()

    # ─── Export Tab ───────────────────────────────────────────────────────────

    def createExportTab(self):
        page = CardWidget()
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(20)

        titleLabel = StrongBodyLabel("Project Summary")

        self.summaryCard = QFrame()
        self.summaryCard.setStyleSheet(
            "QFrame { background-color: #3A3A3A; border-radius: 10px; }"
            if isDarkTheme() else
            "QFrame { background-color: #EFEFEF; border-radius: 10px; }"
        )
        summaryLayout = QVBoxLayout(self.summaryCard)
        summaryLayout.setContentsMargins(16, 16, 16, 16)
        summaryLayout.setSpacing(8)

        self.summaryProjectLabel = BodyLabel("Project: —")
        self.summaryDescLabel = BodyLabel("Description: —")
        self.summaryTasksLabel = BodyLabel("Tasks: —")
        self.summaryMilestonesLabel = BodyLabel("Milestones: —")
        self.summaryImagesLabel = BodyLabel("Images: —")

        for lbl in [self.summaryProjectLabel, self.summaryDescLabel,
                    self.summaryTasksLabel, self.summaryMilestonesLabel, self.summaryImagesLabel]:
            summaryLayout.addWidget(lbl)

        exportLabel = StrongBodyLabel("Export Options")

        self.exportPdfButton = PrimaryPushButton("  Export as PDF")
        self.exportPdfButton.setMinimumHeight(44)
        self.exportPdfButton.clicked.connect(self.exportAsPdf)

        self.exportImageButton = PrimaryPushButton("  Export as Image")
        self.exportImageButton.setMinimumHeight(44)
        self.exportImageButton.clicked.connect(self.exportAsImage)

        pageLayout.addWidget(titleLabel)
        pageLayout.addWidget(self.summaryCard)
        pageLayout.addWidget(exportLabel)
        pageLayout.addWidget(self.exportPdfButton)
        pageLayout.addWidget(self.exportImageButton)
        pageLayout.addStretch()

        return page

    def refreshExportSummary(self):
        if not self.project:
            return
        self.summaryProjectLabel.setText(f"Project: {self.project.title}")
        self.summaryDescLabel.setText(f"Description: {self.project.description}")
        self.summaryTasksLabel.setText(
            f"Tasks: {len(self.project.completedTasks())} / {len(self.project.tasks)} completed"
        )
        self.summaryMilestonesLabel.setText(
            f"Milestones: {sum(1 for m in self.project.milestones if m.isReached())} / {len(self.project.milestones)} achieved"
        )
        self.summaryImagesLabel.setText(f"Images: {len(self.project.media)}")

    def exportAsImage(self):
        """Export project as a PNG image (shareable on Instagram etc.)"""
        if not self.project:
            return
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Export as Image", f"{self.project.title}.png", "PNG Image (*.png)"
        )
        if not filePath:
            return
        self.renderProjectImage(filePath, asPdf=False)

    def exportAsPdf(self):
        if not self.project:
            return
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Export as PDF", f"{self.project.title}.pdf", "PDF Files (*.pdf)"
        )
        if not filePath:
            return
        self.renderProjectImage(filePath, asPdf=True)

    def renderProjectImage(self, filePath, asPdf=False):
        _DATA_DIR = Path(getAppDataDir())
        _AVATAR_FILE = _DATA_DIR / "avatar.png"

        profile = {"username": "", "bio": ""}
        mainWindow = self.window()
        if hasattr(mainWindow, "hobbyist"):
            profile["username"] = mainWindow.hobbyist.username or ""
            profile["bio"] = mainWindow.hobbyist.bio or ""

        CANVAS_W, CANVAS_H = 1080, 1920
        margin = 60
        contentW = CANVAS_W - margin * 2

        img = QImage(CANVAS_W, CANVAS_H, QImage.Format.Format_ARGB32)
        img.fill(QColor("#FFFFFF"))
        painter = QPainter(img)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Clip everything to canvas
        painter.setClipRect(0, 0, CANVAS_W, CANVAS_H)

        x = float(margin)
        y = float(margin)

        def drawText(text, fontSize, bold, ypos, color=QColor("#111111"), indent=0, spacing=6, width=None):
            font = QFont("Segoe UI", fontSize)
            font.setBold(bold)
            painter.setFont(font)
            painter.setPen(color)
            w = (width if width else contentW) - indent
            rect = QRectF(x + indent, ypos, w, 9999)
            br = painter.boundingRect(rect, Qt.TextFlag.TextWordWrap, text)
            painter.drawText(rect, Qt.TextFlag.TextWordWrap, text)
            return ypos + br.height() + spacing

        def drawStrikeText(text, fontSize, bold, ypos, color=QColor("#111111"), indent=0, spacing=6, width=None):
            font = QFont("Segoe UI", fontSize)
            font.setBold(bold)
            font.setStrikeOut(True)
            painter.setFont(font)
            painter.setPen(color)
            w = (width if width else contentW) - indent
            rect = QRectF(x + indent, ypos, w, 9999)
            br = painter.boundingRect(rect, Qt.TextFlag.TextWordWrap, text)
            painter.drawText(rect, Qt.TextFlag.TextWordWrap, text)
            return ypos + br.height() + spacing

        def drawDivider(ypos):
            painter.setPen(QPen(QColor("#E0E0E0"), 1))
            painter.drawLine(int(x), int(ypos), int(x + contentW), int(ypos))
            return ypos + 14

        def drawCheckmark(cx, cy, size=14, checked=True, color=QColor("#2B5CE6")):
            painter.setPen(QPen(QColor("#CCCCCC"), 1.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(QRectF(cx, cy, size, size), 3, 3)
            if checked:
                painter.setBrush(color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(QRectF(cx, cy, size, size), 3, 3)
                pen = QPen(QColor("#FFFFFF"), 2.0)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                painter.setPen(pen)
                # Draw checkmark polyline: 2,6 -> 5,9 -> 10,3 scaled
                s = size / 12.0
                pts = [
                    (cx + 2*s, cy + 6*s),
                    (cx + 5*s, cy + 9*s),
                    (cx + 10*s, cy + 3*s),
                ]
                poly = QPolygonF([QPointF(px, py) for px, py in pts])
                painter.drawPolyline(poly)

        # ── Avatar + profile ──────────────────────────────────────────────────────
        avatarSize = 160
        if _AVATAR_FILE.exists():
            avatarPixmap = QPixmap(str(_AVATAR_FILE)).scaled(
                avatarSize, avatarSize,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            path = QPainterPath()
            path.addEllipse(x, y, avatarSize, avatarSize)
            painter.setClipPath(path)
            painter.drawPixmap(int(x), int(y), avatarPixmap)
            painter.setClipping(False)
            painter.setClipRect(0, 0, CANVAS_W, CANVAS_H)

        textX = x + avatarSize + 24
        textW = contentW - avatarSize - 24
        nameFont = QFont("Segoe UI", 26); nameFont.setBold(True)
        painter.setFont(nameFont); painter.setPen(QColor("#111111"))
        nameRect = QRectF(textX, y + 20, textW, 9999)
        nameBR = painter.boundingRect(nameRect, Qt.TextFlag.TextWordWrap, profile["username"])
        painter.drawText(nameRect, Qt.TextFlag.TextWordWrap, profile["username"])
        bioFont = QFont("Segoe UI", 15)
        painter.setFont(bioFont); painter.setPen(QColor("#666666"))
        bioY = y + 20 + nameBR.height() + 8
        bioBR = painter.boundingRect(QRectF(textX, bioY, textW, 9999), Qt.TextFlag.TextWordWrap, profile["bio"])
        painter.drawText(QRectF(textX, bioY, textW, 9999), Qt.TextFlag.TextWordWrap, profile["bio"])

        y += max(avatarSize, nameBR.height() + bioBR.height() + 40) + 28
        y = drawDivider(y)

        # ── Title + description ───────────────────────────────────────────────────
        y = drawText(self.project.title, 26, True, y, QColor("#111111"), spacing=8)
        y = drawText(self.project.description, 15, False, y, QColor("#555555"), spacing=16)

        y = drawDivider(y)

        # ── Tasks & Milestones side by side ───────────────────────────────────────
        if self.project.tasks or self.project.milestones:
            colW = (contentW - 24) // 2
            leftX = x
            rightX = x + colW + 24

            progress = self.project.getProgress()
            y += 10

            labelFont = QFont("Segoe UI", 14); labelFont.setBold(True)
            painter.setFont(labelFont); painter.setPen(QColor("#111111"))
            painter.drawText(QRectF(x, y, contentW, 30), Qt.TextFlag.TextWordWrap, "Progress")
            pctFont = QFont("Segoe UI", 13)
            painter.setFont(pctFont); painter.setPen(QColor("#1A6FA8"))
            painter.drawText(
                QRectF(x, y, contentW, 30),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"{progress:.0f}%"
            )
            y += 36

            barH = 16
            barRadius = barH / 2

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#E8EEF4"))
            painter.drawRoundedRect(QRectF(x, y, contentW, barH), barRadius, barRadius)

            if progress > 0:
                fillW = contentW * (progress / 100)
                painter.setBrush(QColor("#1A6FA8"))
                painter.drawRoundedRect(QRectF(x, y, fillW, barH), barRadius, barRadius)

                painter.setBrush(QColor(255, 255, 255, 35))
                painter.drawRoundedRect(QRectF(x, y, fillW, barH / 2), barRadius, barRadius)

            y += barH + 24

        # ── Tasks & Milestones side by side ───────────────────────────────────────
        if self.project.tasks or self.project.milestones:
            colW = (contentW - 24) // 2
            leftX = x
            rightX = x + colW + 24

            startY = y

            # Left col: Tasks
            leftY = startY
            if self.project.tasks:
                leftY = drawText("Tasks", 14, True, leftY, QColor("#111111"), width=colW, spacing=8)
                BOX = 13
                LINE_H = 20
                for task in self.project.tasks:
                    done = task.dateCompleted is not None
                    # draw checkbox
                    drawCheckmark(leftX, leftY + 3, BOX, checked=done,
                                color=QColor("#2B5CE6"))
                    # draw label (with or without strikethrough)
                    font = QFont("Segoe UI", 12)
                    font.setStrikeOut(done)
                    painter.setFont(font)
                    painter.setPen(QColor("#2B5CE6") if done else QColor("#333333"))
                    painter.drawText(
                        QRectF(leftX + BOX + 6, leftY, colW - BOX - 6, LINE_H),
                        Qt.TextFlag.TextWordWrap, task.name
                    )
                    leftY += LINE_H + 2

            # Right col: Milestones
            rightY = startY
            if self.project.milestones:
                # Temporarily shift x for right column
                origX = x
                rightY = startY

                # Draw heading manually since drawText uses closure x
                headFont = QFont("Segoe UI", 14); headFont.setBold(True)
                painter.setFont(headFont); painter.setPen(QColor("#111111"))
                painter.drawText(QRectF(rightX, rightY, colW, 30), Qt.TextFlag.TextWordWrap, "Milestones")
                rightY += 8 + 16

                BOX = 13
                LINE_H = 20
                for milestone in self.project.milestones:
                    done = milestone.isReached()
                    drawCheckmark(rightX, rightY + 3, BOX, checked=done, color=QColor("#2B5CE6"))
                    font = QFont("Segoe UI", 12); font.setBold(True); font.setStrikeOut(done)
                    painter.setFont(font)
                    painter.setPen(QColor("#2B5CE6") if done else QColor("#333333"))
                    pct = f"  {milestone.getProgress():.0f}%"
                    painter.drawText(
                        QRectF(rightX + BOX + 6, rightY, colW - BOX - 6, LINE_H),
                        Qt.TextFlag.TextWordWrap, milestone.name + pct
                    )
                    rightY += LINE_H + 2
                    # sub-tasks
                    for task in milestone.tasks:
                        tdone = task.dateCompleted is not None
                        drawCheckmark(rightX + 14, rightY + 3, 10, checked=tdone, color=QColor("#2B5CE6"))
                        sfont = QFont("Segoe UI", 12); sfont.setStrikeOut(tdone)
                        painter.setFont(sfont)
                        painter.setPen(QColor("#2B5CE6") if tdone else QColor("#888888"))
                        painter.drawText(
                            QRectF(rightX + 28, rightY, colW - 28, LINE_H),
                            Qt.TextFlag.TextWordWrap, task.name
                        )
                        rightY += LINE_H
                    rightY += 6

            y = max(leftY, rightY) + 16
            y = drawDivider(y)

        # ── Images grid (2 cols) ──────────────────────────────────────────────────
        if self.project.media:
            y = drawText("Images", 14, True, y, QColor("#111111"), spacing=12)

            cols = 2
            gap = 20
            imgW = (contentW - gap * (cols - 1)) // cols
            maxImgH = int(imgW * 0.55)  # max cell height; actual image may be shorter
            captionH = 30

            for i, media in enumerate(self.project.media):
                pixmap = media.getPixmap()
                if pixmap is None or pixmap.isNull():
                    continue

                col = i % cols
                row = i // cols
                cellX = x + col * (imgW + gap)
                cellY = y + row * (maxImgH + captionH + gap)

                if cellY + maxImgH + captionH > CANVAS_H - margin:
                    break

                # Scale to fit fully inside the cell — no cropping
                pixmap = pixmap.scaled(
                    imgW, maxImgH,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )

                actualH = pixmap.height()
                actualW = pixmap.width()

                # Draw rounded rect background behind the image
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor("#F4F4F4"))
                painter.drawRoundedRect(QRectF(cellX, cellY, imgW, maxImgH), 8, 8)

                # Center the image inside the cell both horizontally and vertically
                imgX = int(cellX + (imgW - actualW) / 2)
                imgY = int(cellY + (maxImgH - actualH) / 2)

                painter.save()
                path2 = QPainterPath()
                path2.addRoundedRect(QRectF(cellX, cellY, imgW, maxImgH), 8, 8)
                painter.setClipPath(path2)
                painter.drawPixmap(imgX, imgY, pixmap)
                painter.restore()
                painter.setClipRect(0, 0, CANVAS_W, CANVAS_H)

                if media.description:
                    capFont = QFont("Segoe UI", 11)
                    painter.setFont(capFont)
                    painter.setPen(QColor("#555555"))
                    painter.drawText(
                        QRectF(cellX, cellY + maxImgH + 6, imgW, captionH),
                        Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                        media.description
                    )

        painter.end()

        # ── Save ──────────────────────────────────────────────────────────────────
        if asPdf:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filePath)
            pageSizeMM = QSizeF(CANVAS_W * 25.4 / 96, CANVAS_H * 25.4 / 96)
            printer.setPageSize(QPageSize(pageSizeMM, QPageSize.Unit.Millimeter))
            printer.setPageMargins(QMarginsF(0, 0, 0, 0))
            pdfPainter = QPainter(printer)
            prRect = printer.pageRect(QPrinter.Unit.DevicePixel)
            scaled = img.scaled(
                int(prRect.width()), int(prRect.height()),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            pdfPainter.drawImage(0, 0, scaled)
            pdfPainter.end()
        else:
            img.save(filePath, "PNG")

        InfoBar.success(
            title="Exported!",
            content=f"Saved to {filePath}",
            parent=self,
            duration=3000,
            position=InfoBarPosition.TOP
        )

        # ─── Tab switching ────────────────────────────────────────────────────────

    def setActiveTab(self, index):
        self.contentStack.setCurrentIndex(index)
        for i, button in enumerate(self.tabButtons):
            button.setChecked(i == index)
        if index == 3:
            self.refreshExportSummary()
        self.applyThemeColors()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.Type.PaletteChange, QEvent.Type.StyleChange):
            if hasattr(self, "contentStack"):
                currentIndex = self.contentStack.currentIndex()
                self.applyThemeColors()
                self.setActiveTab(currentIndex)
                self.refreshTaskList()
                self.refreshMilestoneList()

    def showEvent(self, event):
        super().showEvent(event)
        self.applyThemeColors()

    # ─── Navigation ───────────────────────────────────────────────────────────

    def goBackToProjects(self):
        mainWindow = self.window()
        if hasattr(mainWindow, "switchTo") and hasattr(mainWindow, "projectPage"):
            mainWindow.switchTo(mainWindow.projectPage)

    def setProject(self, project):
        self.project = project
        self.projectTitle.setText(project.title)
        self.projectDescription.setText(project.description)

        self.taskList.clear()
        for task in project.tasks:
            self.renderTask(task)

        self.milestoneList.clear()
        for milestone in project.milestones:
            self.renderMilestone(milestone)

        while self.imageGrid.count() > 1:
            item = self.imageGrid.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        for media in project.media:
            self.renderImage(media)

        self.setActiveTab(0)

    def save(self):
        if self.storage and self.project:
            self.storage.saveProject(self.project)
    
    def syncProjectStatus(self):
        if not self.project:
            return
        self.project.getProgress()  
        self.save()

        mainWindow = self.window()
        if hasattr(mainWindow, "projectPage"):
            mainWindow.projectPage.refreshProjects()
