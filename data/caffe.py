#-*- coding: utf-8 -*-  

url = "http://192.168.99.100:5000/classify_url"

import os
from urllib import urlopen

jsons = os.listdir('./jsons/')
for image in os.listdir('./images/'):
	if image[:-3] + "json" in jsons:
		continue
	if image[-3:] != 'jpg':
		continue
	r = urlopen(url + '?imageurl=/opt/caffe/res/soma_train/' + image)
	f = open('./jsons/' + image[:-3] + 'json', 'w')
	f.write(r.read())
	f.close()