#!/usr/bin/python3

import os
import wget
#link to the positive dataset
caltech_objects_dataset_url='http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar'
inria_negative_dataset_url='http://pascal.inrialpes.fr/data/human/INRIAPerson.tar'
positive_dataset_path="256_ObjectCategories.tar"
negative_dataset_path="INRIAPerson.tar"
dataset_path ='~/Datasets/'
if not os.path.exists(positive_dataset_path) and not os.path.exists(negative_dataset_path):
		if not os.path.exists(dataset_path):
			os.system("mkdir ~/Datasets")
		caltech  = wget.download(caltech_objects_dataset_url)
		inria = wget.download(inria_negative_dataset_url)
		os.system("tar -xvf {} -C {} ".format(positive_dataset_path, dataset_path))
		os.system("tar -xvf {} -C {} ".format(negative_dataset_path, dataset_path))
		os.system("rm -rf *.tar")
