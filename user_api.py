from flask import Blueprint, jsonify, make_response, request, abort

import data.database_session as database_session
from data.users import User

blueprint = Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/users')
def get_users():
    session = database_session.create_session()
    all_users = session.query(User).all()
    return jsonify({'users': [item.to_dict() for item in all_users]})


@blueprint.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    session = database_session.create_session()
    user = session.query(User).get(user_id)

    if user is not None:
        return jsonify({'user': user.to_dict()})
    else:
        abort(404)


@blueprint.route('/users', methods=['POST'])
def add_user():
    session = database_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in [
                'id', 'name', 'surname', 'age', 'position', 'speciality',
                'address', 'email', 'password'
            ]):
        return jsonify({'error': 'Bad request'})
    elif session.query(User).get(request.json['id']) is not None:
        return jsonify({'error': 'ID already exists'})
    else:
        user = User(
            id=request.json['id'],
            name=request.json['name'],
            surname=request.json['surname'],
            age=request.json['age'],
            position=request.json['position'],
            speciality=request.json['speciality'],
            address=request.json['address'],
            email=request.json['email']
        )
        user.set_password(request.json['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = database_session.create_session()
    if session.query(User).get(user_id) is None:
        return jsonify({'error': 'Invalid ID'})
    else:
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/users/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    session = database_session.create_session()
    if session.query(User).get(user_id) is None:
        return jsonify({'error': 'Invalid ID'})
    elif all(key in request.json for key in [
                'name', 'surname', 'age', 'position', 'speciality', 'address',
                'email', 'password'
            ]):
        user = session.query(User).get(user_id)

        user.name = request.json['name']
        user.surname = request.json['surname']
        user.age = request.json['age']
        user.position = request.json['position']
        user.speciality = request.json['speciality']
        user.address = request.json['address']
        user.email = request.json['email']
        user.hashed_password = request.json['hashed_password']
        session.commit()
        return jsonify({'success': 'OK'})

    return jsonify({'error': 'Invalid data'})


@blueprint.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': 'Server error'}), 500)


@blueprint.errorhandler(404)
def not_found_error(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
