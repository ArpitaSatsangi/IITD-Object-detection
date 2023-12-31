# -*- coding: utf-8 -*-
"""00 save images.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cMO9HZ6K64op_HhV0xIpW9JVl8A4oTm2
"""

!pip install mean_average_precision
import mean_average_precision

import os
import torch
import torchvision
from torchvision.transforms import functional as F
from PIL import Image, ImageDraw
import numpy as np
from mean_average_precision import MetricBuilder

#original

def save_images_from_dataset(dataset, save_folder):
    # Create the save folder
    os.makedirs(save_folder, exist_ok=True)

    for i in range(len(dataset)):
        image, _ = dataset.__getitem__(i)
        image = image.convert('RGB')

        # Save the image
        image_path = os.path.join(save_folder, f'image_{i}.jpg')
        image.save(image_path)

        # Print progress
        print(f'Saved image {i+1}/{len(dataset)}')

if __name__ == '__main__':
    # Load PASCAL VOC dataset
    dataset = torchvision.datasets.VOCDetection(root='./VOCdevkit', year='2007', image_set='trainval', download=True)

    # Specify the save folder
    save_folder = 'original_saved_images'

    # Save images from the dataset
    save_images_from_dataset(dataset, save_folder)

#faster rcnn




# Load pre-trained Faster R-CNN model
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Load PASCAL VOC dataset
dataset = torchvision.datasets.VOCDetection(root='./VOCdevkit', year='2007', image_set='trainval', download=True)


def detect_objects(image):
    # Transform image to tensor
    image_tensor = F.to_tensor(image)
    image_tensor = torch.unsqueeze(image_tensor, 0)

    # Run object detection
    with torch.no_grad():
        predictions = model(image_tensor)

    boxes = predictions[0]['boxes'].tolist()
    labels = predictions[0]['labels'].tolist()
    scores = predictions[0]['scores'].tolist()

    return boxes, labels, scores


def get_ground_truth(index):
    _, target = dataset.__getitem__(index)
    objects = target['annotation']['object']
    gt_boxes = []
    for obj in objects:
        bbox = obj['bndbox']
        xmin = int(bbox['xmin'])
        ymin = int(bbox['ymin'])
        xmax = int(bbox['xmax'])
        ymax = int(bbox['ymax'])
        gt_boxes.append([xmin, ymin, xmax, ymax])
    return np.array(gt_boxes)


def get_predicted_boxes(image, gt_boxes, confidence_threshold=0.5):
    boxes, labels, scores = detect_objects(image)
    predicted_boxes = []
    for box, label, score in zip(boxes, labels, scores):
        if score > confidence_threshold:
            x1, y1, x2, y2 = box
            if has_matching_gt_box(x1, y1, x2, y2, gt_boxes):
                predicted_boxes.append([x1, y1, x2, y2, label, score])
    return np.array(predicted_boxes)


def has_matching_gt_box(x1, y1, x2, y2, gt_boxes, iou_threshold=0.5):
    for gt_box in gt_boxes:
        iou = compute_iou(x1, y1, x2, y2, gt_box)
        if iou >= iou_threshold:
            return True
    return False


def compute_iou(x1, y1, x2, y2, box):
    x_intersection = max(0, min(x2, box[2]) - max(x1, box[0]))
    y_intersection = max(0, min(y2, box[3]) - max(y1, box[1]))
    intersection_area = x_intersection * y_intersection

    box_area = (box[2] - box[0]) * (box[3] - box[1])
    predicted_box_area = (x2 - x1) * (y2 - y1)
    union_area = box_area + predicted_box_area - intersection_area

    iou = intersection_area / union_area
    return iou

def main():
    # Create a folder to save the images
    save_folder = 'faster_rcnn_saved_images'
    os.makedirs(save_folder, exist_ok=True)

    for i in range(len(dataset)):
        image, _ = dataset.__getitem__(i)
        image = image.convert('RGB')

        gt_boxes = get_ground_truth(i)
        pred_boxes = get_predicted_boxes(image, gt_boxes)

        # Draw ground truth bounding boxes
        draw = ImageDraw.Draw(image)
        for box in gt_boxes:
            x1, y1, x2, y2 = box
            draw.rectangle([(x1, y1), (x2, y2)], outline='green', width=2)

        # Draw predicted bounding boxes
        for box in pred_boxes:
            x1, y1, x2, y2, _, _ = box[:6]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            draw.rectangle([(x1, y1), (x2, y2)], outline='red', width=2)

        # Save the image
        image_path = os.path.join(save_folder, f'image_{i}.jpg')
        image.save(image_path)

        print(f'Saved image {i+1}/{len(dataset)}')


        # Convert ground truth and predicted boxes to numpy arrays
        #gt = get_ground_truth(i)
        #preds = get_predicted_boxes(image, gt)

        # Create metric_fn
        #metric_fn = MetricBuilder.build_evaluation_metric("map_2d", async_mode=True, num_classes=1)

        # Add samples to evaluation
        #metric_fn.add(preds, gt)

        # Compute PASCAL VOC metric
        #print(f"VOC PASCAL mAP: {metric_fn.value(iou_thresholds=0.3, recall_thresholds=np.arange(0., 1.1, 0.1))['mAP']}")

        # Compute PASCAL VOC metric at all points
        #print(f"VOC PASCAL mAP in all points: {metric_fn.value(iou_thresholds=0.3)['mAP']}")

        # Compute COCO metric
        #print(f"COCO mAP: {metric_fn.value(iou_thresholds=np.arange(0.5, 1.0, 0.05), recall_thresholds=np.arange(0., 1.01, 0.01), mpolicy='soft')['mAP']}")


if __name__ == '__main__':
    main()

#viola jones
import torch
import cv2
import torchvision
from torchvision.transforms import ToTensor
from PIL import Image, ImageDraw
import numpy as np


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

def main():
    # Create output directory if it doesn't exist
    output_dir = 'viola_jones_saved_images'
    os.makedirs(output_dir, exist_ok=True)

    # Load PASCAL VOC dataset
    dataset = torchvision.datasets.VOCDetection(root='./VOCdevkit', year='2007', image_set='trainval', download=True)

    for i in range(len(dataset)):
        image, target = dataset.__getitem__(i)
        image = image.convert('RGB')
        face_boxes = detect_faces(image)

        # Draw bounding boxes and labels on the image
        draw = ImageDraw.Draw(image)
        if isinstance(target['annotation']['object'], list):
            objects = target['annotation']['object']
        else:
            objects = [target['annotation']['object']]

        # Draw ground truth bounding box
        for obj in objects:
            name = obj['name']
            bbox = obj['bndbox']
            x1, y1, x2, y2 = int(bbox['xmin']), int(bbox['ymin']), int(bbox['xmax']), int(bbox['ymax'])
            draw.rectangle([(x1, y1), (x2, y2)], outline='green', width=2)
            draw.text((x1, y1 - 10), name, fill='green')

        # Draw detected face bounding boxes
        for (x, y, x2, y2) in face_boxes:
            draw.rectangle([(x, y), (x2, y2)], outline='red', width=2)

        # Save the image
        image_path = os.path.join(output_dir, f'image_{i}.jpg')
        image.save(image_path)

        print(f'Saved image {i+1}/{len(dataset)}')

if __name__ == '__main__':
    main()

#saving images
import cv2
import os

def save_horizontal_stack(original_images_folder, viola_jones_folder, faster_rcnn_folder, output_folder):
    # Get the list of filenames in the original images folder
    original_images = os.listdir(original_images_folder)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Load, resize, and save the horizontal stack of images
    count = 0  # Counter for limiting the processing to 2600 images
    for filename in original_images:
        if count >= 2600:
            break

        original_image_path = os.path.join(original_images_folder, filename)
        viola_jones_path = os.path.join(viola_jones_folder, filename)
        faster_rcnn_path = os.path.join(faster_rcnn_folder, filename)

        # Check if the Faster R-CNN image exists
        if not os.path.exists(faster_rcnn_path):
            continue

        original_image = cv2.imread(original_image_path)
        viola_jones_image = cv2.imread(viola_jones_path)
        faster_rcnn_image = cv2.imread(faster_rcnn_path)

        # Resize the images to the same width
        width = 300  # Adjust this value according to your preference
        original_image = cv2.resize(original_image, (width, original_image.shape[0]))
        viola_jones_image = cv2.resize(viola_jones_image, (width, viola_jones_image.shape[0]))
        faster_rcnn_image = cv2.resize(faster_rcnn_image, (width, faster_rcnn_image.shape[0]))

        # Create a horizontal stack of the three images using numpy.hstack
        horizontal_stack = np.hstack((original_image, viola_jones_image, faster_rcnn_image))

        # Save the horizontal stack image
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, horizontal_stack)

        count += 1

    print("Horizontal stacks saved successfully!")

# Provide the paths to the folders containing the original images, Viola-Jones outputs, and Faster R-CNN outputs
original_images_folder = "/content/original_saved_images"
viola_jones_folder = "/content/viola_jones_saved_images"
faster_rcnn_folder = "/content/faster_rcnn_saved_images"

# Provide the output folder path for the horizontal stacks
output_folder = "/content/combination"

# Save the horizontal stacks of images
save_horizontal_stack(original_images_folder, viola_jones_folder, faster_rcnn_folder, output_folder)

from google.colab import drive
import shutil

def save_to_drive(source_folder, destination_folder_id):
    # Mount Google Drive
    drive.mount('/content/drive')

    # Copy the source folder to the destination folder in Google Drive
    destination_folder_path = "/content/drive/MyDrive/" + destination_folder_id
    shutil.copytree(source_folder, destination_folder_path)

# Provide the path to the folder you want to save to Google Drive
source_folder = "/content/combination"

# Provide the Google Drive folder ID where you want to save the folder
destination_folder_id = "1ZSTGByF7ZLWyq5H3k977AMd50076fUe2"

# Save the "combination" folder to Google Drive
save_to_drive(source_folder, destination_folder_id)