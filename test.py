import json
from datetime import datetime

class habitTracker: #how to know if member functions should only manage an instance or persisted class?
    def __init__(self):
        self.habits = []
        try:
            self._loadData() 
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON string: {e}")
            self.clear()
    def _loadData(self): #underscore infront indicates internal use only function
        with open("data.txt", "r") as data:
            self.habits = json.load(data)
    def _saveData(self):
        with open("data.txt", "w") as data:
            data.write(json.dumps(self.habits, indent=2))
    def _findEntry(self, habitName):
        for entry in self.habits:
            if entry["name"] == habitName:
                return entry
        return -1
    def clear(self):
        with open("data.txt", "w") as data:
            pass
    def addHabit(self):
        while (True):
            habit = input("What habit would you like to add? ").strip()
            if habit.strip() != "": #find a way to check if it is only whitespace (has to be some string feature or inbuilt function)
                habitDict = {}
                if self._findEntry(habit) != -1:
                    print("You already have this habit!")
                    continue
                habitDict["name"] = habit
                habitDict["completed"] = []
                self.habits.append(habitDict)
                break
        self._saveData()
    def removeHabit(self, habitName):
        toRemove = {}
        removable = False
        toRemove = self._findEntry() #assumes toRemove is a copy of entry
        removable= True if toRemove != -1 else False 
        if removable: #assumes only activates if the dictionary is not empty
            self.habits.remove(toRemove)
        else:
            print("Does not exist in the tracker!") 
        self._saveData()
    def completedHabit(self, habitName):
        today = datetime.now().isoformat()
        if self._findEntry() == -1: 
            print("This habit does not exist!")
            return
        entry = self._findEntry()          
        for i in entry["completed"]:
            if i == today: #make sure the datetime just receives the day not second or hour
                print("You already completed this habit today")
                return
        if habitName:
            entry["completed"].append(today)
        self._saveData()
    


if __name__ == "__main__":
    tracker = habitTracker()
    tracker.addHabit()
    tracker.addHabit()    
    # tracker.removeHabit('sd')
    # tracker.completedHabit("ad")
    
