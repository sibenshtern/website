import json

import requests


url = "http://localhost:5000/api/jobs"

task_json = {
    "id": 1,
    "team_leader": 1,
    "job": "Слетать на Землю",
    "work_size": 3_600_000_000,
    "collaborators": "2, 3",
    "is_finished": False
}

correct_json = {
    "id": 1,
    "team_leader": 1,
    "job": "Слетать на Землю",
    "work_size": 3_600_000_000,
    "collaborators": "2, 3",
    "is_finished": True
}

incorrect_json1 = {
    "id": 7,
    "job": "Слетать на Землю",
    "work_size": 3_600_000_000,
    "is_finished": False
}  # в запросе отсутствуют некоторые поля

incorrect_json2 = {
    "id": 7,
    "team_leader": 1,
    "job": "Слетать на Землю",
    "work_size": 3_600_000_000,
    "collaborators": "2, 3",
    "is_finished": "RIGHT"
}  # неправильный тип данных is_finished

requests.post(url, json=task_json)

print(requests.get(url + '/1').json())
print(requests.put(url + '/1', json=correct_json).json())
print(requests.get(url + '/1').json())

print(requests.put(url + '/1', json=incorrect_json1).json())
print(requests.get(url + '/1').json())

print(requests.put(url + '/1', json=incorrect_json2).json())
print(requests.get(url + '/1').json())


