import requests


API_URL = "http://127.0.0.1:5000/api/v2/users"

# GET

print(requests.get(API_URL).json())
print(requests.get(API_URL + "/1").json())
print(requests.get(API_URL + "/1000").json())
print(requests.get(API_URL + "/string").json())

# POST

print(requests.post(API_URL, json={
    'id': 1000,
    'name': "asd",
    'surname': "asdasdads",
    'email': 'asd@asd',
    'position': "asd",
    'address': 'asdasd',
    'password': "1",
    'age': 123,
    'speciality': "asdasdasd",
}).json())

print(requests.post(API_URL, json={
    'id': 1000,
    'name': "asd",
    'surname': "asdasdads",
    'email': 'asd@asd',
    'position': "asd",
    'address': 'asdasd',
    'password': "1",
    'age': 123,
    'speciality': "asdasdasd",
}).json())

print(requests.post(API_URL, json={
    'id': 1001,
    'name': "asd",
    'surname': "asdasdads",
    'email': 'asd@asd',
    'position': "asd",
    'address': 'asdasd',
    'password': "1",
    'age': 123,
    'speciality': "asdasdasd",
}).json())

print(requests.post(API_URL, json={
    'name': "asd",
    'email': 'asd@asd2',
    'position': "asd",
    'address': 'asdasd',
    'password': "1",
    'age': 123,
    'speciality': "asdasdasd",
}).json())

print(requests.post(API_URL, json={
    'name': "asd",
    'surname': "asdasdads",
    'email': 'asd@asd3',
    'position': "asd",
    'address': 'asdasd',
    'password': "1",
    'age': "asd",
    'speciality': "asdasdasd",
}).json())

print(requests.post(API_URL).json())
print(requests.get(API_URL).json())

# DELETE

print(requests.delete(API_URL + "/1000").json())
print(requests.get(API_URL).json())
print(requests.delete(API_URL + "/99999").json())
print(requests.delete(API_URL + "/string").json())
