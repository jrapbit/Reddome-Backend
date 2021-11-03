from flask import jsonify, Blueprint, request
from playhouse.shortcuts import model_to_dict
from model import User

api = Blueprint('api', __name__)


@api.get('/')
def default():
    return 'type the path u little shit!'


@api.post('/login')
def login():
    rq = request.get_json()
    result = User.get_or_none(User.username == rq['username'], User.password == rq['password'])
    if result is None:
        return jsonify({'status': 'fail'})
    return jsonify({'id': model_to_dict(result)['id']})


@api.post('/register')
def register():
    rq = request.get_json()
    result = User.create(
        username=rq['username'],
        password=rq['password'],
        email=rq['email'],
        birth_date=rq['birth_date'],
        profile_picture=rq['profile_picture']
    )
    if result is None:
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})
