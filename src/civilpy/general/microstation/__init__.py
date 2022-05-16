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

# The following DLL Directory need loaded to enable the python library MSPyMstnPlatform
import os

# Default locations
directories = [
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded",
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\smartsolid",
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\assemblies"
]

def load_dll_directories(directories):
    for directory in directories:
        os.add_dll_directory(directory)

load_dll_directories(directories)

from MSPyBentley import *
from MSPyBentleyGeom import *
from MSPyECObjects import *
from MSPyDgnPlatform import *
from MSPyDgnView import *
from MSPyMstnPlatform import *
import pydevd_pycharm
import time

# Pycharm Debugging
pydevd_pycharm.settrace('127.0.0.1', port=5678, stdoutToServer=True, stderrToServer=True)

# VSCode Debugging
# debugpy.listen(('0.0.0.0',5678), in_process_debug_adapter=True)
# print("Waiting for debugger attach")
# debugpy.wait_for_client()
# debugpy.breakpoint()

# Get list of active models
models = ''

print('test')

if __name__ == "__main__":
    print('test')


"""
Classes defined in the microstation imports

Microstation doesn't allow you to easily inspect the classes contained within the API. They've been imported and
converted to lists of tuples below for inspection.
"""
