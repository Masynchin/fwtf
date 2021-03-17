from contextlib import contextmanager

import pytest
import requests


@contextmanager
def temp_user():
    try:
        post_temp_user()
        temp_user = get_temp_user()
        yield temp_user
    finally:
        delete_temp_user(temp_user)


URL = "http://localhost:5000/api/v2/users"


def test_incorrect_id_int():
    res = requests.get(f"{URL}/0").json()
    assert res == {"message": "User 0 not found"}


def test_correct_one():
    with temp_user() as user:
        res = requests.get(f"{URL}/{user['id']}").json()
    assert res != {"message": f"User {user['id']} not found"}


def test_correct_all():
    res = requests.get(URL).json()
    assert "message" not in res


def post_temp_user():
    requests.post(URL, data=dict(
        surname="",
        name="",
        age=0,
        position="",
        speciality="",
        address="",
        email="",
        city_from="",
    ))


def delete_temp_user(user):
    requests.delete(f"{URL}/{user['id']}")


def get_temp_user():
    users = requests.get(URL).json()["users"]
    last_user = max(users, key=lambda u: u["id"])
    return last_user
