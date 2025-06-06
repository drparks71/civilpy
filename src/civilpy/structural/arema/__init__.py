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

from civilpy.structural.arema.steel import (
    LoadRatingMember
)
from civilpy.general import units

from civilpy.general import PrintColors
from civilpy.structural.midas import analysis_results_request

future_ballast_depth = 6 * units("in")
design_rail_spacing = 5 * units("ft")
design_rail_height = 8 * units("in")
design_tie_depth = 7 * units("in")

from dataclasses import dataclass, field
import pint

units = pint.UnitRegistry()


@dataclass
class CooperE80:
    """
    Class for providing quick access to cooper e80 loadings, provides all values
    for standard coopers e80 us the class as follows:

    loads = CooperE80()

    for all CooperE80 variants (i.e. E60) the class can be converted like so:

    e60_loads = CooperE80().to_e_series(60)
    """

    series: int = 80
    distances: list = field(
        default_factory=lambda: [
            x * units.feet
            for x in [
                0,
                8,
                13,
                18,
                23,
                32,
                37,
                43,
                48,
                56,
                64,
                69,
                74,
                79,
                88,
                93,
                99,
                104,
            ]
        ]
    )
    magnitudes: list = field(
        default_factory=lambda: [
            x * units.kips
            for x in [
                40,
                80,
                80,
                80,
                80,
                52,
                52,
                52,
                52,
                40,
                80,
                80,
                80,
                80,
                52,
                52,
                52,
                52,
            ]
        ]
    )
    distributed: dict = field(
        default_factory=lambda: {
            "distance": 109 * units.feet,
            "magnitude": 8 * units("kip/ft"),
        }
    )
    spacing: str = 59.5 * units("in")

    def __repr__(self):
        return_string = (
                "\n".join(
                    "{}: {}".format(x, y) for x, y in zip(self.distances, self.magnitudes)
                )
                + "\n"
                + "{}: {}".format(
            self.distributed["distance"], self.distributed["magnitude"]
        )
        )

        return return_string

    def __post_init__(self):
        if self.series != 80:
            new_magnitudes = [
                x * units.kips
                for x in [
                    40,
                    80,
                    80,
                    80,
                    80,
                    52,
                    52,
                    52,
                    52,
                    40,
                    80,
                    80,
                    80,
                    80,
                    52,
                    52,
                    52,
                    52,
                ]
            ]
            self.magnitudes = [x * (self.series / 80) for x in new_magnitudes]
        else:
            pass

        return self


class CooperE80EqStrip:
    """
    Class to represent Cooper's E80 loading as a series of distributed loads.

    Currently ignores the front 40k axel and starts with the first 80K axel in order to align with Geotech teams calculations done up
    to this point as well as extending the loads 1.5' in front of and behind each axel.
    """

    def __init__(self, length_of_train=150 * units.ft):
        self.tie_width: float = 8.5 * units.ft  # feet for single tie length
        self.distances: list[tuple] = [
            x * units.feet
            for x in [
                (0, 18),  # LS1 # Displayed this way to show paired distances
                (24, 43),  # LS2
                (48, 51),  # LS3
                (56, 74),  # LS4
                (80, 99),  # LS5
                (102.5,),  # LS6
            ]
        ]
        self.magnitudes: list[int] = [
            x
            for x in [
                80
                * units.kips
                * 4
                / (
                        (self.distances[0][1] - self.distances[0][0]) * self.tie_width
                ),  # LS1
                52
                * units.kips
                * 4
                / (
                        (self.distances[1][1] - self.distances[1][0]) * self.tie_width
                ),  # LS2
                40
                * units.kips
                * 1
                / (
                        (self.distances[2][1] - self.distances[2][0]) * self.tie_width
                ),  # LS3
                80
                * units.kips
                * 4
                / (
                        (self.distances[3][1] - self.distances[3][0]) * self.tie_width
                ),  # LS4
                52
                * units.kips
                * 4
                / (
                        (self.distances[4][1] - self.distances[4][0]) * self.tie_width
                ),  # LS5
                8
                * units("kips/ft")
                * (length_of_train - self.distances[5][0])
                / ((length_of_train - self.distances[5][0]) * self.tie_width),  # LS6
            ]
        ]
        self.linear_loads = {
            "LS1": (
                self.distances[0][0],
                self.distances[0][1],
                self.magnitudes[0] * self.tie_width,
            ),
            "LS2": (
                self.distances[1][0],
                self.distances[1][1],
                self.magnitudes[1] * self.tie_width,
            ),
            "LS3": (
                self.distances[2][0],
                self.distances[2][1],
                self.magnitudes[2] * self.tie_width,
            ),
            "LS4": (
                self.distances[3][0],
                self.distances[3][1],
                self.magnitudes[3] * self.tie_width,
            ),
            "LS5": (
                self.distances[4][0],
                self.distances[4][1],
                self.magnitudes[4] * self.tie_width,
            ),
            "LS6": (
                self.distances[5][0],
                length_of_train,
                self.magnitudes[5] * self.tie_width,
            ),
        }

    def __repr__(self):
        max_len = max(len(self.distances), len(self.magnitudes), len(self.linear_loads))
        rows = []

        for i in range(max_len):
            distance = f"{self.distances[i]}" if i < len(self.distances) else ""
            magnitude = f"{self.magnitudes[i]}" if i < len(self.magnitudes) else ""
            load_key_value = (
                list(self.linear_loads.items())[i]
                if i < len(self.linear_loads)
                else ("", "")
            )
            load = (
                f"{load_key_value[0]}: {load_key_value[1]}" if load_key_value[0] else ""
            )
            rows.append(f"\t{distance:<15} \t\t\t| {magnitude:<15} \t\t\t| {load}")

        table_str = "\n".join(rows)
        return (
            f"CooperE80EqStrip(\n\ttie_width={self.tie_width},"
            f"\n\tdistances          \t\t\t| magnitudes        \t\t\t\t\t| linear_loads"
            f"\n{table_str}\n)"
        )



