import requests


API_URL = "http://127.0.0.1:5000/api/jobs"

# В БД должно уже быть добавлены 4 пользователя и 1 работа, по предыдущим заданиям
print(requests.get(API_URL).json())
print(requests.post(API_URL, json={
    "id": 2,
    'team_leader': 1,
    'job': 'test',
    'work_size': 123,
    'collaborators': '2, 3',
    'is_finished': False,
}).json())

print(requests.post(API_URL, json={
    "id": 2,
    'team_leader': 1,
    'job': 'test2',
    'work_size': 123,
    'collaborators': '2, 3',
    'is_finished': False,
}).json())

print(requests.post(API_URL, json={
    'team_leader': 1,
    'work_size': 123,
    'collaborators': '2, 3',
    'is_finished': False,
}).json())

print(requests.post(API_URL, json={
    "id": 3,
    'team_leader': 1,
    'job': 'test2',
    'work_size': "asdasd",
    'collaborators': '2, 3',
    'is_finished': False,
}).json())

print(requests.post(API_URL, json={
    "id": 3,
    'team_leader': 1000,
    'job': 'test2',
    'work_size': 123,
    'collaborators': '2, 3',
    'is_finished': False,
}).json())

print(requests.post(API_URL, json={
    "id": 3,
    'team_leader': 1000,
    'job': 'test2',
    'work_size': 123,
    'collaborators': '2, 3, 4, 5, 6, 7, 1000',
    'is_finished': False,
}).json())

print(requests.post(API_URL).json())

# All jobs:
print(requests.get(API_URL).json())
