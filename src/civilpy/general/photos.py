"""
CivilPy
Copyright (C) 2019 - Dane Parks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import re
import sys
import shutil
import unicodedata
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime


class CivImageMap(Image.Image):
    def __init__(self, file_path, output="show"):
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
            GPSTAGS.get(key, key): value for key, value in gps_info.items()
        }

    def build_image_list_from_path(self, path=None):
        empty_dict = {}

        # Build a list of every file directory in the given folder
        for root, dirs, files in os.walk(Path(path).resolve()):
            print(root)
            # Filter out directories that contain unimportant or hidden files
            dirs[:] = [d for d in dirs if not d[0] == "."]
            dirs[:] = [d for d in dirs if not d[0] == "_"]

            # use files and dirs
            for directory in dirs:
                print(f"\n\nSaving files in: {root}/{directory}")
                directory = Path(f"{root}/{directory}")

                for file_var in os.listdir(directory):
                    root_dir = Path(f"{root}")
                    print(f"Saving: {Path(root) / directory / file_var}")

                    empty_dict[file_var][
                        "path"
                    ] = f"{Path(root / directory / file_var)}"

        self.file_dict = empty_dict


def get_list_of_files_from_folder(path=r"C:\Users\dane\Desktop\test_photos"):
    """
    Builds a list of files given a root folder, can be given a folder with multiple sub-folders

    Parameters
    ----------
    path: str - A string representation of a file path, for windows paths, either has to be passed in as a raw string,
        or with escaped/converted '\' characters. Once inside the function, the string is converted using the pathlib
        Path() module, eliminating further issues with windows paths.

    Returns
    -------
    return_list: list - A full list of every file found by the function
    """
    return_list = []

    # Build a list of every file in the given folder
    for root, dirs, files in os.walk(Path(path).resolve()):
        # Get all the files in the root folder
        for file in files:
            return_list.append(f"{Path(root) / file}")

    return return_list


def get_photos_from_file_list(file_list=None):
    """
    Takes a list of file paths and uses regex to only return files with photo related file types (svg, heif, bmp, tiff,
    webp, jpeg, png, jpg). Not case-sensitive.

    Parameters
    ----------
    file_list: list - a list of files to be filtered for Photos

    Returns
    -------
    photos: list - a filtered list containing only the paths from the original list that are photos
    """

    photos = [
        file
        for file in file_list
        if re.search("(svg|heif|bmp|tiff|webp|jpeg|png|jpg)$", str(file), re.IGNORECASE)
    ]

    return photos


def create_folder_for_renamed_files(path=None):
    """
    Creates a folder named "Renamed_Photos" to store the new photos in

    Parameters
    ----------
    path: str - A string representation of the root folder for photos where you want the "Renamed_Photos" folder to be
        created

    Returns
    -------
    None - Creates a folder in the designated location
    """
    # Create a new folder
    renamed_folder = Path(path) / "Renamed_Photos"
    os.mkdir(renamed_folder)


def get_photo_creation_date(img):
    """
    Extracts the creation date of a photo from its EXIF metadata
    and returns it in MM/DD/YYYY format.

    :param file_path: Path to the image file
    :return: Creation date in MM/DD/YYYY format, or None if not available
    """
    # Get EXIF data
    exif_data = img.getexif()

    if not exif_data:
        print("No EXIF data found in the image.")
        return None

    date = exif_data.get(36867)
    if date is None:
        date = exif_data.get(306)
    formatted_date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")

    return formatted_date.strftime("%m/%d/%Y %H:%M")


def add_timestamp(image, date):
    """
    Adds a timestamp with date and time extracted from an image's metadata
    (if available) to the bottom right of the image.

    Args:
        image (PIL.Image.Image): An Image object.

    Returns:
        PIL.Image.Image: The modified image with the timestamp.
    """
    try:
        date = datetime.strptime(date, "%m/%d/%Y %H:%M")
        # Convert to "MM/DD/YYYY HH:MM" format
        timestamp_text = date.strftime("%m/%d/%Y %H:%M")

        # Prepare drawing context
        draw = ImageDraw.Draw(image)
        try:
            # Try loading a truetype font (e.g., Arial)
            font = ImageFont.truetype("arial.ttf", size=36)
        except IOError:
            # Fallback to a default PIL font if the font is missing
            font = ImageFont.load_default()

        # Calculate text size using textbbox
        text_bbox = draw.textbbox((0, 0), timestamp_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Determine position for the text (bottom-right corner with padding)
        x = image.width - text_width - 10  # 10-pixel padding from the right
        y = image.height - text_height - 10  # 10-pixel padding from the bottom

        # Add the timestamp to the image
        draw.text((x, y), timestamp_text, fill="white", font=font)

        return image

    except Exception as e:
        print(f"Error: {e}")
        return None


# This function drops illegal characters from file names (like '/', '%', '#' or ',')
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.

    Parameters
    ----------
    value: str - the original value containing potentially illegal characters
    allow_unicode: bool - Defaults to False, prevents things like language characters and emojis from being used in
        file names

    Returns
    -------
    str - a string stripped of all illegal characters for use in file names
    """

    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def convert_filenames_from_excel(
    excel_file=None,
    root_folder=None,
    project_name=None,
    keep_existing_fns=False,
):
    """
    Function that copies a series of file paths from column 'A' of an Excel file (sheet 0, with no header) and changes
    the file names to the new filename values held in column 'B'. The function uses Django's slugify function to remove
    illegal or confusing characters like '/', '\', ',', or '#'

    Parameters
    ----------
    excel_file: str - Path to Excel file containing file paths and new file names
    root_folder: str - Path to the folder the Renamed_Photos folder is located
    project_name: str - Name of the project to be included within the photo names
    keep_existing_fns: bool - Option to either append the original file names to the new name or not

    Returns
    -------
    None - creates the files within the new renamed folder
    """
    # Get a list of current files and what you want them renamed to
    photo_list_excel = pd.read_excel(Path(excel_file), 0, header=None)
    file_list = photo_list_excel[0].tolist()
    new_names = photo_list_excel[1].tolist()

    # Loop through the Existing files and copy them into the new folder
    for index, name in enumerate(new_names):
        old_name = Path(file_list[index])
        if keep_existing_fns:
            new_name = (
                Path(root_folder)
                / "Renamed_Photos"
                / f"{slugify(name)}-{slugify(old_name.stem)}.jpg"
            )
        else:
            new_name = Path(root_folder) / "Renamed_Photos" / f"{slugify(name)}.jpg"
        shutil.copy(old_name, new_name)
        print(f"Created File: {new_name}")


def resize_image(img, width=1024, height=768, bar_color=(0, 0, 0)):
    """
    Resize an image while preserving the aspect ratio and add vertical (or horizontal) bars
    to fit the image in the specified width and height.

    Args:
        img (PIL.Image): Path to the input image.
        width (int): Target width of the final image.
        height (int): Target height of the final image.
        bar_color (tuple): RGB color for the bars (default is black).
    """
    try:
        # Preserve aspect ratio by resizing into a box
        img.thumbnail((width, height), Image.LANCZOS)

        # Create a new image with the target dimensions and bar color
        new_image = Image.new("RGB", (width, height), bar_color)

        # Center the resized image on the new canvas
        x_offset = (width - img.width) // 2
        y_offset = (height - img.height) // 2
        new_image.paste(img, (x_offset, y_offset))

        return new_image

    except Exception as e:
        print(f"Error: {e}")


def photo_renaming_tool(
    root_folder=None, excel_file=None, project_name=None
):
    """
    Function to simplify the above functions, given a root folder, returns a list of files and
    searches for an Excel file to use with the renaming tool function

    Parameters
    ----------
    root_folder: str - Path to folder containing photos and Excel file defining new names
    excel_file: str - Path override for if the function can't find the correct file or if it's
        in a different folder
    project_name: str - Name of the project to be included in the photo names

    Returns
    -------
        None - prints list of photo files found and renames them into another folder
    """
    full_file_list = get_list_of_files_from_folder(root_folder)

    # Only finds first Excel file, multiple Excel files in the folder will break this
    if excel_file is None:
        excel_file = [
            file
            for file in full_file_list
            if re.search("(xlsx|xls|xlsm)$", str(file), re.IGNORECASE)
        ][0]

    photo_list = get_photos_from_file_list(full_file_list)

    create_folder_for_renamed_files(root_folder)
    convert_filenames_from_excel(
        excel_file=excel_file, root_folder=root_folder, project_name=project_name
    )


# This allows the file to be run as a script by running `python PhotoOrganizer.py 'path_to_folder'
if __name__ == "__main__":
    if len(sys.argv) > 1:
        testing_root_folder = Path(sys.argv[1])
        testing_excel_file = Path(sys.argv[2])

        # These are put here to demonstrate the workflow process and test the file
        test_files_list = get_list_of_files_from_folder(testing_root_folder)
        test_photo_list = get_photos_from_file_list(test_files_list)
        print(test_photo_list)

        input('Copy the files and names into the excel sheet, then hit "enter"')
        create_folder_for_renamed_files(testing_root_folder)
        convert_filenames_from_excel(testing_excel_file, testing_root_folder)

    else:
        testing_root_folder = r"C:\Users\dane\Desktop\test_photos"
        testing_excel_file = r"C:\Users\dane\Desktop\test_photos\test.xlsx"
