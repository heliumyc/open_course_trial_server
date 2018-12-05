# from collections import Counter
# import pymongo
# import os
# import math

# MONGO_URI = '127.0.0.1:27017'
# MONGO_DATABASE = 'open_couese'
# CLIENT = pymongo.MongoClient(MONGO_URI)
# DB = CLIENT[MONGO_DATABASE]

# def tfidf():
#     """
#     using tf-idf to calculate most important keywords
#     """
#     filedir = '../main/data/keywords_extracted'
#     files = os.listdir('%s' %filedir)

#     text_dict = dict()
#     for eachfile in files:
#         eachfname, eachfext = os.path.splitext(eachfile)
#         list_of_pairs = []
#         with open('%s/%s' %(filedir, eachfile), 'r', encoding='utf8') as procf:
#             for line in procf:
#                 temp = line.split('@')
#                 list_of_pairs.append((temp[0].replace('.', ''), int(temp[1])))
#         text_dict[eachfname] = list_of_pairs
    
#     words_freq_wrt_text = [item[0] for text, pairs in text_dict.items() for item in pairs]
#     words_freq_wrt_text = Counter(words_freq_wrt_text)
#     N = len(text_dict)
#     # tf-idf: weight = (1+log(f_ij))*log(N/n_i)
#     tfidf_dict = dict()
#     for text, list_of_pairs in text_dict.items():
#         total_num = sum([int(item[1]) for item in list_of_pairs])
#         tfidf_a = {item[0]: (1+math.log10(int(item[1])))*math.log10(N/words_freq_wrt_text[item[0]])
#                    for item in list_of_pairs}
#         # tfidf_a = sorted(tfidf_a,key=lambda x: x[1],reverse=True)
#         tfidf_dict[text] = tfidf_a
#     return tfidf_dict

# def calc_norm(arr):
#     return math.sqrt(sum(map(lambda x: x**2, arr)))

# def main():
#     tfdict = tfidf()
#     for k, v in tfdict.items():
#         try:
#             article = DB['articles'].find_one({'title': k})
#             if not article:
#                 raise ValueError(k)
#             DB['tfidf'].insert({
#                 'aid': article['aid'],
#                 'title': article['title'],
#                 'tf-idf': v,
#                 'norm': calc_norm([val for k, val in v.items()])
#             })
#         except ValueError as e:
#             print(e)
#         except Exception as e:
#             print(e)
# if __name__ == "__main__":
#     main()
