import requests

json = {
    "name": "Egor",
    "surname": "Ivanov",
    "email": "tyaplyap@gmail.com",
    "age": "15",
    "position": "Inhabitant",
    "speciality": "",
    "password": "NONONO",
    "address": "module_2"
}

print(requests.get("http://127.0.0.1:5000/api/v2/users/1").json())
print(requests.get("http://127.0.0.1:5000/api/v2/users/dffdfs").json())

requests.delete("http://127.0.0.1:5000/api/v2/users/1")

requests.post("http://127.0.0.1:5000/api/v2/users", json=json)
print(requests.get("http://127.0.0.1:5000/api/v2/users").json())