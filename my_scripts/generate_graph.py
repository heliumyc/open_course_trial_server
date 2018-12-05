# 用于将txt存储的graph数据解析后按照存入数据库, 无论是txt还是数据库都以邻接表方式存储
# 将graph的每个节点的子节点按照计算公式排序

import os
import re
import pymongo

PATTERN = re.compile(r'ID:(\d+)\|\|extent=\[(.*)\]\|\|intent=\[(.*)\]\|\|fah=\[(.*)\]\|\|chd=\[(.*)\]')
MONGO_URI = '127.0.0.1:27017'
MONGO_DATABASE = 'open_course'
CLIENT = pymongo.MongoClient(MONGO_URI)
DB = CLIENT[MONGO_DATABASE]

def sort_children(node_list):
    # 计算公式为, sim = (a/maxA+b/maxB)/2
    # a为父子节点intent相同数量, b为父子节点extent相同数量
    # maxA为父子节点intent的数量最大值, maxB为父子节点extent的数量最大值
    sim = [0]*len(node_list)
    for node in node_list:
        intent_set = set(node['intent'])
        extent_set = set(node['extent'])
        for childId in node['chd']:
            child = node_list[childId]
            a = len(set(child['intent'])&intent_set)
            b = len(set(child['extent'])&extent_set)
            maxA = max(len(node['intent']), len(child['intent']))
            maxB = max(len(node['extent']), len(child['extent']))
            sim[child['nid']] = (a/maxA+b/maxB)/2
        node['chd'] = sorted(node['chd'], key=lambda childId: sim[childId])
    return node_list

def insert_nodes(filepath):
    node_list = []
    with open(filepath, 'r', encoding='utf8') as f:
        for line in f:
            groups = PATTERN.search(line).groups()
            node = dict(nid=int(groups[0]),
                        extent=[int(x) for x in groups[1].split(',') if x is not ''],
                        intent=[int(x) for x in groups[2].split(',') if x is not ''],
                        fah=[int(x) for x in groups[3].split(',') if x is not ''],
                        chd=[int(x) for x in groups[4].split(',') if x is not ''])
            node_list.append(node)
    node_list = sort_children(node_list)
    for node in node_list:
        DB['nodes'].insert(node)

def insert_keywords(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        keywords = [x.rstrip('\n') for x in f if x is not '']
        print(len(keywords))
        # print(keywords)
    for index, kw in enumerate(keywords):
        DB['keywords'].insert({
            'wid': index,
            'keyword': kw
        })

def main():
    insert_nodes('../data/courses_cl.txt')
    insert_keywords('../data/courses_keywords.txt')

if __name__ == "__main__":
    main()