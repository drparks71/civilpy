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

# These are required for the script to start working
os.chdir("C:\\Program Files\\Bentley\\MicroStation 2024\\MicroStation\\")

import sys

sys.path.append("C:\\Program Files\\Bentley\\MicroStation 2024\\MicroStation\\")

import os

# All DLLs Microstation Depends on
os.add_dll_directory(r"C:\Program Files\Bentley\ProjectWise\bin\v1000")
os.add_dll_directory(r"C:\Program Files\Bentley\ProjectWise\bin")
os.add_dll_directory(r"C:\Program Files\Bentley\MicroStation 2024\MicroStation")
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\smartsolid"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\acis"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\luxology"
)
# os.add_dll_directory(r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\pointools")
os.add_dll_directory(r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlapps")
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\assemblies"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\required"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\filehandler"
)
# os.add_dll_directory(r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\filehandler\DgnDbPlatform")
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue\Application"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue\Environment"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue\Kernels"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue\Modules"
)
# os.add_dll_directory(r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue\Python")
os.add_dll_directory(r"C:\Users\dane.parks\AppData\Local\anaconda3\envs\microstation")
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\filehandler\RealDwg2025"
)
os.add_dll_directory(r"C:\Program Files\Bentley\ProjectWise\bin")
os.add_dll_directory(r"C:\Program Files\Bentley\ProjectWise\bin\v1000")
os.add_dll_directory(r"C:\Program Files\Bentley\MicroStation 2024\MicroStation")
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\smartsolid"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\acis"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\luxology"
)
# os.add_dll_directory(r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\pointools")
os.add_dll_directory(r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlapps")
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\assemblies"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\required"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\filehandler"
)
# os.add_dll_directory(r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\filehandler\DgnDbPlatform")
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue\Application"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue\Environment"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue\Kernels"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue\Modules"
)
# os.add_dll_directory(r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\vue\Python")
os.add_dll_directory(r"C:\Users\dane.parks\AppData\Local\anaconda3\envs\microstation")
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\filehandler\RealDwg2025"
)
os.add_dll_directory(
    r"C:\Program Files (x86)\Common Files\Intel\Shared Libraries\intel64\libfabric\bin"
)
os.add_dll_directory(
    r"C:\Program Files (x86)\Common Files\Intel\Shared Libraries\intel64\libfabric\bin\utils"
)
os.add_dll_directory(
    r"C:\Program Files (x86)\Common Files\Intel\Shared Libraries\intel64\bin"
)
os.add_dll_directory(r"C:\Program Files (x86)\Common Files\Intel\Shared Libraries\ia32")
os.add_dll_directory(
    r"C:\Program Files (x86)\Common Files\Intel\Shared Libraries\intel64"
)
os.add_dll_directory(r"C:\Program Files (x86)\Common Files\Intel\Shared Libraries")
os.add_dll_directory(r"C:\Program Files\Python310\Scripts")
os.add_dll_directory(r"C:\Program Files\Python310")
os.add_dll_directory(
    r"C:\Program Files (x86)\Common Files\Intel\Shared Libraries\redist\intel64_win\compiler"
)
os.add_dll_directory(r"C:\WINDOWS\system32")
os.add_dll_directory(r"C:\WINDOWS")
os.add_dll_directory(r"C:\WINDOWS\System32\Wbem")
os.add_dll_directory(r"C:\WINDOWS\System32\WindowsPowerShell\v1.0")
os.add_dll_directory(r"C:\WINDOWS\System32\OpenSSH")
os.add_dll_directory(r"C:\Program Files\dotnet")
os.add_dll_directory(
    r"C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn"
)
os.add_dll_directory(r"C:\Program Files (x86)\Microsoft SQL Server\150\Tools\Binn")
os.add_dll_directory(r"C:\Program Files\Microsoft SQL Server\150\Tools\Binn")
os.add_dll_directory(r"C:\Program Files\Microsoft SQL Server\150\DTS\Binn")
os.add_dll_directory(r"C:\Program Files (x86)\Microsoft SQL Server\150\DTS\Binn")
os.add_dll_directory(r"C:\Program Files\Azure Data Studio\bin")
os.add_dll_directory(r"C:\Program Files\nodejs")
os.add_dll_directory(r"C:\Program Files\Docker\Docker\resources\bin")
os.add_dll_directory(r"C:\Program Files\Git\cmd")
os.add_dll_directory(r"C:\Users\dane.parks\Drivers")
os.add_dll_directory(
    r"C:\Users\dane.parks\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
)
os.add_dll_directory(r"C:\Users\dane.parks\AppData\Local\Pandoc")
os.add_dll_directory(
    r"C:\Users\dane.parks\AppData\Local\Programs\Microsoft VS Code\bin"
)
os.add_dll_directory(r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10")
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\cellmgr"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\compare"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\remover"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\fixer"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\changer"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\office"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\refmgr"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\Assemblies\ECFramework"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\Assemblies\ECFramework\extensions"
)
os.add_dll_directory(r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10")
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\cellmgr"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\compare"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\remover"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\fixer"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\changer"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\office"
)
os.add_dll_directory(
    r"C:\Users\Public\CADDServices\Bentley\3partyLocal\Axiom\V10\refmgr"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded"
)
os.add_dll_directory(
    r"C:\Program Files\Bentley\MicroStation 2024\MicroStation\mdlsys\asneeded\smartsolid"
)