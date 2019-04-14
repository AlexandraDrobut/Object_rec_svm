import os

#gather_datasets.py script downloaded the datasets in the directory from whch we will execute the current script
root_dir = os.getcwd()
object_dataset_path = '/home/alexandra/Datasets/256_ObjectCategories'
negative_dataset_path = '/home/alexandra/Datasets/INRIAPerson/Train/neg'
negative_dataset = 'neg_data.txt'
positive_dataset = 'positive_dataset.txt'

#preparing positive_dataset and negative dataset ex. [class_value] ; [ path to positive sample]
def save_dataset_to_file(dir, filename, is_positive):
	save_to_file_path = os.path.join(root_dir, filename)
	save_to_file = open(save_to_file_path, 'a')

	for root, dir, files in os.walk(dir):
		for name in files:
			if is_positive == 1:
				image_name = os.path.join(root, name)
				content = os.path.split(os.path.dirname(image_name))[-1] + " ; " + image_name + "\n"
			elif is_positive == 0:
				content = "-1" + " ; " + os.path.join(root, name) + "\n"
			save_to_file.write(content)

	save_to_file.close()


for root, dirs, files in os.walk(root_dir):
	for name in dirs:
			dir_name = os.path.join(root, name)
			if dir_name.find(object_dataset_path) != -1:
				save_dataset_to_file(dir_name, positive_dataset, 1)

			dir_name = os.path.join(root, name)
			if dir_name.find(negative_dataset_path) != -1:
				save_dataset_to_file(dir_name, negative_dataset, 0)

