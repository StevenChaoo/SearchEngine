# Author:STEVEN

import question_process as qp
import sentences_cut as sc
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import json
import math

def GetIndex():
    '''
    arguments:
    returns
        idx:
    '''
    schema = Schema(title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                    path=TEXT(stored=True),
                    content=TEXT(stored=True, analyzer=ChineseAnalyzer())
                    )
    idx = create_in('index', schema)
    writer = idx.writer()
    answers = sc.GetInfo()
    for answer in answers:
        path = answer['name']
        title = answer['content']['filename']
        content = answer['content']['content']
        writer.add_document(title=title, path=path, content=content)
    writer.commit()
    return idx

def GetKeyQuestion():
    '''
    arguments:
    returns:
        querys_cut:[Counter({'再生': 1, '医学': 1}), Counter({'美国': 1, '贫铀': 1, '炸弹': 1, '姿态': 1})]
        indexs:['N01', 'N02', 'N03', 'N04', 'N05', 'N06', 'N07', 'N08', 'N09', 'N10', 'N11', 'N12', 'N13', 'N14', 'N15', 'N16']
        querys:['请说说再生医学。', '请说说美国对于贫铀炸弹的姿态', '请说说“911”恐怖袭击后美国经济发生了什么变化？。']
    '''
    results = qp.CutQuery()
    querys_cut, indexs, querys = [], [], []
    for result in results:
        query = result['QUESTION']
        query_cut = result['CONTENT']
        index = result['ID']
        querys_cut.append(query_cut)
        indexs.append(index)
        querys.append(query)
    return querys_cut, indexs, querys


def Search(idx, query_cut, qinx, query):
    '''
    arguments:
        idx:GetIndex()
        query_cut:Counter({'再生': 1, '医学': 1})
        qinx:N01
        query:请说说再生医学。
    output:
        query is 请说说再生医学。
        Founding 10 documents for N01
            综述:世界性的再生医疗研究开发热 from N01
            日本开发国产人体干细胞 from N01
            日本计划应用再生医疗技术使盲人重见光明 from N01
            日科学家拟加强国产化胚胎干细胞研究 from N01
            日本科学家用淋巴细胞合成“万能细胞” from N01
            日专家用患者自身细胞制作血管 from N01
            日本将禁止克隆人的胚胎 from N01
            日本实施“关于制作和使用人类胚胎干细胞的方针” from N01
            日本用患者自身干细胞培养可移植角膜 from N01
            人类克隆纷争再起 from N01
    '''
    searcher = idx.searcher()
    query_cut = query_cut.most_common(len(query_cut))
    resultlist = []
    for i in query_cut:
        if i[0] in ['中俄','泰国','叙利亚','俄罗斯','中国','科索沃','尼泊尔','印尼','波兰','美国']:
            resultlist = []
            results = searcher.find("content", i[0])
            resultlist.append(results)
            break
        else:
            results = searcher.find("content", i[0])
            resultlist.append(results)
    k = 0
    for i in resultlist:
        if len(i) > k:
            flag = i
            k = len(i)
    print('query is ' + query)
    print('Founding %d documents for ' % len(flag) + qinx)
    for i in range(min(10, len(flag))):
        result = json.dumps(flag[i].fields(), ensure_ascii=False)
        resultdict = json.loads(result)
        print(resultdict['title'] + ' from ' + resultdict['path'][:3])
    print('\n')

def ManSearch(idx, query):
    '''
    arguments:
        idx:GetIndex()
        query:再生医学
    output:
        query is 请说说再生医学。
        Founding 10 documents for N01
            综述:世界性的再生医疗研究开发热 from N01
            日本开发国产人体干细胞 from N01
            日本计划应用再生医疗技术使盲人重见光明 from N01
            日科学家拟加强国产化胚胎干细胞研究 from N01
            日本科学家用淋巴细胞合成“万能细胞” from N01
            日专家用患者自身细胞制作血管 from N01
            日本将禁止克隆人的胚胎 from N01
            日本实施“关于制作和使用人类胚胎干细胞的方针” from N01
            日本用患者自身干细胞培养可移植角膜 from N01
            人类克隆纷争再起 from N01
    '''
    searcher = idx.searcher()
    results = searcher.find('content', query)
    print('query is ' + query)
    print('Founding %d documents for ' % len(results))
    for i in range(min(10, len(results))):
        result = json.dumps(results[i].fields(), ensure_ascii=False)
        resultdict = json.loads(result)
        print(resultdict['title'] + ' from ' + resultdict['path'][:3])
    print('\n')

def Evaluate(idx, str):
    '''
    arguments:
        idx:
        str:
    output:
        final score is 100%(PRE=100%, REC=100%) on N05
        or
        Error
    '''
    N = idx['doc_num']
    avg_l = idx['avg_l']
    k1 = 1.5
    b = 0.75
    qtf = str[1] / str
    counter = qp.Counter()
    try:
        df = idx[str[0]]['df']
        postings = idx[str[0]]['postings']
        for posting in postings:
            tf = posting['tf']
            ld = posting['ld']
            score = (k1 * tf) / (tf + k1 * (1 - b + b * ld / avg_l))
            weight = score * math.log2((N - df + 0.5) / (df + 0.5))

            key = (posting['doc_id'], posting['doc_name'])
            counter += qp.Counter({key: weight})
        print('final score is ' + counter + ' on ' + counter[ID])
    except:
        print('Error')

if __name__ == '__main__':
    index = GetIndex()
    querys_cut, qindexs, querys = GetKeyQuestion()
    for num in range(len(querys_cut)):
        Search(index, querys_cut[num], qindexs[num], querys[num])
    # ManSearch(index, '')
