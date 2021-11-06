from datetime import datetime

from flask import request, jsonify
from playhouse.shortcuts import model_to_dict

from model import Post, PostLike, GroupMember
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
        return jsonify({'status': 'success', 'id': model_to_dict(result)['id']})
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})


@api.get('/getallpost')
def get_all_post():
    try:
        result = Post.select()
        response = []
        for i in result:
            data = model_to_dict(i)
            data['owner_id'] = {
                'id': data['owner_id']['id'],
                'username': data['owner_id']['username']
            }
            data['group_id'] = {
                'id': data['group_id']['id'],
                'name': data['group_id']['name'],
                'group_profile': data['group_id']['group_profile']
            }
            data['isLiked'] = is_like(data['id'], request.args.get('userId'))
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
        data['owner_id'] = {
            'id': data['owner_id']['id'],
            'username': data['owner_id']['username']
        }
        data['group_id'] = {
            'id': data['group_id']['id'],
            'name': data['group_id']['name'],
            'group_profile': data['group_id']['group_profile']
        }
        data['isLiked'] = is_like(data['id'], request.args.get('userId'))
        return jsonify(data)
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})


@api.get('/getpostbygroup')
def get_post_by_group():
    try:
        result = Post.select().where(Post.group_id == request.args.get('groupId'))
        response = []
        for i in result:
            data = model_to_dict(i)
            data['owner_id'] = {
                'id': data['owner_id']['id'],
                'username': data['owner_id']['username']
            }
            data['group_id'] = {
                'id': data['group_id']['id'],
                'name': data['group_id']['name'],
                'group_profile': data['group_id']['group_profile']
            }
            data['isLiked'] = is_like(data['id'], request.args.get('userId'))
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


@api.post('/like')
def like_post():
    try:
        rq = request.get_json()
        postlike = PostLike()
        postlike.post = rq['postId']
        postlike.user = rq['userId']
        postlike.save()
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})


@api.post('/unlike')
def unlike_post():
    try:
        rq = request.get_json()
        result = PostLike.delete().where(PostLike.post == rq['postId'], PostLike.user == rq['userId'])
        result.execute()
        print(result)
        if result == 0:
            return jsonify({'status': 'fail'})
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})


def is_like(post, user):
    try:
        result = PostLike.get_or_none(PostLike.post == post, PostLike.user == user)
        return result is not None
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return None


@api.get('/getpostbyuserid')
def get_post_by_user():
    try:
        user_id = request.args.get('userId')
        groups = GroupMember.select().where(GroupMember.member == user_id)
        response = []
        for group_id in groups:
            print(group_id)
            result = Post.select().where(Post.group_id == group_id)
            for i in result:
                data = model_to_dict(i)
                data['owner_id'] = {
                    'id': data['owner_id']['id'],
                    'username': data['owner_id']['username']
                }
                data['group_id'] = {
                    'id': data['group_id']['id'],
                    'name': data['group_id']['name'],
                    'group_profile': data['group_id']['group_profile']
                }
                data['isLiked'] = is_like(data['id'], user_id)
                response.append(data)
        return jsonify(response)
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
