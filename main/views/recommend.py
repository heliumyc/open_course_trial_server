'''
Project: views
File Created: 2018-10-03
Author: Helium (ericyc4@gmail.com)
Description: 推荐模块
------
Last Modified: 2018-12-23
Modified By: Helium (ericyc4@gmail.com)
'''

from flask import request
from flask import jsonify
from wtforms import ValidationError
from main import app
from main import DB
from main import COURSE_VECTORS_BASELINE
from main import COURSE_VECTORS_KM
from main.utils.validator import RatingParams
from main.utils.validator import RecommendCoursesParams
from main.utils.util_func import calc_sim
from main.utils.util_func import after_pop
from main.utils.auth import verify_auth_token
from main.utils.recommend import recommend
from main.utils.recommend import merge_vectors
from main.models import ResponseType
from main.models import Response

RECOMMEND_PARAMS = {
    '1': 0, '2': 0.3, '3': 0.4, '4': 0.5, '5': 0.6, '6': 0.7, '7': 1
}
print('start of init course_vectors for diff version')
COURSE_VECTORS_DICT = {
    mode: merge_vectors(alpha, 1-alpha, COURSE_VECTORS_BASELINE, COURSE_VECTORS_KM)
    for mode, alpha in RECOMMEND_PARAMS.items()
}
# with open('f:/test.txt', 'w', encoding='utf8') as wf:
#     for k,v in COURSE_VECTORS_DICT.items():
#         wf.write(str(v)+'\n')
print('end of init course_vectors for diff version')

@app.route('/api/rating', methods=['GET'], strict_slashes=False)
def rating():
    """
    打分
    /api/rating?course_id=<int>&rate=<int>&is_evaluation=<bool>
    """

    try:
        rate_params = RatingParams(request.args)
        if not rate_params.validate():
            raise ValidationError
        rate = rate_params.rate.data * 0.2 # 1 - 5 => 0.2 - 1
        course_id = rate_params.course_id.data
        is_evalution = rate_params.is_evaluation.data
        token = request.headers.get('Authorization', '')

        # by convention jwt token is like "Bearer <token string>"
        uname = verify_auth_token(token[7:])
        if not uname:
            raise ValueError('Invalid Token')

        if is_evalution:
            # check whether this rate exists
            if not DB['users'].find_one({'username': uname, 'evaluation.cid': course_id}):
                DB['users'].update(
                    {'username': uname}, 
                    {'$push': {'evaluation': {'cid': course_id, 'rate': rate}}})
            else:
                DB['users'].update(
                    {'username': uname, 'evaluation.cid': course_id}, 
                    {'$set': {'evaluation.$.rate': rate}})
        else:
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
        mode = recommend_params.mode.data
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
        user_rates = user.get('rates', None)
        if not user_rates:
            return Response.get_custom_response(
                ResponseType.FAILURE, "unable to recommend").get_json()
        
        course_vectors = COURSE_VECTORS_DICT[str(mode)]
        user_model = recommend(user_rates, course_vectors)

        # store user model
        DB['users'].update(
            {'username': uname}, 
            {'$set': {'usermodel': user_model}}
        )

        user_courses = [x['cid'] for x in user_model]

        # change the order the full rating items
        user_rates_dict = {x['cid']: x['rate'] for x in user_rates}
        full_rates = [c for c in user_courses if user_rates_dict.get(c,0) == 1]
        other_rates = [c for c in user_courses if user_rates_dict.get(c,0) < 1]
        user_courses = full_rates + other_rates

        courses = [
            after_pop(DB['courses'].find_one({'cid': a}), '_id')
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
    /api/user-rating
    """

    try:
        token = request.headers.get('Authorization', '')

        # by convention jwt token is like "Bearer <token string>"
        uname = verify_auth_token(token[7:])
        if not uname:
            raise ValueError('Invalid Token')

        user = DB['users'].find_one({'username': uname})
        user_rates = user.get('rates', [])
        user_eval = user.get('evaluation', [])
        
        if not user_rates:
            user_rates = []
        if not user_eval:
            user_eval = []
        response = Response(ResponseType.SUCCESS)
        response.update_attr('rates', 
                {str(rate['cid']): rate['rate'] for rate in user_rates})
        response.update_attr('evaluation',
                {str(rate['cid']): rate['rate'] for rate in user_eval})

    except ValueError as ve:
        response = Response.get_custom_response(ResponseType.FAILURE, str(ve))
    except Exception as e:
        print(e)
        response = Response(ResponseType.INTERNAL_ERR)

    return response.get_json()
