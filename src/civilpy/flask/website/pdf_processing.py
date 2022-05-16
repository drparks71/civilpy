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
import json


def get_data_from_pdf(user, path):
    """
    Function to pull data from a json file and load it into the applications html template
    # //TODO - move this function out of this file
    """
    x = os.listdir(f"uploads/{user}")
    for value in x:
        if not value:
            pass
        else:
            with open(f"uploads/{user}/{value}", "r") as f:
                response = json.load(f)

    return response
