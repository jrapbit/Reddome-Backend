from flask import request, jsonify
from playhouse.shortcuts import model_to_dict

from model import User
from routes import api


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
    try:
        result = User.create(
            username=rq['username'],
            password=rq['password'],
            email=rq['email'],
            birth_date=rq['birth_date'],
            profile_picture=rq['profile_picture']
        )
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})

@api.get('/getuserbyid')
def get_user_by_id():
    try:
        result = User.get_by_id(request.args.get('id'))
        return model_to_dict(result)
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
