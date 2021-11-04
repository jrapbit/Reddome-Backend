from datetime import datetime

from flask import request, jsonify
from playhouse.shortcuts import model_to_dict

from model import Comment
from routes import api


@api.post('/createcomment')
def create_comment():
    rq = request.get_json()
    try:
        result = Comment.create(
            post_id=rq['post_id'],
            content=rq['content'],
            owner_id=rq['owner_id'],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})


@api.get('/getcommentsbypost')
def get_comment_by_post():
    try:
        result = Comment.select().where(Comment.post_id == request.args.get('postId'))
        response = []
        for i in result:
            data = model_to_dict(i)
            data['post_id'] = data['post_id']['id']
            data['owner_id'] = data['owner_id']['id']
            response.append(data)
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify(response)


@api.get('/getcommentbyid')
def get_comment_by_id():
    try:
        result = Comment.get_by_id(request.args.get('id'))
        data = model_to_dict(result)
        data['post_id'] = data['post_id']['id']
        data['owner_id'] = data['owner_id']['id']
        return jsonify(data)
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})