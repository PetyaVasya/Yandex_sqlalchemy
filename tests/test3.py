import requests


API_URL = "http://127.0.0.1:5000/api/jobs"

# В БД должно уже быть добавлены 4 пользователя и 1 работа, по предыдущим заданиям
print(requests.get(API_URL).json())
print(requests.delete(API_URL + "/1").json())

print(requests.get(API_URL).json())
print(requests.delete(API_URL + "/1000").json())
print(requests.delete(API_URL + "/string").json())
