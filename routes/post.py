from datetime import datetime

from flask import request, jsonify
from playhouse.shortcuts import model_to_dict

from model import Post
from routes import api


@api.post('/createpost')
def create_post():
    rq = request.get_json()
    try:
        result = Post.create(
            content=rq['content'],
            owner_id=rq['owner_id'],
            group_id=rq['group_id'],
            updated_at=datetime.now(),
            created_at=datetime.now()
        )
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})


@api.get('/getallpost')
def get_all_post():
    try:
        result = Post.select()
        response = []
        for i in result:
            data = model_to_dict(i)
            data['owner_id'] = data['owner_id']['id']
            data['group_id'] = data['group_id']['id']
            response.append(data)
        return jsonify(response)
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})


@api.get('/getpostbyid')
def get_post_by_id():
    try:
        result = Post.get_by_id(request.args.get('id'))
        data = model_to_dict(result)
        data['owner_id'] = data['owner_id']['id']
        data['group_id'] = data['group_id']['id']
        return jsonify(data)
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})

@api.get('/getpostbygroup')
def get_post_by_group():
    try:
        result = Post.select().where(Post.group_id==request.args.get('groupId'))
        response = []
        for i in result:
            data = model_to_dict(i)
            data['owner_id'] = data['owner_id']['id']
            data['group_id'] = data['group_id']['id']
            response.append(data)
        return jsonify(response)
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})