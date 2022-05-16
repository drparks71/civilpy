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
from pathlib import Path


# Create a class object to hold functions and values
class MicrostationPidginScript:
    def __init__(self):
        """
        Defines the attributes of the class, for this class the primary thing we'll be building is a set of
        instructions for the script to execute.
        """
        self.text = ""
        self.set_level()
        self.set_color()
        self.set_style()
        self.set_weight()

    def create_script_file(self, file_name: str = "test1.txt"):
        """
        Creates the Script file to actually be run in MicroStation family of products

        :param file_name: (str) The location the script file will be saved to, relative to present working python
            directory

        :returns: None, opens and saves file to disk
        """
        with open(f"scripts/{file_name}", "w") as f:
            f.write(self.text)

        print(f"Script file:\n\t@{Path(os.getcwd() + '/scripts/' + file_name)}")

    def print_script_as_command(self):
        self.text = self.text.replace("\n", ";")
        print(self.text)

    def set_level(self, level=1):
        """
        Sets the current level the object is working with

        :param level:(int) the level you want to set active
        :returns: None, updates self.text string within object for writing to file later
        """
        self.text += f"LV={level}\n"

    def set_color(self, color=1):
        """
        Sets the current color the object is working with

        :param color:(int) the level you want to set active
        :returns: None, updates self.text string within object for writing to file later
        """
        self.text += f"CO={color}\n"

    def set_style(self, style=1):
        """
        Sets the current Line Style the object is working with

        :param style:(int) the style you want to set active
        :returns: None, updates self.text string within object for writing to file later
        """
        self.text += f"LC={style}\n"

    def set_weight(self, weight=1):
        """
        Sets the current Line weight the object is working with

        :param weight:(int) the weight you want to set active
        :returns: None, updates self.text string within object for writing to file later
        """
        self.text += f"WT={weight}\n"

    def place_circle_radius(self, radius: int = 10, location: str = None):
        """
        Places a circle of a specified radius, in a specified location

        :param:
            radius: (int) The radius of the circle to place
            location: (str) The location to place the circle
        :returns:
            None, updates self.text string within object for writing to file later
        """
        if location is None:
            self.text += f"E,Place Circle Radius;T,{radius};M,Placed Circle Radius = {radius};%d;null\n"
        else:
            self.text += f"E,Place Circle Radius;T,{radius};M,Placed Circle Radius = {radius};{location};null\n"

    def print_message(
        self,
        location: str = "left",
        style: str = "status",
        message: str = "Message Default",
    ):
        """
        Displays a message to the user in various ways depending on values

        :param
            location:(str) left/right - The side of the bar to display the message on
            stye:(str) prompt/status - The type of message to display
            message:(str) The message to display

        :returns:
            None, updates self.text string within object for writing to file later
        """

        if location.lower() == "left" and style.lower() == "prompt":
            self.text += f"M,CF {message}\n"
        elif location.lower() == "left" and style.lower() == "status":
            self.text += f"M,ER {message}\n"
        elif location.lower() == "right" and style.lower() == "prompt":
            self.text += f"M,PR {message}\n"
        elif location.lower() == "right" and style.lower() == "status":
            self.text += f"M,ST {message}\n"
        else:
            print(
                f"ERROR print_message({location}, {style}, {message}) combination resulted in error, check docs"
            )

    def create_sheet_model(
        self,
        model_type: str = "design",
        name: str = "Untitled Sheet",
        description: str = "",
    ):
        """
        Adds the create sheet model dialog to the script

        :param
            model_type: (str) design/sheet/drawing - The type of model to create
            name: (str) The name of the model
            description: (str) Description of the model

        :returns:
            None, updates self.text string within object for writing to file later
        """
        self.text += f'model create sheet "{name}" "{description}"\n'

    def insert_cell(self, default_cell: str = "A-1-b"):
        """
        Inserts an "insert cell" dialogue into the script

        :param
            default_cell: (str) The name of the Cell to insert into the drawing, any cell name in the library can be
            used

        :returns:
            None, updates self.text string within object for writing to file later
        """
        self.text += f"ac={default_cell}\nplace cell interactive absolute;/d\n"

    def insert_border(self, default_border="BORDER_3N"):
        """
        Helper function of the insert_cell function, that defaults to the "BORDER_3N" cell

        :param
            default_border: (str) The name of the border Cell to insert into the drawing, any cell name in the
            library can be used

        :returns:
            None, updates self.text string within object for writing to file later
        """
        self.insert_cell(default_cell=default_border)

    def select_model(self):
        """
        Allows user to change the active model
        """
        self.text += f"model manager;/d/n"

    def clear_text(self):
        """
        Resets the text in the active object
        """
        self.text = ""
