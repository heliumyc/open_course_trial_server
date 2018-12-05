'''
Project: views
File Created: 2018-10-03
Author: Helium (ericyc4@gmail.com)
Description: user login and register
------
Last Modified: 2018-11-27
Modified By: Helium (ericyc4@gmail.com)
'''

from flask import jsonify
from flask import request
from main import app
from main import DB
from main.utils.auth import verify_password
from main.utils.auth import hash_password
from main.utils.auth import generate_auth_token
from main.utils.auth import verify_auth_token
from main.models import ResponseType
from main.models import Response

# 这一切! 都可以用json字段检验库完成, 不需要手写ifelse to check
# 可以使用json-lint库, 但是懒得改, 而且登陆功能已经废弃
@app.route('/api/register', methods=['POST'], strict_slashes=False)
def register():
    '''
    register func
    '''
    response = {
        'status': 'success',
        'message': '',
        'username': '',
        'token': ''
    }
    try:
        user_info = request.get_json()
        username = user_info.get('username', None)
        password = user_info.get('password', None)
        if not username or not password:
            response['message'] = '用户名或密码不能为空'
            raise ValueError
        mongo_col = DB['users']
        if mongo_col.find_one({"username": username}):
            response['message'] = '用户名已经存在'
            raise Exception
        mongo_col.insert_one({'username': username,
                              'password_hash': hash_password(password)})
        response['token'] = generate_auth_token(username)
        response['username'] = username
    except Exception as e:
        print(e)
        response['status'] = 'error'
    return jsonify(response)

@app.route('/api/login', methods=['POST'], strict_slashes=False)
def login():
    '''
    login func
    '''
    response = {
        'status': 'success',
        'message': '',
        'username': '',
        'token': ''
    }
    try:
        user_info = request.get_json()
        username = user_info.get('username', None)
        password = user_info.get('password', None)
        token = user_info.get('token', None)
        if not username:
            response['message'] = '用户名不能为空'
            raise ValueError
        valid = False
        mongo_col = DB['users']
        user = mongo_col.find_one({"username": username})
        if not user:
            raise ValueError('User does not exist!')
        if token:
            valid = verify_auth_token(token) == username
        elif password:
            valid = verify_password(password, user["password_hash"])
        else:
            raise ValueError
        if valid:
            response['token'] = generate_auth_token(username)
            response['username'] = username
        else:
            response['message'] = '密码验证失败'
    except ValueError as ve:
        response['status'] = 'error'
        response['message'] = str(ve)
    except Exception as e:
        print(e)
        response['status'] = 'error'
        response['message'] = '请求无效'
    return jsonify(response)
