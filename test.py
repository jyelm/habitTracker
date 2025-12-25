import json
from datetime import datetime


habits = []

def addHabit():
    while (True):
        habit = input("What habit would you like to add? ").strip()
        if habit.strip() != "": #find a way to check if it is only whitespace (has to be some string feature or inbuilt function)
            habitDict = {}
            habitDict["name"] = habit
            habitDict["completed"] = []
            habits.append(habitDict)
            break
    with open("data.txt", "w") as data:
        data.write(json.dumps(habits))
def removeHabit(habitName):
    toRemove = {}
    for entry in habits:
        if entry["name"] == habitName:
            toRemove = entry #assumes toRemove is a copy of entry
            break
    if toRemove: #assumes only activates if the dictionary is not empty
        habits.remove(toRemove) 
    with open("data.txt", "w") as data:
        data.write(json.dumps(habits))
def completedHabit(habitName):
    today = datetime.now().isoformat()
    if habitName:
        for entry in habits:
            if entry[habitName]:
                entry["completed"].append(today)


if __name__ == "__main__":
    addHabit()
    addHabit()    
    removeHabit('sd')
    
