import requests


API_URL = "http://127.0.0.1:5000/api/jobs"

print(requests.get(API_URL).json())
print(requests.get(API_URL + "/1").json())
print(requests.get(API_URL + "/1000").json())
print(requests.get(API_URL + "/string").json())
