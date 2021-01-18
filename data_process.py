# Author:STEVEN

import os
import chardet
import re


def GetFileList(dir, filelist):
    '''
    arguments:
        dir:
        filelist:
    returns:
        filelist:['/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/data/N13/XIN_CMN_20010716_0060.stno',
                  '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/data/N02/za2001_001865.stno',
                  '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/data/N13/XIN_CMN_20010911_0034.stno']
    '''
    if os.path.isfile(dir):
        filelist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileList(newDir, filelist)
    return filelist


def GetFileName(filedir):
    '''
    arguments:
        filedir:
    returns:
        filename:['N13-XIN_CMN_20010716_0060',
                  'N02-za2001_001865',
                  'N13-XIN_CMN_20010911_0034']
    '''
    j = 0
    tag = 0
    for i in filedir:
        j = j + 1
        if (i == '/'):
            tag = j - 4
    filename = filedir[tag:len(filedir) - 5]
    filename = filename.replace('/', '-')
    return filename


def CreateFileName(str):
    '''
    arguments:
        str:
    returns:
        filename:['日专家用患者自身细胞制作血管',
                  '综述:世界性的再生医疗研究开发热',
                  '日本将禁止克隆人的胚胎']
    '''
    if 'HEADLINE>' in str:
        str = str.replace('<HEADLINE>', '')
        str = str.replace('</HEADLINE>', '')
        if len(str) > 1:
            realname = str.strip()
        else:
            realname = ''
    else:
        realname = ''
    return realname


def RemoveTag(dir_list):
    '''
    arguments:
        dir_list:
    returns:
        filelist:['/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/file/N13-XIN_CMN_20010716_0060.txt',
                  '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/file/N02-za2001_001865.txt',
                  '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/file/N13-XIN_CMN_20010911_0034.txt']
    '''
    for dir in dir_list:
        filebi = open(dir, 'rb')
        data = filebi.read()
        enctype = chardet.detect(data)['encoding']
        filename = GetFileName(dir)
        if filename[4] != '.':
            filestno = open(dir, 'r', encoding=enctype, errors='ignore')
            filename = 'file/' + filename + '.txt'
            filetxt = open(filename, 'w', encoding=enctype)
            for line in filestno.readlines():
                realname = CreateFileName(line)
                if len(realname) > 1:
                    filetxt.write(realname.strip())
                    filetxt.write('\n')
                re_html = re.compile(r'<[^>]+>')
                line = re_html.sub('', line)
                if len(line.strip()) == 4:
                    filetxt.write('\n')
                else:
                    filetxt.write(line.strip())
    txtdir = '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/file'
    txtlist = GetFileList(txtdir, [])
    return txtlist


def GetAbsolutePath(filelist):
    '''
    arguments:
        filelist:
    '''
    path = open('TXTPath.txt', 'w', encoding='utf-8')
    for file in filelist:
        path.write(file)
        path.write('\n')


if __name__ == '__main__':
    dir = '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/data'
    txtdir = '/Users/steven/Documents/课程/搜索引擎/搜索引擎/final/file'
    stnolist = GetFileList(dir, [])
    txtlist = RemoveTag(stnolist)
    GetAbsolutePath(txtlist)
