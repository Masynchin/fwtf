import pytest
import requests


URL = "http://localhost:5000/api/v2/users"


def test_incorrect_empty():
    res = requests.post(URL, data=dict()).json()
    assert res != {"success": "OK"}


def test_incorrect_not_all():
    res = requests.post(URL, data=dict(
        surname="",
        name="",
        age=0,
        position="",
        speciality="",
        address="",
        email="",
    )).json()
    # `city_from` param is missing
    assert res != {"success": "OK"}


def test_correct():
    assert len(requests.get(URL).json()["users"]) == 3
    res = requests.post(URL, data=dict(
        surname="",
        name="",
        age=0,
        position="",
        speciality="",
        address="",
        email="",
        city_from="",
    )).json()
    assert res == {"success": "OK"}

    users = requests.get(URL).json()
    last_user = max(users["users"], key=lambda u: u["id"])
    requests.delete(f"{URL}/{last_user['id']}")
