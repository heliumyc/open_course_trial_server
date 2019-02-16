'''
Project: utils
File Created: 2018-09-27
Author: Helium (ericyc4@gmail.com)
Description: 包含一些自定义的小函数
------
Last Modified: 2018-12-19
Modified By: Helium (ericyc4@gmail.com)
'''

def after_pop(dictionary, key):
    """
    去除字典的某个字段, 返回处理后的字典
    """
    dictionary.pop(key, None)
    return dictionary

def convert_int(arr):
    res = []
    for s in arr:
        try:
            res.append(int(s))
        except ValueError as e:
            raise ValueError
    return res

def calc_sim(vec1, vec2, norm_vec2):
    """
    vec 1 and vec 2 both are vector as of a dict
    sim = vec1*vec2/|vec2|
    cuz norm of vec 1 appears in every iteration, therefore no need to consider it
    """
    if norm_vec2 == 0:
        return 0
    sim = 0
    for word, weight in vec1.items():
        sim += weight*vec2.get(word, 0)
    sim = sim/norm_vec2
    return sim

def is_close(a, b, delta=1e-3):
    return abs(a-b) < delta
