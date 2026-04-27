### Project View Page 
## This page will show the details of a specific project when selected within the
## Projects pages.
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QStackedWidget, QWidget, QVBoxLayout,
    QCheckBox, QFileDialog, QGridLayout, QDateEdit,
    QDialog, QDialogButtonBox, QLineEdit, 
)
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import QEvent, Qt, QDate, QRectF, QSizeF, QMarginsF
from PyQt6.QtGui import (
    QFont, QPixmap, QPainter, QPageSize, QColor, 
    QPainterPath, QPen, QImage, QPageSize
    )
from PyQt6.QtPrintSupport import QPrinter
from qfluentwidgets import (
    SubtitleLabel, BodyLabel, StrongBodyLabel, CardWidget,
    PrimaryPushButton, LineEdit, InfoBar, InfoBarPosition, isDarkTheme,
)
from classes.Task import Task
from classes.Milestone import Milestone
from classes.Media import Media
from datetime import datetime
import json
from pathlib import Path

class projectViewPage(QWidget):
    def __init__(self):
        super().__init__()

        self.project = None
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

        layout.addWidget(self.contentStack)
        layout.addStretch()

        self.taskTab.clicked.connect(lambda: self.setActiveTab(0))
        self.milestonesTab.clicked.connect(lambda: self.setActiveTab(1))
        self.imagesTab.clicked.connect(lambda: self.setActiveTab(2))
        self.exportTab.clicked.connect(lambda: self.setActiveTab(3))

        self.setLayout(layout)
        self.applyThemeColors()
        self.setActiveTab(0)

    # ─── Theme ────────────────────────────────────────────────────────────────

    def _assignBtnStyle(self):
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

    def _deleteBtnStyle(self):
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
            self.renderTask(task)
            self.taskInput.clear()
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

        checkbox = QCheckBox(task.name)
        if isDarkTheme():
            checkbox.setStyleSheet(
                "QCheckBox { color: #FFFFFF; font-weight: 500; }"
                "QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid #FFFFFF; border-radius: 4px; background: transparent; }"
                "QCheckBox::indicator:checked { background-color: #FFFFFF; }"
            )
        else:
            checkbox.setStyleSheet(
                "QCheckBox { color: #202020; font-weight: 500; }"
                "QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid #202020; border-radius: 4px; background: transparent; }"
                "QCheckBox::indicator:checked { background-color: #202020; }"
            )

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
                self.refreshMilestoneList()
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
        assignBtn.setStyleSheet(self._assignBtnStyle())
        assignBtn.clicked.connect(lambda checked=False, t=task: self.showAssignToMilestoneDialog(t))

        editBtn = QPushButton("✎")
        editBtn.setFixedSize(28, 28)
        editBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        editBtn.setStyleSheet(self._assignBtnStyle())
        editBtn.clicked.connect(lambda checked=False, t=task: self.editTask(t))

        deleteBtn = QPushButton("✕")
        deleteBtn.setFixedSize(28, 28)
        deleteBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        deleteBtn.setStyleSheet(self._deleteBtnStyle())
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
            self.refreshTaskList()

    def deleteTask(self, task: Task):
        try:
            for milestone in self.project.milestones:
                if task in milestone.tasks:
                    milestone.removeTask(task)
            self.project.removeTask(task.taskId)
            self.refreshTaskList()
            self.refreshMilestoneList()
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

        checkbox = QCheckBox()
        checkbox.setChecked(milestone.isReached())
        if isDarkTheme():
            checkbox.setStyleSheet(
                "QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid #FFFFFF; border-radius: 4px; background: transparent; }"
                "QCheckBox::indicator:checked { background-color: #FFFFFF; }"
            )
        else:
            checkbox.setStyleSheet(
                "QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid #202020; border-radius: 4px; background: transparent; }"
                "QCheckBox::indicator:checked { background-color: #202020; }"
            )

        def onChecked(state, m=milestone):
            if state == Qt.CheckState.Checked.value:
                m.markComplete()
            else:
                m.unmarkComplete()
            self.refreshMilestoneList()

        checkbox.stateChanged.connect(onChecked)

        infoLayout = QVBoxLayout()
        infoLayout.setSpacing(2)

        titleLabel = BodyLabel(milestone.name)
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
        assignBtn.setStyleSheet(self._assignBtnStyle())
        assignBtn.clicked.connect(lambda checked=False, m=milestone: self.showAssignTasksDialog(m))

        editBtn = QPushButton("✎")
        editBtn.setFixedSize(28, 28)
        editBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        editBtn.setStyleSheet(self._assignBtnStyle())
        editBtn.clicked.connect(lambda checked=False, m=milestone: self.editMilestone(m))

        deleteBtn = QPushButton("✕")
        deleteBtn.setFixedSize(28, 28)
        deleteBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        deleteBtn.setStyleSheet(self._deleteBtnStyle())
        deleteBtn.clicked.connect(lambda checked=False, m=milestone: self.deleteMilestone(m))

        btnRow = QHBoxLayout()
        btnRow.setSpacing(4)
        btnRow.addWidget(assignBtn)
        btnRow.addWidget(editBtn)
        btnRow.addWidget(deleteBtn)

        btnCol = QVBoxLayout()
        btnCol.setSpacing(4)
        btnCol.addLayout(btnRow)

        rowLayout.addWidget(checkbox)
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
        self.milestoneDateInput.setMinimumDate(QDate.currentDate())
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
        self.refreshMilestoneList()

    def deleteMilestone(self, milestone: Milestone):
        try:
            for task in list(milestone.tasks):
                milestone.removeTask(task)
            self.project.removeMilestone(milestone.milestoneId)
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
        pageLayout = QVBoxLayout(page)
        pageLayout.setContentsMargins(24, 24, 24, 24)
        pageLayout.setSpacing(16)

        self.uploadButton = QPushButton("↑\nClick to upload an image")
        self.uploadButton.setFixedSize(180, 120)
        self.uploadButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.uploadButton.setStyleSheet(
            "QPushButton { border: 2px dashed #AAAAAA; border-radius: 10px;"
            "color: #888888; font-size: 12px; background: transparent; }"
            "QPushButton:hover { border-color: #555555; color: #555555; }"
        )
        self.uploadButton.clicked.connect(self.uploadImage)

        self.imageGridContainer = QWidget()
        self.imageGridContainer.setStyleSheet("background: transparent;")
        self.imageGrid = QGridLayout(self.imageGridContainer)
        self.imageGrid.setSpacing(16)
        self.imageGrid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.imageGrid.addWidget(self.uploadButton, 0, 0)

        pageLayout.addWidget(self.imageGridContainer)

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
            self.renderImage(media)
        except Exception as e:
            InfoBar.warning(title="Couldn't add image", content=str(e), parent=self,
                            duration=3000, position=InfoBarPosition.TOP)

    def renderImage(self, media: Media):
        pixmap = media.getPixmap().scaled(
            180, 140,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        cellWidget = QWidget()
        cellWidget.setStyleSheet("background: transparent;")
        cellLayout = QVBoxLayout(cellWidget)
        cellLayout.setContentsMargins(0, 0, 0, 0)
        cellLayout.setSpacing(6)

        imgLabel = QLabel()
        imgLabel.setPixmap(pixmap)
        imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imgLabel.setStyleSheet("background: transparent;")

        label = media.description if media.description else media.filePath.split("/")[-1]
        nameLabel = QLabel(label)
        nameLabel.setFont(QFont("Segoe UI", 10))
        nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nameLabel.setWordWrap(True)
        nameLabel.setMaximumWidth(180)
        nameLabel.setStyleSheet(
            f"color: {'#CCCCCC' if isDarkTheme() else '#444444'}; background: transparent;"
        )

        cellLayout.addWidget(imgLabel)
        cellLayout.addWidget(nameLabel)

        count = self.imageGrid.count()
        cols = 3
        gridRow = count // cols
        gridCol = count % cols
        self.imageGrid.addWidget(cellWidget, gridRow, gridCol)

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
        self._renderProjectImage(filePath, asPdf=False)

    def exportAsPdf(self):
        if not self.project:
            return
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Export as PDF", f"{self.project.title}.pdf", "PDF Files (*.pdf)"
        )
        if not filePath:
            return
        self._renderProjectImage(filePath, asPdf=True)

    def _renderProjectImage(self, filePath, asPdf=False):
        _DATA_DIR = Path(__file__).parent.parent.parent / "data"
        _AVATAR_FILE = _DATA_DIR / "avatar.png"
        _PROFILE_JSON = _DATA_DIR / "profile.json"

        profile = {"username": "", "bio": ""}
        if _PROFILE_JSON.exists():
            try:
                profile = json.loads(_PROFILE_JSON.read_text(encoding="utf-8"))
            except Exception:
                pass

        # ── Canvas setup ─────────────────────────────────────────────────────────
        # We render at a fixed logical width (like a screen), then scale for output
        # Instagram friendly: square or portrait, high res
        CANVAS_W = 1080
        margin = 60
        contentW = CANVAS_W - margin * 2

        # ── First pass: measure total height ─────────────────────────────────────
        # We need to know total height before creating QImage
        # Use a dummy image to measure text
        dummy = QImage(1, 1, QImage.Format.Format_ARGB32)
        dummyPainter = QPainter(dummy)

        def measureText(text, fontSize, bold, width, indent=0):
            font = QFont("Segoe UI", fontSize)
            font.setBold(bold)
            dummyPainter.setFont(font)
            rect = QRectF(0, 0, width - indent, 9999)
            br = dummyPainter.boundingRect(rect, Qt.TextFlag.TextWordWrap, text)
            return br.height()

        avatarSize = 120
        profileH = max(avatarSize, measureText(profile.get("username",""), 22, True, contentW - avatarSize - 16)
                                + measureText(profile.get("bio",""), 13, False, contentW - avatarSize - 16) + 8)

        imgW = int(contentW * 0.38)
        imgH = int(imgW * 0.7)
        mediaCount = len(self.project.media) if self.project.media else 0

        titleH = measureText(self.project.title.upper(), 28, True, contentW)
        descH = measureText(self.project.description, 13, False, contentW)
        progressH = 18 + 6 + 20  # label + bar + pct

        imagesH = mediaCount * (imgH + 20)

        totalH = (margin                    # top margin
                + profileH + 20            # avatar + gap
                + 1 + 16                   # divider + gap
                + titleH + 12              # title
                + descH + 20              # description
                + progressH + 20           # progress
                + 1 + 16                   # divider
                + (40 + imagesH if mediaCount else 0)  # images section
                + margin)                  # bottom margin

        dummyPainter.end()

        CANVAS_H = int(totalH)

        # ── Create actual image ───────────────────────────────────────────────────
        img = QImage(CANVAS_W, CANVAS_H, QImage.Format.Format_ARGB32)
        img.fill(QColor("#FFFFFF"))
        painter = QPainter(img)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        x = float(margin)
        y = float(margin)

        # ── Helpers ───────────────────────────────────────────────────────────────
        def drawText(text, fontSize, bold, y, color=QColor("#111111"), indent=0, spacing=8, width=None):
            font = QFont("Segoe UI", fontSize)
            font.setBold(bold)
            painter.setFont(font)
            painter.setPen(color)
            w = (width if width else contentW) - indent
            rect = QRectF(x + indent, y, w, 9999)
            br = painter.boundingRect(rect, Qt.TextFlag.TextWordWrap, text)
            painter.drawText(rect, Qt.TextFlag.TextWordWrap, text)
            return y + br.height() + spacing

        def drawDivider(y):
            painter.setPen(QPen(QColor("#E0E0E0"), 1))
            painter.drawLine(int(x), int(y), int(x + contentW), int(y))
            return y + 16

        # ── Avatar + profile ──────────────────────────────────────────────────────
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

        textX = x + avatarSize + 16
        textW = contentW - avatarSize - 16

        nameFont = QFont("Segoe UI", 22)
        nameFont.setBold(True)
        painter.setFont(nameFont)
        painter.setPen(QColor("#111111"))
        nameRect = QRectF(textX, y + 18, textW, 9999)
        nameBR = painter.boundingRect(nameRect, Qt.TextFlag.TextWordWrap, profile.get("username", ""))
        painter.drawText(nameRect, Qt.TextFlag.TextWordWrap, profile.get("username", ""))

        bioFont = QFont("Segoe UI", 13)
        painter.setFont(bioFont)
        painter.setPen(QColor("#666666"))
        bioY = y + 18 + nameBR.height() + 6
        painter.drawText(QRectF(textX, bioY, textW, 9999), Qt.TextFlag.TextWordWrap, profile.get("bio", ""))

        y += max(avatarSize, nameBR.height() + 8 + 20) + 20
        y = drawDivider(y)

        # ── Project title ─────────────────────────────────────────────────────────
        y = drawText(self.project.title.upper(), 28, True, y, QColor("#111111"), spacing=12)

        # ── Description ───────────────────────────────────────────────────────────
        y = drawText(self.project.description, 13, False, y, QColor("#555555"), spacing=20)

        # ── Progress ──────────────────────────────────────────────────────────────
        progress = self.project.getProgress()

        labelFont = QFont("Segoe UI", 11)
        labelFont.setBold(True)
        painter.setFont(labelFont)
        painter.setPen(QColor("#111111"))
        painter.drawText(QRectF(x, y, contentW, 9999), Qt.TextFlag.TextWordWrap, "Progress")
        y += 22

        barH = 10
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#EEEEEE"))
        painter.drawRoundedRect(QRectF(x, y, contentW, barH), 5, 5)
        if progress > 0:
            painter.setBrush(QColor("#1A6FA8"))
            painter.drawRoundedRect(QRectF(x, y, contentW * (progress / 100), barH), 5, 5)
        y += barH + 6

        pctFont = QFont("Segoe UI", 10)
        painter.setFont(pctFont)
        painter.setPen(QColor("#888888"))
        painter.drawText(QRectF(x, y, contentW, 9999), Qt.TextFlag.TextWordWrap, f"{progress:.0f}% complete")
        y += 20 + 20

        y = drawDivider(y)

        # ── Images ────────────────────────────────────────────────────────────────
        if self.project.media:
            y = drawText("Images", 11, True, y, QColor("#111111"), spacing=14)

            for media in self.project.media:
                pixmap = media.getPixmap().scaled(
                    imgW, imgH,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                painter.drawPixmap(int(x), int(y), pixmap)

                if media.description:
                    captionFont = QFont("Segoe UI", 13)
                    painter.setFont(captionFont)
                    painter.setPen(QColor("#333333"))
                    capX = x + pixmap.width() + 20
                    capW = contentW - pixmap.width() - 20
                    capRect = QRectF(capX, y, capW, 9999)
                    capBR = painter.boundingRect(capRect, Qt.TextFlag.TextWordWrap, media.description)
                    capY = y + max(0.0, (pixmap.height() - capBR.height()) / 2)
                    painter.drawText(QRectF(capX, capY, capW, 9999), Qt.TextFlag.TextWordWrap, media.description)

                y += pixmap.height() + 20

        painter.end()

        # ── Save ──────────────────────────────────────────────────────────────────
        if asPdf:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filePath)

            # Set custom page size to match our image exactly
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