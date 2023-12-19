# Object Detection: Viola-Jones and Faster R-CNN on PASCAL VOC 2007

## Introduction:
The project aims to achieve comprehensive object detection on the PASCAL VOC 2007 dataset through the integration of two distinct methodologies: Viola-Jones, a classical machine learning algorithm, and Faster R-CNN, a state-of-the-art deep learning model.

## Viola-Jones: Classical Object Detection
### Overview:
The Viola-Jones algorithm is initially employed for its efficiency in face detection, leveraging Haar-like features and cascade classifiers within the OpenCV library.

### Implementation:
The project begins by loading the PASCAL VOC 2007 dataset, preparing it for subsequent processing.
The Viola-Jones algorithm is applied to detect frontal faces within the dataset, utilizing a pre-trained cascade classifier.
Bounding boxes are generated around detected faces, showcasing the algorithm's capability in localized object detection.

### Visualization:
The resulting images display annotated bounding boxes around detected faces, providing a visual representation of the Viola-Jones output.


## Faster R-CNN: Deep Learning for Object Detection
### Overview:
The project seamlessly transitions to Faster R-CNN, a deep learning-based model renowned for its accuracy in general object detection.

### Implementation:
A pre-trained Faster R-CNN model is incorporated from the torchvision library, tailored for the nuances of the PASCAL VOC 2007 dataset.
The model is applied to identify objects within the images, producing bounding boxes, associated labels, and confidence scores.
### Evaluation:
The performance of Faster R-CNN is assessed through the visualization of bounding boxes and their alignment with ground truth annotations.


## Comparison and Fusion:
### Side-by-Side Analysis:
The project facilitates a direct comparison between the Viola-Jones and Faster R-CNN methodologies by saving and visualizing individual images with annotated bounding boxes from both approaches.
The side-by-side analysis provides insights into the strengths and limitations of each method.
### Horizontal Stacking:
For a holistic perspective, the results from Viola-Jones and Faster R-CNN are horizontally stacked, creating a consolidated visual representation of their respective outputs.
This visual fusion aids in the nuanced examination of how these methodologies complement or differ from each other.

![image_159](https://github.com/ArpitaSatsangi/IITD-Object-detection/assets/107709451/aeaa9951-67bb-43c9-a6b1-b8b2a47e87e9)

![image_1414](https://github.com/ArpitaSatsangi/IITD-Object-detection/assets/107709451/9a5afc3f-5105-43ff-bc41-67837e0241de)

![image_2622](https://github.com/ArpitaSatsangi/IITD-Object-detection/assets/107709451/3c12b185-d7ad-4cbd-b95b-f649f244ca90)

![image_245](https://github.com/ArpitaSatsangi/IITD-Object-detection/assets/107709451/8764039e-1c77-47f9-ba19-968ed0052894)


## Conclusion:
In conclusion, "Unified Vision" underscores the project's overarching theme of harmonizing classical and modern approaches to object detection. By seamlessly integrating Viola-Jones for face detection and Faster R-CNN for general object detection on the PASCAL VOC 2007 dataset, the project provides a comprehensive exploration of methodologies, emphasizing the potential synergies in leveraging both machine learning and deep learning techniques for robust object detection.

