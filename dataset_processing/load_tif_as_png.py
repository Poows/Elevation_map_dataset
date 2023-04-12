import cv2
import numpy as np
import os
from tqdm import tqdm
import argparse
from dataset_processing.config import TifToPngConfig
import shutil

def load_tif_file(tif_file_path):
    tif_file = cv2.imread(tif_file_path, -1)
    float_tif_file = np.divide(tif_file, np.max(tif_file))
    uint_tif = (float_tif_file * 255).astype(np.uint8)
    return uint_tif

def convert_tif_as_png(files_path, save_path, maps_name):
    
    try:
        os.mkdir(save_path)
    except Exception:
        shutil.rmtree(save_path)
        os.mkdir(save_path)
    
    for idx, file in tqdm(enumerate(os.listdir(files_path))):
        if file.endswith(".tif") and file.endswith("_dem.tif"):
            tif_file_path = os.path.join(files_path, file)
            uint_tif = load_tif_file(tif_file_path)
            name = maps_name + str(idx) + ".png"
            full_save_path = os.path.join(save_path, name)
            cv2.imwrite(full_save_path, uint_tif)

# test
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser = parser.parse_args()

    config_path = parser.config
    config = TifToPngConfig.parse_file(config_path)

    dataroot = config.dataroot
    folder_save = config.path_to_save
    name = config.name
    convert_tif_as_png(dataroot, folder_save, name)
    # uint_tif = load_tif_file("D:\VKR\dataset\Dataset_gorges\ASTGTMV003_N00E020_num.tif")
    # cv2.imwrite("colored_tiff.png", uint_tif)