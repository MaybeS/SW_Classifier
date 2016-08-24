
# coding: utf-8

# 

# In[1]:

from sklearn.externals import joblib


# In[2]:

clf = joblib.load('classify.model')
cate_dict = joblib.load('cate_dict.dat')
vectorizer = joblib.load('vectorizer.dat')


# In[3]:

joblib.dump(clf,'n_classify.model')
joblib.dump(cate_dict,'n_cate_dict.dat')
joblib.dump(vectorizer,'n_vectorizer.dat')


# In[4]:

cate_id_name_dict = dict(map(lambda (k,v):(v,k),cate_dict.items()))


# In[5]:

from konlpy.tag import Twitter; t = Twitter()
from nltk import pos_tag, word_tokenize
from nltk.util import ngrams


# In[6]:

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


# In[7]:

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


# In[8]:

getImageName = lambda name : name.split('/')[-1][:-4]


# In[9]:

from classify_image_module import getImageJson
def getImge(name):
    return getImageJson(name)


# In[10]:

test_name = u"인텔 인텔 코어i7-4세대 4770K (하스웰) (정품)"
test_imge = u"90985"
name = getName(test_name)
imge = getImge(test_imge)
print "name: ", name
print "image: ", imge


# In[11]:

pred = clf.predict(vectorizer.transform([name + imge]))[0]
print cate_id_name_dict[pred]


# In[12]:

name_test = u"(퀸)국내생산100% 바자르 번아웃극세사 차렵세트"
imge_test = "http://image.hnsmall.com/images/goods/477/11924477_g.jpg"
name = getName(name_test)
imge = getName(getImge(getImageName(imge_test)))
q = getName(name_test) + " " + getName(getImge(getImageName(imge_test)))
print "name: ", name
print "image: ", imge
print "q:", q
print cate_id_name_dict[clf.predict(vectorizer.transform([q]))[0]]


# In[ ]:

from IPython.display import clear_output


# In[ ]:

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
    q =  getName(name.decode('utf-8') + " " + getImge(getImageName(img)).decode('utf-8'))
    pred = clf.predict(vectorizer.transform([q]))[0]
    return {'cate':cate_id_name_dict[pred]}

run(host='0.0.0.0', port=8887)


# In[ ]:




# In[ ]:




# In[ ]:



