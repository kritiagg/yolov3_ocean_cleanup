This folder contains sample data and data processing scripts, to convert the zooniverse_conversion.py output data format to the yolo model data format.

Zooniverse format(.csv): The zooniverse formatted data indexed by box in image. That is, each row corresponds to each box in an image. One image may have multiple rows.

Yolo format(.txt): The yolo model takes data indexed by image. That is, each row corresponds to each image. One image has one row and all boxes information in that image.

convertFilenames.py: takes folder path as input; if there is space in the image file name, this script help replace the ' ' by '_'

remove_rows_without_image.py: takes .txt format data as input; remove the rows in train.txt and test.txt set, where images cannot be found.

train_test_set_division.py: takes .csv format data as input; to train set and test set

river_data:

river_data_to_yolo_converter.py: takes .csv format data as input; convert the river data from zooniverse converted .csv format to yolo input .txt format

  1. river_cam:
  train_labels.csv/test_labels.csv: train and test set in the .csv format of the zooniverse_conversion.py output
  train_rivercam.txt/test_rivercam.txt: data converted to the yolo input .txt format, by running river_data_to_yolo_converter.py

  2. river_drone:
  similar to river_cam data, except that corrected_train/test_riverdrone.txt is the version by removing the rows where images cannot be found, by running remove_rows_without_image.py
  
  3. river_all:
  combine data from river_cam and river_drone.
  

ocean_data:

  filter_acceptable_boxes.py: filter the boxes when an object get multiple bounding boxes
  
  ocean_to_yolo_csv_convertor.py: takes ocean .csv data as input, convert to yolo input .txt format
  
  1. ocean_drone:
  by running the ocean_to_yolo_csv_convertor.py convert the zooniverse conversion format to the yolo input format

3_set_combine:
  combine data from river_cam, river_drone and ocean_drone
  3_set_combine_train/test.txt: by simply combine the two data set and perform train-test split.
  corrected_3_set_combine_train/test.txt: remove the rows where image cannot be found
  
  
  
