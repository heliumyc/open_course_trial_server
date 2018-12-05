'''
Project: backend
File Created: 2018-09-21
Author: Helium (ericyc4@gmail.com)
Description: 关于验证的函数
------
Last Modified: 2018-10-06
Modified By: Helium (ericyc4@gmail.com)
'''

import time
from passlib.apps import custom_app_context as pwd_context
from jwt import ExpiredSignatureError
import jwt
from main import app

def hash_password(password):
    """ 
    hash password
    """
    password_hash = pwd_context.encrypt(password)
    return password_hash

def verify_password(password, password_hash):
    """ 
    compare hash password with thereof in db 
    """
    return pwd_context.verify(password, password_hash)

def generate_auth_token(username, expiration=app.config['TOKEN_VALID_TIME']):
    """ 
    generate token 
    """
    payload = {
        "iss": "sigir search",
        "iat": int(time.time()),
        "exp": int(time.time()) + expiration,
        "sub": username
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'],
                        algorithm=app.config['ENCRYPTION']).decode()
    return token

def verify_auth_token(token):
    """ 
    verify token 
    """
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], 
                            algorithms=[app.config['ENCRYPTION']])
    except ExpiredSignatureError:
        return None
    except Exception:
        return None
    # print(payload)
    if not payload:
        return None
    try:
        username = payload['sub']
    except Exception:
        return None
    return username
    