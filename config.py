# -*- coding: UTF-8 -*-
#!/usr/bin/python3
'''
Project: backend
File Created: 2018-09-21
Author: Helium (ericyc4@gmail.com)
Description: some config
------
Last Modified: 2018-12-05
Modified By: Helium (ericyc4@gmail.com)
'''

import os

class Config:
    """
    config class to be included in app
    """
    SECRET_KEY = 'courses search project' # 注意这个不应该被存储在code中
    # 在production环境下应该有OS.ENV获取
    ENCRYPTION = 'HS256'
    TOKEN_VALID_TIME = 86400
    MONGO_USER = 'helium'
    MONGO_PWD = '42'
    MONGO_URI = '127.0.0.1:27017'
    MONGO_DATABASE = 'open_course'

    @staticmethod
    def init_app(app):
        pass
