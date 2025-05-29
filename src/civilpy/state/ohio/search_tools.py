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
import math
import tifftools
import pandas as pd
from pathlib import Path
from natsort import natsorted
from PIL import Image, ImageSequence

from civilpy.state.ohio.DOT.legacy import TimsBridge

test_init = True

default_bridge_labels = [
    "Bridge Status Code",
    "Bridge Status Description calc",
    "Structure File Number",
    "District Number",
    "Deck Area",
    "Overall Structure Length",
    "Over 20 Ft (Fedl Brdg) (Y/N/Null) calc",
    "Sufficiency Rating",
    "Sufficiency Rating Converted calc",
    "SD/FO",
    "SD/FO calc",
    "Functional Class Code",
    "Functional Class Old Name calc",
    "Functional Class Old Group calc",
    "Functional Class FHWA Code calc",
    "Functional Class New Code calc",
    "Funct Class New Name calc",
    "Maintenance Responsibility Code",
    "Maintenance Responsibility Description calc",
    "Maintenance Responsibility plus Null calc",
    "Type Service On Bridge Code",
    "Type of Service On Bridge Description calc",
    "Type Service Under Bridge Code",
    "County Code",
    "Highway System Code",
    "Invent Hwy Sys Name calc",
    "Invent Hwy Sys Description calc",
    "Route",
    "Inventory Route",
    "Route On Bridge Code",
    "Route On Bridge Description calc",
    "Route Under Bridge Code",
    "Route Under Bridge Description calc",
    "Facility Carried By Structure",
    "Feature Intersected",
    "Latitude",
    "Longitude",
    "NHS Code",
    "NHS (Y/N) calc",
    "NHS Description calc",
    "Year Rebuilt Calc",
    "Load Rating Year",
    "Main Span Type Code",
    "Main Structure Type",
    "Load Inventory Rating",
    "Inventory County",
    "FIPS Number",
    "BTRS Link Number",
    "BTRS Linked (Y/N) calc",
    "Analyzed By",
    "Approach Alignment Code",
    "Approach Guardrail Code",
    "Approach Pavement Grade Code",
    "Approach Pavement Material Code",
    "Approach Roadway Width",
    "Approach Slab ",
    "Approach Slab Length",
    "Approach Span Description Code",
    "Approach Span Material Code",
    "Approach Span Type Code",
    "Approach Spans",
    "Approach Structure Type",
    "BARS Code",
    "Bearing Device1 Code",
    "Bearing Device2 Code",
    "Bridge Roadway Width Cb Cb",
    "Bypass Length",
    "Calculated Deck Geometry",
    "Calculated Structural Evaluation",
    "Calculated Underclearance",
    "Channel Protection Type Code",
    "Min Horizontal Clearance On Bridge Cardinal",
    "Min Horizontal Clearance On Bridge Non-Cardinal",
    "Min Horizontal Clearance Under Cardinal",
    "Min Horizontal Clearance Under Non-Cardinal",
    "Min Lateral Clearance Cardinal Left",
    "Min Lateral Clearance Cardinal Right",
    "Min Lateral Clearance Non-Cardinal Left",
    "Min Lateral Clearance Non-Cardinal Right",
    "Min Lateral Clearance Under Cardinal Left",
    "Min Lateral Clearance Under Cardinal Right",
    "Min Lateral Clearance Under Non-Cardinal Left",
    "Min Lateral Clearance Under Non-Cardinal Right",
    "Min Vertical Clearance Bridge Cardinal",
    "Min Vertical Clearance Bridge Non-Cardinal",
    "Min Vertical Clearance Under Bridge Cardinal",
    "Min Vertical Clearance Under Bridge Non-Cardinal",
    "Clearance Practical Max Vertical On Bridge",
    "Clearance Practical Max Vertical Under Bridge",
    "Combined",
    "Composite Structure Code",
    "Culvert Fill Depth",
    "Culvert Headwalls/Endwalls Type Code",
    "Culvert Length",
    "Culvert Sufficiency Rating Default",
    "Culvert Type Code",
    "Curb/Sidewalk Material Type Left",
    "Curb/Sidewalk Material Type Right",
    "Curb/Sidewalk Type Left",
    "Curb/Sidewalk Type Right",
    "Deck Concrete Type Code",
    "Deck Drainage Type Code",
    "Deck Protection External Code",
    "Deck Protection Internal Code",
    "Deck Type Code",
    "Deck Width Out/Out",
    "Design Load Code",
    "Directional Suffix Code",
    "Expansion Joint Retrofit1 Code",
    "Expansion Joint Retrofit2 Code",
    "Expansion Joint Retrofit3 Code",
    "Expansion Joint Type1 Code",
    "Expansion Joint Type2 Code",
    "Expansion Joint Type3 Code",
    "Expansion Joint With Trough Retrofit1",
    "Expansion Joint With Trough Retrofit2",
    "Expansion Joint With Trough Retrofit3",
    "Future ADT",
    "Future ADT Year",
    "Haunched Girder",
    "Haunched Girder Depth",
    "Highway Designation Code",
    "Hinge Code",
    "Horizontal Curve Radius",
    "Lanes On Number",
    "Lanes Under Number",
    "Macro Corridor",
    "Main Member Depth",
    "Main Member Type Code",
    "Main Span Description Code",
    "Main Span Material Code",
    "Main Spans Number",
    "Major Rehab Date",
    "Maximum Span Length",
    "Median Code",
    "Median Type1 Code",
    "Median Type2 Code",
    "Median Type3 Code",
    "Method Of Analysis Code",
    "Moment Plates Code",
    "MPO Code",
    "Min Vertical Clearance Lift Bridge",
    "Navigable Stream",
    "Navigable Stream Horizontal Clearance",
    "Navigable Stream Vertical Clearance",
    "Ohio Percent Of Legal Load",
    "On/Under",
    "Operating Rating HS",
    "Parallel Structure Code",
    "Paint Condition Rating Date",
    "Paint Supplier",
    "Paint Surface Area",
    "Preferred Route",
    "Railing Type Code",
    "Ramp Lateral Under Clearance Cardinal Left",
    "Ramp Lateral Under Clearance Cardinal Right",
    "Ramp Lateral Under Clearance Non-Cardinal Left",
    "Ramp Lateral Under Clearance Non-Cardinal Right",
    "Ramp Roadway Width Cardinal",
    "Ramp Roadway Width Non-Cardinal",
    "Ramp Vertical Under Clearance Cardinal",
    "Ramp Vertical Under Clearance Non-Cardinal",
    "Record Add Date",
    "Record Update Date",
    "Remarks",
    "Retire Reason Code",
    "SFN Control Authority",
    "Sidewalk Width Left",
    "Sidewalk Width Right",
    "Skew",
    "Slope Protection Type Code",
    "Software Of Rating Analysis",
    "Inventory Special Designation",
    "Straight Line Kilometers",
    "Straight Line Mileage",
    "Structure Location",
    "Toll Road",
    "Total Spans",
    "Traffic Direction Code",
    "Water Direction Code",
    "Waterway Adequacy Code",
    "Wearing Surface Date",
    "Wearing Surface Thickness",
    "Wearing Surface Type Code",
    "Total",
    "SubClass",
    "Subclass1",
    "SubClass2",
    "Cty",
    "9",
    "8",
    "7",
    "6",
    "A",
    "5",
    "4",
    "3",
    "2",
    "1",
    "0",
    "N",
    "Maintained",
    "Inventoried",
    "Date Built",
    "Contractor Name",
    "Drainage Area",
    "Framing Type",
    "Historical Bridge Type Code",
    "Historical Builder Code",
    "Historical Significance Code",
    "Longitudinal Member Type",
    "Microfilm Number",
    "Original Project Number",
    "Structural Steel Protection Code",
    "Railing Structural Steel Type",
    "Standard Drawing Number",
    "Stream Velocity",
    "Structural Steel Fabricator",
    "Structural Steel Paint Type Code",
    "Structural Steel Pay Weight",
    "Predominant Structural Steel Type",
    "Boat Inspection",
    "Critical Structure",
    "Dive Inspection",
    "Dive Inspection Date",
    "Dive Inspection Frequency",
    "Fracture Critical Inspection",
    "Fracture Critical Inspection Date",
    "Fracture Critical Inspection Frequency",
    "Inspection Frequency",
    "Inspection Responsibility Code",
    "Probe Inspection",
    "Probe Inspection Frequency",
    "Scour Critical Code",
    "Snooper Inspection",
    "Special Inspection",
    "Special Inspection Date",
    "Special Inspection Frequency",
    "Major Bridge Indicator (Y/N)",
    "NBIS Length (Y/N)",
    "Aperture Card Original",
    "Aperture Fabrication",
    "Aperture Repairs",
    "Bridge Dedicated Name",
    "Cable Stayed",
    "Catwalks",
    "Designated National Network",
    "Fencing",
    "Fencing Height",
    "Flared",
    "GASB 34",
    "Glare Screen",
    "Lighting",
    "Noise Barrier",
    "Other Features",
    "Post Tensioned",
    "Railroad Code",
    "Scenic Waterway",
    "Seismic Susceptibility Code",
    "Signs Attached On",
    "Signs Attached Under",
    "Splash Guard",
    "Strahnet Highway Designation",
    "Temporary Barrier",
    "Temporary Debris Netting",
    "Temporary Shored",
    "Temporary Structure",
    "Temporary Subdecking",
    "Utility - Electric",
    "Utility - Gas",
    "Utility - Other",
    "Utility - Sewer",
    "Utility - Telephone",
    "Utility - TV Cable",
    "Utility - Water",
    "Abutment Forward Material Code",
    "Abutment Forward Type Code",
    "Abutment Rear Material Code",
    "Abutment Rear Type Code",
    "Dynamic Load Test Abutment Forward",
    "Dynamic Load Test Abutment Rear",
    "Dynamic Load Test Pier Predominate",
    "Dynamic Load Test Pier Type1",
    "Dynamic Load Test Pier Type2",
    "Foundation Abutment Forward Code",
    "Foundation Abutment Rear Code",
    "Foundation Length Abutment",
    "Foundation Length Pier",
    "Foundation Pier Predominate Code",
    "Foundation Pier Type1 Code",
    "Foundation Pier Type2 Code",
    "Pier Predominant  ",
    "Pier Predominate Material Code",
    "Pier Predominate Type Code",
    "Pier Type1 Number",
    "Pier Type1 Material Code",
    "Pier Type1 Type Code",
    "Pier Type2 Number",
    "Pier Type2 Material Code",
    "Pier Type2 Type Code",
    "Pile Log",
    "Static Load Test Abutment Forward",
    "Static Load Test Abutment Rear",
    "Static Load Test Pier Predominate",
    "Static Load Test Pier Type1",
    "Static Load Test Pier Type2",
]


class D6BridgeLookup(TimsBridge):
    def __init__(
        self,
        sfn,
        column_labels=default_bridge_labels,
        data_path="G:\\ref\\New folder\\Bridges.tsv",
    ):
        df = pd.read_csv(f"{data_path}", sep="\t", low_memory=False)
        self.SFN = sfn

        bridge_details = (
            df.iloc[df.index[df["Structure File Number"] == sfn]].iloc[0].to_dict()
        )

        self.raw_data = bridge_details
        self.photo_url = ""
        self.plan_sets_list = []

        # //TODO - Seperate the following lines into a function
        dirty_long = str(self.raw_data["Longitude"])
        dirty_lat = str(self.raw_data["Latitude"])

        self.clean_lat = (
            float(dirty_lat[:2])
            + (float(dirty_lat[2:4]) / 60)
            + (float(f"{dirty_lat[4:6]}.{dirty_lat[6:]}") / 3600)
        )
        self.clean_long = -(
            float(dirty_long[:2])
            + (
                (float(dirty_long[2:4]) / 60)
                + (float(f"{dirty_long[4:6]}.{dirty_long[6:]}") / 3600)
            )
        )

        self.cty_rte_sec = self.get_summary()

    def get_summary(self):
        substring_1 = f"{self.raw_data['County Code']} - "
        substring_2 = f"{self.raw_data['Facility Carried By Structure']} over "
        substring_3 = f"{self.raw_data['Feature Intersected']}"

        temp_string = substring_1 + substring_2 + substring_3
        print(
            f'Report for SFN: {self.raw_data["Structure File Number"]} ({temp_string})'
        )

        print(f"\nLatitude: {self.clean_lat:.5f}, Longitude: {self.clean_long:.5f}")

        county_code = self.raw_data["County Code"]
        # The next two values use regex to adjust them after being pulled from the database
        route_num = self.raw_data["Inventory Route"]
        route_num = re.sub("\D", "", route_num).lstrip("0")
        # Inserts a decimal to convert text based milepost to usable value
        section_num = (
            self.raw_data["Straight Line Mileage"][:-3]
            + "."
            + self.raw_data["Straight Line Mileage"][2:]
        )
        section_num = re.sub("/[^0-9.]/g", "", section_num).lstrip("0")

        return f"{county_code}-{route_num}-{section_num}"

    def get_d6_plan_sets(self, district_df_path="G:\\ref\\New folder\\PLANINDX.TXT"):
        """
        Using the "CTY-RT-SEC" from a SFN, this function finds the various
        plan sets potentially associated with that structure, it rounds the 'section'
        value up and down to be inclusive, effectively giving every plan segment
        for that 1 mile segment.

        :param district_df_path: set to default but overrideable to allow development on various devices without network
        access
        :return: Dumps .pdf files into a folder on the local machine at W:\CivilPy_Output\pulled_plans\
        """
        # //TODO - Replace this dataframe with a version that works with new plans, map other districts fs's
        d6_plans_df = pd.read_csv(district_df_path, delimiter="^", quotechar="~")
        county_code, route_num, section_num = self.cty_rte_sec.split("-")

        # The next four lines of code filter the d6_plans_df by county route section to get associated plans
        first_filtered_df = d6_plans_df[d6_plans_df["County_code"] == county_code]
        second_filtered_df = first_filtered_df[first_filtered_df["Route"] == route_num]
        third_filtered_df = second_filtered_df[
            second_filtered_df["Log_beg"] <= str(math.floor(float(section_num)))
        ]
        fourth_filtered_df = third_filtered_df[
            third_filtered_df["Log_end"] >= math.ceil(float(section_num))
        ]

        # Displays the results of the filter to the user via commandline, stores values in list for later
        list_of_plan_folder_paths = []

        for index, row in fourth_filtered_df.iterrows():
            list_of_plan_folder_paths.append(row["Path"])
            print(
                f"Plan set found:\n{row['Yr']}-{row['Type']}-{row['Archno']}\n{row['Commnt']}\n{row['Path']}\n\n"
            )

        dict_of_all_paths = {}

        for folder in list_of_plan_folder_paths:
            dict_of_all_paths[folder] = self.get_tiff_files(folder)

        # Loop through each folder that was found, uses a natural sorting algo imported at top of file
        for folder, list_of_files in dict_of_all_paths.items():
            sorted_file_list = natsorted(list_of_files)

            tiff_objects_list = []

            # Create a folder to put the pdf plans into if it doesn't exist
            if os.path.exists(f"W:\\CivilPy_Output\\pulled_plans\\{self.SFN}"):
                pass
            else:
                os.mkdir(f"W:\\CivilPy_Output\\pulled_plans\\{self.SFN}")

            file_set_name = Path(sorted_file_list[0]).parent.name

            # Turns a list of file paths into a list of tiff objects loaded into memory
            for file in sorted_file_list:
                tiff_objects_list.append(tifftools.read_tiff(file))

            # Converts single page tiffs into multi-page tiffs
            for tiff_object in tiff_objects_list[1:]:
                tiff_objects_list[0]["ifds"].extend(tiff_object["ifds"])

            # Check if file exists, move on if so
            if os.path.exists(
                f"W:\\CivilPy_Output\\pulled_plans\\{self.SFN}\\{file_set_name}.tiff"
            ):
                pass
            else:
                print(
                    f"\nWriting tiff file to W:\\CivilPy_Output\\pulled_plans\\{self.SFN}\\{file_set_name}.tiff...\n"
                )
                try:
                    tifftools.write_tiff(
                        tiff_objects_list[0],
                        f"W:\\CivilPy_Output\\pulled_plans\\{self.SFN}\\{file_set_name}.tiff",
                    )
                except AttributeError:
                    print(
                        f"There is a problem with the tiff file at \nW:\\CivilPy_Output\\"
                        f"pulled_plans\\{self.SFN}\\{file_set_name}.tiff\nYou might want to check there"
                        f"to resolve the issue\n\n"
                    )

            # Convert multipage tiff file to pdf
            try:
                self.tiff_to_pdf(
                    f"W:\\CivilPy_Output\\pulled_plans\\{self.SFN}\\{file_set_name}.tiff"
                )
            except:
                print(
                    f"There was an error during conversion of the file: W:\\CivilPy_Output\\pulled_plans\\{self.SFN}"
                    f"\\{file_set_name}.tiff, it's possibly corrupted"
                )

        return f"Files written to W:\\CivilPy_Output\\pulled_plans\\"

    def get_tiff_files(self, path):
        """
        This is a helper function to the self.get_d6_plansets() function, giving it a path to a folder returns a
        list of all files in that folder

        :return: list of tiff file paths
        """
        # Build a list of tiff files in the folder:
        root_path = Path(path)

        # List all the files in that directory location
        all_tiff_files = os.listdir(root_path)

        # Filter by tiff files
        tif_files = [f for f in all_tiff_files if f.lower().endswith(".tif")]

        # Display all the files for that plan set
        all_tiff_files = []

        print(f"folder: {path}")
        for file in tif_files:
            all_tiff_files.append(f"{root_path}\\{file}")
            print(f"{root_path}\\{file}", sep="\n")

        print("\n")

        return all_tiff_files

    def tiff_to_pdf(self, tiff_path: str) -> str:
        """
        Helper function to be used by the bridge object to convert tiff files to pdf
        :param tiff_path:
        :return:
        """
        pdf_path = tiff_path.replace(".tiff", ".pdf")
        if not os.path.exists(tiff_path):
            raise Exception(f"{tiff_path} Not found.")
        image = Image.open(tiff_path)

        images = []
        for i, page in enumerate(ImageSequence.Iterator(image)):
            page = page.convert("RGB")
            images.append(page)
        if len(images) == 1:
            images[0].save(pdf_path)
        else:
            images[0].save(pdf_path, save_all=True, append_images=images[1:])
        return pdf_path
