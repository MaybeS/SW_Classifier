#-*- coding: utf-8 -*-
import json

def readJson(filename):
	f = open(filename, "r")
	r = f.read()
	if r[0] == "<":
		js = {"result": ["False", [], []]}
	else:
		js = json.loads(r)
	return js

def getRatio(jss):
	if len(jss) > 0 and float(jss[0][1]) > 1.0:
		return jss[0][0]
	else:
		return ""

def getImageJsonLast(image):
	js = readJson("./jsons/" + image + ".json")
	if js['result'][0] == "False":
		return ""
	return getRatio(js['result'][1]) + " " + getRatio(js['result'][2])

def getImageJson(image):
	f = open('data/images_result.txt', 'r')
	lines = f.readlines()
	for line in lines:
		q = line.split('/**/')
		flag = q[0].split('/')[-1][:-4]
		result = q[1]
		if flag == image:
			return result
	return ""

if __name__ == '__main__':
	name = u"인텔 인텔 코어i7-4세대 4770K (하스웰) (정품)"
	imge = "90985"
	print getImageJson(imge)