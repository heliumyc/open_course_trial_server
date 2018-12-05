'''
Project: mylib
File Created: 2018-11-24
Author: Helium (ericyc4@gmail.com)
Description: small tools to calculate tf-idf
------
Last Modified: 2018-11-25
Modified By: Helium (ericyc4@gmail.com)
'''

from typing import Callable
import numpy as np
import itertools

class Tfidf():
    """ a class for tf-idf calculation """
    def __init__(self, sparse=False):
        self.corpse = None
        self.words_list = None
        self.words_id = dict()
        self.idf = None
        self.tf = None
        self.matrix = None
        self.corpse_size = 0
        self.sparse = sparse
        # TODO
        if self.sparse:
            import scipy

    def _build_words_list(self) -> None:
        """
        build a dict mapping an word to id
        """
        # words_set = reduce(lambda s1, s2: s1|s2, map(lambda words: set(words), self.corpse))
        # the implementation below is faster than that above, after all it is done by native code
        words_set = set(itertools.chain.from_iterable(self.corpse))
        self.words_list = sorted(list(words_set))
        self.words_id = {w: i for i, w in enumerate(self.words_list)}

    def _build_idf(self) -> None:
        """
        count idf
        """
        self.idf = np.count_nonzero(self.tf, axis=0)
        self.idf = np.log10(self.corpse_size/self.idf)

    # 不加@staticmethod或者@classmethod
    # 是因为里面有个函数要拿这个作为默认值, 但是当时class尚未解析完全
    # 所以要么显示not defined要么显示not callable
    # 这个函数也可以放在外面, 只是一个普通函数罢了
    def default_tokenizer(content: str) -> list:
        """ 
        default tokenizer uses any white space token
        to cut the sentence
        """
        return content.split()
        
    def _count_frequency(self) -> None:
        """
        count frequency
        """
        # 这样实现不适用于语料很大的情况, 矩阵会相当大而且稀疏
        # 应该用之前的实现方法, 用哈希表, 不存0
        # 或者用scipy自带的稀疏矩阵 TODO
        self.tf = np.zeros((len(self.corpse), len(self.words_id)))
        for index, text in enumerate(self.corpse):
            for word in text:
                self.tf[index][self.words_id[word]] += 1

    def vectorize(self, corpse: list, tokenizer: Callable[[str],list]=default_tokenizer) -> list:
        """
        main part of this algorithm
        this implementation is not suit for sparse lexical space
        """
        if corpse is None or len(corpse) == 0:
            return []
        if tokenizer is None:
            self.corpse = corpse
        else:
            # 本来可以惰性求值的, 但是因为后面要多次遍历
            # 但是map里面的迭代器, 遍历一次用完了就用不了了
            self.corpse_size = len(corpse)
            self.corpse = list(map(tokenizer, corpse))

        self._build_words_list()
        self._count_frequency()
        self._build_idf()

        # calculate tf-idf
        # tf-idf: weight = (1+log(f_ij))*log(N/n_i)
        # no sure whether it is proper to do so
        np.seterr(divide = 'ignore')
        self.tf = np.log10(self.tf)
        self.tf = np.where(np.isfinite(self.tf), self.tf+1, 0)
        self.matrix = self.tf*self.idf
        return self.matrix.tolist()

    def get_words_list(self):
        return self.words_list

    def get_words_weight_table(self):
        """
        get table, the single text of which only contains words appearing in the text
        """
        # 本来以为!=0会有浮点数精度的问题, 可能numpy or python内部处理了? 不然的话得用np.isclose了
        return [
            {self.words_list[index]: weight for index, weight in enumerate(vector) if weight != 0}
            for vector in self.matrix
        ]

if __name__ == "__main__":
    tfidf = Tfidf()
    corpse = ['hello world', 'damn world', 'fuck']
    res = tfidf.vectorize(corpse)
    print(res)
    print(tfidf.get_words_list())
    print(tfidf.get_words_weight_table())

    # using chinese tokenizer
    import jieba
    tfidf = Tfidf()
    corpse = ['小明去上学', '小明回家啦', '小明不想写作业']
    res = tfidf.vectorize(corpse, lambda t: list(jieba.cut(t)))
    print(res)
    print(tfidf.get_words_list())
    print(tfidf.get_words_weight_table())
