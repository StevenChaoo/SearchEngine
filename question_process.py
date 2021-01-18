# Author:STEVEN

import os
import xml.dom.minidom as xmldom
import jieba
from collections import Counter

def GetFileList(dir, filelist):
    '''
    arguments:
        dir:
        filelist:
    returns:
        filelist:['/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/question/.DS_Store',
                  '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/question/Q1-2.xml',
                  '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/question/Q3-16.xml']
    '''
    if os.path.isfile(dir):
        filelist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileList(newDir, filelist)
    return filelist

def GetContent(dir):
    '''
    arguments:
        dir:
    returns:
        IDs:['N01', 'N02']
        TITLEs:['再生医学', '美国对于贫铀炸弹的姿态']
        QUESTIONs:['请说说再生医学。', '请说说美国对于贫铀炸弹的姿态']
    '''
    filepath = os.path.abspath(dir)
    obj = xmldom.parse(filepath)
    elem = obj.documentElement
    sub_elem = elem.getElementsByTagName('TOPIC')
    IDs, TITLEs, QUESTIONs = [], [], []
    for i in range(len(sub_elem)):
        ID = sub_elem[i].getAttribute('ID')
        TITLE = sub_elem[i].getAttribute('TITLE')
        QUESTION = ''
        sub_sub_elem = sub_elem[i].getElementsByTagName('DESC')
        for j in range(len(sub_sub_elem)):
            if sub_sub_elem[j].getAttribute('LANG') == 'CS':
                QUESTION = sub_sub_elem[j].firstChild.data
            else:
                continue
        IDs.append(ID[-3:])
        TITLEs.append(TITLE)
        QUESTIONs.append(QUESTION)
    return IDs, TITLEs, QUESTIONs

def GetQuestion():
    '''
    arguments:
    returns:
        IDs:['N01', 'N02', 'N03', 'N04', 'N05', 'N06', 'N07', 'N08', 'N09', 'N10', 'N11', 'N12', 'N13', 'N14', 'N15', 'N16']
        TITLEs:['再生医学', '美国对于贫铀炸弹的姿态', ...]
        QUESTIONs:['请说说再生医学。', '请说说美国对于贫铀炸弹的姿态', ...]
    '''
    dir = '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/question'
    xmllist = GetFileList(dir, [])
    del(xmllist[0])
    IDs, TITLEs, QUESTIONs = [], [], []
    for xmlfile in xmllist:
        a, b, c = GetContent(xmlfile)
        IDs += a
        TITLEs += b
        QUESTIONs += c
    return IDs, TITLEs, QUESTIONs

def StopWords(dir, results=[]):
    '''
    arguments:
        dir:
    returns:
        results:['请', '说', '“', '”', '后', '？', '各国', '（', '）', ',']
    '''
    f = open(dir, 'r', encoding='utf-8')
    for line in f.readlines():
        results.append(line.strip())
    return results

def CutQuery():
    '''
    arguments:
    returns:
        resultsum:[{'ID': 'N01', 'QUESTION': '请说说再生医学', 'CONTENT': Counter({'再生': 1, '医学': 1})},
                   {'ID': 'N02', 'QUESTION': '请说说美国对于贫铀炸弹的姿态', 'CONTENT': Counter({'美国': 1, '贫铀': 1, '炸弹': 1})}]
    '''
    stopwordsdir = '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/stop_words.txt'
    stopwords = StopWords(stopwordsdir)
    IDs, TITLEs, QUESTIONs = GetQuestion()
    counters = []
    for query in QUESTIONs:
        results = jieba.lcut_for_search(query)
        counter = Counter(results)
        for x in sorted(counter):
            if x in stopwords:
                del counter[x]
        counters.append(counter)
    resultsum = []
    for i in range(len(IDs)):
        result = {}
        result['ID'] = IDs[i]
        result['QUESTION'] = QUESTIONs[i]
        result['CONTENT'] = counters[i]
        resultsum.append(result)
    return resultsum


