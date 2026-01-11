import pytest 
from habit_tracker import HabitTracker, ExistenceError

@pytest.fixture
def tracker():
    t = HabitTracker()
    t.clear
    return t #this object is returned as an object for the paramter to operate on; reduces the need to rewrite these two lines for each function

def test_add_habit_success(tracker): #this parameter looks for a pytest fixture function
    tracker.addHabit("Exersize")
    habits = tracker.getAllHabits()
    assert len(habits) == 1 #raises an assertion error which is easier to trace
    assert habits[0]["name"] == "Exersize"

def test_add_duplicate_habit_failes(tracker):
    """
    We want the code to fail here; essentially we are figuring out whether the code properly fails,
    raises the right error, and raises and error in the first place. The least verbose and most 
    straighforward way to do this is via a pytest.raises() call
    """
    tracker.addHabit("Exersize") #so does this return just a boolean value?
    with pytest.raises(ExistenceError):
        tracker.addHabit("Exersize")

def test_remove_habit_success(tracker):
    tracker.addHabit("Exersize")
    tracker.removeHabit("Exersize")
    habits = tracker.getAllHabits()
    assert len(habits) == 0 #if this fails assertion error

def try_remove_nonexistent_habits_fails(tracker):
    with pytest.raises(ExistenceError):
        tracker.removeHabit("Exersize")

def test_complete_habit_success(tracker):
    tracker.addHabit("Exersize")
    tracker.completedHabit("Exersize")
    habits = tracker.getAllHabits()
    assert len(habits[0]["completed"]) == 1

def test_complete_twice_fails(tracker):
    tracker.addHabit("Exersize")
    tracker.completedHabit("Exersize")
    with pytest.raises(ExistenceError):
        tracker.completed("Exersize")
    

