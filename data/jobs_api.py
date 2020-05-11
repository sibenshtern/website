from flask import Blueprint, jsonify, abort

from data import database_session
from data.jobs import Jobs
from data.users import User


api = Blueprint('jobs_api', __name__, template_folder="templates")


@api.route('/jobs')
def return_all_jobs():
    session = database_session.create_session()
    jobs = session.query(Jobs).all()
    json_jobs = [
        job.to_dict(
            only=(
                "id", "team_leader", "job",
                "work_size", "collaborators", "is_finished"
            )
        )
        for job in jobs]

    return jsonify({'jobs': json_jobs})


@api.route('/job/<int:job_id>')
def return_one_job_by_id(job_id):
    session = database_session.create_session()
    job = session.query(Jobs).get(job_id)

    if job is None:
        abort(404)

    return jsonify(
        {
            "job": job.to_dict(only=(
                "id", "team_leader", "job",
                "work_size", "collaborators", "is_finished"
            ))
        }
    )
