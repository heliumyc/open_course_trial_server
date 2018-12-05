'''
Project: views
File Created: 2018-10-03
Author: Helium (ericyc4@gmail.com)
Description: 推荐模块
------
Last Modified: 2018-12-04
Modified By: Helium (ericyc4@gmail.com)
'''

from flask import request
from flask import jsonify
from wtforms import ValidationError
from main import app
from main import DB
from main.utils.validator import RatingParams
from main.utils.validator import RecommendCoursesParams
from main.utils.util_func import calc_sim
from main.utils.util_func import after_pop
from main.utils.auth import verify_auth_token
from main.models import ResponseType
from main.models import Response

@app.route('/api/rating', methods=['GET'], strict_slashes=False)
def rating():
    """
    打分
    /api/rating?course_id=<int>&rate=<int>
    """

    try:
        rate_params = RatingParams(request.args)
        if not rate_params.validate():
            raise ValidationError
        rate = rate_params.rate.data * 0.2 # 1 - 5 => 0.2 - 1
        course_id = rate_params.course_id.data
        token = request.headers.get('Authorization', '')

        # by convention jwt token is like "Bearer <token string>"
        uname = verify_auth_token(token[7:])
        if not uname:
            raise ValueError('Invalid Token')

        # check whether this rate exists
        if not DB['users'].find_one({'username': uname, 'rates.cid': course_id}):
            DB['users'].update(
                {'username': uname}, 
                {'$push': {'rates': {'cid': course_id, 'rate': rate}}})
        else:
            DB['users'].update(
                {'username': uname, 'rates.cid': course_id}, 
                {'$set': {'rates.$.rate': rate}})
        response = Response(ResponseType.SUCCESS)

    except ValidationError:
        response = Response(ResponseType.VALIDATION_ERR)
    except ValueError as ve:
        response = Response.get_custom_response(ResponseType.FAILURE, str(ve))
    except Exception as e:
        print(e)
        response = Response(ResponseType.INTERNAL_ERR)

    return response.get_json()

    """
    推荐
    /api/rating
    """

    try:
        token = request.headers.get('Authorization', '')
        if not token:
            raise ValueError('Invalid Token')
        uname = verify_auth_token(token[7:])
        if not uname:
            raise ValueError('Invalid Token')

        # create user model
        user_vector = dict()
        user_rates = DB['users'].find_one({'username': uname})['rates']
        if not user_rates:
            return Response(ResponseType.SUCCESS).get_json()
        for rate in user_rates:
            weights = DB['tfidf'].find_one({'cid': rate['cid']})['tf-idf']
            for word, weight in weights.items():
                user_vector[word] = user_vector.get(word, 0) + weight*rate['rate']
        
        # sort courses using user model
        course_vectors = DB['tfidf'].find()
        course_sim = [{
            'cid': vec['cid'],
            'sim': calc_sim(user_vector, vec['tf-idf'], vec['norm'])
        } for vec in course_vectors]
        user_sort = sorted(course_sim, key=lambda x: x['sim'], reverse=True)

        # filter out what user had viewed that is what has been rated
        rates_id = set([r['cid'] for r in user_rates])
        user_sort = filter(lambda x: x['cid'] not in rates_id, user_sort)

        test = list(user_sort)
        print(test)

        # store user model
        DB['users'].update(
            {'username': uname}, 
            {'$set': {'usermodel': test}}
        )
        response = Response(ResponseType.SUCCESS)
    except Exception as e:
        print('recommend err', e)
        response = Response(ResponseType.INTERNAL_ERR)

    return response.get_json()

@app.route('/api/recommend', methods=['GET'], strict_slashes=False)
def recommend_courses():
    """
    recommend courses
    /api/recommend?page=<int>&page_size=<int>
    """

    try:
        recommend_params = RecommendCoursesParams(request.args)
        if not recommend_params.validate():
            raise ValidationError

        page = recommend_params.page.data
        page_size = recommend_params.page_size.data
        token = request.headers.get('Authorization', '')

        # auth validation
        uname = verify_auth_token(token[7:])
        if not uname:
            raise ValueError('Invalid Token')
        
        # find user
        user = DB['users'].find_one({'username': uname})
        if not user:
            raise ValueError('User Not Found')

        # create user model
        user_vector = dict()
        user_rates = user.get('rates', None)

        if not user_rates:
            return Response.get_custom_response(
                ResponseType.FAILURE, "unable to recommend").get_json()
        for rate in user_rates:
            weights = DB['tfidf'].find_one({'cid': rate['cid']})['tf-idf']
            for word, weight in weights.items():
                user_vector[word] = user_vector.get(word, 0) + weight*rate['rate']

        # sort sim
        course_vectors = DB['tfidf'].find()
        course_sim = [{
            'cid': vec['cid'],
            'sim': calc_sim(user_vector, vec['tf-idf'], vec['norm'])
        } for vec in course_vectors]
        user_sort = sorted(course_sim, key=lambda x: x['sim'], reverse=True)
        
        # filter out what user had viewed that is what has been rated
        # rates_id = set([r['cid'] for r in user_rates])
        # user_sort = filter(lambda x: x['cid'] not in rates_id, user_sort)

        user_model = list(user_sort)
        # store user model
        DB['users'].update(
            {'username': uname}, 
            {'$set': {'usermodel': list(user_sort)}}
        )

        user_courses = [x for x in user_model]
        courses = [
            after_pop(DB['courses'].find_one({'cid': a['cid']}), '_id')
            for a in user_courses[(page-1)*page_size:page*page_size]
        ]

        response = Response(ResponseType.SUCCESS)
        response.update_attr('courses', courses)
        response.update_attr('page', page)
        response.update_attr('pageSize', page_size)
        response.update_attr('totalSize', len(user_courses))

    except ValidationError:
        response = Response(ResponseType.VALIDATION_ERR)
    except ValueError as ve:
        response = Response.get_custom_response(ResponseType.FAILURE, str(ve))
    except Exception as e:
        print('unknown err', e)
        response = Response(ResponseType.INTERNAL_ERR)
    return response.get_json()

@app.route('/api/user-rating', methods=['GET'], strict_slashes=False)
def user_rating():
    """
    打分
    /api/rating?course_id=<int>&rate=<int>
    """

    try:
        token = request.headers.get('Authorization', '')

        # by convention jwt token is like "Bearer <token string>"
        uname = verify_auth_token(token[7:])
        if not uname:
            raise ValueError('Invalid Token')
        
        user_rates = DB['users'].find_one({'username': uname})['rates']
        if not user_rates:
            user_rates = []
        response = Response(ResponseType.SUCCESS)
        response.update_attr('rates', 
                {str(rate['cid']): rate['rate'] for rate in user_rates})

    except ValueError as ve:
        response = Response.get_custom_response(ResponseType.FAILURE, str(ve))
    except Exception as e:
        print(e)
        response = Response(ResponseType.INTERNAL_ERR)

    return response.get_json()
