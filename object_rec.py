import os
import cv2
import math
import PySide
import pandas as pd
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
from sklearn import svm
from  PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
#gather_datasets.py script downloaded the datasets in the directory from whch we will execute the current script
root_dir = os.getcwd()

# --------------------------------------------- Training Data Preprocessing -------------------------------------
object_dataset_path = '/home/alexandra/Datasets/256_ObjectCategories'
negative_dataset_path = '/home/alexandra/Datasets/INRIAPerson/Train/neg'
negative_dataset = 'neg_data.txt'
positive_dataset = 'positive_dataset.txt'

#preparing positive_dataset and negative dataset ex. [class_value/ name of dir] ; [ path to positive sample]
def save_dataset_to_file(dir, filename, is_positive):
	save_to_file_path = os.path.join(root_dir, filename)
	save_to_file = open(save_to_file_path, 'a')

	for root, dir, files in os.walk(dir):
		for name in files:
			if is_positive == 1:
				image_name = os.path.join(root, name)
				content = os.path.split(os.path.dirname(image_name))[-1] + " ; " + image_name + "\n"
			elif is_positive == 0:
				content = "-1" + ";" + os.path.join(root, name) + "\n"
			save_to_file.write(content)

	save_to_file.close()

# ----------------------------- End of Preprocessing ----------------------------------------------------------------

# ----------------------------- Training Image Preprocessing  + Writing CSV for + - dataset--------------------------------------------------------
positive_dataset_csv = 'object_database.csv'
negative_dataset_csv = 'object_database.csv'

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
				if is_positive == 0:
					class_no , image_path = line.split(";")
					output_csv_fd.write(class_no)
					img = load_image_as_arr(os.path.abspath(image_path))
					chans = cv2.split(img)
					for i,chan in enumerate(chans):
						output_csv_fd.write(";")
						hist = channel_histogram(chan, [i])
						for x in hist:
							output_csv_fd.write(str(x))
				output_csv_fd.write("\n")
	output_csv_fd.close()
	fp.close()

datasets = '/home/alexandra/Datasets'
for root, dirs, files in os.walk(datasets):
	for name in dirs:
			dir_name = os.path.join(root, name)
			if dir_name.find(object_dataset_path) != -1:
				save_dataset_to_file(dir_name, positive_dataset, 1)

			dir_name = os.path.join(root, name)
			if dir_name.find(negative_dataset_path) != -1:
				save_dataset_to_file(dir_name, negative_dataset, 0)
file = os.path.join(root_dir, negative_dataset)
print(file)
generate_features_to_csv(file, 0, "negative_csv.csv")