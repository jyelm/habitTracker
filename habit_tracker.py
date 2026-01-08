import json
from datetime import datetime, date, timedelta
from .database import get_connection #since this is now being run as a package the do indicates this can be found in the same directory as this file
from collections import defaultdict

class ExistenceError(Exception):
    pass
"""
THIS THE LOGIC FOR TEXT FILE CODE; THE UNCOMMENT LOGIC IS FOR THE CODE ASSOCIATED WITH A POSTGRESQL

class HabitTracker: #how to know if member functions should only manage an instance or persisted class?
    def __init__(self):
        #I wonder how all this logic would change if the data was stored in a database
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
    #must this exist in the web browser version?
    def clear(self):
        with open("data.txt", "w") as data:
            pass
        self.habits = []
    def addHabit(self, habitName):
        if habitName != "": 
            habitDict = {}
            if self._findEntry(habitName) is not None:
                raise ExistenceError("You already have this habit!")
            habitDict["name"] = habitName
            habitDict["completed"] = []
            self.habits.append(habitDict)
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
    def removeComplete(self, habitName, dateToRemove):
        entry = self._findEntry(habitName)
        if entry is None:
            raise ExistenceError("This habit does not exist!")
        if dateToRemove not in entry["completed"]:
            raise ExistenceError("This date was not marked complete!")
        indexEntry = self.habits.index(entry)
        self.habits[indexEntry]["completed"].remove(dateToRemove)
        self._saveData()
    #must this exist in the web browser version?
    def displayHabits(self):
        print("The habits you have:")
        for entry in self.habits:
            habit = entry["name"]
            if entry["completed"]:
                if datetime.now().date().isoformat() in entry["completed"]:
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
    """

    # def run(self):
    #     while True:
    #         method = input("What would you like to do? (type quit in any looped entry to go back to main menu)\n" \
    #         "Press 1 to clear\nPress 2 to add a Habit\nPress" \
    #         " 3 to remove a habit\nPress 4 to mark a habit as" \
    #         " complete today\nPress 5 to display the habits you" \
    #         " have completed\nPress 6 to quit\n") #argparse as a better CLI package?
    #         match method:
    #             case "1":
    #                     self.clear()
    #             case "2":
    #                 self.addHabit()
    #             case "3":
    #                 while True:
    #                     habitToRemove = input("What habit would you like to remove? ")
    #                     if habitToRemove == "quit":
    #                         break
    #                     try:
    #                         self.removeHabit(habitToRemove)
    #                         break
    #                     except ExistenceError as e:
    #                         print(e)
    #                         continue
    #             case "4":
    #                 while True:
    #                     habitToComplete = input("What habit would you like to mark as complete? ")
    #                     if habitToComplete == "quit":
    #                         break
    #                     try:
    #                         self.completedHabit(habitToComplete)
    #                         break
    #                     except ExistenceError as e:
    #                         print(e)
    #                         continue
    #             case "5":
    #                 self.displayHabits()
    #             case "6":
    #                 break
    #             case _:
    #                 print("invalid input, try again")
    #                 continue

# if __name__ == "__main__":
#     tracker = HabitTracker()
#     tracker.run()


class HabitTracker():
    def __init__(self):
        pass
    def addHabit(self, habitName):
        if habitName == "":
            return 
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM habits WHERE name = %s", (habitName,)) # assuming habitName hills in for "%s" placeholder; habits has a name column
                                                                              # think about language - "select the id from the habits table where the name is equal to habitName"
        existing = cursor.fetchone() #fetches the first instance of the query

        if existing:
            cursor.close() #close the cursor first
            conn.close()
            raise ExistenceError("You already have this habit!")
        cursor.execute("INSERT INTO habits (name) VALUES (%s)", (habitName,)) #comma after makes it a tuple which is required by the python library
        conn.commit() #saves changes

        cursor.close()
        conn.close()
    def removeHabit(self, habitName):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM habits WHERE name = %s", (habitName,))
        existing = cursor.fetchone()
        if existing is None:
          cursor.close()
          conn.close()
          raise ExistenceError("Does not exist in tracker")
        cursor.execute("DELETE FROM habits WHERE name = %s", (habitName,))
        conn.commit()

        cursor.close()
        conn.close()

    def getAllHabits(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Single query with LEFT JOIN and ORDER BY

        #Left join allows it to where a habit can exist where it has never been completed
        #Order by allows the habits and completions to be grouped together; maybe order by index
        cursor.execute("""
            SELECT habits.id, habits.name, completions.completed_date
            FROM habits
            LEFT JOIN completions ON habits.id = completions.habit_id
            ORDER BY habits.id, completions.completed_date 
        """)
        
        rows = cursor.fetchall()
        if not rows: #fetcall returns an empty string
            return []

        habits = {} #use dictionary where each key is the habit_id
        for row in rows:  #habit id not always starting at 1 or in order
            habit_id = row[0]
            habit_name = row[1]
            habit_completion = row[2]
            if habit_id not in habits:
                habits[habit_id] = {"name": habit_name, "completed": []}
            if habit_completion is not None: #should be None if does not exist
                habits[habit_id]["completed"].append(habit_completion.isoformat())
        
        cursor.close()
        conn.close()
        
        return list(habits.values())
    
    def completedHabit(self, habitName):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM habits WHERE name = %s", (habitName,)) #select from the id column of the habits datatable where the name is the value of this placeholder
                habit_id_tuple = cursor.fetchone() #should be a tuple with one element
                if habit_id_tuple is None:
                    raise ExistenceError("This habit doesn't exist!")
                habit_id = habit_id_tuple[0]
                date_today = date.today() 
                cursor.execute("SELECT id FROM completions WHERE habit_id = %s AND completed_date = %s", 
                               (habit_id, date_today)) #select id since it is guranteed to be unique; maybe use "where keyword" when specifying column name
                exists = cursor.fetchone()
                if exists:
                    raise ExistenceError("This habit has already been completed!")
                cursor.execute("INSERT INTO completions (habit_id, completed_date) VALUES (%s, %s)", (habit_id, date_today))
                conn.commit()                
            
    def removeComplete(self, habitName, dateToRemove):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM habits WHERE name = %s", (habitName,))
                habit_id_tuple = cursor.fetchone() 
                if habit_id_tuple is None:
                    raise ExistenceError("This habit doesn't exist!")
                habit_id = habit_id_tuple[0]
                cursor.execute("SELECT id FROM completions WHERE habit_id = %s AND completed_date = %s", 
                               (habit_id, dateToRemove))
                to_remove = cursor.fetchone()
                if not to_remove:
                    raise ExistenceError("This date doesn't exist!")
                cursor.execute("DELETE FROM completions WHERE habit_id = %s AND completed_date = %s", (habit_id, dateToRemove))
                conn.commit() 

    def clear(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM habits") #should cascade and delete from completions aswell
                conn.commit()
    
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



