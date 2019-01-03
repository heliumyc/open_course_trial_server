import pymongo
from collections import Counter

MONGO_URI = '127.0.0.1:27017'
MONGO_DATABASE = 'open_course'
CLIENT = pymongo.MongoClient('127.0.0.1') # PYTHON和MONGODB连接的客户端
DB = CLIENT['open_course'] # 指定的数据库

word_count = []
for each in DB['courses'].find():
    word_count += each['keywords']
print(len(word_count)) # 3369
cnt = Counter(word_count)
# print(cnt) # very sparse
print(len(set(word_count))) # 1322  avg <- 2.58
print({k:v for k, v in cnt.items() if v > 3})
print(len({k:v for k, v in cnt.items() if v > 3}))




