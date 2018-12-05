import re
import queue
import os
PATTERN = re.compile(r'ID:(\d+)\|\|extent=\[(.*)\]\|\|intent=\[(.*)\]\|\|fah=\[(.*)\]\|\|chd=\[(.*)\]')
node_list = []
# with open('../data/693cl.txt', 'r', encoding='utf8') as f:
#     for line in f:
#         groups = PATTERN.search(line).groups()
#         node = dict(nid=int(groups[0]),
#                     extent=[int(x) for x in groups[1].split(',') if x is not ''],
#                     intent=[int(x) for x in groups[2].split(',') if x is not ''],
#                     fah=[int(x) for x in groups[3].split(',') if x is not ''],
#                     chd=[int(x) for x in groups[4].split(',') if x is not ''],
#                     layer=-1)
#         node_list.append(node)
# print(len(node_list[1]['fah']))

# # bfs看下有没有出现跨层的现象, 跨层的话, 一定有一个点根据遍历的顺序不同一定有两个不同的layer
# q = []
# root = list(filter(lambda x: x['fah'] == [], node_list))[0]
# q.append(root)
# print(root['nid'])
# root['layer'] = 1
# while q:
#     cur = q.pop()
#     next_layer = cur['layer'] + 1
#     for chd_id in cur['chd']:
#         if node_list[chd_id]['layer'] < next_layer:
#             node_list[chd_id]['layer'] = next_layer
#         # elif node_list[chd_id]['layer'] is not next_layer:
#         #     print('%s->%s' % (cur['nid'], chd_id), cur['layer'], node_list[chd_id]['layer'])
#         q.append(node_list[chd_id])

# # for x in node_list:
# #     if x['layer'] != 1:
# #         print('error')

# print(node_list[2]['layer'])
# print(node_list[1]['layer'])
# print(node_list[5]['layer'])
# temp = set()
# for node in node_list:
#     for pnode_id in node['fah']:
#         if node_list[pnode_id]['layer'] >= node['layer']:
#             temp.add(node['nid'])

# print(temp)
# print(len(temp))


# # 检查包含关系
# temp = set()
# for node in node_list:
#     for pnode_id in node['fah']:
#         pnode = node_list[pnode_id]
#         if set(pnode['extent']) <= set(node['extent']):
#             print(node['nid'], pnode['nid'])
#         if set(pnode['intent']) >= set(node['intent']):
#             print(node['nid'], pnode['nid'])

# pdf = [os.path.splitext(x)[0] for x in os.listdir('../data/pdf')]
# text = [os.path.splitext(x)[0] for x in os.listdir('../data/keywords_extracted')]
# pdf = set(pdf)
# text = set(text)
# cnt = 0
# for x in pdf:
#     if x not in text:
#         cnt += 1
#         print(x)
# print(cnt, pdf == text)

# for t in text:
#     if '.' in t:
#         print(t)

# from enum import Enum, unique
# class ResponseType(Enum):
#     SUCCESS = ('success', 'ok')
#     FAILURE = ('failure', '')
#     PARAMETERS_ERR = ('failure', 'parameters error')
#     INTERNAL_ERR = ('failure', 'internal error')
#     VALIDATION_ERR = ('failure', 'validation error')

# print(ResponseType.VALIDATION_ERR.value)

with open('./stopwords.txt', 'r', encoding='utf8') as rf:
    stopwords = rf.read().split('\n')

print(stopwords)
print(len(stopwords))