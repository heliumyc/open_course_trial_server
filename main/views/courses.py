'''
Project: views
File Created: 2018-10-05
Author: Helium (ericyc4@gmail.com)
Description: return courses
------
Last Modified: 2018-11-27
Modified By: Helium (ericyc4@gmail.com)
'''

from flask import request
from flask import jsonify
from flask import send_from_directory
from wtforms import ValidationError
from main import app
from main import DB
from main.utils.validator import CourseListParams
from main.utils.util_func import after_pop
from main.models import ResponseType
from main.models import Response

@app.route('/api/courses', methods=['GET'], strict_slashes=False)
def get_courses_list():
    # 返回图和返回文章的接口分离
    # 因为文章还要翻页 查询文章直接在mongodb中查询
    # 因为不需要做查询相关度排序, 提供排序为, 年份, 默认(字典序), 被引量

    try:
        course_params = CourseListParams(request.args)
        # validate params passed in
        if not course_params.validate():
            raise ValidationError
        # return courses
        node_id = course_params.node_id.data
        page = course_params.page.data
        page_size = course_params.page_size.data
        # order = course_params.order.data

        node = DB['nodes'].find_one({'nid': node_id})
        if not node:
            raise ValueError('no such node id exists')
        extents = node['extent']
        courses = DB['courses'].find({'cid': {"$in": extents}}) \
                                .limit(page_size) \
                                .skip((page-1)*page_size)
        # if order == 'time':
        #     courses = DB['courses'].find({'cid': {"$in": extents}}) \
        #                         .sort([('date',-1)]).limit(page_size) \
        #                         .skip((page-1)*page_size)
        # elif order == 'citation':
        #     courses = DB['courses'].find({'cid': {"$in": extents}}) \
        #                         .sort([('citation',-1)]).limit(page_size) \
        #                         .skip((page-1)*page_size)
        courses = [after_pop(d, '_id') for d in courses]
        response = Response(ResponseType.SUCCESS)
        response.update_attr('courses', courses)
        response.update_attr('page', page)
        response.update_attr('pageSize', page_size)
        response.update_attr('totalSize', len(extents))
    except ValidationError as ve:
        print(ve)
        response = Response(ResponseType.PARAMETERS_ERR)
    except ValueError as ve:
        response = Response.get_custom_response(ResponseType.FAILURE, str(ve))
    except Exception as e:
        print(e)
        response = Response(ResponseType.INTERNAL_ERR)

    return response.get_json()
