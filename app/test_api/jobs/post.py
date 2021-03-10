import pytest
import requests


all_jobs = requests.get("http://localhost:5000/api/jobs").json()


def test_incorrect_job_post_on_empty():
    res = requests.post("http://localhost:5000/api/jobs", json=dict()).json()
    assert res == {"error": "Empty request"}


def test_incorrect_job_post_on_not_all_keys():
    res = requests.post("http://localhost:5000/api/jobs", json={
        "job": "Create API tests"
    }).json()
    assert res == {"error": "Empty request"}


def test_incorrect_job_post_on_already_exists():
    res = requests.post("http://localhost:5000/api/jobs", json={
        "id": 1, "team_leader": 1, "job": "", "work_size": 1,
        "collaborators": "", "is_finished": False, "category_id": 1,
    }).json()
    assert res == {"error": "Id already exists"}


def test_correct_job_post():
    res = requests.post("http://localhost:5000/api/jobs", json={
        "id": 99999999, "team_leader": 1, "job": "", "work_size": 1,
        "collaborators": "", "is_finished": False, "category_id": 1,
    }).json()

    assert res == {"success": "OK"}

    updated_jobs = requests.get("http://localhost:5000/api/jobs").json()
    assert all_jobs != updated_jobs
