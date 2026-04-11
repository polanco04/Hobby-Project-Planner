from datetime import datetime
    
class Reminder:
    def __init__(self, remindAt: datetime, repeat: bool):
        self.remindAt = remindAt
        self.enabled = True
        self.repeat = repeat
        self.lastTriggered: datetime = None

    def updateTime(self, newTime: datetime):
        self.remindAt = newTime

    def toggle(self):
        self.enabled = not self.enabled

class ReminderSystem:
    def __init__(self):
        self.reminders: list[Reminder] = []

    def scheduleReminder(self, time: datetime, repeat: bool):
        reminder = Reminder(time, repeat)
        self.reminders.append(reminder)

    def cancel(self, reminder: Reminder):
        if reminder in self.reminders:
            self.reminders.remove(reminder)
    
    def trigger(self, reminder: Reminder):
        reminder.lastTriggered = datetime.now()
        if not reminder.repeat:
            self.cancel(reminder)
    
    def getAllReminders(self) -> list[Reminder]:
        return self.reminders