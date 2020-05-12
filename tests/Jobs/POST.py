import json

import requests


url = "http://localhost:5000/api/jobs"

correct_json = {
    "id": 7,
    "team_leader": 1,
    "job": "Слетать на Землю",
    "work_size": 3_600_000_000,
    "collaborators": "2, 3",
    "is_finished": False
}

incorrect_json = {
    "id": 7,
    "team_leader": 1,
    "job": "Слетать на Землю",
    "work_size": 3_600_000_000,
    "collaborators": "2, 3",
    "is_finished": False
}  # существующий id

incorrect_json2 = {
    "id": 7,
    "job": "Слетать на Землю",
    "work_size": 3_600_000_000,
    "is_finished": False
}  # в запросе отсутствуют некоторые поля

incorrect_json3 = {
    "id": 7,
    "team_leader": 1,
    "job": "Слетать на Землю",
    "work_size": 3_600_000_000,
    "collaborators": "2, 3",
    "is_finished": "RIGHT"
}  # неправильный тип данных is_finished

print(requests.get(url).json())
print(requests.post(url, json=correct_json).json())
print(requests.post(url, json=incorrect_json).json())
print(requests.post(url, json=incorrect_json2).json())
print(requests.post(url, json=incorrect_json3).json())
print(requests.get(url).json())


