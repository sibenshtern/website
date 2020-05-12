import requests

json = {
    "id": 1,
    "team_leader": 1,
    "job": "Слетать на Землю",
    "work_size": 3_600_000_000,
    "collaborators": "2, 3",
    "is_finished": False
}

print(requests.get("http://127.0.0.1:5000/api/v2/jobs/1").json())
print(requests.get("http://127.0.0.1:5000/api/v2/jobs/WTF").json())

requests.delete("http://127.0.0.1:5000/api/v2/jobs/1")

requests.post("http://127.0.0.1:5000/api/v2/jobs", json=json)

print(requests.get("http://127.0.0.1:5000/api/v2/jobs").json())
