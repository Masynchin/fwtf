from contextlib import contextmanager

import pytest
import requests


@contextmanager
def zero_user():
    try:
        delete_and_post_zero_user()
        yield
    finally:
        delete_zero_user()


URL = "http://localhost:5000/api/users"


def test_incorrect_already_exists():
    res = requests.put(f"{URL}/0").json()
    assert res == {"error": "User with this ID doesn't exists"}


def test_incorrect_empty_json():
    with zero_user():
        res = requests.put(f"{URL}/0").json()
        assert res == {"error": "Empty request"}


def test_incorrect_not_all_keys():
    with zero_user():
        res = requests.put(f"{URL}/0", json={"name": ""}).json()
        assert res == {"error": "Empty request"}


def test_correct():
    with zero_user():
        old_user = requests.get(f"{URL}/0").json()
        new_json = old_user["users"].copy()
        new_json.pop("id")
        new_json["password"] = ""
        new_json["age"] += 1

        res = requests.put(f"{URL}/0", json=new_json).json()
        assert res == {"success": "OK"}

        new_user = requests.get(f"{URL}/0").json()
        assert old_user != new_user


def delete_and_post_zero_user():
    delete_zero_user()
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
    })


def delete_zero_user():
    requests.delete(f"{URL}/0")
