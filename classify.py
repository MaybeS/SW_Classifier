#-*- coding: utf-8 -*-
import pandas as pd
train_df = pd.read_pickle("model/soma_goods_train.df")

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
#vectorizer = CountVectorizer(max_features=10000)

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
getTokn = lambda name, chk_ko, chk_en : [token[0].lower() for token in t.pos(name) if (token[1] == "Alpha") or token[1] in chk_ko]
getGram = lambda name, cnt : [" ".join(["".join(grams)]) for grams in ngrams(name, cnt)]
def getName(name, cate):
    brac = getBrac(name)
    noun = getTokn(brac[0], chk_NAN, chk_NC) + getTokn(brac[1], chk_NAN, chk_NC)
    extr = [n for n in noun if n in getTokn(cate, chk_NAN, chk_NC)]
    gram = getGram(noun, min(gram_cnt, max(len(noun)-1, 1)))
    return " ".join(list(set(noun)) + list(set(gram)))

from classify_image_module import getImageJson
def getImge(name):
    return getImageJson(name)

d_list = []
cate_list = []
for each in train_df.iterrows():
    cate = ";".join([each[1]['cate1'], each[1]['cate2'], each[1]['cate3']])
    d = getName(each[1]['name'] + " " + getImge(str(each[0])), cate)
    d_list.append(d)
    cate_list.append(cate)

cate_dict = dict(zip(list(set(cate_list)),range(len(set(cate_list)))))

x_list = vectorizer.fit_transform(d_list)
y_list = [cate_dict[";".join([each[1]['cate1'], each[1]['cate2'], each[1]['cate3']])] for each in train_df.iterrows()]

from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
import numpy as np
svc_param = {'C':np.logspace(-0.10950 - 0.2, -0.10950 + 0.2, 3)}

gs_svc = GridSearchCV(LinearSVC(),svc_param,cv=10, n_jobs=4)
gs_svc.fit(x_list, y_list)
print gs_svc.best_params_, gs_svc.best_score_

clf = LinearSVC(C=gs_svc.best_params_['C'])
clf.fit(x_list,y_list)

from sklearn.externals import joblib
joblib.dump(clf,'model/classify.model',compress=3)
joblib.dump(cate_dict,'model/cate_dict.dat',compress=3)
joblib.dump(vectorizer,'model/vectorizer.dat',compress=3)
