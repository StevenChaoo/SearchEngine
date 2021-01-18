# Author:STEVEN

import jieba
import chardet
from collections import Counter

def StopWords(dir):
    '''
    arguments:
        dir:
    returns:
        results:['请', '说', '“', '”', '后', '？', '各国', '（', '）', ',']
    '''
    results=[]
    f = open(dir, 'r', encoding='utf-8')
    for line in f.readlines():
        results.append(line.strip())
    return results

def CutSentences(sentences, stopwords):
    '''
    arguments:
        sentences:(list)
        stopwords:(list)
    returns:
        length:The length of sentences.
        counter:Counter({'科索沃': 8, '解决': 5, '罗斯': 4, '俄罗斯': 4, '地区': 3, '武力': 3, '24': 3, '反对': 2})
    '''
    results = []
    for sentence in sentences:
        results += jieba.lcut_for_search(sentence)
    counter = Counter(results)
    for x in sorted(counter):
        if x in stopwords:
            del counter[x]
    length = sum(counter.values())
    return length, counter


def GetSentences(dir):
    '''
    arguments:
        dir:
    returns:
        sentnces:['述评:中俄关系史上的新篇章新华社莫斯科7月16日电', '述评:中俄关系史上的新篇章', '新华社记者陈鹤高\u3000黄慧珠\u3000车玉明']
        name:述评:中俄关系史上的新篇章
    '''
    sentences = []
    dataf = open(dir, 'rb')
    data = dataf.read()
    enctype = chardet.detect(data)['encoding']
    f = open(dir, 'r', encoding=enctype)
    i = 0
    for line in f.readlines():
        # print(line)
        i += 1
        if i > 1:
            sentences.append(line.strip())
        else:
            name = line.strip()
    return sentences, name

def GetResult(dir, stopwordsdir):
    '''
    arguments:
        dir:
        stopwordsdir:
    returns:
        result:{'filename': '中俄青年论坛在北京举行',
                'filelength': 292,
                'content': '中俄青年论坛在北京举行新华社北京9月2……',
                'content_cut':Counter({'科索沃': 8, '解决': 5, '罗斯': 4, '俄罗斯': 4, '地区': 3, '武力': 3, '24': 3})}
    '''
    result = {}
    content = ''
    stopwords = StopWords(stopwordsdir)
    sentences, name = GetSentences(dir)
    length, cuts = CutSentences(sentences, stopwords)
    for sentence in sentences:
        content += sentence
    result['filename'] = name
    result['filelength'] = length
    result['content'] = content
    result['content_cut'] = cuts
    return result

def GetInfo():
    '''
    arguments:
    returns:
        Infos:[{'name':'N13-XIN_CMN_20010716_0060.txt'
                'content':{'filename':'述评:中俄关系史上的新篇章'
                           'filelength':652
                           'content':'述评:中俄关系史上的新篇章新华社莫斯科7月...'
                           'content_cut':Counter({'、': 26, '关系': 23, '中': 21, '俄': 19, '两国': 19, '合作': 15})}}

                {'name':'N02-za2001_001865.txt'
                 'content':{'filename':'贫铀武器和“人道罪行”'
                            'filelength':1096
                            'content':'贫铀武器和“人道罪行”2001-01-09本文由美国在...'
                            'content_cut':Counter({'贫铀': 31, '美国': 26, '武器': 22, '、': 14, '政府': 13})}}]
    '''
    TXTPath = open('/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/TXTPath.txt', 'r', encoding='utf-8')
    stopwordsdir = '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/stop_words.txt'
    Infos = []
    tag = 0
    for dir in TXTPath.readlines():
        tag += 1
        if tag < 200:
            Info = {}
            result = GetResult(dir.strip(), stopwordsdir)
            Info['name'] = dir.strip().split('/')[-1]
            Info['content'] = result
            Infos.append(Info)
    return Infos

