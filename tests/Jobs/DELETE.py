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


# делаем для того, чтобы убедиться, что задача с таким id будет
print(requests.post(url, json=task_json).json())
print(requests.get(url).json())
print(requests.delete(url + '/1').json())
print(requests.delete(url + '/asd').json())  # неправильный id
print(requests.get(url).json())


