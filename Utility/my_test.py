import pandas as pd

train_df = pd.read_pickle("model/soma_goods_train.df")

from konlpy.tag import Twitter; t = Twitter()
from nltk import pos_tag, word_tokenize

check_nltk = ["NN", "CD"]
check_Twitter = ["Noun", "Alpha", "Number"]

brackets = ["[", "{", "("]
brackete = ["]", "}", ")"]
bracRate = 0.3

def removeBracket(name):
    ret = ""
    chk = True
    for c in name:
        if c in brackets:
            chk = False
        if chk:
            ret += c
        if c in brackete:
            chk = True
    return ret

def getBrackets(name):
    ret = ""
    chk = False
    for c in name:
        if c in brackete:
            chk = False
        if chk:
            ret += c
        if c in brackets:
            chk = True
            ret += " "
    return ret

getName = lambda name : " ".join([token[0] for token in t.pos(removeBracket(name)) if token[1] in check_Twitter])

cate_dic = {}
text_dic = {}
products = []
cate_list = []
for each in train_df.iterrows():
	cate_list.append(";".join([each[1]['cate1'], each[1]['cate2'], each[1]['cate3']]))
	products.append((getName(each[1]['name']), [each[1]['cate1'],each[1]['cate2'],each[1]['cate3']]))

cate_dict = dict(zip(list(set(cate_list)),range(len(set(cate_list)))))

def insertText(text, cates, dic):
    if text not in dic:
        dic[text] = [{},{},{}]
    for i in range(3):
        if cates[i] not in dic[text][i]:
            dic[text][i][cates[i]] = 0
        dic[text][i][cates[i]]+=1

def insertCate(cate, text, dic):
    if cate not in dic:
        dic[cate] = {}
    if text not in dic[cate]:
        dic[cate][text] = 1
    dic[cate][text]+=1

def dicfy(names, cates):
    for name in list(set(names.split(" "))):
        for cate in cates:
            insertCate(cate, name, cate_dic)
        insertText(name, cates, text_dic)

for pro in products:
    dicfy(pro[0], pro[1])

getTupleList = lambda dic : [(k, v) for k, v in dic.iteritems()]
getPercent = lambda l, s : [(item[0], float(item[1])/s) for item in l]
getSorted = lambda tl : sorted(tl, key=lambda x : x[1], reverse=True)

for key in text_dic:
    for i in range(3):
        sorted_list = getSorted(getTupleList(text_dic[key][i]))
        text_dic[key][i] = getPercent(sorted_list, sum(item[1] for item in sorted_list))

for key in cate_dic:
    sorted_list = getSorted(getTupleList(cate_dic[key]))
    cate_dic[key] = getPercent(sorted_list, sum(item[1] for item in sorted_list))

def getCates(token, dic):
    cates = []
    for cate in dic:
        if not cates or cates[-1][1]/2. < cate[1]:
            cates.append(cate)
    return cates

def getResult(tokens, dic):
    result_cate = [{}, {}, {}]
    for token in tokens:
        if token not in dic:
            continue
        for i in range(3):
            for cate in getCates(token, dic[token][i]):
                if cate[0] not in result_cate[i]:
                    result_cate[i][cate[0]] = 0
                result_cate[i][cate[0]] += cate[1]
    return result_cate


def detailResult(name, DEBUG=False):
    result_cate = [{}, {}, {}]
        
    for token in list(set(name.split(" "))):
        for step in range(len(token) - 1, 1, -1):
            tokens = [token[i:i+step] for i in range(len(token) - step + 1)]
            result = getResult(tokens, text_dic)
            for i in range(3):
                for k, v in result[i].items():
                    if k not in result_cate[i]:
                        result_cate[i][k] = 0
                    result_cate[i][k] += v
    if DEBUG:
        print "== detail RESULT =="
        print getSorted(getTupleList(result_cate[0]))
        print getSorted(getTupleList(result_cate[1]))
        print getSorted(getTupleList(result_cate[2]))
        
    return result_cate

def simpleResult(text, DEBUG=False):
    brac = getName(getBrackets(text.decode('utf-8')))
    name = getName(text.decode('utf-8'))
    
    result_cate = getResult(list(set(name.split(" "))), text_dic)
    
    if brac:
        result_cate_brac = getResult(list(set(brac.split(" "))), text_dic)
        for i in range(3):
            for key, value in result_cate_brac[i].items():
                if key not in result_cate[i]:
                    result_cate[i][key] = 0
                result_cate[i][key] += value * bracRate
    
    if DEBUG:
        print text
        print brac
        print name
        print result_cate_brac
        print result_cate
        print getSorted(getTupleList(result_cate[0]))
        print getSorted(getTupleList(result_cate[1]))
        print getSorted(getTupleList(result_cate[2]))
        
    if not result_cate[0] or not result_cate[1] or not result_cate[2]:
        result_cate = detailResult(name, DEBUG)
    #print result_cate[i]
    result = [getSorted(getTupleList(result_cate[i])) for i in range(3)]
    #print result
    return ";".join([result[i][0][0] for i in range(3)])

def cate_match(name ,imge):
	result = simpleResult(name)
	if result in cate_list:
		return "y: " + result.encode('utf-8')
	else:
		return "x: " + result.encode('utf-8')

def process(name, imge):
	return simpleResult(name).encode('utf-8')

from test_module import TEST
TEST("mymodel.test", process)


