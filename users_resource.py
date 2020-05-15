from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import database_session
from data.users import User


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('city_from', required=True)
parser.add_argument('password', required=True)

USER_ARGUMENTS = (
    'name', 'surname', 'age', 'position', 'speciality', 'address', 'email',
    'city_from'
)


class UsersResource(Resource):

    @staticmethod
    def get(user_id):
        abort_if_users_not_found(user_id)

        session = database_session.create_session()
        user = session.query(User).get(user_id)

        return jsonify({'user': user.to_dict(only=USER_ARGUMENTS)})

    @staticmethod
    def delete(user_id):
        abort_if_users_not_found(user_id)

        session = database_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()

        return jsonify({'success': 'OK'})


class UsersListResource(Resource):

    @staticmethod
    def get():
        session = database_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {'users': [user.to_dict(only=USER_ARGUMENTS) for user in users]})

    @staticmethod
    def post():
        args = parser.parse_args()

        session = database_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            city_from=args['city_from']
        )
        user.set_password(args['password'])

        session.add(user)
        session.commit()

        return jsonify({'success': 'OK'})


def abort_if_users_not_found(user_id):
    session = database_session.create_session()
    if session.query(User).get(user_id) is None:
        abort(404, message=f"User with id {user_id} not found")
