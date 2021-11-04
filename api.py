from datetime import datetime

from flask import jsonify, Blueprint, request
from playhouse.shortcuts import model_to_dict
from model import User, Group, Post, Comment

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
