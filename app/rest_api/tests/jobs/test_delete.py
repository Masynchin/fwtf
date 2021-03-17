from contextlib import contextmanager

import pytest
import requests


@contextmanager
def temp_job():
    try:
        post_temp_job()
        temp_job = get_temp_job()
        yield temp_job
    finally:
        delete_temp_job(temp_job)


URL = "http://localhost:5000/api/v2/jobs"


def test_incorrect_id_int():
    res = requests.delete(f"{URL}/0").json()
    assert res == {"message": "Job 0 not found"}


def test_correct():
    with temp_job() as job:
        res = requests.delete(f"{URL}/{job['id']}").json()
    assert res == {"success": "OK"}


def post_temp_job():
    requests.post(URL, data=dict(
        team_leader=1,
        job="",
        work_size=1,
        collaborators="2,3",
        is_finished=True,
        category_id=1,
    ))


def delete_temp_job(job):
    requests.delete(f"{URL}/{job['id']}")


def get_temp_job():
    jobs = requests.get(URL).json()["jobs"]
    last_job = max(jobs, key=lambda j: j["id"])
    return last_job
