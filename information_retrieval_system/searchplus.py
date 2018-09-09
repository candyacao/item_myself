# coding:utf-8

import os
import re
import json


class GloabalAttr:
    def __init__(self, stopwordfn='stopword.txt', sep=','):
        """stopwordfn: 由,分割的停用词文件名
        sep: stopwordfn文件的分割符，默认为,
        """
        self.stopword = None
        self.init(stopwordfn, sep)

    def init(self, filename, sep):
        with open(filename, 'r') as f:
            self.stopword = frozenset(f.read().split(','))


class Search:
    def __init__(self, globalattr, text):
        """globalattr: GloabalAttr对象
        text: 文档字典，格式为如下：
        ```python
        [
            {
                "num":"doc1",
                "string":"...."
            }, {}, ...
        ]
        ```
        """
        self.globalattr = globalattr
        self.text = text
        self.shun = dict()
        self.dao = None

    def qieci(self, text):
        # TODO: 正则处理的文字 有-和“green”没有处理出来，之后处理

        # pattern = r'''(?x)
        #      ([A-Z]\.)+
        #    | \w+(-\w+)*
        #    | \$?\d+(\.\d+)?%?
        #    | \.\.\.
        #    | [][.,;"'?():-_`]
        #    '''

        # return re.findall(pattern, text)
        return list(filter(lambda x: x != '', re.split('\s+|,|; |\.|\?\|\"|\*|\n ', text.lower())))

    def shunpai(self):
        return self._shun(self.text)

    def daopai(self):
        return self._daopai(self.shun)

    def research(self):
        return self._research(self.dao)

    def run(self):
        self.shunpai()
        self.daopai()
        self.research()

    def _shun(self, text):
        """顺排档
        text: self.text
        """
        for doc in text:
            name = doc['num']
            string = doc['string']
            fenci = self.qieci(doc['string'])
            nochongfu = set(fenci) - self.globalattr.stopword
            self.shun[doc['num']] = dict()
            for word in nochongfu:
                count = fenci.count(word)
                # shun[doc['num']].setdefault(word, count)
                self.shun[doc['num']][word] = count
            # print(shun)
        return self.shun

    def _daopai(self, shun):
        """到排档
        shun: self.shun
        """
        dao = dict()
        word_bao = set()
        for doc in shun:
            set1 = set(shun[doc].keys())
            word_bao.update(set1)

        for word in word_bao:
            dao[word] = dict()
            for doc in self.shun:
                if None != shun[doc].get(word):
                    tmp_dict = {doc: shun[doc].get(word)}
                    dao[word].update(tmp_dict)
        self.dao = dao
        return self.dao

    def _research(self, dao):
        """检索
        dao: self.dao
        """
        input_string = input("输入检索词：")
        while(input_string != ''):
            if dao.get(input_string):
                print(dao.get(input_string))
            else:
                print("None")
            input_string = input("输入检索词：")

        with open("result/shun.txt", 'w', encoding="utf8") as file:
            file.write('顺拍档\n')
            file.write(str(self.shun))
        with open("result/dao.txt", 'w', encoding="utf8") as file:
            file.write('倒排档\n')
            file.write(str(self.dao))
        json.dump(self.shun, open('result/shun.json', 'w', encoding='utf8'), indent=4)
        json.dump(self.dao, open('result/dao.json', 'w', encoding='utf8'), indent=4)
        print('exit')


def main():
    """读取文件，并整理到text中"""
    text = list()
    for file in os.listdir(os.path.join(os.getcwd(), 'doc')):
        one_file_info = {'num': None, "string": None}
        file_path = file
        # print(file_path)
        if not os.path.isdir(file_path):
            with open("doc/" + file_path, 'r', encoding="utf8")as f:
                one_file_info['num'] = file_path.split('.')[0]
                one_file_info['string'] = f.read()
        text.append(one_file_info)

    # 检索过程
    searcher = Search(GloabalAttr(), text)
    searcher.run()


if __name__ == '__main__':
    main()
