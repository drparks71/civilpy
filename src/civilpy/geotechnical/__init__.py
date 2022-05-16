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

import math
import numpy as np
import matplotlib.pyplot as plt


def rankine_active_pressure(unit_weight, height, friction_angle):
    """
    Calculate active earth pressure against an abutment using the Rankine method.

    Parameters:
    unit_weight (float): Unit weight of the soil (kN/m³ or lb/ft³)
    height (float): Height of the abutment (meters or feet)
    friction_angle (float): Internal friction angle of the soil (degrees)

    Returns:
    float: Active earth pressure (kN/m or lb/ft)
    """

    # Convert the friction angle to radians
    friction_angle_rad = math.radians(friction_angle)

    # Calculate the active earth pressure coefficient (Ka)
    Ka = math.tan(math.radians(45) - friction_angle_rad / 2) ** 2

    # Calculate the active earth pressure (Pa)
    Pa = 0.5 * unit_weight * height**2 * Ka

    return Pa


def rankine_active_pressure_with_surcharge(
    unit_weight, height, friction_angle, surcharge_load
):
    """
    Calculate active earth pressure against an abutment using the Rankine method with a surcharge load.

    Parameters:
    unit_weight (float): Unit weight of the soil (kN/m³ or lb/ft³)
    height (float): Height of the abutment (meters or feet)
    friction_angle (float): Internal friction angle of the soil (degrees)
    surcharge_load (float): Surcharge load at the surface (kN/m² or lb/ft²)

    Returns:
    float: Active earth pressure (kN/m² or lb/ft²)
    """

    # Convert the friction angle to radians
    friction_angle_rad = math.radians(friction_angle)

    # Calculate the active earth pressure coefficient (Ka)
    Ka = math.tan(math.radians(45) - friction_angle_rad / 2) ** 2

    # Calculate the active earth pressure due to soil (Pa_soil)
    Pa_soil = 0.5 * unit_weight * height**2 * Ka

    # Calculate the active earth pressure due to surcharge (Pa_surcharge)
    Pa_surcharge = surcharge_load * height * Ka

    # Total active earth pressure (Pa)
    Pa = Pa_soil + Pa_surcharge

    return Pa


def coulomb_active_pressure(
    unit_weight,
    height,
    friction_angle,
    wall_friction_angle,
    backfill_inclination,
    wall_inclination,
):
    """
    Calculate active earth pressure against an abutment using the Coulomb method.

    Parameters:
    unit_weight (float): Unit weight of the soil (kN/m³ or lb/ft³)
    height (float): Height of the abutment (meters or feet)
    friction_angle (float): Internal friction angle of the soil (degrees)
    wall_friction_angle (float): Angle of wall friction (delta) (degrees)
    backfill_inclination (float): Angle of inclination of the backfill surface (theta) (degrees)
    wall_inclination (float): Inclination of the back side of the wall (beta) (degrees)

    Returns:
    float: Active earth pressure (kN/m² or lb/ft²)
    """

    # Convert angles to radians
    phi_rad = math.radians(friction_angle)
    delta_rad = math.radians(wall_friction_angle)
    theta_rad = math.radians(backfill_inclination)
    beta_rad = math.radians(wall_inclination)

    # Calculate the active earth pressure coefficient (Ka')
    numerator = math.cos(phi_rad - theta_rad) * math.cos(theta_rad)
    denominator_part1 = math.cos(delta_rad + theta_rad) * math.cos(delta_rad)
    denominator_part2 = math.sin(phi_rad + delta_rad) * math.sin(
        phi_rad - beta_rad - delta_rad
    )
    denominator = denominator_part1 * (
        1 + math.sqrt(denominator_part2 / (math.cos(delta_rad + theta_rad) ** 2))
    )
    Ka_prime = numerator / denominator

    # Calculate the active earth pressure (Pa)
    Pa = 0.5 * unit_weight * height**2 * Ka_prime

    return Pa


def coulomb_active_pressure_with_surcharge(
    unit_weight,
    height,
    friction_angle,
    wall_friction_angle,
    backfill_inclination,
    wall_inclination,
    surcharge_load,
):
    """
    Calculate active earth pressure against an abutment using the Coulomb method with a surcharge load.

    Parameters:
    unit_weight (float): Unit weight of the soil (kN/m³ or lb/ft³)
    height (float): Height of the abutment (meters or feet)
    friction_angle (float): Internal friction angle of the soil (degrees)
    wall_friction_angle (float): Angle of wall friction (delta) (degrees)
    backfill_inclination (float): Angle of inclination of the backfill surface (theta) (degrees)
    wall_inclination (float): Inclination of the back side of the wall (beta) (degrees)
    surcharge_load (float): Surcharge load at the surface (kN/m² or lb/ft²)

    Returns:
    float: Active earth pressure (kN/m² or lb/ft²)
    """

    if (
        unit_weight < 0
        or height < 0
        or friction_angle < 0
        or wall_friction_angle < 0
        or backfill_inclination < 0
        or wall_inclination < 0
        or surcharge_load < 0
    ):
        raise ValueError("All input parameters should be non-negative.")

    phi_rad = math.radians(friction_angle)
    delta_rad = math.radians(wall_friction_angle)
    theta_rad = math.radians(backfill_inclination)
    beta_rad = math.radians(wall_inclination)

    numerator = math.cos(phi_rad - theta_rad) * math.cos(theta_rad)
    denominator_part1 = math.cos(delta_rad + theta_rad) * math.cos(delta_rad)
    denominator_part2 = math.sin(phi_rad + delta_rad) * math.sin(
        phi_rad - beta_rad - delta_rad
    )
    denominator = denominator_part1 * (
        1 + math.sqrt(denominator_part2 / (math.cos(delta_rad + theta_rad) ** 2))
    )
    Ka_prime = numerator / denominator

    soil_pressure = 0.5 * unit_weight * height**2 * Ka_prime
    surcharge_pressure = surcharge_load * height * Ka_prime
    Pa = soil_pressure + surcharge_pressure

    return Pa


def culmann_lateral_pressure(
    unit_weight, height, cohesion, friction_angle, wall_friction_angle, num_slices=100
):
    """
    Calculate horizontal lateral earth pressure using Culmann's method.

    Parameters:
    unit_weight (float): Unit weight of the soil (kN/m³)
    height (float): Height of the wall (meters)
    cohesion (float): Cohesion of the soil (kPa)
    friction_angle (float): Internal friction angle of the soil (degrees)
    wall_friction_angle (float): Wall friction angle (degrees)
    num_slices (int): Number of slices for the graphical method

    Returns:
    float: Horizontal lateral earth pressure (kPa)
    """

    # Convert angles to radians
    friction_angle_rad = np.radians(friction_angle)
    wall_friction_angle_rad = np.radians(wall_friction_angle)

    # Initialize variables
    max_pressure = 0
    best_failure_angle = 0

    # Search for the angle of the failure plane (slices of angles)
    for i in range(num_slices):
        # Angle of the failure plane (in radians)
        theta = i * (np.pi / 2) / num_slices

        # Calculate parameters for the force polygon
        t = cohesion / (unit_weight * height)
        n = (1 - np.sin(friction_angle_rad)) / (
            1 + np.sin(wall_friction_angle_rad + theta)
        )

        # Rankine's active earth pressure coefficient for given angle theta
        K_a = np.tan(np.pi / 4 - friction_angle_rad / 2) ** 2 * (1 - (t / n)) ** 2

        # Calculate horizontal earth pressure
        P_a = 0.5 * unit_weight * height**2 * K_a

        # Update the maximum pressure and best failure angle
        if P_a > max_pressure:
            max_pressure = P_a
            best_failure_angle = np.degrees(theta)

    # Plotting the failure surfaces
    theta_values = np.linspace(0, np.pi / 2, num_slices)
    pressure_values = [
        0.5
        * unit_weight
        * height**2
        * np.tan(np.pi / 4 - friction_angle_rad / 2) ** 2
        * (
            1
            - cohesion
            / (unit_weight * height)
            / (
                (1 - np.sin(friction_angle_rad))
                / (1 + np.sin(wall_friction_angle_rad + th))
            )
        )
        ** 2
        for th in theta_values
    ]

    plt.plot(np.degrees(theta_values), pressure_values)
    plt.xlabel("Failure Angle (degrees)")
    plt.ylabel("Lateral Earth Pressure (kPa)")
    plt.title("Culmann's Method - Failure Surface Analysis")
    plt.grid(True)
    plt.show()

    return max_pressure


def culmann_lateral_pressure_with_surcharge(
    unit_weight,
    height,
    cohesion,
    friction_angle,
    wall_friction_angle,
    surcharge_load,
    num_slices=100,
):
    """
    Calculate horizontal lateral earth pressure using Culmann's method including a live load surcharge.

    Parameters:
    unit_weight (float): Unit weight of the soil (kN/m³)
    height (float): Height of the wall (meters)
    cohesion (float): Cohesion of the soil (kPa)
    friction_angle (float): Internal friction angle of the soil (degrees)
    wall_friction_angle (float): Wall friction angle (degrees)
    surcharge_load (float): Live load surcharge at the surface (kPa)
    num_slices (int): Number of slices for the graphical method

    Returns:
    float: Horizontal lateral earth pressure (kPa)
    """

    # Convert angles to radians
    friction_angle_rad = np.radians(friction_angle)
    wall_friction_angle_rad = np.radians(wall_friction_angle)

    # Initialize variables
    max_pressure = 0
    best_failure_angle = 0

    # Search for the angle of the failure plane (slices of angles)
    for i in range(num_slices):
        # Angle of the failure plane (in radians)
        theta = i * (np.pi / 2) / num_slices

        # Calculate parameters for the force polygon
        t = cohesion / (unit_weight * height)
        n = (1 - np.sin(friction_angle_rad)) / (
            1 + np.sin(wall_friction_angle_rad + theta)
        )

        # Rankine's active earth pressure coefficient for given angle theta
        K_a = np.tan(np.pi / 4 - friction_angle_rad / 2) ** 2 * (1 - (t / n)) ** 2

        # Calculate horizontal earth pressure
        P_a = 0.5 * unit_weight * height**2 * K_a

        # Add the effect of the live load surcharge
        P_surcharge = surcharge_load * height * K_a

        # Total lateral pressure including surcharge
        P_total = P_a + P_surcharge

        # Update the maximum pressure and best failure angle
        if P_total > max_pressure:
            max_pressure = P_total
            best_failure_angle = np.degrees(theta)

    # Plotting the failure surfaces
    theta_values = np.linspace(0, np.pi / 2, num_slices)
    pressure_values = [
        0.5
        * unit_weight
        * height**2
        * np.tan(np.pi / 4 - friction_angle_rad / 2) ** 2
        * (
            1
            - cohesion
            / (unit_weight * height)
            / (
                (1 - np.sin(friction_angle_rad))
                / (1 + np.sin(wall_friction_angle_rad + th))
            )
        )
        ** 2
        + surcharge_load
        * height
        * np.tan(np.pi / 4 - friction_angle_rad / 2) ** 2
        * (
            1
            - cohesion
            / (unit_weight * height)
            / (
                (1 - np.sin(friction_angle_rad))
                / (1 + np.sin(wall_friction_angle_rad + th))
            )
        )
        ** 2
        for th in theta_values
    ]

    plt.plot(np.degrees(theta_values), pressure_values)
    plt.xlabel("Failure Angle (degrees)")
    plt.ylabel("Lateral Earth Pressure (kPa)")
    plt.title("Culmann's Method with Surcharge - Failure Surface Analysis")
    plt.grid(True)
    plt.show()

    return max_pressure
