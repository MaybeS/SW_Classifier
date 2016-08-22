
from sklearn.externals import joblib

clf = joblib.load('model/classify.model')
cate_dict = joblib.load('model/cate_dict.dat')
vectorizer = joblib.load('model/vectorizer.dat')

joblib.dump(clf,'model/server/n_classify.model')
joblib.dump(cate_dict,'model/server/n_cate_dict.dat')
joblib.dump(vectorizer,'model/server/n_vectorizer.dat')

cate_id_name_dict = dict(map(lambda (k,v):(v,k),cate_dict.items()))

from konlpy.tag import Twitter; t = Twitter()
from nltk import pos_tag, word_tokenize
from nltk.util import ngrams

brackets = ["[", "{", "("]
brackete = ["]", "}", ")"]
def getBrac(name, chk=True):
    brac = {True:"", False:""}
    for c in name:
        chk = not c in brackets and chk
        if c not in brackets and c not in brackete: brac[chk] += c
        else: brac[chk] += " "; brac[not chk] += " "
        chk = c in brackete or chk
    return (brac[True], brac[False])

gram_cnt = 2
chk_NC = ["NN", "CD"]
chk_NA = ["Noun"]
chk_NAN = ["Noun", "Number"]

getNLTK = lambda name, chk : [token[0] for token in pos_tag(name) if token[1][:2] in chk]
getKONL = lambda name, chk : [token[0] for token in t.pos(name) if token[1] in chk]
getTokn = lambda name, chk_ko, chk_en : [token[0] for token in t.pos(name) if (token[1] == "Alpha") or token[1] in chk_ko]
getGram = lambda name, cnt : [" ".join(["".join(grams)]) for grams in ngrams(name, cnt)]
def getName(name):
	brac = getBrac(name)
	noun = getTokn(brac[0], chk_NAN, chk_NC) + getTokn(brac[1], chk_NAN, chk_NC)
	gram = getGram(noun, min(gram_cnt, max(len(noun)-1, 1)))
	return " ".join(list(set(noun)) + list(set(gram)))

getImageName = lambda name : name.split('/')[-1][:-4]

from classify_image_module import getImageJson
def getImge(name):
    return getImageJson(name)

isImage = False
def get(n, i):
	if isImage:
		return [getName(n.decode('utf-8')) + getImge(getImageName(i))]
	return [getName(n.decode('utf-8'))]

from IPython.display import clear_output
from bottle import route, run, template,request,get, post

import  time
from threading import  Condition
_CONDITION = Condition()

count = 0
@route('/classify')
def classify():
    global count
    count += 1
    print count
    if not count % 100:
        clear_output()
    img = request.GET.get('img','')
    name = request.GET.get('name', '')
    pred = clf.predict(vectorizer.transform(get(name, img)))[0]
    return {'cate':cate_id_name_dict[pred]}

run(host='0.0.0.0', port=8887)
