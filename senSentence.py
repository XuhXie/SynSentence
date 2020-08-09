from LAC import LAC
import jieba
import jieba.analyse as analyse
# import synonyms
import numpy as np
import random

cilinpath = 'cilin.txt'
synwords = []

synwords_dic = {}
with open(cilinpath, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        items = line.strip().split()
        if items[0][-1] != '=':
            continue
        items = items[1:]
        for word in items:
            if (len(word) < 2): continue
            if word in synwords_dic:
                synwords_dic[word] = synwords_dic[word] + items
            else:
                synwords_dic[word] = items

# 去重/去掉单个字
for key in list(synwords_dic.keys()):
    rawSyns = synwords_dic[key]
    rawSyns = list(set(rawSyns))
    for word in rawSyns:
        if (len(word) < 2):
            rawSyns.remove(word)
    synwords_dic[key] = rawSyns

print("finish Synword_dic: ", len(synwords_dic))


def findsyn(word):
    if len(word) == 1:
        return []
    if word in synwords_dic:
        return synwords_dic[word]
    return []


def synSenByCilin(origin, keywords=-1, replaceVaue=0.2, keyWordsStep=25, fix=('n', 'v', 'vd', 'a', 'ad', 'an', 'd', 'c')):
    '''
     Keywords: 默认 -1 是表示自动通过 jieba分词提取tage，如果要手动导入，则需要输入 元组格式
     replaceVaue: 遇到一个词是，不替换其同义词的概率
     keyWordsStep: 通过jieba获取tag的个数，这里用 int（输入语句长度/keyWordsStep）来计算个数
     fix：通过LAC 进行标注词性后，选择哪些词性的词语需要进行同义词替换。一般不替换命名实体、量词。
    '''

    lac = LAC(mode='lac')
    a, b = lac.run(origin)
    numofkeywords = int(len(origin) / keyWordsStep)
    if keywords == -1:
        keywords = tuple(analyse.extract_tags(origin, topK=numofkeywords, withWeight=False, allowPOS=()))
    for i in range(len(a)):
        current = b[i]
        if (current in fix) and (a[i] not in keywords):
            synList = findsyn(a[i])
            lenList = len(synList)
            replace = (random.random() > replaceVaue)
            if lenList > 0 and replace:
                randomIndex = int(random.random() * lenList)
                a[i] = synList[randomIndex]
    return ''.join(a)

# 通过第三方库 synonyms 对同义词进行排序对进阶版。效果不是很好。
# def synSenByCilinPlus(origin, keywords = -1,  key_top_n = 3, top_n = 5, fix = ('n','v','vd','a','ad','an','d','c')):
#     lac = LAC(mode='lac')
#     a,b = lac.run(origin)
#     if keywords == -1:
#         keywords = tuple(analyse.extract_tags(origin, topK= key_top_n, withWeight=False, allowPOS=()))

#     for i in range(len(a)):
#         current = b[i]
#         if (current in fix) and (a[i] not in keywords):
#             synList = []
#             synList = findsyn(a[i])
#             lenList = len(synList)
#             synValues = []
#             if lenList > 0:
#                 for item in synList:
#                     synValues.append(synonyms.compare(item, a[i]))
#                 synList = [x for _,x in sorted(zip(synValues, synList), key=lambda pair: pair[0], reverse = True)]
#                 temp = top_n if lenList > top_n else lenList
#                 randomIndex = int (random.random() * temp)
# #                 randomIndex = int (random.random() * lenList)
#                 a[i] = synList[randomIndex]
#     return ''.join(a)