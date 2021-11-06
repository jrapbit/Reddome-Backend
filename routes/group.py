from datetime import datetime

from flask import request, jsonify
from playhouse.shortcuts import model_to_dict

from model import Group, GroupMember
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
        return jsonify({'status': 'success', 'id': model_to_dict(result)['id']})
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})


@api.get('/getgroupbyid')
def get_group_by_id():
    try:
        result = Group.get_by_id(request.args.get('groupId'))
        data = model_to_dict(result)
        data['isMember'] = is_group_member(request.args.get('groupId'), request.args.get('userId'))
        return jsonify(data)
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
            data = model_to_dict(i)
            data['isMember'] = is_group_member(data['id'], request.args.get('userId'))
            response.append(data)
        return jsonify(response)
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})


@api.post('/join')
def join_group():
    try:
        rq = request.get_json()
        groupmember = GroupMember()
        groupmember.group = rq['groupId']
        groupmember.member = rq['userId']
        groupmember.save()
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})


@api.post('/leave')
def leave_group():
    try:
        rq = request.get_json()
        result = GroupMember.delete().where(GroupMember.group == rq['groupId'], GroupMember.member == rq['userId'])
        result.execute()
        if result == 0:
            return jsonify({'status': 'fail'})
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success'})


def is_group_member(group, member):
    try:
        result = GroupMember.get_or_none(GroupMember.group == group, GroupMember.member == member)
        return result is not None
    except Exception as e:
        print('error:', end=' ')
        print(e)
        return None
