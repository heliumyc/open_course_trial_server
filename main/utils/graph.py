'''
Project: backend
File Created: 2018-09-26
Author: Helium (ericyc4@gmail.com)
Description: 涉及图处理的函数
------
Last Modified: 2018-10-08
Modified By: Helium (ericyc4@gmail.com)
'''
import copy

def sub_graph(graph, intents):
    """
    graph: 全图G
    intents: 需要的intent列表
    在graph中, 找到所有包含intent的点, 找到layer最高(最小)的node, 作为root node
    返回该子图, 因为概念格图的性质, 子图一定包含所有的含需要的intent的点
    因为G为所有node的列表, 只需要把无关信息删除, 就能得到一个子图, 
    寻找根节点的任务由外部处理
    未来是不是需要加入LCA之类的待定
    """
    intents = set(intents)
    # 慎用deepcopy
    # 这个地方使用deepcopy是因为不能污染原图G
    # 因为deepcopy会一直递归复制每一个对象, 可能会有性能问题
    # 但是此处已知对象的结构比较简单, 所以使用, 否则应该人工手动复制
    # 因为intent不止一个, 需要两个集合的判断
    new_graph = {k: v for k, v in enumerate(copy.deepcopy(graph)) 
                 if intents <= set(v['intent']) and len(v['extent']) != 0}
    # print(len(new_graph))
    # 将无关的点和无关的连接信息(fah和chd)清除
    for k, v in new_graph.items():
        # 去除chd
        new_chd = [chd_id for chd_id in v['chd'] if chd_id in new_graph]
        # 列表生成式, 等价于以下
        # for chd_id in v['chd']:
        #     if chd_id in new_graph:
        #         new_chd.append(chd_id)
        v['chd'] = new_chd
        # 去除fah
        new_fah = [fah_id for fah_id in v['fah'] if fah_id in new_graph]
        # 列表生成式, 等价于以下
        # for fah_id in v['fah']:
        #     if fah_id in new_graph:
        #         new_fah.append(fah_id)
        v['fah'] = new_fah
    # print(len(new_graph[1]['fah']))
    # print([v for k,v in new_graph.items() if v['fah'] == []][0])
    # print(len([v for k,v in new_graph.items() if v['fah'] == []]))
    return new_graph

def add_info(graph_dict, KEYWORDS_DICT):
    '''
    add data part
    '''
    for k, v in graph_dict.items():
        fah_intents = set([i for fah in v['fah'] for i in graph_dict[fah]['intent']])
        v['data'] = {
            'keywords': [KEYWORDS_DICT[wid] for wid in v['intent']],
            'number': len(v['extent']),
            'labels': [
              KEYWORDS_DICT[wid] for wid in 
                filter(lambda i: i not in fah_intents, v['intent'])
            ]
        }
    
    return graph_dict
