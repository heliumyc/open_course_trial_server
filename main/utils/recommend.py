'''
Project: utils
File Created: 2018-12-20
Author: Helium (ericyc4@gmail.com)
Description: 
------
Last Modified: 2018-01-11
Modified By: Helium (ericyc4@gmail.com)
'''
from main.utils.util_func import calc_sim
import math

RATE_MAPPING = {
    1: -0.5, 2: -0.3, 3: 0, 4: 0.8, 5: 1
}

def merge_vectors(alpha, beta, vecs1, vecs2):
    new_vectors = dict()
    for cid, c1_data in vecs1.items():
        new_vectors[cid] = dict()
        c2_data = vecs2.get(cid, {})
        kws = set(c1_data['tf-idf']).union(set(c2_data['tf-idf']))
        new_tfidf = {
            k: alpha*c1_data['tf-idf'].get(k,0) + beta*c2_data['tf-idf'].get(k,0) 
            for k in kws
        }
        new_tfidf = normalization(new_tfidf)
        new_vectors[cid]['tf-idf'] = new_tfidf
        new_vectors[cid]['norm'] = math.sqrt(sum(
            map(lambda x: new_tfidf[x]**2, new_tfidf)
        ))
    return new_vectors

def normalization(vec):
    x_max = -1
    x_min = 0xffffffff
    for k, v in vec.items():
        x_min = min(v, x_min)
        x_max = max(v, x_max)
    scale = x_max - x_min
    for k, v in vec.items():
        vec[k] = v-x_min/scale
    return vec

def recommend(user_rates, course_vectors):
    user_vector = dict()
    for rate in user_rates:
        weights = course_vectors[rate['cid']]['tf-idf']
        for word, weight in weights.items():
            # change rate
            new_rate = RATE_MAPPING[int(rate['rate'])]
            user_vector[word] = user_vector.get(word, 0) + weight*new_rate

    # sort sim
    course_sim = [{
        'cid': cid,
        'sim': calc_sim(user_vector, vec['tf-idf'], vec['norm'])
    } for cid, vec in course_vectors.items()]

    user_sort = sorted(course_sim, key=lambda x: x['sim'], reverse=True)
    user_model = list(user_sort)
    # filter out what user had viewed that is what has been rated
    # rates_id = set([r['cid'] for r in user_rates])
    # user_sort = filter(lambda x: x['cid'] not in rates_id, user_sort)
    # print(user_model)
    return user_model
