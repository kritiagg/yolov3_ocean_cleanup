# coding: utf-8

from __future__ import division, print_function

import tensorflow as tf
import numpy as np
import argparse
import cv2

from utils.misc_utils import read_class_names
from utils.plot_utils import get_color_table, plot_one_box
from utils.data_aug import letterbox_resize

from model import yolov3

parser = argparse.ArgumentParser(description="YOLO-V3 test single image test procedure.")
parser.add_argument("input_image", type=str,
                    help="The path of the input image.")
parser.add_argument("--new_size", nargs='*', type=int, default=[1024, 1024],
                    help="Resize the input image with `new_size`, size format: [width, height]")
parser.add_argument("--class_name_path", type=str, default="./data/my_data_river.names",
                    help="The path of the class names.")
parser.add_argument("--restore_path", type=str, default="./saved_model/",
                    help="The path of the weights to restore.")
parser.add_argument("--letterbox_resize", type=lambda x: (str(x).lower() == 'true'), default=True,
                    help="Whether to use the letterbox resize.")
args = parser.parse_args()

args.classes = read_class_names(args.class_name_path)
args.num_class = len(args.classes)

color_table = get_color_table(args.num_class)

img_ori = cv2.imread(args.input_image)
if args.letterbox_resize:
    img, resize_ratio, dw, dh = letterbox_resize(img_ori, args.new_size[0], args.new_size[1])
else:
    height_ori, width_ori = img_ori.shape[:2]
    img = cv2.resize(img_ori, tuple(args.new_size))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = np.asarray(img, np.float32)
img = img[np.newaxis, :] / 255.

with tf.Session() as sess:
    input_data = tf.placeholder(tf.float32, [1, args.new_size[1], args.new_size[0], 3], name='input_data')

    tf.saved_model.loader.load(sess, ["serve"], args.restore_path)
    graph = tf.get_default_graph()

    # concat_XX:0 are names of output tensors printed out by save_model.py script
    # no idea why it is `input_data_1` instead of `input_data` for the name of input tensor
    boxes_, scores_, labels_ = sess.run(['concat_10:0', 'concat_11:0', 'concat_12:0'], feed_dict={'input_data_1:0': img})

    # rescale the coordinates to the original image
    if args.letterbox_resize:
        boxes_[:, [0, 2]] = (boxes_[:, [0, 2]] - dw) / resize_ratio
        boxes_[:, [1, 3]] = (boxes_[:, [1, 3]] - dh) / resize_ratio
    else:
        boxes_[:, [0, 2]] *= (width_ori/float(args.new_size[0]))
        boxes_[:, [1, 3]] *= (height_ori/float(args.new_size[1]))

    print("box coords:")
    print(boxes_)
    print('*' * 30)
    print("scores:")
    print(scores_)
    print('*' * 30)
    print("labels:")
    print(labels_)

    for i in range(len(boxes_)):
        x0, y0, x1, y1 = boxes_[i]
        plot_one_box(img_ori, [x0, y0, x1, y1], label=args.classes[labels_[i]] + ', {:.2f}%'.format(scores_[i] * 100), color=color_table[labels_[i]])
    cv2.imshow('Detection result', img_ori)
    cv2.imwrite('detection_result.jpg', img_ori)
    cv2.waitKey(0)
