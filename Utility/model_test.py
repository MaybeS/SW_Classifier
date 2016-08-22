from sklearn.externals import joblib

clf = joblib.load('model/classify.model')
cate_dict = joblib.load('model/cate_dict.dat')
vectorizer = joblib.load('model/vectorizer.dat')

joblib.dump(clf,'model/n_classify.model')
joblib.dump(cate_dict,'model/n_cate_dict.dat')
joblib.dump(vectorizer,'model/n_vectorizer.dat')

cate_id_name_dict = dict(map(lambda (k,v):(v,k),cate_dict.items()))

from konlpy.tag import Twitter; t=Twitter()
from nltk import pos_tag, word_tokenize

brackets = ["[", "{", "("]
brackete = ["]", "}", ")"]
def bracTokenize(name, chk=True):
    brac = {True:"", False:""}
    for c in name:
        chk = not c in brackets and chk
        if c not in brackets and c not in brackete: brac[chk] += c
        else: brac[chk] += " "; brac[not chk] += " "
        chk = c in brackete or chk
    return (brac[True], brac[False])

check_nltk = ["NN", "CD"]
check_Twitter = ["Noun", "Alpha"]

getTokn = lambda name : list(set([token[0] for token in t.pos(name)]))
getNoun = lambda name : list(set([token[0] for token in t.pos(name) if token[1] in check_Twitter]))
def getName(name):
    brac = bracTokenize(name)
    return " ".join([" ".join(getTokn(bra)) for bra in brac] + [" ".join(getNoun(brac[0]))])

def process(name, imge):
	result = cate_id_name_dict[clf.predict(vectorizer.transform([getName(name.decode('utf-8'))]))[0]]
	return result.encode('utf-8')

from test_module import TEST
TEST("classify.test", process)