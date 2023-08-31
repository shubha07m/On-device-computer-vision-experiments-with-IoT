"""
Script Name: coco2yolo_conversion.py
License: MIT License (https://opensource.org/licenses/MIT).

Description:
This script convert a coco json format dataset to YOLO format.
The current one uses a FLIR V2 infrared dataset as an example.

Note:
1. Make sure the source (unzipped folder) and this script is in
the same path. 
2. For testing with a small samples (default 10)
select 1, else use 0 as argument.
3. This script use multiprocessing for Process-based parallelism.

Author: Shubh
Date: August 31, 2023
"""
import json
import os
import shutil
import time
from multiprocessing import Process


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
    count = 0
    start = os.path.join(input_path, database, 'data')

    for filename in os.listdir(start):
        source = os.path.join(start, filename)
        if thermal:
            destination = f"{new_yolodata_path}/flirv2_thermal/{data_part}/images/img{count}.jpg"
        else:
            destination = f"{new_yolodata_path}/flirv2_rgb/{data_part}/images/img{count}.jpg"

        shutil.copy(source, destination)
        file_names.append(filename)
        count += 1

        if count > count_max:
            break

    return file_names


def get_coco_jsonfile(thermal, data_type):
    database = get_data_type(data_type, thermal)
    with open(os.path.join(input_path, database, 'coco.json')) as f:
        cocodata = json.load(f)
    return cocodata


def get_img_ann(image_id, thermal, data_type):
    data = get_coco_jsonfile(thermal, data_type)
    img_ann = [ann for ann in data['annotations'] if ann['image_id'] == image_id]
    return img_ann


def get_img(filename, thermal, data_type):
    data = get_coco_jsonfile(thermal, data_type)
    img = next((img for img in data['images'] if img['file_name'][5:] == filename), None)
    return img


def save_annotation_folder(thermal, data_type):
    fnames = save_images_folder(thermal, data_type)
    count = 0
    for filename in fnames:
        img = get_img(filename, thermal, data_type)
        if img is None:
            print(f"Image not found: {filename} in {data_type} dataset.")
            continue
        img_id = img['id']
        img_w = img['width']
        img_h = img['height']
        img_ann = get_img_ann(img_id, thermal, data_type)

        if img_ann:
            folder = 'flirv2_thermal' if thermal else 'flirv2_rgb'
            labels_folder = f"{new_yolodata_path}/{folder}/{data_type}/labels"
            os.makedirs(labels_folder, exist_ok=True)
            label_filename = f"{labels_folder}/img{count}.txt"

            with open(label_filename, "a") as file_object:
                for ann in img_ann:
                    current_category = ann['category_id'] - 1
                    current_bbox = ann['bbox']
                    x, y, w, h = current_bbox

                    x_centre = (x + (x + w)) / 2
                    y_centre = (y + (y + h)) / 2
                    x_centre /= img_w
                    y_centre /= img_h
                    w /= img_w
                    h /= img_h

                    line = f"{current_category} {x_centre:.6f} {y_centre:.6f} {w:.6f} {h:.6f}\n"
                    file_object.write(line)

            count += 1

            if count > count_max:
                break


if __name__ == '__main__':
    current_path = os.getcwd()
    new_yolodata_path = folder_creation(current_path)

    # For testing only#

    print('testing or actual - enter 1 for testing, else 0:\n')

    testing = int(input())
    if testing:
        count_max = 9
    else:
        count_max = 50000


    for thermal in [0, 1]:
        for data_type in ['train', 'val', 'test']:
            p = Process(target=save_annotation_folder, args=(thermal, data_type))
            p.start()
            p.join()

print(time.time() - t)
