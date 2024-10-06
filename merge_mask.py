import numpy as np
import cv2
import os
def merge_images(image_paths, output_path):
    print(image_paths[0])
    img = cv2.imread(image_paths[0])
    data = np.zeros(img.shape)
    count = 1
    for image in image_paths:
        img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        data[img > 0] = count
        count += 1
    
    cv2.imwrite(output_path, data)

def get_filename_without_extension(file_path):
    base_name = os.path.basename(file_path)
    file_name, _ = os.path.splitext(base_name)
    return file_name


file_names = ['chua_kham_son.tif', 'kho_xang.tif', 'sun_hoabinh_cuoiha_1.tif', 'sun_hoabinh_cuoiha_2.tif',
            'sun_hoabinh_sangolf.tif', 'van_don34.tif', 'vinaconex.tif']
folders = os.listdir('mask')
mask_folder = 'mask'

for file_name in file_names:
    file_paths = []
    for folder in folders:
        file_path = os.path.join(os.path.join(mask_folder, folder), file_name)
        # print(file_path)
        file_paths.append(file_path)

    merge_images(file_paths, f'6_classes_mask/{get_filename_without_extension(file_name)}.png', )
    print(file_paths)


