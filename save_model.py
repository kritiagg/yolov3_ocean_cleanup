# coding: utf-8

from __future__ import division, print_function

import tensorflow as tf
import numpy as np
import argparse

from utils.misc_utils import parse_anchors, read_class_names
from utils.nms_utils import gpu_nms

from model import yolov3

parser = argparse.ArgumentParser(description="YOLO-V3 test single image test procedure.")
parser.add_argument("--anchor_path", type=str, default="./data/yolo_anchors.txt",
                    help="The path of the anchor txt file.")
parser.add_argument("--new_size", nargs='*', type=int, default=[416, 416],
                    help="Resize the input image with `new_size`, size format: [width, height]")
parser.add_argument("--class_name_path", type=str, default="./data/coco.names",
                    help="The path of the class names.")
parser.add_argument("--restore_path", type=str, default="./data/darknet_weights/yolov3.ckpt",
                    help="The path of the weights to restore.")
args = parser.parse_args()

args.anchors = parse_anchors(args.anchor_path)
args.classes = read_class_names(args.class_name_path)
args.num_class = len(args.classes)


with tf.Session() as sess:
    # Input tensor placeholder
    input_data = tf.placeholder(tf.float32, [1, args.new_size[1], args.new_size[0], 3], name='input_data')
    
    # Create model & retrieve temp-result tensors
    yolo_model = yolov3(args.num_class, args.anchors)
    with tf.variable_scope('yolov3'):
        pred_feature_maps = yolo_model.forward(input_data, False)

    pred_boxes, pred_confs, pred_probs = yolo_model.predict(pred_feature_maps)
    pred_scores = pred_confs * pred_probs

    # Gets final result tensors through processing tensors returned from model with non-max-supression
    boxes, scores, labels = gpu_nms(pred_boxes, pred_scores, args.num_class, max_boxes=200, score_thresh=0.3, nms_thresh=0.45)

    # Load model into current session & therefore graph
    saver = tf.train.Saver()
    saver.restore(sess, args.restore_path)

    inputs = {
        "picture": input_data,
    }

    outputs = {
        "boxes": boxes,
        "scores": scores,
        "labels": labels
    }

    tf.saved_model.simple_save(
        sess, './saved_model/', inputs, outputs
    )

    print("done")