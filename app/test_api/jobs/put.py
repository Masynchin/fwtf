from contextlib import contextmanager

import pytest
import requests


@contextmanager
def zero_job():
    try:
        delete_and_post_test_job()
        yield
    finally:
        delete_test_job()


def test_incorrect_job_put_invalid_id():
    res = requests.put("http://localhost:5000/api/jobs/0").json()
    assert res == {"error": "Job with this ID doesn't exists"}


def test_incorrect_job_put_empty_json():
    with zero_job():
        res = requests.put("http://localhost:5000/api/jobs/0").json()
        assert res == {"error": "Empty request"}


def test_incorrect_job_put_not_all_keys():
    with zero_job():
        res = requests.put("http://localhost:5000/api/jobs/0", json={
            "team_leader": 1,
        }).json()
        assert res == {"error": "Empty request"}


def test_correct_job_put():
    with zero_job():
        old_test_job = requests.get("http://localhost:5000/api/jobs/0").json()
        new_json = old_test_job["jobs"].copy()
        new_json["is_finished"] = not new_json["is_finished"]

        requests.put("http://localhost:5000/api/jobs/0", json=new_json)
        new_test_job = requests.get("http://localhost:5000/api/jobs/0").json()
        assert old_test_job != new_test_job


def delete_and_post_test_job():
    delete_test_job()
    requests.post("http://localhost:5000/api/jobs", json={
        "id": 0, "team_leader": 1, "job": "", "work_size": 0,
        "collaborators": "", "is_finished": True, "category_id": 1
    })


def delete_test_job():
    requests.delete("http://localhost:5000/api/jobs/0")
