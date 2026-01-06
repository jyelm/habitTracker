from ..habit_tracker import HabitTracker

tracker = HabitTracker()
try:
    tracker.addHabit("TestHabit1")
    tracker.addHabit("TestHabit2")
except:
    pass

result = tracker.getAllHabits()
print(result)