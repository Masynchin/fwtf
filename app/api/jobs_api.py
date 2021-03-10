from flask import Blueprint, request
from flask.json import jsonify

from app import db
from app.models import Jobs


blueprint = Blueprint("jobs_api", __name__, template_folder="templates")

JOB_KEYS = {
    "id", "team_leader", "job", "work_size",
    "collaborators", "is_finished", "category_id"
}

JOB_PUT_KEYS = JOB_KEYS - {"id"}


@blueprint.route("/api/jobs", methods=["GET"])
def get_jobs():
    jobs = Jobs.query.all()
    return jsonify({
        "jobs": [job.to_dict(only=JOB_KEYS) for job in jobs]
    })


@blueprint.route("/api/jobs/<int:job_id>", methods=["GET"])
def get_one_job(job_id):
    job = Jobs.query.get(job_id)
    if job is None:
        return jsonify({"error": "Not found"})
    return jsonify({"jobs": job.to_dict(only=JOB_KEYS)})


@blueprint.route("/api/jobs", methods=["POST"])
def post_jobs():
    job_json = request.json
    if not job_json or (JOB_KEYS - job_json.keys()):
        return jsonify({"error": "Empty request"})
    if Jobs.query.get(job_json["id"]) is not None:
        return jsonify({"error": "Id already exists"})

    job = Jobs(
        id=job_json["id"],
        team_leader=job_json["team_leader"],
        job=job_json["job"],
        work_size=job_json["work_size"],
        collaborators=job_json["collaborators"],
        is_finished=job_json["is_finished"],
        category_id=job_json["category_id"],
    )

    db.session.add(job)
    db.session.commit()
    return jsonify({"success": "OK"})


@blueprint.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_jobs(job_id):
    job = Jobs.query.get(job_id)
    if job is None:
        return jsonify({"error": "Job with this ID doesn't exists"})

    db.session.delete(job)
    db.session.commit()
    return jsonify({"success": "OK"})


@blueprint.route("/api/jobs/<int:job_id>", methods=["PUT"])
def edit_jobs(job_id):
    job = Jobs.query.get(job_id)
    if job is None:
        return jsonify({"error": "Job with this ID doesn't exists"})

    job_json = request.json
    if not job_json or (JOB_PUT_KEYS - job_json.keys()):
        return jsonify({"error": "Empty request"})
    
    job.team_leader = job_json["team_leader"]
    job.job = job_json["job"]
    job.work_size = job_json["work_size"]
    job.collaborators = job_json["collaborators"]
    job.is_finished = job_json["is_finished"]
    job.category_id = job_json["category_id"]

    db.session.commit()
    return jsonify({"success": "OK"})
