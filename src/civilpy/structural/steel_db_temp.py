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
import sqlite3
import pandas as pd
from dataclasses import dataclass, field

from civilpy.general import units
from civilpy.structural.res.definitions import A325_bolt_weights

def get_steel_table():
    """
    Query the entire steel_shapes table from the database and return it as a pandas DataFrame.
    """
    # Resolve the relative path to the database
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "civilpy.db")

    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)

    try:
        # Query all records from the steel_shapes table
        query = "SELECT * FROM steel_shapes"
        steel_tables = pd.read_sql_query(query, connection)  # Read results directly into a DataFrame
        return steel_tables
    except sqlite3.Error as e:
        raise RuntimeError(f"Database query failed: {e}")
    finally:
        # Ensure the database connection is always closed
        connection.close()


def conv_frac_str(fraction_string: str) -> float:
    try:
        return float(fraction_string)
    except ValueError:
        num, denominator = fraction_string.split("/")
        try:
            leading, num = num.split()
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denominator)
        return whole - frac if whole < 0 else whole + frac


@dataclass
class SteelSection:
    label: str  # Identifier for the section (e.g., "W44X335")

    # Define all attributes (shared for all sections)
    special_note: str = field(init=False, default=None)
    weight: float = field(init=False, default=None)
    area: float = field(init=False, default=None)
    W: float = field(init=False, default=None)

    I_x: float = field(init=False, default=None)
    Z_x: float = field(init=False, default=None)
    S_x: float = field(init=False, default=None)
    r_x: float = field(init=False, default=None)


    I_y: float = field(init=False, default=None)
    Z_y: float = field(init=False, default=None)
    S_y: float = field(init=False, default=None)
    r_y: float = field(init=False, default=None)


    def query_database(self):
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "civilpy.db")
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        try:
            query = """
                SELECT * FROM steel_shapes WHERE EDI_Std_Nomenclature = ?
            """
            cursor.execute(query, (self.label,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error occurred: {e}")
        finally:
            connection.close()

    def __post_init__(self):
        # Adjust for user input
        self.label = self.label.upper()
        row = self.query_database()

        if row:
            # Assign shared attributes dynamically
            self.special_note = row["T_F"]
            self.weight = row["W"]
            self.W = row["W"]
            self.area = row["A"]

            self.I_x = row["Ix"]
            self.Z_x = row["Zx"]
            self.S_x = row["Sx"]
            self.r_x = row["rx"]

            self.I_y = row["Iy"]
            self.Z_y = row["Zy"]
            self.S_y = row["Sy"]
            self.r_y = row["ry"]

        else:
            raise ValueError(f"No section found with label '{self.label}'")


@dataclass
class W(SteelSection):
    depth: float = field(init=False, default=None)
    d: float = field(init=False, default=None)
    ddet: float = field(init=False, default=None)
    bf: float = field(init=False, default=None)
    bfdet: float = field(init=False, default=None)
    flange_width: float = field(init=False, default=None)
    tw: float = field(init=False, default=None)
    twdet: float = field(init=False, default=None)
    twdet_2: float = field(init=False, default=None)
    tf: float = field(init=False, default=None)
    tfdet: float = field(init=False, default=None)
    kdes: float = field(init=False, default=None)
    kdet: float = field(init=False, default=None)
    J: float = field(init=False, default=None)
    Cw: float = field(init=False, default=None)
    Wno: float = field(init=False, default=None)
    Sw1: float = field(init=False, default=None)
    Qf: float = field(init=False, default=None)
    Qw: float = field(init=False, default=None)
    rts: float = field(init=False, default=None)
    ho: float = field(init=False, default=None)
    PA: float = field(init=False, default=None)
    PB: float = field(init=False, default=None)
    PC: float = field(init=False, default=None)
    PD: float = field(init=False, default=None)
    T: float = field(init=False, default=None)
    bf_2tf: float = field(init=False, default=None)
    h_tw: float = field(init=False, default=None)
    k1: float = field(init=False, default=None)
    WGi: float = field(init=False, default=None)
    WGo: float = field(init=False, default=None)


    def __post_init__(self):
        # Handle missing or incorrectly formatted prefixes
        if not self.label.upper().startswith("W"):
            self.label = f"W{self.label.upper()}"

        super().__post_init__()

        # Subclass-specific initialization
        row = self.query_database()
        if row:
            self.depth = row["d"]
            self.flange_width = row["bf"]
            self.depth = row["d"]
            self.d = row["d"]
            self.ddet = row["ddet"]
            self.bf = row["bf"]
            self.bfdet = row["bfdet"]
            self.flange_width = row["bf"]
            self.tw = row["tw"]
            self.twdet = row["twdet"]
            self.twdet_2 = row["twdet/2"]
            self.tf = row["tf"]
            self.tfdet = row["tfdet"]
            self.kdes = row["kdes"]
            self.kdet = row["kdet"]
            self.J = row["J"]
            self.Cw = row["Cw"]
            self.Wno = row["Wno"]
            self.Sw1 = row["Sw1"]
            self.Qf = row["Qf"]
            self.Qw = row["Qw"]
            self.rts = row["rts"]
            self.ho = row["ho"]
            self.PA = row["PA"]
            self.PB = row["PB"]
            self.PC = row["PC"]
            self.PD = row["PD"]
            self.T = row["T"]
            self.bf_2tf = row["bf/2tf"]
            self.h_tw = row["h/tw"]
            self.k1 = row["k1"]
            self.WGi = row["WGi"]
            self.WGo = row["WGo"]


@dataclass
class M(SteelSection):
    depth: float = field(default=None)  # Match with "d"
    flange_width: float = field(default=None)  # Match with "bf"
    web_thickness: float = field(default=None)  # Match with "tw"

    ATTRIBUTE_TO_COLUMN = {
        "depth": "d",
        "flange_width": "bf",
        "web_thickness": "tw",
    }
    ATTRIBUTE_TYPES = {
        "depth": float,
        "flange_width": float,
        "web_thickness": float,
    }


@dataclass
class S(SteelSection):
    depth: float = field(default=None)  # Match with "d"
    flange_width: float = field(default=None)  # Match with "bf"
    web_thickness: float = field(default=None)  # Match with "tw"
    flange_thickness: float = field(default=None)  # Match with "tf"
    J: float = field(default=None)  # Match with "J"

    ATTRIBUTE_TO_COLUMN = {
        "depth": "d",
        "flange_width": "bf",
        "web_thickness": "tw",
        "flange_thickness": "tf",
        "J": "J",
    }
    ATTRIBUTE_TYPES = {
        "depth": float,
        "flange_width": float,
        "web_thickness": float,
        "flange_thickness": float,
        "J": float,
    }


@dataclass
class HP(SteelSection):
    depth: float = field(default=None)  # Match with "d"
    flange_width: float = field(default=None)  # Match with "bf"
    web_thickness: float = field(default=None)  # Match with "tw"
    flange_thickness: float = field(default=None)  # Match with "tf"

    ATTRIBUTE_TO_COLUMN = {
        "depth": "d",
        "flange_width": "bf",
        "web_thickness": "tw",
        "flange_thickness": "tf",
    }
    ATTRIBUTE_TYPES = {
        "depth": float,
        "flange_width": float,
        "web_thickness": float,
        "flange_thickness": float,
    }


@dataclass
class C(SteelSection):
    depth: float = field(default=None)  # Match with "d"
    flange_width: float = field(default=None)  # Match with "bf"
    web_thickness: float = field(default=None)  # Match with "tw"

    ATTRIBUTE_TO_COLUMN = {
        "depth": "d",
        "flange_width": "bf",
        "web_thickness": "tw",
    }
    ATTRIBUTE_TYPES = {
        "depth": float,
        "flange_width": float,
        "web_thickness": float,
    }


@dataclass
class L(SteelSection):
    leg1_length: float = field(default=None)  # Match with "l1"
    leg2_length: float = field(default=None)  # Match with "l2"
    thickness: float = field(default=None)  # Match with "t"

    ATTRIBUTE_TO_COLUMN = {
        "leg1_length": "l1",
        "leg2_length": "l2",
        "thickness": "t",
    }
    ATTRIBUTE_TYPES = {
        "leg1_length": float,
        "leg2_length": float,
        "thickness": float,
    }


@dataclass
class M(SteelSection):
    depth: float = field(default=None)
    flange_width: float = field(default=None)
    web_thickness: float = field(default=None)

    ATTRIBUTE_TO_COLUMN = {
        "depth": "d",
        "flange_width": "bf",
        "web_thickness": "tw",
    }
    ATTRIBUTE_TYPES = {
        "depth": float,
        "flange_width": float,
        "web_thickness": float,
    }


@dataclass
class S(SteelSection):
    depth: float = field(default=None)
    flange_width: float = field(default=None)
    web_thickness: float = field(default=None)
    flange_thickness: float = field(default=None)
    J: float = field(default=None)

    ATTRIBUTE_TO_COLUMN = {
        "depth": "d",
        "flange_width": "bf",
        "web_thickness": "tw",
        "flange_thickness": "tf",
        "J": "J",
    }
    ATTRIBUTE_TYPES = {
        "depth": float,
        "flange_width": float,
        "web_thickness": float,
        "flange_thickness": float,
        "J": float,
    }


@dataclass
class HP(SteelSection):
    depth: float = field(default=None)
    flange_width: float = field(default=None)
    web_thickness: float = field(default=None)
    flange_thickness: float = field(default=None)

    ATTRIBUTE_TO_COLUMN = {
        "depth": "d",
        "flange_width": "bf",
        "web_thickness": "tw",
        "flange_thickness": "tf",
    }
    ATTRIBUTE_TYPES = {
        "depth": float,
        "flange_width": float,
        "web_thickness": float,
        "flange_thickness": float,
    }


@dataclass
class C(SteelSection):
    depth: float = field(default=None)
    flange_width: float = field(default=None)
    web_thickness: float = field(default=None)

    ATTRIBUTE_TO_COLUMN = {
        "depth": "d",
        "flange_width": "bf",
        "web_thickness": "tw",
    }
    ATTRIBUTE_TYPES = {
        "depth": float,
        "flange_width": float,
        "web_thickness": float,
    }


@dataclass
class L(SteelSection):
    leg1_length: float = field(default=None)
    leg2_length: float = field(default=None)
    thickness: float = field(default=None)

    ATTRIBUTE_TO_COLUMN = {
        "leg1_length": "l1",
        "leg2_length": "l2",
        "thickness": "t",
    }
    ATTRIBUTE_TYPES = {
        "leg1_length": float,
        "leg2_length": float,
        "thickness": float,
    }


@dataclass
class WT(SteelSection):
    depth: float = field(default=None)
    flange_width: float = field(default=None)
    web_thickness: float = field(default=None)
    flange_thickness: float = field(default=None)

    ATTRIBUTE_TO_COLUMN = {
        "depth": "d",
        "flange_width": "bf",
        "web_thickness": "tw",
        "flange_thickness": "tf",
    }
    ATTRIBUTE_TYPES = {
        "depth": float,
        "flange_width": float,
        "web_thickness": float,
        "flange_thickness": float,
    }


@dataclass
class MT(SteelSection):
    depth: float = field(default=None)
    flange_width: float = field(default=None)
    web_thickness: float = field(default=None)
    flange_thickness: float = field(default=None)

    ATTRIBUTE_TO_COLUMN = {
        "depth": "d",
        "flange_width": "bf",
        "web_thickness": "tw",
        "flange_thickness": "tf",
    }
    ATTRIBUTE_TYPES = {
        "depth": float,
        "flange_width": float,
        "web_thickness": float,
        "flange_thickness": float,
    }


@dataclass
class Pipe(SteelSection):
    outer_diameter: float = field(default=None)
    wall_thickness: float = field(default=None)
    area: float = field(default=None)

    ATTRIBUTE_TO_COLUMN = {
        "outer_diameter": "od",
        "wall_thickness": "t",
        "area": "area",
    }
    ATTRIBUTE_TYPES = {
        "outer_diameter": float,
        "wall_thickness": float,
        "area": float,
    }


@dataclass
class TwoL(SteelSection):
    leg1_length: float = field(default=None)
    leg2_length: float = field(default=None)
    thickness: float = field(default=None)
    spacing: float = field(default=None)

    ATTRIBUTE_TO_COLUMN = {
        "leg1_length": "l1",
        "leg2_length": "l2",
        "thickness": "t",
        "spacing": "spacing",
    }
    ATTRIBUTE_TYPES = {
        "leg1_length": float,
        "leg2_length": float,
        "thickness": float,
        "spacing": float,
    }


@dataclass
class HSS(SteelSection):
    shape_type: str = field(default=None)
    depth: float = field(default=None)
    width: float = field(default=None)
    thickness: float = field(default=None)

    ATTRIBUTE_TO_COLUMN = {
        "shape_type": "type",
        "depth": "H",
        "width": "B",
        "thickness": "t",
    }
    ATTRIBUTE_TYPES = {
        "shape_type": str,
        "depth": float,
        "width": float,
        "thickness": float,
    }





def get_bolt_weights(length: float, diameter: float, no_of_washers: int) -> float:
    """
    Function to get the bolt weights from the A325_bolt_weights dictionary and calculate the weight per bolt if it's
    not contained in the table.

    Original table from:
    https://www.portlandbolt.com/print/?table=7587

    The A325_bolt_weights dictionary reports the weight indexed by bolt length and diameter, and reports the value in
    lbs/100 bolts. This function simplifies that by reducing the value to that of a single bolt.

    If bolt weights are not contained in the dictionary, the function will utilize the following formula to calculate
    the weight per bolt, if no_of_washers is greater than 0, it will include the weight of the washers in the
    calculation with the following values:

    Per inch Adder (dia):
        0.5: 5.5
        0.625: 8.6
        0.75: 12.4
        0.875: 16.9
        1.0: 22.1
        1.125: 28
        1.25: 34.4
        1.375: 42.5
        1.5: 49.7

    F436 Round Washers
        0.5: 2.1
        0.625: 3.6
        0.75: 4.8
        0.875: 7
        1.0: 9.4
        1.125: 11.3
        1.25: 13.8
        1.375: 16.8
        1.5: 20

    Weight in table includes the weight of nuts.

    Parameters
    -------
    length : float
    diameter : float
    no_of_washers : int

    Returns
    -------
    Weight : float - the weight of the individual bolt
    """

    # Test if the inputs are in the table or if the formula must be used to calculate weight
    if length in A325_bolt_weights.keys() and diameter in A325_bolt_weights[9].keys():
        total_weight = A325_bolt_weights[length][diameter]

    # Make sure user input is one of the available diameters
    elif (
        diameter not in A325_bolt_weights[9].keys()
        or length not in A325_bolt_weights.keys()
    ):
        print(
            "\nNon-existant diameter or length used, please use a value from the following list:"
        )
        print(
            "\n\t0.5\n\t0.625\n\t0.75\n\t0.875\n\t1.0\n\t1.125\n\t1.25\n\t1.375\n\t1.5\n\n"
        )

        return None

    # Calculates the weight of bolts longer than 9", uses 6" bolt to have all dias
    elif diameter in A325_bolt_weights[9].keys() and length > max(
        A325_bolt_weights.keys()
    ):
        length_adder = {
            0.5: 5.5,
            0.625: 8.6,
            0.75: 12.4,
            0.875: 16.9,
            1.0: 22.1,
            1.125: 28,
            1.25: 34.4,
            1.375: 42.5,
            1.5: 49.7,
        }

        added_length = length - 6
        total_weight = (
            A325_bolt_weights[6][diameter] + added_length * length_adder[diameter]
        )

    # Adds washer weight if no of washers > 0
    for washer in range(0, no_of_washers, 1):
        washer_weight = {
            0.5: 2.1,
            0.625: 3.6,
            0.75: 4.8,
            0.875: 7,
            1.0: 9.4,
            1.125: 11.3,
            1.25: 13.8,
            1.375: 16.8,
            1.5: 20,
        }

        total_weight = total_weight + washer_weight[diameter]

    return round((total_weight / 100), 3) * units.lbs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
