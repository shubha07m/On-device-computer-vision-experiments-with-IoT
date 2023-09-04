"""
Script Name: coco2yolo_conversion.py
License: MIT License (https://opensource.org/licenses/MIT).

Description:
This script convert a coco json format dataset to YOLO format.
The current one uses a FLIR V2 infrared dataset as an example.

Note:
1. Make sure the source (unzipped folder) and this script is in
the same path.
2. For testing with some small samples enter the number,
else use 0 as argument to access all samples.

Author: Shubh
Date: Sept 4, 2023
"""
import json
import os
import shutil
import time

t = time.time()

current_path = os.getcwd()
input_path = os.path.join(current_path, "FLIR_ADAS_v2")


# Creation of new folder structure #
def folder_creation(base_path):
    os.makedirs(os.path.join(base_path, "flirv2_yoloformat"), exist_ok=True)
    output_path = os.path.join(base_path, "flirv2_yoloformat")

    for img_type in ['flirv2_rgb', 'flirv2_thermal']:
        for data_type in ['train', 'val', 'test']:
            for img_lbl in ['images', 'labels']:
                os.makedirs(os.path.join(output_path, img_type, data_type, img_lbl), exist_ok=True)

    return output_path


def get_data_type(part, thermal):
    if thermal:
        return {
            'train': 'images_thermal_train',
            'val': 'images_thermal_val',
            'test': 'video_thermal_test'
        }[part]
    else:
        return {
            'train': 'images_rgb_train',
            'val': 'images_rgb_val',
            'test': 'video_rgb_test'
        }[part]


def save_images_folder(thermal, data_part):
    file_names = []
    database = get_data_type(data_part, thermal)
    count_img = 0
    start = os.path.join(input_path, database, 'data')

    for filename in os.listdir(start):
        source = os.path.join(start, filename)
        if thermal:
            destination = f"{new_yolodata_path}/flirv2_thermal/{data_part}/images/img{count_img}.jpg"
        else:
            destination = f"{new_yolodata_path}/flirv2_rgb/{data_part}/images/img{count_img}.jpg"

        shutil.copy(source, destination)
        file_names.append(filename)
        count_img += 1
        if count_img == count_max:
            break
    return file_names


def get_coco_jsonfile(thermal, data_type):
    database = get_data_type(data_type, thermal)
    with open(os.path.join(input_path, database, 'coco.json')) as f:
        cocodata = json.load(f)
    return cocodata


def get_img_ann(image_id, thermal, data_type):
    data = get_coco_jsonfile(thermal, data_type)
    img_ann = []
    isFound = False
    for ann in data['annotations']:
        if ann['image_id'] == image_id:
            img_ann.append(ann)
            isFound = True
    if isFound:
        return img_ann
    else:
        return None


def get_img(filename, thermal, data_type):
    data = get_coco_jsonfile(thermal, data_type)
    for img in data['images']:
        if img['file_name'] == ('data/' + filename):
            return img


def save_annotation_folder(thermal, data_type):
    file_names = save_images_folder(thermal, data_type)
    count = 0
    for filename in file_names:
        # Extracting image
        img = get_img(filename, thermal, data_type)
        if img is None:
            print(f"Warning: {filename} returned None")
            continue

        img_id = img['id']
        img_w = img['width']
        img_h = img['height']

        # Get Annotations for this image
        img_ann = get_img_ann(img_id, thermal, data_type)

        if img_ann:
            folder = 'flirv2_thermal' if thermal else 'flirv2_rgb'
        # Opening file for current image
            file_object = open(f"{new_yolodata_path}/{folder}/{data_type}/labels/img{count}.txt", "a")

            for ann in img_ann:
                current_category = ann['category_id'] - 1  # As yolo format labels start from 0
                current_bbox = ann['bbox']
                x = current_bbox[0]
                y = current_bbox[1]
                w = current_bbox[2]
                h = current_bbox[3]

                # Finding midpoints
                x_centre = (x + (x + w)) / 2
                y_centre = (y + (y + h)) / 2

                # Normalization
                x_centre = x_centre / img_w
                y_centre = y_centre / img_h
                w = w / img_w
                h = h / img_h

                # Limiting upto fix number of decimal places
                x_centre = format(x_centre, '.6f')
                y_centre = format(y_centre, '.6f')
                w = format(w, '.6f')
                h = format(h, '.6f')

                # Writing current object
                file_object.write(f"{current_category} {x_centre} {y_centre} {w} {h}\n")

            file_object.close()

        count += 1  # This should be outside the if img_ann block.
        if count == count_max:
            break


if __name__ == '__main__':
    current_path = os.getcwd()
    new_yolodata_path = folder_creation(current_path)

    # For testing only#
    print('Please enter the sample per folder else enter 0 for all:\n')
    testing = int(input())
    if testing:
        count_max = testing
    else:
        count_max = 50000

    for thermal in [0, 1]:
        for data_type in ['train', 'val', 'test']:
            save_annotation_folder(thermal, data_type)

print(time.time() - t)
