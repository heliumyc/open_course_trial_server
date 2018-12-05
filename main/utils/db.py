'''
Project: utils
File Created: 2018-09-26
Author: Helium (ericyc4@gmail.com)
Description: 关于数据库的函数, 未来可能会在函数中分别加入不同功能, 但是在暂时都是一样
------
Last Modified: 2018-10-02
Modified By: Helium (ericyc4@gmail.com)
'''

import pymongo

def get_all_nodes(mongo_col):
    """
    返回所有节点
    """
    cur = mongo_col.find()
    return list(cur)

def get_all_keywords(mongo_col):
    """
    返回所有关键词
    """
    return list(mongo_col.find())