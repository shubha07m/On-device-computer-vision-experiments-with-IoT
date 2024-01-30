"""
Script Name: new_class_id_creation.py
License: MIT License (https://opensource.org/licenses/MIT).

Description:
This script create multimodal train, validation and test data
using ONLY train and validation data section of RGB and thermal
images of our curated FLIR V2 dataset

Author: Shubh
Date: Jan 29, 2024
"""

import os
import shutil


def folder_creation(base_path):
    os.makedirs(os.path.join(base_path, "FLIR_V2_multimodal_data_large"), exist_ok=True)
    output_path = os.path.join(base_path, "FLIR_V2_multimodal_data_large")

    for datatype in ['train', 'val']:
        for img_lbl in ['images', 'labels']:
            os.makedirs(os.path.join(output_path, datatype, img_lbl), exist_ok=True)

    return output_path


def combine_data(d_type):
    new_base_path = folder_creation(os.getcwd())

    # Combine data from both thermal and RGB for the specified data_type
    for thermal_ in [True, False]:
        if thermal_:
            source_path = os.path.join(os.getcwd(), 'FLIR_V2_curated_limited', 'flirv2_thermal', d_type)
        else:
            source_path = os.path.join(os.getcwd(), 'FLIR_V2_curated_limited', 'flirv2_rgb', d_type)

        img_files = os.listdir(os.path.join(source_path, 'images'))

        images_multimodal = img_files
        sources_images_multimodal = [os.path.join(source_path, 'images', i) for i in images_multimodal]
        sources_labels_multimodal = [os.path.join(source_path, 'labels', i[:-4]) + '.txt' for i in images_multimodal]

        # Create the combined data
        j = 0
        relative_path = os.path.join(new_base_path, d_type, 'images')
        total_len = len(os.listdir(relative_path))

        if total_len:
            j += total_len

        for source in sources_images_multimodal:
            destination = os.path.join(relative_path, str(j) + '.jpg')
            shutil.copy(source, destination)
            j += 1

        j = 0
        relative_path = os.path.join(new_base_path, d_type, 'labels')
        total_len = len(os.listdir(relative_path))

        if total_len:
            j += total_len

        for source in sources_labels_multimodal:
            destination = os.path.join(relative_path, str(j) + '.txt')
            shutil.copy(source, destination)
            j += 1


combine_data('train')
print('Train data combination completed!')
combine_data('val')
print('Validation data combination completed!')