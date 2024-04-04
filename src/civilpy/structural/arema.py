from civilpy.structural.midas import get_elements_by_section_index, get_api_key, midas_api
from civilpy.general import pint, units

from src.civilpy.general import PrintColors
from src.civilpy.structural.midas import analysis_results_request

from pathlib import Path
import pandas as pd
import numpy as np
import os

future_ballast_depth = 6 * units('in')
design_rail_spacing = 5 * units('ft')
design_rail_height = 8 * units('in')
design_tie_depth = 7 * units('in')


class LoadRatingMember:
    """
    Class for load rating bridge members based on the guidance in AREMA Chapter 15
    """
    def __init__(
            self,
            ballast_cover: pint.Quantity = None,
            length: pint.Quantity = None,
            multi_track_factor: int = 1,
            span_length: pint.Quantity = None,
            speed: pint.Quantity = None,
            degree_of_curvature: pint.Quantity = None,
            super_elevation = None,
            distance_to_top_of_rail: pint.Quantity = None,
            cl_track_to_cl_girders: pint.Quantity = 0 * units('in'),
            rail_spacing: pint.Quantity = design_rail_spacing,
            load_cases: list = None,
            section_ids: list = None,
            element_ids: list = None,
            results_request: dict = analysis_results_request,
            export_path: str = Path(os.getcwd()) / 'output' / 'output.json',
            dl_case_name: str = '',
            ll_case_name: str = '',
            rocking_case_name: str = '',
            wind_load: bool = True,
            load_factor: bool = True,
            f_y: pint.Quantity = None,
            e_s: pint.Quantity = None,
            poissons_ratio: float = None,
            l_brace: float = None,
            r_yf: float = None,
            depth_girder: pint.Quantity = None,
            web_thickness: pint.Quantity = None,
            area_flange: pint.Quantity = None,
            s_x: pint.Quantity = None
    ):
        # General Properties
        self.poisson_ration = poissons_ratio
        self.impact_ballast_factor = 0.9 if ballast_cover > 8 * units.inch else 1
        self.length = length
        self.rail_spacing = rail_spacing
        self.speed = speed
        self.degree_of_curvature = degree_of_curvature
        self.super_elevation = super_elevation

        # Impact Loads and Mult-presence factor
        self.impact_load = None
        self.no_of_tracks = multi_track_factor

        # Centrifugal force
        self.CF_force = (0.00117 * (self.speed / units('mph')) ** 2 * self.degree_of_curvature)
        self.CF_percentage = (8 * units('ft') * self.CF_force / rail_spacing) / 100

        # Track Eccentricity
        self.track_eccentricity = cl_track_to_cl_girders
        self.EC = self._calculate_eccentricity()

        # Wind Loads
        self.wind_height = 8 * units('ft') + distance_to_top_of_rail
        self.wind_load_live = 200 * units('lbf/ft')

        # Longitudinal Forces
        # //TODO - Verify these are properly applied for members running perpendicular, like troughs
        self.breaking_force = (45 + 1.2 * (span_length / units('ft'))) * units('kip')
        self.breaking_load = self.breaking_force / span_length

        self.traction_force = 25 * np.sqrt(span_length / units('ft')) * units('kip')
        self.traction_height = 3 * units('ft') + distance_to_top_of_rail

        # Midas API Inputs
        self.load_cases = load_cases
        self.section_ids = section_ids

        if not self.length:  # Forces user to enter a member length if not previously provided
            print(f"{PrintColors.FAIL}Error: Length of member is Required!{PrintColors.ENDC}")
            self.length = float(input('Length of member (float, in ft.): ')) * units('ft')
            self._get_impact_load()
        else:
            self._get_impact_load()
        if self.no_of_tracks > 1:
            self._multi_presence_impact_load()
        self.span_length = span_length
        self.section_ids = section_ids

        get_api_key(Path(os.getcwd()).parent.parent / 'secrets.json')

        self.element_ids = [list(get_elements_by_section_index(value)['ELEM'].keys()) for value in self.section_ids] \
            if not element_ids else element_ids
        # Flatten the previously created list
        self.element_ids = [item for sublist in self.element_ids for item in sublist]
        self.results_request = results_request
        self.export_path = export_path
        self.results_request['Argument']['NODE_ELEMS']['KEYS'] = [int(x) for x in self.element_ids]
        self.results_request['Argument']['LOAD_CASE_NAMES'] = self.load_cases
        self.results_request['Argument']['EXPORT_PATH'] = str(self.export_path)

        try:
            with open(self.export_path):
                pass
        except FileNotFoundError as e:
            print(f"Couldn't find file at {self.export_path}, {e}, creating the directory and output file")
            os.mkdir('output')
            with open("output/output.json", "w") as file:
                file.write("Your text goes here")

        # Get the Analysis Results
        self.analysis_results = midas_api("POST", 'POST/TABLE', self.results_request)

        # Store the results in a dataframe
        self.results_df = pd.DataFrame.from_dict(self.analysis_results['BeamForce']['DATA'])
        self.results_df.columns = self.analysis_results['BeamForce']['HEAD']

        # Start pulling the values you need from the results
        self.max_moment_dead_load, self.max_shear_dead_load = self._get_max_load_values(load_type=dl_case_name)
        self.max_moment_live_load, self.max_shear_live_load = self._get_max_load_values(load_type=ll_case_name)
        self.max_moment_rocking, self.max_shear_rocking = self._get_max_load_values(load_type=rocking_case_name)

        # Impact Moments
        self.impact_moment = self.max_moment_live_load * self.impact_load
        self.impact_shear = self.max_shear_live_load * self.impact_load
        self.impact_reduction_factor = 1 - (0.8 / 2500) * (60 - self.speed / units('mph')) ** 2

        # Reduce impact based on impact reduction factor
        self.M_reduced_impact = self.impact_moment * self.impact_reduction_factor
        self.V_reduced_impact = self.impact_shear * self.impact_reduction_factor

        # Centrifugal Force
        self.M_centrifugal = self.max_moment_live_load * self.CF_percentage
        self.V_centrifugal = self.max_shear_live_load * self.CF_percentage

        # Superelevation
        self.M_super_elevaion = self.max_moment_live_load * self.EC
        self.V_super_elevation = self.max_shear_live_load * self.EC

        # Wind Loads
        if wind_load:
            print('Wind Load effects have not been accounted for yet, must manually calculate')
        else:
            self.M_wind = 0
            self.V_wind = 0

        # Load Factor
        if load_factor:
            print('Wind Load effects have not been accounted for yet, must manually calculate')
        else:
            self.M_LF = 0
            self.V_LF = 0

        # Perform Load Rating
        self.allowable_stress = self.F_bt = (0.55 * f_y).to('ksi')
        self.F_bc = min(
            0.55*f_y,
            max(
                0.55*f_y - ((0.55 * f_y ** 2) / (6.3 * np.pi ** 2 * e_s))*(l_brace / r_yf) ** 2,
                (0.131 * np.pi * e_s) / ((l_brace * depth_girder * np.sqrt(1+poissons_ratio)).to('in^2') /
                                         area_flange).to('dimensionless')
            )
        ).to('ksi')

        self.allowable_bending_stress = self.F_b = min(self.F_bt, self.F_bc).to('ksi')
        self.allowable_shear_stress = self.F_v = (0.35 * f_y).to('ksi')

        # Load Rating Values
        self.E80_M = (((self.F_b * s_x - self.max_moment_dead_load) / (
                    self.max_moment_live_load + self.M_reduced_impact + self.max_moment_rocking + self.M_centrifugal +
                    self.M_super_elevaion + self.M_wind + self.M_LF)) * 80).to(
            'dimensionless')

        self.E80_V = (((self.F_v * (depth_girder * web_thickness) - self.max_shear_dead_load) / (
                self.max_shear_live_load + self.V_reduced_impact + self.max_shear_rocking + self.V_centrifugal +
                self.V_super_elevation + self.V_wind + self.V_LF)) * 80).to('dimensionless')

        self.k_max = 0.8 * f_y
        self.k_bt = self.k_max
        self.k_bc = min(
            self.k_max,
            max(
                self.k_max - ((self.k_max * f_y / units('psi')) / 1.8e9) * (l_brace / r_yf) ** 2,
                (self.k_max * units('psi') / (0.55 * f_y)) * (10500000 /
                                                         ((l_brace * depth_girder) / area_flange).to('dimensionless'))
            )
        ).to('ksi')
        self.k_b = min(self.k_bt, self.k_bc).to('ksi')
        self.k_v = (0.75 * self.k_max).to('ksi')

        self.max_M = (((self.k_b * s_x - self.max_moment_dead_load) /
                        (self.max_moment_live_load + self.max_moment_rocking + self.M_super_elevaion + self.M_wind +
                        self.M_LF + self.M_reduced_impact + self.M_centrifugal)) * 80).to('dimensionless')

        self.max_V = (((self.k_v * (depth_girder * web_thickness) - self.max_shear_dead_load) / (
                    self.max_shear_live_load + self.V_reduced_impact + self.max_shear_rocking + self.V_centrifugal
                    + self.V_super_elevation + self.V_wind + self.V_LF)) * 80).to('dimensionless')

        # //TODO - a lot of these had LL_i and LL_o, make sure you don't have to double the LL values since it wasn't calced

    def _get_impact_load(self):
        """
        Calculates the impact load for a given member as defined in AREMA 15-7.3.2.3, 15-1.3.5 and AREMA 15-1.3.5b,
        updates self.impact_load, returns nothing

        Returns
        -------
        None
        """
        if self.length < 80 * units('ft'):
            self.impact_load = (self.impact_ballast_factor * (40 - ((3 * self.length ** 2) /
                                                                    (1600 * units('ft') ** 2)))) / 100
        else:
            self.impact_load = (16 + ((600 * units('ft')) / (self.length - 30 * units('ft')))) / 100

    def _multi_presence_impact_load(self):
        """
        Calcuates the effect of impact load for a track based on the length of the span and the number of tracks loading
        the member, based on AREMA Table 15-1-5.

        Returns
        -------
        None
        """
        # //TODO - Verify this is referring to span length, not member length
        if self.no_of_tracks > 2:
            # //TODO - Determine how to handle this case
            print(f'{PrintColors.FAIL}Error: Special Case, calculate impact load and set self.impact_load \
             manually{PrintColors.ENDC}')
        elif self.span_length < 175 * units.ft:
            self.impact_load = self.impact_ballast_factor * 2
        elif 175 * units.ft < self.span_length < 225 * units.ft:
            self.impact_load = self.impact_ballast_factor * (450 * units.ft - 2 * self.span_length)

    def _calculate_eccentricity(self):
        """
        Uses the Super Elevation and eccentricity of the member to calculate and eccentricity force for a particular
        member

        # //TODO - Merchant Street had N/A for e_TR - Verify
        # //TODO - This function returns a decimal percentage while most others return unreduced percentages

        Returns
        -------
        Eccentricity effect for inside rail as a percentage
        """
        e_se = 8 * units('ft') * self.super_elevation / self.rail_spacing
        e_cc = self.track_eccentricity + e_se

        return ((2 * e_cc) / self.rail_spacing).to('dimensionless')

    def _get_max_load_values(self, load_type):
        element_loads = self.results_df[self.results_df['Load'] == load_type]

        max_load_moment = max(pd.to_numeric(element_loads['Moment-y']).abs()) * units('kip*ft')
        max_load_shear = max(pd.to_numeric(element_loads['Shear-z']).abs()) * units('kip')

        return max_load_moment, max_load_shear

    def print_results(self):
        print(f"{self.impact_load = :}")
        print(f"{self.CF_force = :}")
        print(f"{self.CF_percentage = :}\n\n")

        print(f"{self.EC = :}\n\n")

        print(f"{self.wind_height = :}")
        print(f"{self.wind_load_live = :}\n\n")  # Not actually being used

        print(f"{self.max_moment_dead_load = :}")
        print(f"{self.max_moment_live_load = :}")
        print(f"{self.max_moment_rocking = :}\n\n")

        print(f"{self.max_shear_dead_load = :}")
        print(f"{self.max_shear_live_load = :}")
        print(f"{self.max_shear_rocking = :}\n\n")

        # Print Original Impact Values
        print(f"{self.impact_moment = :}")
        print(f"{self.impact_shear = :}")
        print(f"{self.impact_reduction_factor = :}\n\n")

        # Print reduced Impact
        print(f"{self.M_reduced_impact = :}")
        print(f"{self.V_reduced_impact = :}\n\n")

        # Print Centrifugal Values
        print(f"{self.M_centrifugal = :}")
        print(f"{self.V_centrifugal = :}\n\n")

        # Print Superelevation Values
        print(f"{self.M_super_elevaion = :}")
        print(f"{self.M_super_elevaion = :}\n\n")

        # Print Wind Values
        print(f"{self.M_wind = :}")
        print(f"{self.V_wind = :}\n\n")

        # Print Load Factor Values
        print(f"{self.M_LF = :}")
        print(f"{self.V_LF = :}\n\n")

        # Print Allowable Stress
        print(f"{self.allowable_stress = :}")
        print(f"{self.F_bc = :}\n\n")

        # Print Allowable Stress
        print(f"{self.allowable_bending_stress = :}")
        print(f"{self.allowable_shear_stress = :}\n\n")

        # Print E80 Load rating
        print(f"{self.E80_M = :}")
        print(f"{self.E80_V = :}\n\n")

        # Print Max E80 Load rating
        print(f"{self.k_max = :}")
        print(f"{self.k_bt = :}")
        print(f"{self.k_bc = :}")
        print(f"{self.k_b = :}")
        print(f"{self.k_v = :}\n\n")
        print(f"{self.max_M = :}")
        print(f"{self.max_V = :}")
