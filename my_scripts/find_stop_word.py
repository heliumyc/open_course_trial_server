import jieba.posseg as pseg
import pymongo
import json
MONGO_URI = '127.0.0.1:27017'
MONGO_DATABASE = 'open_course'
CLIENT = pymongo.MongoClient(MONGO_URI)
DB = CLIENT[MONGO_DATABASE]
def analyzer(content: str, allow_pos: set, synonyms: dict) -> list:
    segments = [synonyms[word] if word in synonyms else word for word, pos in pseg.cut(content) if pos in allow_pos]
    return list(segments)

def load_synonyms(syn_file_path: str):
    with open(syn_file_path, 'r', encoding='utf8') as rf:
        synonyms = json.load(rf)
    return synonyms

def main():
    col = DB['courses']
    corpse = [c['intro'] + c['episodes'] for c in col.find()]

    synonyms = load_synonyms('./synonyms.json')

    allow_pos = {'n','nr','ns','nt','nz'}

    segs = ['   '.join(analyzer(c, allow_pos, synonyms)) for c in corpse]
    with open('./corpse_segmented.txt', 'w', encoding='utf8') as wf:
        wf.write('\n'.join(segs))

    
        

if __name__ == "__main__":
    main()
