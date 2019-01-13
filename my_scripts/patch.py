#!/usr/bin/python
# -*- coding: utf8 -*-
import pymongo

MONGO_URI = '127.0.0.1:27017'
MONGO_DATABASE = 'open_course'
CLIENT = pymongo.MongoClient(MONGO_URI)
DB = CLIENT[MONGO_DATABASE]


new_val = '《视觉·文化·创新》课程主要研究视觉对象、视觉心理和视觉生理，使信息通过设计媒介能准确、巧妙、快捷地传达出去，让受众在学习过程中，熟练掌握视觉传达设计在不同媒介中的语言与表达。课程内容以二维（平面）、三维（空间）、四维（动态）全面贯穿视觉传达设计领域的相关内容。本课程面向设计类相关专业的学生和从业人员，涵盖视觉传达设计、环境设计、产品设计、时尚设计、建筑设计、景观设计等专业领域，及其他交叉学科的学生和受众，对提高国内理工科院校学生的艺术修养、审美情操、设计创意等方面起到积极作用。'
DB['courses'].update({'cid':14}, {'$set': {'intro': new_val}})
