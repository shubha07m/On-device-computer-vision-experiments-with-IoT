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

3. This script can handle multiple types of missing annotations issues.

* This script can now handle wrongly annotated class ids and also limited class choices *

Author: Shubh
Date: Jan 29, 2024
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
    os.makedirs(os.path.join(base_path, "FLIR_V2_curated_limited"), exist_ok=True)
    output_path = os.path.join(base_path, "FLIR_V2_curated_limited")

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


def save_images_folder(data_part, thermal):
    file_names = []
    database = get_data_type(data_part, thermal)
    start = os.path.join(input_path, database, 'data')
    count_img = 0
    if thermal:
        destination_img_folder = f"{new_yolodata_path}/flirv2_thermal/{data_part}/images"
    else:
        destination_img_folder = f"{new_yolodata_path}/flirv2_rgb/{data_part}/images"

    for filename in os.listdir(start):
        if not filename.startswith('.'):
            source = os.path.join(start, filename)
            destination = f"{destination_img_folder}/img{count_img}.jpg"

            shutil.copy(source, destination)
            file_names.append(filename)
            count_img += 1
            if count_img == count_max:  # Handling limited number samples curation
                break
    return file_names


def get_coco_jsonfile(data_type, thermal):
    database = get_data_type(data_type, thermal)
    with open(os.path.join(input_path, database, 'coco.json')) as f:
        cocodata = json.load(f)
    return cocodata


def get_img_ann(image_id, data_type, thermal):
    data = get_coco_jsonfile(data_type, thermal)
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


def get_img(filename, data_type, thermal):
    data = get_coco_jsonfile(data_type, thermal)
    for img in data['images']:
        if img['file_name'] == ('data/' + filename):
            return img


def save_annotation_folder(data_type, thermal):
    file_names = save_images_folder(data_type, thermal)
    count = 0
    folder = 'flirv2_thermal' if thermal else 'flirv2_rgb'

    # below cat_list can be defined as per classes required, define all
    # if all classes used, which would be all 0-14 in this case

    cat_list = [0, 2, 9, 11]  # If only selected classes is used not all
    # cat_list = [i for i in range(15)] # Use this if all 15 classes are used
    for filename in file_names:
        # Extracting image
        img = get_img(filename, data_type, thermal)

        if img is None:  # Handling if image file is not referenced in annotation
            print(f"Warning: {filename} returned None")
            os.remove(f"{new_yolodata_path}/{folder}/{data_type}/images/img{count}.jpg")
            count += 1
            continue

        img_id = img['id']
        img_w = img['width']
        img_h = img['height']

        # # Get Annotations for this image
        img_ann = get_img_ann(img_id, data_type, thermal)

        if img_ann is None:  # Handling if annotation box is not present for an image
            print(f"Warning: {filename} returned None")
            os.remove(f"{new_yolodata_path}/{folder}/{data_type}/images/img{count}.jpg")
            count += 1
            continue

        if img_ann:
            # Opening file for current image
            file_object = open(f"{new_yolodata_path}/{folder}/{data_type}/labels/img{count}.txt", "a")

            for ann in img_ann:
                yolo_category = ann['category_id'] - 1  # converting to YOLO format labels which start from 0
                if yolo_category in cat_list:  # Handling if class ids are wrongly labeled
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

                    # Limiting up-to fix number of decimal places
                    x_centre = format(x_centre, '.6f')
                    y_centre = format(y_centre, '.6f')
                    w = format(w, '.6f')
                    h = format(h, '.6f')

                    # Writing current object
                    file_object.write(f"{yolo_category} {x_centre} {y_centre} {w} {h}\n")

            file_object.close()

        count += 1
        if count == count_max:
            break


if __name__ == '__main__':
    current_path = os.getcwd()
    new_yolodata_path = folder_creation(current_path)

    print('Please enter the sample per folder else enter 0 for all:\n')
    testing = int(input())
    if testing:
        count_max = testing
    else:
        count_max = 50000

    for thermal in [0, 1]:
        for data_type in ['train', 'val', 'test']:
            save_annotation_folder(data_type, thermal)

print(time.time() - t)