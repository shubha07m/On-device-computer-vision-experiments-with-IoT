"""
Script Name: new_class_id_creation.py
License: MIT License (https://opensource.org/licenses/MIT).

Description:
This script create multimodal train, validation and test data
ONLY using test data section of RGB and thermal images of
our curated FLIR V2 dataset

Author: Shubh
Date: Jan 29, 2024
"""
import os
import random
import shutil


def folder_creation(base_path):
    os.makedirs(os.path.join(base_path, "FLIR_V2_multimodal_data"), exist_ok=True)
    output_path = os.path.join(base_path, "FLIR_V2_multimodal_data")

    for datatype in ['train', 'val', 'test']:
        for img_lbl in ['images', 'labels']:
            os.makedirs(os.path.join(output_path, datatype, img_lbl), exist_ok=True)

    return output_path


def data_generation(d_type, thermal_):
    new_base_path = folder_creation(os.getcwd())

    if thermal_:
        file_path = os.path.join(os.getcwd(), 'FLIR_V2_curated_limited', 'flirv2_thermal', 'test')
    else:
        file_path = os.path.join(os.getcwd(), 'FLIR_V2_curated_limited', 'flirv2_rgb', 'test')

    img_files = os.listdir(os.path.join(file_path, 'images'))

    # Assuming you have a list of RGB image files called rgb_img_files
    num_images = len(img_files)
    indices = list(range(num_images))

    # Define the sizes for train, validation, and test sets
    train_size = 2450
    val_size = 520
    test_size = 520

    # Shuffle the indices randomly
    random.shuffle(indices)

    # Select the indices for each set without overlap
    train_indices = indices[:train_size]
    val_indices = indices[train_size: train_size + val_size]
    test_indices = indices[train_size + val_size: train_size + val_size + test_size]

    images_multimodal = []
    # Now, we can use these indices to extract the corresponding images

    if d_type == 'train':
        images_multimodal = [img_files[i] for i in train_indices]

    if d_type == 'val':
        images_multimodal = [img_files[i] for i in val_indices]

    if d_type == 'test':
        images_multimodal = [img_files[i] for i in test_indices]

    sources_images_multimodal = [os.path.join(file_path, 'images', i) for i in images_multimodal]
    sources_labels_multimodal = [os.path.join(file_path, 'labels', i[:-4]) + '.txt' for i in
                                 images_multimodal]

    # creating train data

    # creating images data
    j = 0
    relative_path = os.path.join(new_base_path, d_type, 'images')
    total_len = len(os.listdir(relative_path))
    if total_len:
        j += total_len

    for source in sources_images_multimodal:
        destination = os.path.join(relative_path, str(j) + '.jpg')

        shutil.copy(source, destination)
        j += 1
    # creating labels data
    j = 0
    relative_path = os.path.join(new_base_path, d_type, 'labels')
    total_len = len(os.listdir(relative_path))
    if total_len:
        j += total_len
    for source in sources_labels_multimodal:
        destination = os.path.join(relative_path, str(j) + '.txt')
        shutil.copy(source, destination)
        j += 1


for data_type in ['train', 'val', 'test']:
    for thermal in [1, 0]:
        data_generation(data_type, thermal)
        thermal_rgb_data = 'thermal data' if thermal else 'rgb data'
        print(f'{data_type} part for {thermal_rgb_data} completed!')
print('all data generation completed!')
