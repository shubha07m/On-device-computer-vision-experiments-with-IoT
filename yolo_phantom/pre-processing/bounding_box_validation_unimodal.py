"""
Script Name: bounding_box_creation.py
License: MIT License (https://opensource.org/licenses/MIT).

Description:
This script can draw bounding boxes in an image from YOLO format
annotated .txt file and image pair. The current one uses a FLIR V2
infrared dataset as an example.

Note:
1. Make sure the source (YOLO formatted structured dataset) and this
script is in the same path.
2. Arguments to be used as per instructions received

* This script is currently designed for 15 classes as mentioned in FLIR V2 description *
Author: Shubh
Date: Jan 29, 2024
"""

import cv2
import os
import random


def load_image(image_file):
    return cv2.imread(image_file)


def parse_yolo_annotation(annotation_file):
    with open(annotation_file, 'r') as file:
        lines = file.readlines()
    annotations = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 5:
            class_id, center_x, center_y, width, height = map(float, parts)
            annotations.append((int(class_id), center_x, center_y, width, height))
    return annotations


def draw_bounding_boxes(image, annotations, label_names):
    for class_id, center_x, center_y, width, height in annotations:
        # Calculate bounding box coordinates
        x = int((center_x - width / 2) * image.shape[1])
        y = int((center_y - height / 2) * image.shape[0])
        w = int(width * image.shape[1])
        h = int(height * image.shape[0])

        # Draw bounding box
        color = (0, 255, 0)  # BGR color (green in this example)
        thickness = 2
        image = cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)

        # Add label name
        label_name = label_names[class_id]
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        text_size, _ = cv2.getTextSize(label_name, font, font_scale, font_thickness)
        text_x = x
        text_y = y - 5 if y - 5 > 5 else y + 20
        cv2.rectangle(image, (text_x, text_y - text_size[1]), (text_x + text_size[0], text_y), color, cv2.FILLED)
        cv2.putText(image, label_name, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

    return image


def main():
    thermal_ = int(input('Please enter the modality type: 1 for thermal and 0 for RGB\n'))
    datatype_ = int(input('Please enter the data type: 1 for train and 0 for val and 2 for test\n'))

    rgb_thermal = 'flirv2_thermal' if thermal_ == 1 else 'flirv2_rgb'
    data_type = 'train' if datatype_ == 1 else ('val' if datatype_ == 0 else 'test')

    # Constants for file paths
    base_path = os.path.join(os.getcwd(), 'FLIR_V2_curated_limited')
    image_path = os.path.join(base_path, rgb_thermal, data_type, 'images')

    # file_id = random.randint(1, 1000)

    file_id = random.randint(1, 10000) if datatype_ == 1 else (random.randint(1, 1000)
                                                               if datatype_ == 0 else random.randint(1, 3000))

    text_file_name = f"img{file_id}.txt"
    img_file_name = f"img{file_id}.jpg"

    print(img_file_name, text_file_name)

    text_file = os.path.join(base_path, rgb_thermal, data_type, 'labels', text_file_name)
    image_file = os.path.join(image_path, img_file_name)

    # Load the image
    image = load_image(image_file)

    # Parse YOLO annotation
    annotations = parse_yolo_annotation(text_file)

    # Define label names
    label_names = ['person', 'bicycle', 'car', 'motorcycle', 'bus',
                   'train', 'skateboard', 'truck', 'fire-Hydrant',
                   'traffic-light', 'dog', 'street-sign', 'stroller',
                   'scooter', 'other-vehicle']

    # Draw bounding boxes and labels
    image_with_boxes = draw_bounding_boxes(image, annotations, label_names)

    # Display the image with bounding boxes
    cv2.imshow('Image with Bounding Boxes', image_with_boxes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
