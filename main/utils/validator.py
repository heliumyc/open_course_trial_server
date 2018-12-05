'''
Project: backend
File Created: 2018-10-02
Author: Helium (ericyc4@gmail.com)
Description: 使用wtform检验url的params是否合法
------
Last Modified: 2018-11-26
Modified By: Helium (ericyc4@gmail.com)
'''

from wtforms import Form
from wtforms import IntegerField
from wtforms import StringField
from wtforms import FloatField
from wtforms import ValidationError
# from main.utils.util_func import convert_int

class CourseListParams(Form):
    """
    检验course-list的args
    """
    node_id = IntegerField('node_id')
    page = IntegerField('page')
    page_size = IntegerField('page_size')
    # order = StringField('order')

    def validate_node_id(self, field):
        node_id = field.data
        if node_id is None or node_id < 0:
            raise ValidationError

    def validate_page(self, field):
        page = field.data
        # if page is not integer, it will be None
        if page is None or page < 0:
            raise ValidationError

    def validate_page_size(self, field):
        page_size = field.data
        if page_size is None or page_size < 0:
            raise ValidationError

    # def validate_order(self, field):
    #     order = field.data
    #     print(order)
    #     if order:
    #         print('invalid order')
    #         raise ValidationError

class RatingParams(Form):
    """
    params are like ?course_id=<int>&rate=<int>
    rate should be int [1,5]
    course id should not be below 0
    """
    course_id = IntegerField('course_id')
    rate = IntegerField('rate')
    # token = StringField('token')

    def validate_course_id(self, field):
        course_id = field.data
        if course_id is None or course_id < 0:
            raise ValidationError
        
    def validate_rate(self, field):
        rate = field.data
        if rate is None or rate < 0 or rate > 5:
            raise ValidationError

class RecommendCoursesParams(Form):
    """
    params are like ?page=<int>&page_size=<int>&token=<str>
    """
    page = IntegerField('page')
    page_size = IntegerField('page_size')
    # token = StringField('token')

    def validate_page(self, field):
        page = field.data
        if page is None or page < 0:
            raise ValidationError
    
    def validate_page_size(self, field):
        page_size = field.data
        if page_size is None or page_size < 0:
            raise ValidationError

# class GraphParams(Form):
#     """
#     params形式形如 int;int;int
#     """
#     wids = StringField('wids')
    
#     def validate_wids(self, field):
#         wids = field.data
#         print('invalidator', wids)
#         if wids:
#             try:
#                 wids_arr = convert_int(wids.split(';'))
#             except ValueError as e:
#                 raise ValidationError('Illegal Params!')
