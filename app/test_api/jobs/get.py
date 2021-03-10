import pytest
import requests


def test_all_jobs():
    all_jobs = requests.get("http://localhost:5000/api/jobs").json()
    assert all_jobs != {"error": "Not found"}


def test_one_job_correct():
    correct_job = requests.get("http://localhost:5000/api/jobs/1").json()
    assert correct_job != {"error": "Not found"}


def test_one_job_incorrect_id_int():
    incorrect_job = requests.get("http://localhost:5000/api/jobs/-1").json()
    assert incorrect_job == {"error": "Not found"}


def test_one_job_incorrect_id_str():
    incorrect_job = requests.get("http://localhost:5000/api/jobs/q").json()
    assert incorrect_job == {"error": "Not found"}
