from flask import Flask, jsonify, request, send_from_directory #converts list of dictionary form to json which is interpretable by webbrowser
from habit_tracker import HabitTracker, ExistenceError

app = Flask(__name__)
tracker = HabitTracker()

#what does this do?
@app.route("/")
def serve_frontend():
    return send_from_directory(".", "index.html")

@app.route("/api/habits", methods = ["GET"]) #"When someone asks for the habit list, just give it to them; retrieve the data and return the information to the user"
def get_habits(): #may be a naming convention conflict
    return jsonify(tracker.habits) #simple member variable accessing

@app.route("/api/habits/clear", methods = ["POST"]) #2 different functions cannot have the same route and method
def clear_habits(): 
    return jsonify(tracker.clear()) 

@app.route("/api/habits", methods = ["POST"]) #can only make post requests
def add_habits(): #use snake case naming convention
    data = request.get_json() #turns json request back into dictionary
    habit_name = data.get("name", "").strip() #assuming that .get allows the setting of default values
    try:
        tracker.addHabit(habit_name)
        return jsonify({"success": True}) #must be for easier handling for the frontend
    except ExistenceError as e: 
        return jsonify({"success": False, "error": str(e)}), 400 #must be the error code
 
@app.route("/api/habits", methods = ["DELETE"]) 
def remove_habits(): 
    data = request.get_json() 
    habit_name = data.get("name", "").strip() 
    try:
        tracker.removeHabit(habit_name)
        return jsonify({"success": True}) 
    except ExistenceError as e: 
        return jsonify({"success": False, "error": str(e)}), 400 

@app.route("/api/habits/complete", methods = ["POST"]) #PUT works but since we are creating a completion record POST
def complete_habits(): 
    data = request.get_json() 
    habit_name = data.get("name", "").strip() 
    try:
        tracker.completedHabit(habit_name)
        return jsonify({"success": True}) 
    except ExistenceError as e: 
        return jsonify({"success": False, "error": str(e)}), 400      

@app.route("/api/habits/complete", methods = ["DELETE"]) # decorator probablt doing lots behind the scenes
def remove_completed_habits(): 
    data = request.get_json() 
    habit_name = data.get("name", "").strip() #what does .get method do?
    date_to_remove = data.get("completed","").strip() # could be wrong
    try:
        tracker.removeComplete(habit_name, date_to_remove)
        return jsonify({"success": True}) 
    except ExistenceError as e: 
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/habits/details", methods = ["GET"]) #information is really being retrieved; isn't the information about the streak being created?
def get_habit_details():
    detailed_habits = []
    for habit in tracker.habits:
        habit_details = {
            "name": habit["name"],
            "completed": habit["completed"],
            "currentStreak": tracker._curStreak(habit),
            "maxStreak": tracker._maxStreak(habit)
        }
        detailed_habits.append(habit_details)
    return(jsonify(detailed_habits))

@app.route("/api/habits/test-streak", methods=["POST"]) #flow - server started, tracker object created, load data run, so this endpoint needs to be made to    
def test_streak_setup():                                #reload the reading of data.txt if modified for testing purposes
    # Clear and set up test data
    tracker.clear()
    tracker.habits = [
        {"name": "Exercise", "completed": ["2025-01-15", "2025-01-16", "2025-01-17"]},
        {"name": "Read", "completed": ["2025-01-10"]}
    ]
    tracker._saveData()
    return jsonify({"success": True, "message": "Test data loaded"})

      
if __name__ == "__main__":
    app.run(debug=True)