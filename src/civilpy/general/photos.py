import os
import re
from pathlib import Path
from PIL import Image
from PIL.Image import Exif
from PIL.ExifTags import TAGS, GPSTAGS


class CivImageMap(Image.Image):
    def __init__(self, file_path, output='show'):
        """
        Civil Engineering Image class to display one or multiple photos on a map, multiple input and output options
        available

        :param file_path:
        """

        # Checks if the class was passed a file or a folder
        self.file_name = file_path

        if os.path.isfile(self.file_name):
            self.file_mode = True
            self.exif = None
            self.get_exif()
        else:
            # Builds a list of image files if it was given a folder
            self.file_mode = False
            self.file_dict = {}
            self.build_image_list_from_path(file_path)
            self.exif = None
            self.get_exif()
        self.output = output

        self.geo = None
        self.gps_tags = None

    def get_exif(self):
        if self.file_mode:
            image: Image.Image = Image.open(self.file_name)
            self.exif = image.getexif()
        else:
            for file, path in self.file_dict.items():
                image: Image.Image = Image.open(path)
                self.file_dict[file] = image.getexif()

    def get_geo(self):
        for key, value in TAGS.items():
            if value == "GPSInfo":
                break
        gps_info = self.exif.get_ifd(key)
        self.gps_tags = {
            GPSTAGS.get(key, key): value
            for key, value in gps_info.items()
        }

    def build_image_list_from_path(self, path=None):
        empty_dict = {}

        # Build a list of every file directory in the given folder
        for root, dirs, files in os.walk(Path(path).resolve()):
            print(root)
            # Filter out directories that contain unimportant or hidden files
            dirs[:] = [d for d in dirs if not d[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '_']

            # use files and dirs
            for directory in dirs:
                print(f"\n\nSaving files in: {root}/{directory}")
                directory = Path(f"{root}/{directory}")

                for file_var in os.listdir(directory):
                    root_dir = Path(f"{root}")
                    print(f"Saving: {Path(root / directory / file_var)}")

                    empty_dict[file_var]['path'] = f"{Path(root / directory / file_var)}"

        self.file_dict = empty_dict
