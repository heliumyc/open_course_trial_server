'''
Project: views
File Created: 2018-10-03
Author: Helium (ericyc4@gmail.com)
Description: graph api
------
Last Modified: 2018-12-06
Modified By: Helium (ericyc4@gmail.com)
'''

from flask import jsonify
from flask import request
from main import app
from main import NODES
from main import KEYWORDS_DICT
from main.utils.graph import sub_graph
from main.utils.graph import add_info
from main.utils.util_func import convert_int
from main.models import ResponseType
from main.models import Response

@app.route('/api/graph', methods=['GET'], strict_slashes=False)
def get_graph():
    """
    get explicit params from url
    接受url的Param作为root nodeId, 然后返回一张dag
    dag似乎可以提前就计算好? 因为要有children node的相关度排序
    计算好之后就直接提出来用? 在app载入的时候就加到内存里面去
    考虑可拓展性? 如果图特别大呢, 那显然和设计的架构不一致, 
    因为构想是前端处理整个graph的裁剪, 后端提供整张图
    如果图很大, 那么后端必须裁剪好前端直接用, 不能指望前端那点计算能力
    因为不止一个点, <del>但是现在没做多关键词查询</del>, 如果做了那么就是一个列表
    <del>params里面传入的应该是一个serialized json string, 然后解析为json然后得到数组</del>
    使用;分隔, 就像search那样
    """

    # 然而现在需要考虑同时查询两个
    wids = request.args.get('wids', '').lower()

    print('graph params', wids)

    # params = GraphParams(request.args)
    if not wids:
        response = Response(ResponseType.PARAMETERS_ERR)
        return response.get_json()

    try:
        # 由于概念格的特点, 子节点关键词集合一定包含父节点的关键词集合, 文档集合反之
        # 找到含有extent的所有点, 然后把data里面无关的连线删掉, 找到fah==[]就是新root
        wids = convert_int(wids.split(';'))
        g = sub_graph(NODES, wids)
        # add data in g
        g = add_info(g, KEYWORDS_DICT)
        if len(g) == 1:
            # response = Response.get_custom_response(ResponseType.FAILURE, 'No Such sub graph')
            response = Response(ResponseType.SUCCESS)
            response.update_attr('graph', g)
        else:
            response = Response(ResponseType.SUCCESS)
            response.update_attr('graph', g)
    except Exception as e:
        print(e)
        response = Response(ResponseType.INTERNAL_ERR)
    return response.get_json()


# @app.route('/api/init_graph', methods=['GET'], strict_slashes=False)
# def get_init_graph():
#     '''
#     get init graph, a root node and selected second layer node
#     '''
# DEPRECATED
