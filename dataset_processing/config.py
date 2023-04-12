from pydantic import BaseModel
from typing import Literal

class TifToPngConfig(BaseModel):
    dataroot: str
    path_to_save: str
    name: str

class DatasetCreatorConfig(BaseModel):
    dataroot: str
    map_size: int
    path_to_save_dataset: str
    need_create_folder: bool
    mode: str = Literal["resize", "cut", "cut+resize"],
    resize_size = 100
