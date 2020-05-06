from flask import Blueprint, jsonify, make_response, abort, request
from sqlalchemy.exc import StatementError

from data import db_session
from data.jobs import Jobs
from data.users import User

jobs_api = Blueprint('jobs_api', __name__, template_folder='templates')


# jobs_api добавляется по url_prefix=/api, мне, кажется, так логичней


@jobs_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@jobs_api.route("/jobs")
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify({
        "jobs": [job.to_dict(only=("team_leader", "job", "work_size", "collaborators",
                                   "start_date", "end_date", "is_finished")) for job in jobs]
    })


@jobs_api.route("/jobs/<int:job_id>")
def get_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404)
    return jsonify({
        "jobs": job.to_dict(only=("team_leader", "job", "work_size", "collaborators",
                                  "start_date", "end_date", "is_finished"))
    })


@jobs_api.route("/jobs", methods=["POST"])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    form = request.json
    fields = {"team_leader": int, "is_finished": bool, "work_size": int}
    for field, f_type in fields.items():
        try:
            form[field] = f_type(form[field])
        except ValueError:
            return jsonify({'error': 'Bad request'})
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


@jobs_api.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404)
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@jobs_api.route("/jobs/<int:job_id>", methods=["PUT"])
def edit_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404)
    all_fields = {"id", "team_leader", "job", "work_size", "collaborators", "start_date",
                  "end_date", "is_finished"}
    for field in all_fields.intersection(set(request.json)):
        job.__setattr__(field, request.json[field])
    session.commit()
    return jsonify({"success": "OK"})
