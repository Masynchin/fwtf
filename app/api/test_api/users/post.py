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


def test_incorrect_empty_json():
    res = requests.post(URL, json=dict()).json()
    assert res == {"error": "Empty request"}


def test_incorrect_not_all_keys_json():
    res = requests.post(URL, json={
        "name": "name"
    }).json()
    assert res == {"error": "Empty request"}


def test_incorrect_id_already_exists():
    with zero_user():
        res = requests.post(URL, json={
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
        assert res == {"error": "Id already exists"}


def test_incorrect_email_already_exists():
    with zero_user():
        zero_json = requests.get(f"{URL}/0").json()
        email = zero_json["users"]["email"]
        res = requests.post(URL, json={
            "id": 1000000000,
            "surname": "",
            "name": "",
            "age": 0,
            "position": "",
            "speciality": "",
            "address": "",
            "email": email,
            "password": "",
            "city_from": "",
        }).json()
        assert res == {"error": "This email is already used"}


def test_correct():
    all_users = requests.get(URL).json()

    res = requests.post(URL, json={
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
    assert res == {"success": "OK"}

    updated_users = requests.get(URL).json()
    assert all_users != updated_users

    delete_zero_user()


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
