from datetime import datetime

from flask import request, jsonify
from playhouse.shortcuts import model_to_dict

from model import Group
from routes import api


@api.post('/creategroup')
def create_group():
    rq = request.get_json()
    try:
        result = Group.create(
            name=rq['name'],
            group_profile=rq['group_profile'],
            group_banner=rq['group_banner'],
            detail=rq['detail'],
            created_at=datetime.now()
        )
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})


@api.get('/getgroupbyid')
def get_group_by_id():
    try:
        result = Group.get_by_id(request.args.get('groupId'))
        return jsonify(model_to_dict(result))
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})


@api.get('/getallgroup')
def get_all_group():
    try:
        result = Group.select()
        response = []
        for i in result:
            response.append(model_to_dict(i))
        return jsonify(response)
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})