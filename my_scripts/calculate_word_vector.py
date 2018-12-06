import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mylib.tfidf import Tfidf
import pymongo
import math
import json
import jieba.posseg as pseg

MONGO_URI = '127.0.0.1:27017'
MONGO_DATABASE = 'open_course_test'
CLIENT = pymongo.MongoClient(MONGO_URI,  
            username='helium',
            password='42',
            authSource=MONGO_DATABASE)
DB = CLIENT[MONGO_DATABASE]

def read_corpse() -> list:
    col = DB['courses']
    corpse = [c['intro'] + c['episodes'] for c in col.find()]
    return corpse

def read_stopwords(stopwords_path: str):
    with open(stopwords_path, 'r', encoding='utf8') as rf:
        stopwords = rf.read().split('\n')
    return stopwords

def analyzer(content: str, allow_pos: set, synonyms: dict, stopwords: set) -> list:
    # segments = []
    # for word, pos in pseg.cut(content) if pos in allow_pos:
    #     if word in stopwords:
    #         continue
    #     segments.append(synonyms.get(word, word))
    segments = [synonyms.get(word, word) for word, pos in pseg.cut(content) 
                if pos in allow_pos and word not in stopwords ]

    return list(segments)

def calc_norm(arr):
    return math.sqrt(sum(map(lambda x: x**2, arr)))

def store_vector(vectors: list) -> None:
    col = DB['tfidf']
    col.insert_many([
        {
            'cid': index,
            'tf-idf': vec,
            'norm': calc_norm(vec.values())
        } for index, vec in enumerate(vectors)
    ])

def load_synonyms(syn_file_path: str):
    with open(syn_file_path, 'r', encoding='utf8') as rf:
        synonyms = json.load(rf)
    return synonyms

def main():
    tfidf = Tfidf()
    corpse = read_corpse()
    allow_pos = {'n','nr','ns','nt','nz'}
    stopwords = read_stopwords('./stopwords.txt')
    synonyms = load_synonyms('./synonyms.json')
    mat = tfidf.vectorize(corpse, lambda text: analyzer(text, allow_pos, synonyms, stopwords))
    store_vector(tfidf.get_words_weight_table())

if __name__ == "__main__":
    main()
