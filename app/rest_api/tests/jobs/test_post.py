import pytest
import requests


URL = "http://localhost:5000/api/v2/jobs"


def test_incorrect_empty():
    res = requests.post(URL, data=dict()).json()
    assert res != {"success": "OK"}


def test_incorrect_not_all():
    res = requests.post(URL, data=dict(
        team_leader=1,
        job="",
        work_size=1,
        collaborators="2,3",
        is_finished=True,
    )).json()
    # `category_id` param is missing
    assert res != {"success": "OK"}


def test_correct():
    res = requests.post(URL, data=dict(
        team_leader=1,
        job="",
        work_size=1,
        collaborators="2,3",
        is_finished=True,
        category_id=1,
    )).json()
    assert res == {"success": "OK"}

    jobs = requests.get(URL).json()
    last_job = max(jobs["jobs"], key=lambda j: j["id"])
    requests.delete(f"{URL}/{last_job['id']}")
