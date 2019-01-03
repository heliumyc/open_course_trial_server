'''
Project: server
File Created: 2018-10-03
Author: Helium (ericyc4@gmail.com)
Description: main app
------
Last Modified: 2018-12-19
Modified By: Helium (ericyc4@gmail.com)
'''

from flask import Flask
from flask_cors import CORS
# from flask_httpauth import HTTPTokenAuth
import pymongo
from main.utils import util_func
from config import Config

app = Flask(__name__)
app.config.from_object(Config) # 添加配置参数, 在../config.py设定

# auth_request = HTTPTokenAuth()

# 设定跨域访问设定
cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:8081",
                                                "http://127.0.0.1:8081",
                                                "http://open-course-trial.heliumyc.top"]}}) 

CLIENT = pymongo.MongoClient(app.config['MONGO_URI'],
            username=app.config['MONGO_USER'],
            password=app.config['MONGO_PWD'],
            authSource=app.config['MONGO_DATABASE']) # PYTHON和MONGODB连接的客户端
DB = CLIENT[app.config['MONGO_DATABASE']] # 指定的数据库
KEYWORDS = list(DB['keywords'].find()) # 所有keywords的列表, 也即内涵集合
NODES = [util_func.after_pop(x, '_id') for x in list(DB['nodes'].find())] # 所有概念点
KEYWORDS_DICT = {k['wid']: k['keyword'] for k in KEYWORDS}
COURSE_VECTORS = {c['cid']: c for c in DB['kwtfidf'].find()}


# print(sorted([len(x['extent']) for x in NODES], reverse=True))
from main.views import user
from main.views import search
from main.views import graph
from main.views import courses
from main.views import recommend
