import os
import cv2
import math
import PySide
import pandas as pd
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import load_svmlight_file
from  PyQt5 import QtCore, QtGui, QtWidgets

#gather_datasets.py script downloaded the datasets in the directory from which we will execute the current script
root_dir = os.getcwd()
object_dataset_path = '/home/alexandra/Datasets/256_ObjectCategories'
negative_dataset_path = '/home/alexandra/Datasets/INRIAPerson/Train/neg'
negative_dataset = 'negative_dataset.txt'
positive_dataset = 'positive_dataset.txt'
negative_dataset_csv = "negative_csv.csv"
positive_dataset_csv = "positive_csv.csv"
datasets_dir = '/home/alexandra/Datasets'
negative_dataset_file = os.path.join(root_dir, negative_dataset)
positive_dataset_file = os.path.join(root_dir, positive_dataset)

# --------------------------------------------- Training Data Preprocessing -------------------------------------

#preparing positive_dataset and negative dataset ex. [class_label;absolute_path of image\n]
def create_datasets_file(datasets_dir, object_dataset_path, is_positive, dataset_file) :
	for root, dirs, files in os.walk(datasets_dir):
		for name in dirs:
			dir_name = os.path.join(root, name)
			if dir_name.find(object_dataset_path) != -1:
				if is_positive == 1 and dir_name == object_dataset_path:
					continue
				save_dataset_to_file(dir_name, dataset_file, is_positive)

def save_dataset_to_file(dir, filename, is_positive):
	save_to_file_path = os.path.join(root_dir, filename)
	save_to_file = open(save_to_file_path, 'a')
	class_no = 0
	counter = 0
	for root, dir, files in os.walk(dir):
		if is_positive == 1 and root != object_dataset_path:
			class_no += 1
		for name in files:
			image_name = os.path.join(root, name)
			if (is_positive == 1) and (counter < 5):
				content = str(class_no) + ";" + image_name + "\n"
				counter = counter + 1
				save_to_file.write(content)
			elif is_positive == 0 and counter < 5:
				content = "-1" + ";" + image_name + "\n"
				counter = counter + 1
				save_to_file.write(content)
	save_to_file.close()

# ----------------------------- End of Data Preprocessing --------------------------------------------------------

# ----------------------------- Training Image Preprocessing  + Writing CSV for + - dataset-----------------------

def load_image_as_arr(image_path):
	img = cv2.imread(image_path.rstrip(), cv2.IMREAD_COLOR)
	return img

# generate histogram per channel
def channel_histogram(image, channels):
	#color channels
	hist = cv2.calcHist(image, channels, None, [256], [0, 256])
	return hist

def generate_features_to_csv(input_data_file, is_positive, output_csv):
	output_csv_fd = open(output_csv, 'a')
	with open(input_data_file) as fp:
		for line in fp:
			class_no , image_path = line.split(";")
			print(class_no)
			print(image_path)
			output_csv_fd.write(class_no)
			img = load_image_as_arr(os.path.abspath(image_path))
			chans = cv2.split(img)
			counter = 0
			for i,chan in enumerate(chans):
				print(chan)
				output_csv_fd.write(" ")
				hist = channel_histogram(chan, [i])
				for ix,iy in np.ndindex(hist.shape):
					print(counter)
					counter = counter + 1
					content = str(counter) + ":" + str(hist[ix][iy])
					output_csv_fd.write(content)
					output_csv_fd.write(" ")
			output_csv_fd.write("\n")
	output_csv_fd.close()
	fp.close()

#---------------- End Image Preprocessing------------------------------------------------------------------------
#---------------- cleanup ---------------------------------------------------------------------------------------
def cleanup(negative_dataset_file, positive_dataset_file, negative_dataset_csv, positive_dataset_cs):
	paths = locals()
	for k in sorted(paths.keys()):
		if paths[k] is not None:
			path = paths[k]
			if os.path.exists(path):
				os.system("rm -rf {}".format(path))

#-----------------main-------------------------------------------------------------------------------------------
cleanup(negative_dataset_file, positive_dataset_file, negative_dataset_csv, positive_dataset_csv)
create_datasets_file(datasets_dir, object_dataset_path, 1, positive_dataset)
create_datasets_file(datasets_dir, negative_dataset_path, 0, negative_dataset)
generate_features_to_csv(negative_dataset_file, 0, negative_dataset_csv)
generate_features_to_csv(positive_dataset_file, 1, positive_dataset_csv)
X_train, y_train = load_svmlight_file(positive_dataset_csv)
print(X_train.shape)