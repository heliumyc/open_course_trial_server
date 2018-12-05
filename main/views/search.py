'''
Project: views
File Created: 2018-10-03
Author: Helium (ericyc4@gmail.com)
Description: search
------
Last Modified: 2018-11-28
Modified By: Helium (ericyc4@gmail.com)
'''

import Levenshtein
from flask import jsonify
from flask import request
from main import app
from main import DB
from main import KEYWORDS
from main.models import ResponseType
from main.models import Response

@app.route('/api/search', methods=['GET'], strict_slashes=False)
def search():
    '''
    得到一个或者关键词之后, 如果这个或者这些关键词命中了
    返回命中和未命中的关键词, 以及命中的关键词分别的kId
    目前只做一个关键词的好了
    来了一个新词之后, 在所有关键词里面匹配, 精准命中就是直接返回
    如果不中, 那么就计算相似度, 然后返回相似度top5的关键词

    相似度计算可以使用编辑距离自动机或者是BK树, 不想写, 好麻烦
    如果之后要做到实时推荐, 输入一个词出一个词, 那么就需要这样做
    '''

    # 从url的请求参数中获取keyword, like /api/search?keywords=xxx;xxx
    keywords = request.args.get('keywords', '').lower()
    # keywords为一个string, 多个keywords使用;分隔, 因为一个keyword可能是phrase
    keywords = keywords.split(';')
    print(keywords)

    # 同时因为mongodb不会parse指定的key, 所以不存在sql注入的安全风险

    mongo_col = DB['keywords'] # keywords collection
    fail_list = []
    matched_list = []
    match = True
    wids = []
    recommend = []
    try:
        for k in keywords:
            res = mongo_col.find_one({'keyword': k})
            if res:
                matched_list.append(res['keyword'])
                wids.append(res['wid'])
            else:
                match = False
                fail_list.append(k)
        # 将匹配失败的词汇和所有的keywords进行相似度匹配
        match_num = 5
        if fail_list:
            best_matches = sorted(KEYWORDS, reverse=True, key=lambda kwobj: 
                            max(fail_list, key=lambda fail_kw: 
                                Levenshtein.ratio(kwobj['keyword'], fail_kw)))
            recommend = [x['keyword'] for x in best_matches[:match_num]]
        
        response = Response(ResponseType.SUCCESS)
        response.update_attr('keywords', matched_list)
        response.update_attr('match', match)
        response.update_attr('wids', wids)
        response.update_attr('recommend', recommend)
    except Exception as e:
        print(e)
        response = Response(ResponseType.FAILURE)
    return response.get_json()

# @app.route('/api/root', methods=['GET'], strict_slashes=False)
# def get_root():
#         rootId = 1
#         response = Response(ResponseType.SUCCESS)
#         response.update_attr('rootId', rootId)
#     except Exception as e:
#         print(e)
#         response = Response(ResponseType.FAILURE)
#     return response.get_json()