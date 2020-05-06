import requests


API_URL = "http://127.0.0.1:5000/api/jobs"


# В БД должно уже быть добавлены 4 пользователя и 1 работа, по предыдущим заданиям
print(requests.get(API_URL).json())
print(requests.put(API_URL + "/1", json={
    'job': 'edit_test',
    'is_finished': True,
}
).json())

print(requests.put(API_URL + "/1", json={
    'job': 'rollback',
    'is_finished': False,
}
).json())

print(requests.put(API_URL + "/asdasd", json={
    'job': 'edit_test3',
    'is_finished': False,
}).json())

print(requests.get(API_URL).json())
