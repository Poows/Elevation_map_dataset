import cv2
import math
import argparse
import os
import shutil
from dataset_processing.load_tif_as_png import load_tif_file
from dataset_processing.config import DatasetCreatorConfig
from tqdm import tqdm

def write_image(image_map, image_number, y, x, save_path):
    full_path_save = os.path.join(save_path, f"{image_number}_{x}_{y}.png")
    cv2.imwrite(full_path_save, image_map)

def cut_image(image, new_image_size, image_number, save_path, mode, resize):
    samples = math.floor(image.shape[0] / new_image_size)

    for height in range(samples):
        prev_cord_height = height * new_image_size
        new_cord_height = (height + 1) * new_image_size
        for width in range(samples):
            prev_cord_width = width * new_image_size
            new_cord_width = (width + 1) * new_image_size
            cropped_image = image[prev_cord_height:new_cord_height, prev_cord_width:new_cord_width]
            if mode == "cut+resize":
                res_image = cv2.resize(cropped_image, [resize, resize], cv2.INTER_NEAREST)
            write_image(res_image, image_number, height, width, save_path)

def get_dataset(config, mode, need_create_folder):

    dataroot = config.dataroot
    map_size = config.map_size
    save_path = config.path_to_save_dataset
    resize_size = config.resize_size

    if need_create_folder:
        try:
            os.mkdir(save_path)
        except Exception:
            shutil.rmtree(save_path)
            os.mkdir(save_path)

    if mode == "cut" or mode == "cut+resize":
        #cut_images(image_list, dataroot, map_size, save_path)
        image_list = os.listdir(dataroot)
        for idx, image_name in tqdm(enumerate(image_list)):
            image_path = os.path.join(dataroot, image_name)
            image = load_tif_file(image_path)
            cut_image(image, map_size, idx, save_path, mode, resize_size)
    elif mode == "resize":
        image_list = os.listdir(dataroot)
        for idx, image_name in tqdm(enumerate(image_list)):
            image_path = os.path.join(dataroot, image_name)
            image = cv2.imread(image_path)
            res_image = cv2.resize(image, [map_size, map_size], cv2.INTER_NEAREST)
            #image = load_tif_file(image_path)
            write_image(res_image, f"r_{idx}", idx, idx, save_path)
            #cut_image(image, map_size, idx, save_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser = parser.parse_args()

    config_path = parser.config
    config = DatasetCreatorConfig.parse_file(config_path)

    mode = config.mode
    create_folder = config.need_create_folder

    get_dataset(config, mode, create_folder)

if __name__ == "__main__":
    main()