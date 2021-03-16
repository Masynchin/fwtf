import pytest
import requests


URL = "http://localhost:5000/api/users"


def test_all_correct():
    all_users = requests.get(URL).json()
    assert all_users != {"error": "Not found"}


def test_one_correct():
    correct_job = requests.get(f"{URL}/1").json()
    assert correct_job != {"error": "Not found"}


def test_one_incorrect_id_int():
    incorrect_job = requests.get(f"{URL}/-1").json()
    assert incorrect_job == {"error": "Not found"}


def test_one_incorrect_id_str():
    incorrect_job = requests.get(f"{URL}/q").json()
    assert incorrect_job == {"error": "Not found"}
