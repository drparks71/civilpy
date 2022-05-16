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

import numpy as np
import pandas as pd
from civilpy.general import units
from civilpy.structural.arema import CooperE80EqStrip

import matplotlib.pyplot as plt

cooper_e80 = CooperE80EqStrip()


def find_key_for_value_in_tuple_range(data, number):
    """
    Find the key in a dictionary where the number falls between the first two values of the tuple.

    Args:
    data (dict): Dictionary containing lists of tuples.
    number (float): The number to search for within the tuple ranges.

    Returns:
    key: The key in the dictionary whose tuple contains the number, or None if not found.
    """
    for key, values in data.items():
        if len(values) >= 2 and values[0].magnitude <= number <= values[1].magnitude:
            return key
    return None


# Coordinates
default_coordinates_list = {
    # "A": (0, wall_height, find_key_for_value_in_tuple_range(cooper_e80.linear_loads, 0)), # See Excel comment - overridden to match sheet
    "A": (0, 23.9, find_key_for_value_in_tuple_range(cooper_e80.linear_loads, 0)),
    "B": (0, 0, None),
}


def build_coordinates_list(
    starting_coordinates_list=default_coordinates_list,
    total_length=38,
    num_slices=19,
    track_offset=2,
    wall_height=19.5,
    soil_height_above_wall=0,
):

    # Build a list of C values based on the user input
    for x in range(0, num_slices):
        starting_coordinates_list[f"C_{x+1}"] = (
            x * (total_length / num_slices) + track_offset,
            wall_height + soil_height_above_wall,
            find_key_for_value_in_tuple_range(
                cooper_e80.linear_loads, x * total_length / num_slices
            ),
        )
    return starting_coordinates_list


default_coordinates_list = build_coordinates_list()


class CulmannsMethod:
    def __init__(
        self,
        coordinates_list=None,
        soil_unit_weight=117.7 * units("lbf/ft^3"),
        soil_angle_int_friction=29.8 * units("degrees"),
        angle_back_wall_with_horizontal=0 * units("degrees"),
        angle_of_wall_friction_delta=0 * units("degrees"),
        angle_of_wall_friction_gamma=90 * units("degrees"),
        load_scale=2.9059 * units("kips/ft"),
        wall_height=19.5 * units("ft"),
        soil_height_above_wall=4.4 * units("ft"),
        num_slices=19,
        total_length=38 * units("ft"),
        track_offset=2 * units("ft"),
    ):
        self.coordinates_list = coordinates_list
        self.soil_unit_weight = soil_unit_weight
        self.soil_angle_int_friction = soil_angle_int_friction
        self.angle_back_wall_with_horizontal = angle_back_wall_with_horizontal
        self.angle_of_wall_friction_delta = angle_of_wall_friction_delta
        self.angle_of_wall_friction_gamma = angle_of_wall_friction_gamma
        self.load_scale = load_scale
        self.wall_height = wall_height
        self.soil_height_above_wall = soil_height_above_wall
        self.num_slices = num_slices
        self.total_length = total_length
        self.track_offset = track_offset
        self.coordinates_list = (
            default_coordinates_list if coordinates_list is None else coordinates_list
        )

        self.table = self.generate_spreadsheet(
            self.coordinates_list,
            self.soil_unit_weight,
            self.load_scale,
            self.soil_angle_int_friction,
            self.angle_back_wall_with_horizontal,
            self.angle_of_wall_friction_delta,
        )

    def calculate_a_i(self, x_val, y_val):
        """Calculate a_i (ft) based on the current coordinates."""
        result = np.sqrt((x_val * units.ft) ** 2 + (y_val * units.ft) ** 2)
        return result.to(units.ft).round(4)

    def calculate_c_i(self, current_key, keys, coordinates_list):
        """Calculate c_i (ft) based on the previous coordinates. If first point, refer to point 'A'."""
        if current_key == "C_1":
            prev_x_val, prev_y_val, _ = coordinates_list["A"]
        else:
            prev_x_val, prev_y_val, _ = coordinates_list[
                keys[keys.index(current_key) - 1]
            ]
        result = np.sqrt((prev_x_val * units.ft) ** 2 + (prev_y_val * units.ft) ** 2)
        return result.to(units.ft).round(4)

    def calculate_b_i(self, current_key, keys, coordinates_list, x_val, y_val):
        """Calculate b_i (ft) using the previous point's coordinates."""
        if current_key == "C_1":
            prev_x_val, prev_y_val, _ = coordinates_list["A"]
        else:
            prev_key = keys[keys.index(current_key) - 1]
            prev_x_val, prev_y_val, _ = coordinates_list[prev_key]
        result = np.sqrt(
            ((x_val - prev_x_val) * units.ft) ** 2
            + ((y_val - prev_y_val) * units.ft) ** 2
        )
        return result.to(units.ft).round(4)

    def calculate_s_i(self, a_i, b_i, c_i):
        """Calculate s_i (ft) as the semi-perimeter of the triangle."""
        result = (a_i + b_i + c_i) / 2
        return result.to(units.ft).round(4)

    def calculate_A_i(self, s_i, a_i, b_i, c_i):
        """Calculate area A_i (ft^2) using the formula provided."""
        try:
            area = np.sqrt(s_i * (s_i - a_i) * (s_i - b_i) * (s_i - c_i))
        except ValueError:
            area = 0 * units.ft**2  # Set to 0 if there is a math domain error
        return area.to(units.ft**2).round(4)

    def calculate_x_cgi(self, x_val, next_x_val):
        """Calculate x_{cgi} (ft) as the center of gravity x-coordinate."""
        result = ((x_val + next_x_val) / 3) * units.ft
        return result.to(units.ft).round(4)

    def calculate_y_cgi(self, y_val, next_y_val):
        """Calculate y_{cgi} (ft) as the center of gravity y-coordinate."""
        result = ((y_val + next_y_val) / 3) * units.ft
        return result.to(units.ft).round(4)

    def calculate_running_total(self, values):
        """Calculate running total (ft) for a list of values."""
        total = 0 * units.ft
        running_totals = []
        for value in values:
            total += value
            running_totals.append(total.to(units.ft))
        return running_totals

    def calculate_w_i(self, A_i, soil_unit_weight):
        """Calculate w_i (lbf/ft) as the incremental weight of the triangle per unit length."""
        volume = (
            A_i * units.ft
        )  # The height of each wedge in 3D space would be 1 ft for consistency
        result = (volume * soil_unit_weight / units.ft).to(units.lbf / units.ft)
        return result.to_compact().round(4)

    def calculate_cumulative_weights(self, values):
        """Calculate cumulative weights (lbf/ft) for a list of values."""
        total = 0 * units.lbf / units.ft
        cumulative_weights = []
        for value in values:
            total += value
            cumulative_weights.append(total.to(units.lbf / units.ft).round(4))
        return cumulative_weights

    # //TODO - Units are wonky here - Verify formula
    def calculate_ll_surcharge(self, b_i):
        return (
            (80000 * units.lbf * 4 / 18 / 8.5 * b_i.magnitude).to(units("lbf")).round(4)
        )

    # //TODO - Units are wonky here - Verify formula
    def calculate_x_ci(self, total_weight, load_scale, soil_angle_int_friction):
        """
        Calculate x_ci using the formula:
        x_ci = Total Weight * (1 / load_scale / 1000) * cos(soil_angle_int_friction)

        Args:
        total_weight (pint.Quantity): The total weight in lbf/ft.
        load_scale (float): The load scale factor.
        soil_angle_int_friction (float): Soil angle of internal friction in radians.

        Returns:
        float: The calculated x_ci in ft.
        """
        return (
            total_weight.magnitude
            * (1 / load_scale / 1000)
            * np.cos(soil_angle_int_friction)
        ).round(4)

    def calculate_y_ci(self, x_ci, soil_angle_int_friction):
        """
        Calculate y_ci using the formula:
        y_ci = x_ci * tan(soil_angle_int_friction)

        Args:
        x_ci (float): The x_ci value in ft.
        soil_angle_int_friction (float): Soil angle of internal friction in radians.

        Returns:
        float: The calculated y_ci in ft.
        """
        return (x_ci * np.tan(soil_angle_int_friction)).round(4)

    def calculate_x_ci_prime(
        self,
        y_ci,
        x_ci,
        angle_back_wall_with_horizontal,
        angle_of_wall_friction_delta,
        soil_angle_int_friction,
        D,
        C,
    ):
        tan_term = np.tan(
            np.pi / 2
            + angle_back_wall_with_horizontal.to("radians")
            + angle_of_wall_friction_delta.to("radians")
            + soil_angle_int_friction.to("radians")
        )
        denominator = D / C - tan_term
        if denominator == 0:
            raise ZeroDivisionError(
                "Denominator in calculation of x_{c'i} resulted in zero."
            )
        return ((y_ci - tan_term * x_ci) / denominator).round(4)

    def sort_keys(self, keys):
        # Extract the numerical part of the keys and sort
        return sorted(keys, key=lambda x: int(x.split("_")[1]))

    def generate_spreadsheet(
        self,
        coordinates_list,
        soil_unit_weight,
        load_scale,
        soil_angle_int_friction,
        angle_back_wall_with_horizontal,
        angle_of_wall_friction_delta,
    ):
        """
        Calculate various columns for soil and wall friction analysis.

        Args:
        coordinates_list (dict): Dictionary containing coordinate points.
        soil_unit_weight (float): The unit weight of the soil.
        load_scale (float): Load scale value.
        soil_angle_int_friction (float): Angle of internal friction of soil in radians.
        angle_back_wall_with_horizontal (float): Angle between back of wall and horizontal in radians.
        angle_of_wall_friction_delta (float): Angle of wall friction in radians.

        Returns:
        pd.DataFrame: DataFrame containing computed columns.
        """
        results = []

        # Sorting keys numerically based on their suffix
        keys = self.sort_keys(
            [key for key in list(coordinates_list.keys()) if key not in ["A", "B"]]
        )

        phi = soil_angle_int_friction
        tan_phi = np.tan(phi)

        # Calculate max y value and k_Phi
        max_y_val = max([y for _, y, _ in coordinates_list.values()])
        k_Phi = max_y_val / tan_phi
        max_y_val_div_k_Phi = max_y_val / k_Phi

        # Initialize lists for storing intermediate values
        x_cgi_list, y_cgi_list, w_i_list = [], [], []
        cumulative_LL_surcharge = 0 * units.lbf / units.ft

        for key in keys:
            x_val, y_val, _ = coordinates_list[key]

            # Calculate various parameters
            a_i = self.calculate_a_i(x_val, y_val)
            c_i = self.calculate_c_i(key, keys, coordinates_list)
            b_i = self.calculate_b_i(key, keys, coordinates_list, x_val, y_val)
            s_i = self.calculate_s_i(a_i, b_i, c_i)
            A_i = self.calculate_A_i(s_i, a_i, b_i, c_i)

            # Calculate x_{cgi} and y_{cgi}
            prev_x_val, prev_y_val = (
                (coordinates_list["A"][0], coordinates_list["A"][1])
                if key == "C_1"
                else coordinates_list[f'C_{int(key.split("_")[1]) - 1}'][:2]
            )
            x_cgi = self.calculate_x_cgi(prev_x_val, x_val)
            y_cgi = self.calculate_y_cgi(prev_y_val, y_val)

            x_cgi_list.append(x_cgi)
            y_cgi_list.append(y_cgi)

            # Calculate weight and cumulative live load surcharge
            w_i = self.calculate_w_i(A_i, soil_unit_weight)
            w_i_list.append(w_i)
            LL_surcharge = self.calculate_ll_surcharge(b_i) / units("ft")
            cumulative_LL_surcharge += LL_surcharge

            results.append(
                {
                    "$c_i\ (ft)$": c_i,
                    "$a_i\ (ft)$": a_i,
                    "$b_i\ (ft)$": b_i,
                    "$s_i\ (ft)$": s_i,
                    "$A_i\ (ft^2)$": A_i,
                    "$x_{cgi}\ (ft)$": x_cgi,
                    "$y_{cgi}\ (ft)$": y_cgi,
                    "$w_i\ (lbf/ft)$": w_i,
                    "$LL Surcharge\ (lbf/ft)$": round(cumulative_LL_surcharge, 4),
                }
            )

        # Calculate cumulative weights and ccgi values
        W_i_list = self.calculate_cumulative_weights(w_i_list)
        x_ccgi_list, y_ccgi_list = [], []

        for i in range(len(results)):
            if i == 0:
                x_ccgi_list.append(results[i]["$x_{cgi}\ (ft)$"])
                y_ccgi_list.append(results[i]["$y_{cgi}\ (ft)$"])
            else:
                x_ccgi = (
                    (
                        (
                            results[i]["$x_{cgi}\ (ft)$"]
                            * results[i]["$w_i\ (lbf/ft)$"]
                            + x_ccgi_list[i - 1] * W_i_list[i - 1]
                        )
                        / W_i_list[i]
                    )
                    .to(units.ft)
                    .round(4)
                )
                y_ccgi = (
                    (
                        (
                            results[i]["$y_{cgi}\ (ft)$"]
                            * results[i]["$w_i\ (lbf/ft)$"]
                            + y_ccgi_list[i - 1] * W_i_list[i - 1]
                        )
                        / W_i_list[i]
                    )
                    .to(units.ft)
                    .round(4)
                )
                x_ccgi_list.append(x_ccgi)
                y_ccgi_list.append(y_ccgi)

        # Calculate columns for each key and append to results
        for i, key in enumerate(keys):
            results[i]["$x_{ccgi}\ (ft)$"] = x_ccgi_list[i]
            results[i]["$y_{ccgi}\ (ft)$"] = y_ccgi_list[i]
            results[i]["$W_i\ (lbf/ft)$"] = W_i_list[i]
            results[i]["$Total\ Weight\ (lbf/ft)$"] = (
                W_i_list[i] + results[i]["$LL Surcharge\ (lbf/ft)$"]
            )

            # Calculate x_ci and y_ci
            x_ci = self.calculate_x_ci(
                results[i]["$Total\ Weight\ (lbf/ft)$"],
                load_scale,
                soil_angle_int_friction,
            )
            results[i]["$x_{ci}\ (ft)$"] = x_ci
            y_ci = self.calculate_y_ci(x_ci, soil_angle_int_friction)
            results[i]["$y_{ci}\ (ft)$"] = y_ci

            # Fetch x and y (former C and D) values
            x, y, _ = coordinates_list[key]

            try:
                x_ci_prime = self.calculate_x_ci_prime(
                    y_ci,
                    x_ci,
                    angle_back_wall_with_horizontal,
                    angle_of_wall_friction_delta,
                    soil_angle_int_friction,
                    y,
                    x,
                )
                results[i]["$x_{c'i}\ (ft)$"] = x_ci_prime
            except ZeroDivisionError:
                x_ci_prime = np.nan  # Handle by storing NaN
                results[i]["$x_{c'i}\ (ft)$"] = x_ci_prime

            # Calculate y_{c'i}
            y_ci_prime = (
                np.nan if np.isnan(x_ci_prime) else (y / x * x_ci_prime).round(4)
            )
            results[i]["$y_{c'i}\ (ft)$"] = y_ci_prime

            # Calculate length of line c'_i c_i
            length_of_line = (
                np.nan
                if (np.isnan(x_ci_prime) or np.isnan(y_ci_prime))
                else (
                    np.sign(y_ci_prime - x_ci_prime * max_y_val_div_k_Phi)
                    * np.sqrt(
                        (results[i]["$x_{ci}\ (ft)$"] - x_ci_prime) ** 2
                        + (results[i]["$y_{ci}\ (ft)$"] - y_ci_prime) ** 2
                    )
                ).round(4)
            )
            results[i]["$Length\ of\ Line\ c'_i c_i\ (ft)$"] = length_of_line

        # Create DataFrame from results
        df = pd.DataFrame(results)
        df.index += 1

        # Reorder columns
        df = df[
            [
                "$c_i\ (ft)$",
                "$a_i\ (ft)$",
                "$b_i\ (ft)$",
                "$s_i\ (ft)$",
                "$A_i\ (ft^2)$",
                "$x_{cgi}\ (ft)$",
                "$y_{cgi}\ (ft)$",
                "$x_{ccgi}\ (ft)$",
                "$y_{ccgi}\ (ft)$",
                "$w_i\ (lbf/ft)$",
                "$W_i\ (lbf/ft)$",
                "$LL Surcharge\ (lbf/ft)$",
                "$Total\ Weight\ (lbf/ft)$",
                "$x_{ci}\ (ft)$",
                "$y_{ci}\ (ft)$",
                "$x_{c'i}\ (ft)$",
                "$y_{c'i}\ (ft)$",
                "$Length\ of\ Line\ c'_i c_i\ (ft)$",
            ]
        ]

        return df

    def plot_results(self):
        # Extract x and y coordinates
        x_coordinates = [value[0] for value in self.coordinates_list.values()]
        y_coordinates = [value[1] for value in self.coordinates_list.values()]

        # Coordinates for points A and B
        A_x, A_y = self.coordinates_list["A"][0], self.coordinates_list["A"][1]
        B_x, B_y = self.coordinates_list["B"][0], self.coordinates_list["B"][1]

        # Create a scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(x_coordinates, y_coordinates, marker="o", color="b")

        # Annotate the points
        for key, (x, y, label) in self.coordinates_list.items():
            plt.annotate(
                key, (x, y), textcoords="offset points", xytext=(0, 10), ha="center"
            )
            # Draw lines connecting 'C' points to 'B'
            if key.startswith("C"):
                plt.plot([B_x, x], [B_y, y], "g--")

        # Highlight points A and B
        plt.scatter(A_x, A_y, color="r", zorder=5)
        plt.scatter(B_x, B_y, color="r", zorder=5)

        # Create lists to store C points
        C_x_coords = [A_x]  # Start with point A
        C_y_coords = [A_y]  # Start with point A

        # Append only the C points
        for key, (x, y, label) in self.coordinates_list.items():
            if key.startswith("C"):
                C_x_coords.append(x)
                C_y_coords.append(y)

        # Plot the ground line connecting point A with all the C points
        plt.plot(C_x_coords, C_y_coords, "k-", label="Ground Line")

        # Define the retaining wall coordinates
        top_thickness = 1.5
        base_thickness = 2
        retaining_wall_x = [
            A_x,  # Top right
            A_x - top_thickness,  # Top left
            B_x - base_thickness,  # Bottom left
            B_x,  # Bottom right
        ]
        retaining_wall_y = [
            A_y,  # Top (same as point A)
            A_y,  # Top (same height as point A)
            B_y,  # Bottom (same as point B)
            B_y,  # Bottom (same height as point B)
        ]

        # Draw the retaining wall shape with a trapezoidal face
        plt.fill(
            retaining_wall_x,
            retaining_wall_y,
            "blue",
            alpha=0.3,
            label="Retaining Wall",
        )

        # Add legend
        plt.legend()

        # Define titles and labels
        plt.title("Retaining Wall Design - Culmann's Method")
        plt.xlabel("Feet")
        plt.ylabel("Feet")
        plt.grid(True)

        # Show the plot
        plt.show()
