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

@api.delete('/deletepostbyid')
def delete_post():
    try:
        result = Post.delete_by_id(request.args.get('id'))
        if result == 0:
            return jsonify({'status': 'fail'})
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})

@api.post('/editpost')
def edit_post():
    try:
        rq = request.get_json()
        post = Post()
        post.id = rq['id']
        post.owner_id = rq['owner_id']
        post.content = rq['content']
        post.group_id = rq['group_id']
        post.updated_at = datetime.now()
        post.save()
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})