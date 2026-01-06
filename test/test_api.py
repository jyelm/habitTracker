import requests

BASE_URL = "http://localhost:5000/api/habits"
COMPLETE_URL = "http://localhost:5000/api/habits/complete"
DETAILS_URL = "http://localhost:5000/api/habits/details"
CLEAR_URL = "http://localhost:5000/api/habits/clear"
TEST_URL = "http://localhost:5000/api/habits/test-streak"


# requests.post(CLEAR_URL)
# requests.post(BASE_URL, json={"name": "TestHabit"}) #specify the request with method and URL
requests.post(TEST_URL)
response = requests.get(DETAILS_URL)
print(response.json())

