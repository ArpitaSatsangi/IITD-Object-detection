# -*- coding: utf-8 -*-
"""VIOLA JONES mAP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11dnAV4g9BNRZl_gXOQnpDY3ATW02l_uV

WITHOUT FALSE NEGATIVE
"""

import torch
import cv2
import torchvision
from torchvision.transforms import ToTensor
from PIL import Image, ImageDraw
import numpy as np
from collections import defaultdict
from sklearn.metrics import average_precision_score


# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load PASCAL VOC dataset
transform = torchvision.transforms.Compose([
    torchvision.transforms.Resize((24, 24)),
    torchvision.transforms.Grayscale(),
    torchvision.transforms.ToTensor()
])

def detect_faces(image):
    # Convert PIL Image to OpenCV format
    cv_image = np.array(image)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    # Detect faces using Viola-Jones algorithm
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Convert bounding boxes to (x, y, w, h) format
    face_boxes = []
    for (x, y, w, h) in faces:
        face_boxes.append((x, y, x + w, y + h))

    return face_boxes

def calculate_map(dataset):
    true_positives = defaultdict(list)
    false_positives = defaultdict(list)

    for i in range(len(dataset)):
        image, target = dataset.__getitem__(i)
        image = image.convert('RGB')
        face_boxes = detect_faces(image)

        # Get ground truth bounding boxes
        gt_boxes = []
        if isinstance(target['annotation']['object'], list):
            objects = target['annotation']['object']
        else:
            objects = [target['annotation']['object']]
        for obj in objects:
            bbox = obj['bndbox']
            x1, y1, x2, y2 = int(bbox['xmin']), int(bbox['ymin']), int(bbox['xmax']), int(bbox['ymax'])
            gt_boxes.append((x1, y1, x2, y2))

        # Match predicted boxes with ground truth boxes
        matched_gt = set()
        for pred_box in face_boxes:
            pred_box = np.array(pred_box)
            ious = []
            for gt_box in gt_boxes:
                gt_box = np.array(gt_box)
                iou = calculate_iou(pred_box, gt_box)
                ious.append(iou)
            max_iou = np.max(ious)
            if max_iou >= 0.5:
                idx = np.argmax(ious)
                if idx not in matched_gt:
                    true_positives[i].append(1)
                    false_positives[i].append(0)
                    matched_gt.add(idx)
                else:
                    true_positives[i].append(0)
                    false_positives[i].append(1)
            else:
                true_positives[i].append(0)
                false_positives[i].append(1)

        # Handle unmatched ground truth boxes
        for j, gt_box in enumerate(gt_boxes):
            if j not in matched_gt:
                true_positives[i].append(0)
                false_positives[i].append(1)

    # Calculate precision and recall for each image
    precisions = []
    recalls = []
    for image_idx, tp_list in true_positives.items():
        fp_list = false_positives[image_idx]
        tp_cumsum = np.cumsum(tp_list)
        fp_cumsum = np.cumsum(fp_list)
        recall = tp_cumsum / len(tp_list)
        precision = tp_cumsum / (tp_cumsum + fp_cumsum)
        precisions.append(precision)
        recalls.append(recall)

    # Calculate Average Precision (AP) for each class
    ap = average_precision_score(np.concatenate(list(true_positives.values())), np.concatenate(list(false_positives.values())))

    # Calculate Mean Average Precision (mAP)
    mAP = np.mean(ap)

    return mAP


def calculate_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2

    # Calculate intersection area
    intersection_width = max(0, min(x2, x4) - max(x1, x3))
    intersection_height = max(0, min(y2, y4) - max(y1, y3))
    intersection_area = intersection_width * intersection_height

    # Calculate union area
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x4 - x3) * (y4 - y3)
    union_area = box1_area + box2_area - intersection_area

    # Calculate IoU
    iou = intersection_area / union_area

    return iou


def main():
    # Load PASCAL VOC dataset
    dataset = torchvision.datasets.VOCDetection(root='./VOCdevkit', year='2012', image_set='trainval',
                                                download=True)

    mAP = calculate_map(dataset)
    print("Mean Average Precision (mAP):", mAP)


if __name__ == '__main__':
    main()

"""WITH  FALSE NEGATIVE"""

import torch
import cv2
import torchvision
from torchvision.transforms import ToTensor
from PIL import Image, ImageDraw
import numpy as np
from collections import defaultdict
from sklearn.metrics import average_precision_score


# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load PASCAL VOC dataset
transform = torchvision.transforms.Compose([
    torchvision.transforms.Resize((24, 24)),
    torchvision.transforms.Grayscale(),
    torchvision.transforms.ToTensor()
])

def detect_faces(image):
    # Convert PIL Image to OpenCV format
    cv_image = np.array(image)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    # Detect faces using Viola-Jones algorithm
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Convert bounding boxes to (x, y, w, h) format
    face_boxes = []
    for (x, y, w, h) in faces:
        face_boxes.append((x, y, x + w, y + h))

    return face_boxes

def calculate_map(dataset):
    true_positives = defaultdict(list)
    false_positives = defaultdict(list)
    false_negatives = defaultdict(list)

    for i in range(len(dataset)):
        image, target = dataset.__getitem__(i)
        image = image.convert('RGB')
        face_boxes = detect_faces(image)

        # Get ground truth bounding boxes
        gt_boxes = []
        if isinstance(target['annotation']['object'], list):
            objects = target['annotation']['object']
        else:
            objects = [target['annotation']['object']]
        for obj in objects:
            bbox = obj['bndbox']
            x1, y1, x2, y2 = int(bbox['xmin']), int(bbox['ymin']), int(bbox['xmax']), int(bbox['ymax'])
            gt_boxes.append((x1, y1, x2, y2))

        # Match predicted boxes with ground truth boxes
        matched_gt = set()
        for pred_box in face_boxes:
            pred_box = np.array(pred_box)
            ious = []
            for gt_box in gt_boxes:
                gt_box = np.array(gt_box)
                iou = calculate_iou(pred_box, gt_box)
                ious.append(iou)
            max_iou = np.max(ious)
            if max_iou >= 0.5:
                idx = np.argmax(ious)
                if idx not in matched_gt:
                    true_positives[i].append(1)
                    false_positives[i].append(0)
                    matched_gt.add(idx)
                else:
                    true_positives[i].append(0)
                    false_positives[i].append(1)
            else:
                true_positives[i].append(0)
                false_positives[i].append(1)

        # Handle unmatched ground truth boxes
        for j, gt_box in enumerate(gt_boxes):
            if j not in matched_gt:
                true_positives[i].append(0)
                false_positives[i].append(0)  # Additional predicted face, counted as false positive
                false_negatives[i].append(1)  # Unmatched ground truth face, counted as false negative

    # Calculate precision and recall for each image
    precisions = []
    recalls = []
    f1_scores = []
    for image_idx, tp_list in true_positives.items():
        fp_list = false_positives[image_idx]
        fn_list = false_negatives[image_idx]
        tp_cumsum = np.cumsum(tp_list)
        fp_cumsum = np.cumsum(fp_list)
        fn_cumsum = np.cumsum(fn_list)

        # Extend the length of fn_cumsum with zeros
        if len(tp_cumsum) > len(fn_cumsum):
            fn_cumsum = np.concatenate((fn_cumsum, np.zeros(len(tp_cumsum) - len(fn_cumsum)))),

        recall = tp_cumsum / (tp_cumsum + fn_cumsum)
        precision = tp_cumsum / (tp_cumsum + fp_cumsum)
        f1_score = 2 * (precision * recall) / (precision + recall)
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1_score)

    # Calculate Average Precision (AP) for each class
    ap = average_precision_score(np.concatenate(list(true_positives.values())), np.concatenate(list(false_positives.values())))

    # Calculate Mean Average Precision (mAP)
    mAP = np.mean(ap)

    return mAP, precisions, recalls, f1_scores



def calculate_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2

    # Calculate intersection area
    intersection_width = max(0, min(x2, x4) - max(x1, x3))
    intersection_height = max(0, min(y2, y4) - max(y1, y3))
    intersection_area = intersection_width * intersection_height

    # Calculate union area
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x4 - x3) * (y4 - y3)
    union_area = box1_area + box2_area - intersection_area

    # Calculate IoU
    iou = intersection_area / union_area

    return iou


def main():
    # Load PASCAL VOC dataset
    dataset = torchvision.datasets.VOCDetection(root='./VOCdevkit', year='2012', image_set='trainval',
                                                download=True)

    mAP, precisions, recalls, f1_scores = calculate_map(dataset)
    print("Mean Average Precision (mAP):", mAP)
    #print("Recalls:", recalls)


if __name__ == '__main__':
    main()