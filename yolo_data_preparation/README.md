This folder contains sample data and data processing scripts.

Zooniverse format: The zooniverse formatted data indexed by box in image. That is, each row corresponds to each box in an image. One image may have multiple rows.

Yolo format: The yolo model takes data indexed by image. That is, each row corresponds to each image. One image has one row and all boxes information in that image.



river_data:
  1. river_cam:
  train_labels/test_labels: train and test set in the format of the zooniverse_conversion.py 
  train_rivercam/test_rivercam: data converted to the yolo input format, by running river_data_to_yolo_converter.py

  2. river_drone:
  similar to river_cam data, except that corrected_test_riverdrone is the version by removing the rows where images cannot be   found, by running remove_rows_without_image.py

ocean_data:
  filter_acceptable_boxes.py: filter the boxes when an object get multiple bounding boxes
  1. ocean_drone:
  by running the ocean_to_yolo_csv_convertor.py convert the zooniverse conversion format to the yolo input format

