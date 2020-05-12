from flask import Blueprint, jsonify, make_response, request, abort

import data.database_session as database_session
from data.jobs import Jobs
from data.users import User

blueprint = Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/jobs')
def get_jobs():
    session = database_session.create_session()
    all_jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs': [item.to_dict(only=(
                'id', 'team_leader', 'work_size', 'collaborators',
                'is_finished'
            )) for item in all_jobs]
        }
    )


@blueprint.route('/jobs/<int:job_id>')
def get_job_by_id(job_id):
    session = database_session.create_session()
    job = session.query(Jobs).get(job_id)

    if job is not None:
        return jsonify(
            {
                'job': job.to_dict(only=(
                    'id', 'team_leader', 'work_size', 'collaborators',
                    'is_finished'
                ))
            }
        )
    else:
        abort(404)


@blueprint.route('/jobs', methods=['POST'])
def add_job():
    session = database_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in [
                'id', 'team_leader', 'work_size', 'collaborators',
                'is_finished'
            ]):
        return jsonify({'error': 'Bad request'})
    elif session.query(Jobs).get(request.json['id']) is not None:
        return jsonify({'error': 'ID already exists'})
    else:
        job = Jobs(
            id=request.json['id'],
            team_leader=request.json['team_leader'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            is_finished=request.json['is_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    session = database_session.create_session()
    if session.query(Jobs).get(job_id) is None:
        return jsonify({'error': 'Invalid ID'})
    else:
        user = session.query(User).get(job_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/jobs/<int:job_id>', methods=['PUT'])
def put_user(job_id):
    session = database_session.create_session()
    if session.query(Jobs).get(job_id) is None:
        return jsonify({'error': 'Invalid ID'})
    elif all(key in request.json for key in [
                'id', 'team_leader', 'work_size', 'collaborators',
                'is_finished'
            ]):
        job = session.query(Jobs).get(job_id)
        job.id = request.json['id'],
        job.team_leader = request.json['team_leader'],
        job.work_size = request.json['work_size'],
        job.collaborators = request.json['collaborators'],
        job.is_finished = request.json['is_finished']

        session.commit()
        return jsonify({'success': 'OK'})

    return jsonify({'error': 'Invalid data'})


@blueprint.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': 'Server error'}), 500)


@blueprint.errorhandler(404)
def not_found_error(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
