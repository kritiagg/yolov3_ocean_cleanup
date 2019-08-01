#  YOLOv3_TensorFlow For ocean cleanup

### What are we trying to do?

We aim to become able to detect plastics in water anywhere. This repo is directed at providing context on what is available and what we aim to achieve.

### Datasets:

River cam detection: images and labels available, we have a trained model based on Faster RCNN architecture.
River drone detection: images and labels available
Great Pacific Garbage Patch drone detection: images available, labels are work in progress, Find the link to labelling here
Great Pacific Garbage Patch ship detection: images available, labels are work in progress

#### Why YOLOv3? 
We are trying to solve the following problems:
1. Better model for existing data

We developed a model that predict plastic in a river from a camera mounted on a bridge, which achieves 68% mAP. The data and the model can be found in the rivercam folder for retraining and improvement. Images can be processed by the model using the image_processing folder.

So far we have been working with the TFODAPI, of which a tutorial can be found here. While very useful, we expect that there are limitations regarding this and that we eventually need to move towards a more custom solution. Here are the starting points to other models

This is list of tf models <good for starting point>: https://github.com/tensorflow/models/tree/master/research/object_detection
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
These are state of the art models in object detection which have codes available. https://paperswithcode.com/sota/object-detection-on-coco
Objects as points : 2019 paper which has a tensorflow implementation and has much higher mAP than Faster RCNN. https://paperswithcode.com/paper/objects-as-points
The aim is to find a higher precision model to work on our problem.

#### With YOLOv3 we were able to improve the mAP to 70% for the camera on bridge images. 
 

#### 2. Light-weight models suitable for on-edge processing

We have some scenarios (Ghost net hunting!) in mind where we would like to send out a drone while on an ocean expedition, where we would like to retrieve feedback from the drone directly, or where we want the drone to be able to stay with an object for longer to collect more data on it. For this, we should aim for a model that is light-weight, but that does not miss anything. In other words, high-recall, low-precision. Where the rivercam model is based on Faster R-CNN, an SSD, YOLO or Tensorflow-lite model would probably be more suitable.

Starting points:

YOLOv3 seems like a very good candidate as it is very fast and light.
 

#### 3. Find the right model training data

Different models for different datasets:
While detecting plastic with cameras mounted on bridges are a huge step in the right direction, it still only allows us to detect plastic in only a small percentage of water areas. Most river cross-sections don't have bridges, and most ocean cross-sections certainly don't. In short, we have 3 different types of datasets:

River drone detection: images and labels available
Great Pacific Garbage Patch drone detection: images available, labels are work in progress, Find the link to labelling here
Great Pacific Garbage Patch ship detection: images available, labels are work in progress

Combining the datasets and experimenting
In addition from testing whether we can train a reliable AI model on the dataset of each task specifically, we are also interested in learning whether we can enrich each other's models by combining data sets. For example, the river drone and river cam data seem fairly similar, can we combine those? For ocean drones we only have little data, can we also first train on river footage and then on ocean footage to enable accurate prediction?

Adding other parameters to training like height of the drone etc.
It is important to know that new cameras are in development. Among many other things, these cameras will have much higher image resolution, and will be able to determine distance from the water automatically. Two questions arise here. What impact does this have on suitability of our current learning structure? Should we incorporate the height in training as metadata, and how?


## Here is the documentation related to the base YOLOv3.

### 1. Introduction

This is my implementation of [YOLOv3](https://pjreddie.com/media/files/papers/YOLOv3.pdf) in pure TensorFlow. It contains the full pipeline of training and evaluation on your own dataset. The key features of this repo are:

- Efficient tf.data pipeline
- Weights converter (converting pretrained darknet weights on COCO dataset to TensorFlow checkpoint.)
- Extremely fast GPU non maximum supression.
- Full training and evaluation pipeline.
- Kmeans algorithm to select prior anchor boxes.

### 2. Requirements

Python version: 2 or 3

Packages:

- tensorflow >= 1.8.0 (theoretically any version that supports tf.data is ok)
- opencv-python
- tqdm

### 3. Weights convertion

The pretrained darknet weights file can be downloaded [here](https://pjreddie.com/media/files/yolov3.weights). Place this weights file under directory `./data/darknet_weights/` and then run:

```shell
python convert_weight.py
```

Then the converted TensorFlow checkpoint file will be saved to `./data/darknet_weights/` directory.

You can also download the converted TensorFlow checkpoint file by me via [[Google Drive link](https://drive.google.com/drive/folders/1mXbNgNxyXPi7JNsnBaxEv1-nWr7SVoQt?usp=sharing)] or [[Github Release](https://github.com/wizyoung/YOLOv3_TensorFlow/releases/)] and then place it to the same directory.

### 4. Running demos

There are some demo images and videos under the `./data/demo_data/`. You can run the demo by:

Single image test demo:

```shell
python test_single_image.py ./data/demo_data/messi.jpg
```

Video test demo:

```shell
python video_test.py ./data/demo_data/video.mp4
```

Some results:

![](https://github.com/wizyoung/YOLOv3_TensorFlow/blob/master/data/demo_data/results/dog.jpg?raw=true)

![](https://github.com/wizyoung/YOLOv3_TensorFlow/blob/master/data/demo_data/results/messi.jpg?raw=true)

![](https://github.com/wizyoung/YOLOv3_TensorFlow/blob/master/data/demo_data/results/kite.jpg?raw=true)

Compare the kite detection results with TensorFlow's offical API result [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/img/kites_detections_output.jpg).

(The kite detection result is under input image resolution 1344x896)

### 5. Inference speed

How fast is the inference speed? With images scaled to 416*416:


| Backbone              |   GPU    | Time(ms) |
| :-------------------- | :------: | :------: |
| Darknet-53 (paper)    | Titan X  |    29    |
| Darknet-53 (my impl.) | Titan XP |   ~23    |

why is it so fast? Check the ImageNet classification result comparision from the paper:

![](https://github.com/wizyoung/YOLOv3_TensorFlow/blob/master/docs/backbone.png?raw=true)

### 6. Model architecture

For better understanding of the model architecture, you can refer to the following picture. With great thanks to [Levio](https://blog.csdn.net/leviopku/article/details/82660381) for your excellent work!

![](https://github.com/wizyoung/YOLOv3_TensorFlow/blob/master/docs/yolo_v3_architecture.png?raw=true)

### 7. Training

#### 7.1 Data preparation 

(1) annotation file

Generate `train.txt/val.txt/test.txt` files under `./data/my_data/` directory. One line for one image, in the format like `image_index image_absolute_path img_width img_height box_1 box_2 ... box_n`. Box_x format: `label_index x_min y_min x_max y_max`. (The origin of coordinates is at the left top corner, left top => (xmin, ymin), right bottom => (xmax, ymax).) `image_index` is the line index which starts from zero. `label_index` is in range [0, class_num - 1].

For example:

```
0 xxx/xxx/a.jpg 1920 1080 0 453 369 473 391 1 588 245 608 268
1 xxx/xxx/b.jpg 1920 1080 1 466 403 485 422 2 793 300 809 320
...
```

Since so many users report to use tools like LabelImg to generate xml format annotations, I add one demo script on VOC dataset to do the convertion. Check the `misc/parse_voc_xml.py` file for more details.

(2)  class_names file:

Generate the `data.names` file under `./data/my_data/` directory. Each line represents a class name.

For example:

```
bird
person
bike
...
```

The COCO dataset class names file is placed at `./data/coco.names`.

(3) prior anchor file:

Using the kmeans algorithm to get the prior anchors:

```
python get_kmeans.py
```

Then you will get 9 anchors and the average IoU. Save the anchors to a txt file.

The COCO dataset anchors offered by YOLO's author is placed at `./data/yolo_anchors.txt`, you can use that one too.

The yolo anchors computed by the kmeans script is on the resized image scale.  The default resize method is the letterbox resize, i.e., keep the original aspect ratio in the resized image.

#### 7.2 Training

Using `train.py`. The hyper-parameters and the corresponding annotations can be found in `args.py`:

```shell
CUDA_VISIBLE_DEVICES=GPU_ID python train.py
```

Check the `args.py` for more details. You should set the parameters yourself in your own specific task.

### 8. Evaluation

Using `eval.py` to evaluate the validation or test dataset. The parameters are as following:

```shell
$ python eval.py -h
usage: eval.py [-h] [--eval_file EVAL_FILE] 
               [--restore_path RESTORE_PATH]
               [--anchor_path ANCHOR_PATH] 
               [--class_name_path CLASS_NAME_PATH]
               [--batch_size BATCH_SIZE]
               [--img_size [IMG_SIZE [IMG_SIZE ...]]]
               [--num_threads NUM_THREADS]
               [--prefetech_buffer PREFETECH_BUFFER]
               [--nms_threshold NMS_THRESHOLD]
               [--score_threshold SCORE_THRESHOLD] 
               [--nms_topk NMS_TOPK]
```

Check the `eval.py` for more details. You should set the parameters yourself. 

You will get the loss, recall, precision, average precision and mAP metrics results.

For higher mAP, you should set score_threshold to a small number.

### 9. Some tricks

Here are some training tricks in my experiment:

(1) Apply the two-stage training strategy or the one-stage training strategy:

Two-stage training:

First stage: Restore `darknet53_body` part weights from COCO checkpoints, train the `yolov3_head` with big learning rate like 1e-3 until the loss reaches to a low level.

Second stage: Restore the weights from the first stage, then train the whole model with small learning rate like 1e-4 or smaller. At this stage remember to restore the optimizer parameters if you use optimizers like adam.

One-stage training:

Just restore the whole weight file except the last three convolution layers (Conv_6, Conv_14, Conv_22). In this condition, be careful about the possible nan loss value.

(2) I've included many useful training strategies in `args.py`:

- Cosine decay of lr (SGDR)
- Multi-scale training
- Label smoothing
- Mix up data augmentation
- Focal loss

These are all good strategies but it does **not** mean they will definitely improve the performance. You should choose the appropriate strategies for your own task.

This [paper](https://arxiv.org/abs/1902.04103) from gluon-cv has proved that data augmentation is critical to YOLO v3, which is completely in consistent with my own experiments. Some data augmentation strategies that seems reasonable may lead to poor performance. For example, after introducing random color jittering, the mAP on my own dataset drops heavily. Thus I hope  you pay extra attention to the data augmentation.

(4) Loss nan? Setting a bigger warm_up_epoch number or smaller learning rate and try several more times. If you fine-tune the whole model, using adam may cause nan value sometimes. You can try choosing momentum optimizer.

### 10. Fine-tune on VOC dataset

I did a quick train on the VOC dataset. The params I used in my experiments are included under `misc/experiments_on_voc/` folder for your reference. The train dataset is the VOC 2007 + 2012 trainval set, and the test dataset is the VOC 2007 test set.

Finally with the 416\*416 input image, I got a 87.54% test mAP (not using the 07 metric). No hard-try fine-tuning. You should get the similar or better results.

My pretrained weights on VOC dataset can be downloaded [here](https://drive.google.com/drive/folders/1ICKcJPozQOVRQnE1_vMn90nr7dejg0yW?usp=sharing).

### 11. TODO

[ ] Multi-GPUs with sync batch norm. 

[ ] Maybe tf 2.0 ?

-------

### Credits:

I referred to many fantastic repos during the implementation:

[YunYang1994/tensorflow-yolov3](https://github.com/YunYang1994/tensorflow-yolov3)

[qqwweee/keras-yolo3](https://github.com/qqwweee/keras-yolo3)

[eriklindernoren/PyTorch-YOLOv3](https://github.com/eriklindernoren/PyTorch-YOLOv3)

[pjreddie/darknet](https://github.com/pjreddie/darknet)

[dmlc/gluon-cv](https://github.com/dmlc/gluon-cv/tree/master/scripts/detection/yolo)

