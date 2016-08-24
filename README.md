# Classifier
This repository for SW_Maestro_ 7th 3th Assignment.

Develop with Docker, Jupyter, python

Docker Hub - [namsangboy/scikit-classify-server](https://hub.docker.com/r/namsangboy/scikit-classify-server/), [namsangboy/caffe-classifier-scikit](https://hub.docker.com/r/namsangboy/caffe-classifier-scikit/)

check [jupyter notebook](http://maynet.iptime.org:8888)
- maynet.iptime.org:8887-8

## Directory
- data/caffe.py 	
	caffe_demo crawler make json from images(given)
	- data/images/
	- data/jsons(_server)/

	google image search result crawled
	- data/Crawler/result.txt
	- data/images(_server)_result.txt

- model/: latest model(**archive above 73%**)

- Utility/
	utilities for test
	- Utility/test_module.py
	- Utility/model_test.py
	- Utility/my_test.py

- classify_image_module.py
	get data from json; pre defined data from image
- classify_server.py
- classify.py

## Goal
Archive: Raise the classification accuracy

- basemodel: 66.1429%
- finalmodel(model/*): 73.2041%

## Implementation

First using nlp, konlpy and nltk.
*I can archive 70-72% using only nlp.*

Second using image, try given caffe_demo.
*I can archive 68-70% using nlp and image data treated with caffe_demo.*

Finally using image with google.
I send request google image search and parse result.
*data/Crawler/gogo.py implemented for data crawling*
*I can archive above 73% using nlp with image data treated with google.*

#### NLP

In `classifier.ipynb`, `getName` function is for nlp.
- separated by bracket, **see also `getBrac` function** 
- (extra) *i try to more weight with '**inner text of bracket**', but score does not increase.*
- get only *Noun, Alphabet, Number* from text using nltk and twitter(konlpy)
- (extra) *i try to various combinations of black-white list of tag of words, but score does not increase.*
- get 2-gram of result. **see also `getGram` function**
- (extra) *i try 3,4-gram, but score does not increase.*
- remove duplication of each result(result, gram-result)
- (extra) *try append **more important words** to back of result, but score does not increase.*
	- the words which in cate
	- the words which duplicated

#### Image

In `classify_image_module`, `getImageJson` function is for image processing
- first, i try data from caffe_demo result. **see also `data/jsons(_server)`**
- get best score of each category in json, and append to result of nlp, but score decrease.
- get best score and some of good scores and test, but score decrease.
- i crawled from **google image search**. **see also `data/image_result(_server)`**, score increase!!!

