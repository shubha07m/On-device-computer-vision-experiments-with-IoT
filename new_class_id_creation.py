"""
Script Name: new_class_id_creation.py
License: MIT License (https://opensource.org/licenses/MIT).

Description:
This script convert YOLO format class id / category ids to
new class ids starts from 0 onwards. This script is required
because YOLO training throws error if class ids are not aligned
as 0,1,2,3 In case of using only a limited number of classes
instead of using all classes in datasets this conversion can
solve that issue.

Author: Shubh
Date: Sept 18, 2023
"""

import os

base_path = os.path.join(os.getcwd(), 'FLIR_V2_curated_limited')
cat_list = [0, 2, 9, 11]  # This is the category list as per YOLO format

for img_type in ['flirv2_rgb', 'flirv2_thermal']:
    for data_type in ['train', 'val', 'test']:
        common_path = os.path.join(base_path, img_type, data_type)
        os.makedirs(os.path.join(common_path, 'new_labels'), exist_ok=True)  # creating new label directory
        file_names = os.listdir(os.path.join(common_path, 'labels'))

        for file_name in file_names:
            if not file_name.startswith('.'):
                try:
                    old_object = open(f"{common_path}/labels/{file_name}", "r", encoding="ISO-8859-1")
                except:
                    print(f"{common_path}/labels/{file_name}")
                    continue
                new_object = open(f"{common_path}/new_labels/{file_name}", "a")

                for line in old_object:
                    try:
                        list_ = line.split()
                        class_id = cat_list.index(int(list_[0]))
                        new_object.write(f"{class_id} {list_[1]} {list_[2]} {list_[3]} {list_[4]} \n")
                    except:
                        print(f"{common_path}/labels/{file_name}")
                        continue
                new_object.close()
                old_object.close()
