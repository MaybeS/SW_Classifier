# Classifier
This repository for SW_Maestro_ 7th 3th Assignment.

Develop with Docker, Jupyter, python

Docker Hub - [namsangboy/scikit-classify-server](https://hub.docker.com/r/namsangboy/scikit-classify-server/), [namsangboy/caffe-classifier-scikit](https://hub.docker.com/r/namsangboy/caffe-classifier-scikit/)

## Directory
- data/caffe.py 	
	caffe_demo crawler make json from images(given)
	- data/images/
	- data/jsons/

- model/
	SVM learned data;
	- model/server/

- Utility/
	utilities for test
	- Utility/test_module.py
	- Utility/model_test.py
	- Utility/my_test.py

- classify_image_module.py
	get data from json; pre defined data from image
- classify_server.py

- classify.py
- classify.test

## Goal
Archive: Raise the classification accuracy

- basemodel: 66.1429%
- finalmodel(model/Maybe/*): 72.2041%

## Implementation

