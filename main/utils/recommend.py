'''
Project: utils
File Created: 2018-12-20
Author: Helium (ericyc4@gmail.com)
Description: 
------
Last Modified: 2018-12-20
Modified By: Helium (ericyc4@gmail.com)
'''
from main.utils.util_func import calc_sim

def rec1(user_rates, course_vectors):
    user_vector = dict()
    for rate in user_rates:
        weights = course_vectors[rate['cid']]['tf-idf']
        for word, weight in weights.items():
            user_vector[word] = user_vector.get(word, 0) + weight*rate['rate']

    print(course_vectors)
    # sort sim
    course_sim = [{
        'cid': vec['cid'],
        'sim': calc_sim(user_vector, vec['tf-idf'], vec['norm'])
    } for cid, vec in course_vectors.items()]

    user_sort = sorted(course_sim, key=lambda x: x['sim'], reverse=True)
    user_model = list(user_sort)
    # filter out what user had viewed that is what has been rated
    # rates_id = set([r['cid'] for r in user_rates])
    # user_sort = filter(lambda x: x['cid'] not in rates_id, user_sort)
    print(user_model)
    return user_model

def rec2(user_rates, course_vectors):
    user_vector = dict()
    for rate in user_rates:
        weights = course_vectors[rate['cid']]['tf-idf']
        for word, weight in weights.items():
            new_rate = 0 if rate['rate'] < 0.6 else rate['rate']
            user_vector[word] = user_vector.get(word, 0) + weight*new_rate

    print(course_vectors)
    # sort sim
    course_sim = [{
        'cid': vec['cid'],
        'sim': calc_sim(user_vector, vec['tf-idf'], vec['norm'])
    } for cid, vec in course_vectors.items()]

    user_sort = sorted(course_sim, key=lambda x: x['sim'], reverse=True)
    user_model = list(user_sort)
    # filter out what user had viewed that is what has been rated
    # rates_id = set([r['cid'] for r in user_rates])
    # user_sort = filter(lambda x: x['cid'] not in rates_id, user_sort)
    print(user_model)
    return user_model

def rec3(user_rates, course_vectors):
    user_vector = dict()
    for rate in user_rates:
        weights = course_vectors[rate['cid']]['tf-idf']
        for word, weight in weights.items():
            user_vector[word] = user_vector.get(word, 0.6) + weight*rate['rate']

    print(course_vectors)
    # sort sim
    course_sim = [{
        'cid': vec['cid'],
        'sim': calc_sim(user_vector, vec['tf-idf'], vec['norm'])
    } for cid, vec in course_vectors.items()]

    user_sort = sorted(course_sim, key=lambda x: x['sim'], reverse=True)
    user_model = list(user_sort)
    # filter out what user had viewed that is what has been rated
    # rates_id = set([r['cid'] for r in user_rates])
    # user_sort = filter(lambda x: x['cid'] not in rates_id, user_sort)
    print(user_model)
    return user_model

def recommend(user_rates, course_vectors, version):
    if version == 1:
        return rec1(user_rates, course_vectors)
    elif version == 2:
        return rec2(user_rates, course_vectors)
    elif version == 3:
        return rec3(user_rates, course_vectors)
