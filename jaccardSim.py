import LAC
import jieba
from collections import defaultdict


lac = LAC(mode='lac')

def jaccard(x, y):
    x = set(x)
    y = set(y)
    return len(x & y) / len(x|y)
def countDic(x):
    d =  defaultdict(int)
    for i in x:
        d[i] = d[i] + 1
    return d
def jaccardRepeated(a, b):
    longDic = a if len(a) >= len(b) else b
    shortDic = a if len(a) < len(b) else b
    totalLen = len(a) + len(b)
    longLen, shortLen = len(longDic), len(shortDic)
    if totalLen == 0: return 1
    longDic = countDic(longDic)
    shortDic = countDic(shortDic)
    num = 0
    for key in shortDic.keys():
        num = num + min(shortDic[key], longDic[key])
    # 这里如果用总长度当分母会有问题：相似度永远不会到1
    return num/(longLen + shortLen - num)

def jacSeten(x, y, repeat = True, tokenMode = 'jieba'):
    if tokenMode == 'lac':
        x, _ = lac.run(x)
        y, _ = lac.run(y)
    elif tokenMode == 'jieba':
        x = list(jieba.cut(x))
        y = list(jieba.cut(y))
    else:
        x = list(x)
        y = list(y)
    if (repeat): return jaccardRepeated(x, y)
    return jaccard(x, y)


