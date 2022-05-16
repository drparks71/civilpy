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

# importing all necessary modules
# like MDApp, MDLabel Screen, MDTextField
# and MDRectangleFlatButton
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton


# creating Demo Class(base class)
class Demo(MDApp):

    def build(self):
        screen = Screen()

        # defining label with all the parameters
        l = MDLabel(
            text="HI PEOPLE!",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.5, 0, 0.5, 1),
            font_style="Caption",
        )

        # defining Text field with all the parameters
        name = MDTextField(
            text="Enter name",
            pos_hint={"center_x": 0.8, "center_y": 0.8},
            size_hint_x=None,
            width=100,
        )

        # defining Button with all the parameters
        btn = MDRectangleFlatButton(
            text="Submit",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            on_release=self.btnfunc,
        )
        # adding widgets to screen
        screen.add_widget(name)
        screen.add_widget(btn)
        screen.add_widget(l)
        # returning the screen
        return screen

    # defining a btnfun() for the button to
    # call when clicked on it
    def btnfunc(self, obj):
        print("button is pressed!!")


if __name__ == "__main__":
    Demo().run()
