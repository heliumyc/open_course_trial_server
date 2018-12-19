'''
Project: utils
File Created: 2018-12-19
Author: Helium (ericyc4@gmail.com)
Description: 
------
Last Modified: 2018-12-19
Modified By: Helium (ericyc4@gmail.com)
'''

def rec1(user_rates, course_vectors):
    user_vector = dict()
    for rate in user_rates:
        weights = course_vectors[rate['cid']]['tf-idf']
        for word, weight in weights.items():
            user_vector[word] = user_vector.get(word, 0) + weight*rate['rate']

    print(user_vector)
    # sort sim
    course_sim = [{
        'cid': vec['cid'],
        'sim': calc_sim(user_vector, vec['tf-idf'], vec['norm'])
    } for vec in course_vectors]
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
            user_vector[word] = user_vector.get(word, 0) + weight*rate['rate']

    # sort sim
    course_sim = [{
        'cid': vec['cid'],
        'sim': calc_sim(user_vector, vec['tf-idf'], vec['norm'])
    } for vec in course_vectors]
    user_sort = sorted(course_sim, key=lambda x: x['sim'], reverse=True)
    user_model = list(user_sort)
    # filter out what user had viewed that is what has been rated
    # rates_id = set([r['cid'] for r in user_rates])
    # user_sort = filter(lambda x: x['cid'] not in rates_id, user_sort)
    return user_model

def rec3(user_rates, course_vectors):
    user_vector = dict()
    for rate in user_rates:
        weights = course_vectors[rate['cid']]['tf-idf']
        for word, weight in weights.items():
            user_vector[word] = user_vector.get(word, 0) + weight*rate['rate']

    # sort sim
    course_sim = [{
        'cid': vec['cid'],
        'sim': calc_sim(user_vector, vec['tf-idf'], vec['norm'])
    } for vec in course_vectors]
    user_sort = sorted(course_sim, key=lambda x: x['sim'], reverse=True)
    user_model = list(user_sort)
    # filter out what user had viewed that is what has been rated
    # rates_id = set([r['cid'] for r in user_rates])
    # user_sort = filter(lambda x: x['cid'] not in rates_id, user_sort)
    return user_model

def recommend(user_rates, course_vectors, version):
    if version == 1:
        return rec1(user_rates, course_vectors)
    elif version == 2:
        return rec2(user_rates, course_vectors)
    elif version == 3:
        return rec3(user_rates, course_vectors)
