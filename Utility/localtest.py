from sklearn.externals import joblib

clf = joblib.load('model/classify.model')
cate_dict = joblib.load('model/cate_dict.dat')
vectorizer = joblib.load('model/vectorizer.dat')

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

import pandas as pd
train_df = pd.read_pickle("model/soma_goods_train.df")

from tqdm import tqdm
def main():
    cnt_all = 0
    cnt_rig = 0
    for each in tqdm(train_df.iterrows()):
        ans = ";".join([each[1]['cate1'], each[1]['cate2'], each[1]['cate3']])
        q = getName(each[1]['name'] + " " + getImge(str(each[0])))
        cate = cate_id_name_dict[clf.predict(vectorizer.transform([q]))[0]]
        if cate == ans:
            cnt_rig+=1
        else:
            print cate, ans
            print each[1]['name']
        cnt_all+=1
    print cnt_rig, cnt_all
    print float(cnt_rig * 100) / float(cnt_all), "%"

if __name__ == '__main__':
    main()
