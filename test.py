import json
from datetime import datetime, date, timedelta

class ExistenceError(Exception):
    pass

class HabitTracker: #how to know if member functions should only manage an instance or persisted class?
    def __init__(self):
        self.habits = []
        try:
            self._loadData() 
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON string: {e}")
            self.clear()
    def _loadData(self): #underscore infront indicates internal use only function
        try:
            with open("data.txt", "r") as data:
                self.habits = json.load(data)
        except FileNotFoundError as e:
            print("Creating new file")
            self.clear()
    def _saveData(self):
        with open("data.txt", "w") as data:
            data.write(json.dumps(self.habits, indent=2))
    def _findEntry(self, habitName):
        for entry in self.habits:
            if entry["name"] == habitName:
                return entry
        return None
    def _maxStreak(self, entry):
        listDates = entry["completed"]
        lengthList = len(listDates)
        consecutive = 1
        if lengthList <= 1:
            return None
        for i in range(lengthList-1):
            dateLater = date.fromisoformat(listDates[i+1])
            datePrior = date.fromisoformat(listDates[i])
            difference = dateLater - datePrior
            if difference == timedelta(days=1):
                consecutive+=1
        if consecutive > 1:
            return consecutive
        return None
    def _curStreak(self, entry): #counts the streak up to the day prior
        listDates = entry["completed"] #should already be sorted
        lengthList = len(listDates)
        consecutive = 1
        if lengthList <= 1:
            return None
        mostRecent = listDates[-1]
        today = datetime.now().date()
        yesterday = (today - timedelta(days=1)).isoformat()
        today = today.isoformat() 
        index = None
        if mostRecent != today and mostRecent != yesterday:
            return None
        for day in listDates:
            if day == mostRecent:
                index = listDates.index(day) #make sure variable names are unique to avoid variable shadowings
        if index is None:
            return None
        for i in range(index, 0, -1):
            dateLater = date.fromisoformat(listDates[i])
            datePrior = date.fromisoformat(listDates[i-1])
            difference = dateLater - datePrior
            if difference == timedelta(days=1):
                consecutive+=1
        if consecutive > 1:
            return consecutive
        return None
    def clear(self):
        with open("data.txt", "w") as data:
            pass
        self.habits = []
    def addHabit(self):
        while (True):
            habit = input("What habit would you like to add? ").strip()
            if habit != "": 
                habitDict = {}
                if self._findEntry(habit) is not None:
                    print("You already have this habit!")
                    continue
                habitDict["name"] = habit
                habitDict["completed"] = []
                self.habits.append(habitDict)
                break
        self._saveData()
    def removeHabit(self, habitName):
        toRemove = self._findEntry(habitName) #assumes toRemove is a copy of entry
        if toRemove is not None: #assumes only activates if the dictionary is not empty
            self.habits.remove(toRemove)
        else:
            raise ExistenceError("Does not exist in the tracker!")
        self._saveData()
    def completedHabit(self, habitName):
        today = datetime.now().date().isoformat()
        entry = self._findEntry(habitName) 
        if entry is None: 
            raise ExistenceError("This habit does not exist!")
        for date in entry["completed"]:
            if date == today: #make sure the datetime just receives the day not second or hour
                raise ExistenceError("You already completed this habit today")
        if habitName:
            entry["completed"].append(today)
        self._saveData()
    def displayHabits(self):
        print("The habits you have:")
        for entry in self.habits:
            habit = entry["name"]
            if entry["completed"]:
                for date in entry["completed"]:
                    if date==datetime.now().date().isoformat():
                        print(f"{habit} has been completed today")
                dates = ','.join(entry["completed"])        
                print(f"{habit} has been completed on {dates}")
            else:
                print(f"{habit} has not been completed")
            maxStreak = self._maxStreak(entry)
            curStreak = self._curStreak(entry)
            if maxStreak is not None:
                print(f"{habit} has a maximum streak of {maxStreak}")
            if curStreak is not None:
                print(f"{habit} has a current streak of {curStreak}")
    def run(self):
        while True:
            method = input("What would you like to do? (type quit in any looped entry to go back to main menu)\n" \
            "Press 1 to clear\nPress 2 to add a Habit\nPress" \
            " 3 to remove a habit\nPress 4 to mark a habit as" \
            " complete today\nPress 5 to display the habits you" \
            " have completed\nPress 6 to quit\n") #argparse as a better CLI package?
            match method:
                case "1":
                        self.clear()
                case "2":
                    self.addHabit()
                case "3":
                    while True:
                        habitToRemove = input("What habit would you like to remove? ")
                        if habitToRemove == "quit":
                            break
                        try:
                            self.removeHabit(habitToRemove)
                            break
                        except ExistenceError as e:
                            print(e)
                            continue
                case "4":
                    while True:
                        habitToComplete = input("What habit would you like to mark as complete? ")
                        if habitToComplete == "quit":
                            break
                        try:
                            self.completedHabit(habitToComplete)
                            break
                        except ExistenceError as e:
                            print(e)
                            continue
                case "5":
                    self.displayHabits()
                case "6":
                    break
                case _:
                    print("invalid input, try again")
                    continue

if __name__ == "__main__":
    tracker = HabitTracker()
    tracker.run()
    # tracker.clear()  # Start fresh
    
    # # Manually set up test data
    # tracker.habits = [
    #     {"name": "Exercise", "completed": ["2025-12-23", "2025-12-24", "2025-12-25"]},
    #     {"name": "Read", "completed": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-10"]}
    # ]
    
    # # Test streak calculation
    # print(tracker._maxStreak(tracker.habits[0]))  # Should be ?
    # print(tracker._curStreak(tracker.habits[0]))  # Should be ?
    
