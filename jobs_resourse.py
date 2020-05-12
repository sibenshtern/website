from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import database_session
from data.jobs import Jobs
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('team_leader', required=True, type=int)


class JobsListResource(Resource):

    @staticmethod
    def get():
        session = database_session.create_session()
        jobs = session.query(Jobs).all()

        return jsonify(
            {'jobs': [job.to_dict(only=(
                'job', 'work_size', 'collaborators', 'start_date',
                'is_finished', 'team_leader'
            )) for job in jobs]
            }
        )

    @staticmethod
    def post():
        args = parser.parse_args()

        session = database_session.create_session()
        job = Jobs(
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
            team_leader=args['team_leader']
        )
        session.add(job)
        session.commit()

        return jsonify({'success': 'OK'})


class JobsResource(Resource):

    def get(self, job_id):
        self.abort_if_jobs_not_found(job_id)

        session = database_session.create_session()
        job = session.query(Jobs).get(job_id)

        return jsonify(
            {'job': job.to_dict(only=(
                'job', 'work_size', 'collaborators', 'start_date',
                'is_finished', 'team_leader'
            ))
            }
        )

    def delete(self, job_id):
        self.abort_if_jobs_not_found(job_id)

        session = database_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()

        return jsonify({'success': 'OK'})

    @staticmethod
    def abort_if_jobs_not_found(job_id):
        session = database_session.create_session()
        job = session.query(Jobs).get(job_id)
        if not job:
            abort(404, message=f"Job with id {job_id} not found")