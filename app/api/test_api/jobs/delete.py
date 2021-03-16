import pytest
import requests


def test_incorrect_job_delete():
    res = requests.delete("http://localhost:5000/api/jobs/456").json()
    assert res == {"error": "Job with this ID doesn't exists"}


def test_correct_job_delete():
    requests.post("http://localhost:5000/api/jobs", json={
        "id": 10000000, "team_leader": 1, "job": "", "work_size": 1,
        "collaborators": "", "is_finished": False, "category_id": 1,
    })

    res = requests.delete("http://localhost:5000/api/jobs/10000000").json()
    assert res == {"success": "OK"}
