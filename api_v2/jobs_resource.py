from flask import jsonify
from flask_restful import abort, Resource
from sqlalchemy.exc import StatementError

from api_v2.job_parser import parser
from data import db_session
from data.jobs import Jobs
from data.users import User


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Jobs {job_id} not found")


class JobsResource(Resource):

    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({
            "jobs": job.to_dict(only=("team_leader", "job", "work_size", "collaborators",
                                      "start_date", "end_date", "is_finished"))
        })

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):

    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({
            "jobs": [job.to_dict(only=("team_leader", "job", "work_size", "collaborators",
                                       "start_date", "end_date", "is_finished")) for job in jobs]
        })

    def post(self):
        form = parser.parse_args()
        session = db_session.create_session()
        if not session.query(User).filter(User.id == form["team_leader"]).first():
            return jsonify({'error': 'Bad request'})
        for collaborator in form["collaborators"].split(", "):
            try:
                if not session.query(User).filter(User.id == int(collaborator)).first():
                    return jsonify({'error': 'Bad request'})
            except ValueError:
                return jsonify({'error': 'Bad request'})
        if session.query(Jobs).get(form.get("id")):
            return jsonify({"error": "Id already exists"})
        all_fields = {"id", "team_leader", "job", "work_size", "collaborators", "start_date",
                      "end_date", "is_finished"}
        kwargs = {field: form[field] for field in all_fields.intersection(set(form))}
        try:
            job = Jobs(**kwargs)
        except StatementError:
            return jsonify({"error": "Bad request"})
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
