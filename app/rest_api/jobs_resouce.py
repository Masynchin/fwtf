from flask.json import jsonify
from flask_restful import reqparse, abort, Resource

from app import db
from app.models import Jobs


GET_KEYS = {"id", "team_leader", "job", "work_size",
    "collaborators", "is_finished", "category_id"}


class JobsResource(Resource):

    def get(self, job_id):
        job = Jobs.query.get(job_id)
        self.abort_if_job_not_find(job, job_id)
        return jsonify(job.to_dict(only=GET_KEYS))

    def abort_if_job_not_find(self, job, job_id):
        if job is None:
            abort(404, message=f"Job {job_id} not found")

    def delete(self, job_id):
        job = Jobs.query.get(job_id)
        self.abort_if_job_not_find(job, job_id)
        db.session.delete(job)
        db.session.commit()
        return jsonify({"success": "OK"})


parser = reqparse.RequestParser()
parser.add_argument("team_leader", required=True, type=int)
parser.add_argument("job", required=True)
parser.add_argument("work_size", required=True, type=int)
parser.add_argument("collaborators", required=True)
parser.add_argument("is_finished", required=True, type=bool)
parser.add_argument("category_id", required=True, type=int)


class JobsListResource(Resource):
    def get(self):
        jobs = Jobs.query.all()
        return jsonify({"jobs": [u.to_dict(only=GET_KEYS) for u in jobs]})

    def post(self):
        args = parser.parse_args()
        job = Jobs(
            team_leader=args["team_leader"],
            job=args["job"],
            work_size=args["work_size"],
            collaborators=args["collaborators"],
            is_finished=args["is_finished"],
            category_id=args["category_id"],
        )
        db.session.add(job)
        db.session.commit()
        return jsonify({"success": "OK"})
