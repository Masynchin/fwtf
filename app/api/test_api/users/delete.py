import pytest
import requests


URL = "http://localhost:5000/api/users"


def test_incorrect_does_not_exists():
    res = requests.delete(f"{URL}/0").json()
    assert res == {"error": "User with this ID doesn't exists"}


def test_correct():
    requests.post(URL, json={
        "id": 0,
        "surname": "",
        "name": "",
        "age": 0,
        "position": "",
        "speciality": "",
        "address": "",
        "email": "",
        "password": "",
        "city_from": "",
    }).json()

    res = requests.delete(f"{URL}/0").json()
    assert res == {"success": "OK"}
