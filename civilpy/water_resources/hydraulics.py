class CulvertDesign:
    def __init__(self, hw_type='A', des_h="6.5", span=14, wall_theta='All'):
        self.hw_type = hw_type
        self.des_h = des_h
        self.span = span
        self.wall_theta = wall_theta
        self.footing = {
            1: {"v_size": 5, "v_spa": 18, "w,z_size": 5, "w,z_spa": 18},
            2: {"v_size": 5, "v_spa": 15, "w,z_size": 5, "w,z_spa": 18},
            3: {"v_size": 5, "v_spa": 12, "w,z_size": 5, "w,z_spa": 15},
            4: {"v_size": 5, "v_spa": 18, "w,z_size": 5, "w,z_spa": 12},
            5: {"v_size": 5, "v_spa": 15, "w,z_size": 5, "w,z_spa": 9},
            6: {"v_size": 6, "v_spa": 18, "w,z_size": 6, "w,z_spa": 18},
            7: {"v_size": 6, "v_spa": 15, "w,z_size": 6, "w,z_spa": 15},
            8: {"v_size": 6, "v_spa": 9, "w,z_size": 6, "w,z_spa": 18},
            9: {"v_size": 6, "v_spa": 9, "w,z_size": 6, "w,z_spa": 12},
            10: {"v_size": 7, "v_spa": 12, "w,z_size": 7, "w,z_spa": 12},
        }

        self.Headwall_Dimensions = {
            "A": {
                "6.5": {"footing_design": 1, "L": 7.25, "h": 4.0, "wf": 4.50, "hf": 1.5, "hcw": 2.5, "a": 1.1666,
                        "b": 1.00, "x_size": 5.00, "x_spa": 18.0, "y_size": 5, "y_spa": 18.0, "c": 2.416666,
                        "WW_Conc": 3.02, "WW_Reinf": 446, "WW_Foot_Conc": 6.00, "WW_Foot_Reinf": 598,
                        "Culv_Foot_Conc": 0.43, "Culv_Foot_Reinf": 24.55},
                "7.5": {"footing_design": 1, "L": 8.5, "h": 4.5, "wf": 5.00, "hf": 1.5, "hcw": 2.5, "a": 1.5, "b": 1.00,
                        "x_size": 5.00, "x_spa": 18.0, "y_size": 5, "y_spa": 18.0, "c": 2.416666, "WW_Conc": 4.01,
                        "WW_Reinf": 533, "WW_Foot_Conc": 7.38, "WW_Foot_Reinf": 733, "Culv_Foot_Conc": 0.48,
                        "Culv_Foot_Reinf": 27.58},
                "8.5": {"footing_design": 1, "L": 10.0, "h": 5.0, "wf": 5.50, "hf": 1.5, "hcw": 2.5, "a": 1.917,
                        "b": 1.00, "x_size": 5.00, "x_spa": 16.5, "y_size": 5, "y_spa": 16.5, "c": 2.416666,
                        "WW_Conc": 5.27, "WW_Reinf": 726, "WW_Foot_Conc": 9.05, "WW_Foot_Reinf": 830,
                        "Culv_Foot_Conc": 0.52, "Culv_Foot_Reinf": 28.61},
                "9.5": {"footing_design": 2, "L": 11.5, "h": 5.5, "wf": 6.25, "hf": 1.5, "hcw": 2.5, "a": 2.250,
                        "b": 1.00, "x_size": 5.00, "x_spa": 18.0, "y_size": 5, "y_spa": 9.0, "c": 3.833,
                        "WW_Conc": 6.69, "WW_Reinf": 934, "WW_Foot_Conc": 11.35, "WW_Foot_Reinf": 1113,
                        "Culv_Foot_Conc": 0.57, "Culv_Foot_Reinf": 30.11},
                "10.5": {"footing_design": 1, "L": 12.75, "h": 6.0, "wf": 7.00, "hf": 2.0, "hcw": 2.0, "a": 2.917,
                         "b": 1.25, "x_size": 5.00, "x_spa": 18.0, "y_size": 5, "y_spa": 9.0, "c": 4.167,
                         "WW_Conc": 10.25, "WW_Reinf": 1104, "WW_Foot_Conc": 16.19, "WW_Foot_Reinf": 1087,
                         "Culv_Foot_Conc": 0.74, "Culv_Foot_Reinf": 33.95},
                "11.5": {"footing_design": 1, "L": 14.25, "h": 6.5, "wf": 7.50, "hf": 2.0, "hcw": 2.0, "a": 3.417,
                         "b": 1.25, "x_size": 5.00, "x_spa": 17.0, "y_size": 5, "y_spa": 8.5, "c": 5.0,
                         "WW_Conc": 12.43, "WW_Reinf": 1404, "WW_Foot_Conc": 18.87, "WW_Foot_Reinf": 1205,
                         "Culv_Foot_Conc": 0.80, "Culv_Foot_Reinf": 35.06},
                "12.5": {"footing_design": 8, "L": 15.75, "h": 7.0, "wf": 8.75, "hf": 2.0, "hcw": 2.0, "a": 3.5,
                         "b": 1.25, "x_size": 5.00, "x_spa": 17.0, "y_size": 5, "y_spa": 8.5, "c": 5.250,
                         "WW_Conc": 14.82, "WW_Reinf": 1580, "WW_Foot_Conc": 24.41, "WW_Foot_Reinf": 2246,
                         "Culv_Foot_Conc": 0.89, "Culv_Foot_Reinf": 52.90},
                "13.5": {"footing_design": 8, "L": 17.0, "h": 7.5, "wf": 9.5, "hf": 2.0, "hcw": 2.0, "a": 3.917,
                         "b": 1.25, "x_size": 6.00, "x_spa": 18.0, "y_size": 6, "y_spa": 9.0, "c": 6.167,
                         "WW_Conc": 17.18, "WW_Reinf": 2139, "WW_Foot_Conc": 28.17, "WW_Foot_Reinf": 2630,
                         "Culv_Foot_Conc": 0.97, "Culv_Foot_Reinf": 56.94}
            },
            "B": {
                "All": {
                    "6.5": {"footing_design": 1.0, "wf": 4.75, "hf": 1.5, "hcw": 2.5, "a": 1.660, "b": 1.00,
                            "x_size": 5.00, "x_spa": 18.0, "y_size": 5, "y_spa": 18.0, "c": 2.416666},
                    "7.5": {"footing_design": 1.0, "wf": 5.5, "hf": 1.5, "hcw": 2.5, "a": 2.083, "b": 1.00,
                            "x_size": 5.00, "x_spa": 15.0, "y_size": 5, "y_spa": 15.0, "c": 2.416666},
                    "8.5": {"footing_design": 2.0, "wf": 6.25, "hf": 1.5, "hcw": 2.5, "a": 2.500, "b": 1.00,
                            "x_size": 5.00, "x_spa": 18.0, "y_size": 5, "y_spa": 9.0, "c": 2.8333333},
                    "9.5": {"footing_design": 3.0, "wf": 7.0, "hf": 1.5, "hcw": 2.5, "a": 2.917, "b": 1.00,
                            "x_size": 5.00, "x_spa": 18.0, "y_size": 5, "y_spa": 9.0, "c": 3.1666666},
                    "10.5": {"footing_design": 3.0, "wf": 8.0, "hf": 2.0, "hcw": 2.0, "a": 3.750, "b": 1.25,
                             "x_size": 5.00, "x_spa": 14.5, "y_size": 5, "y_spa": 7.25, "c": 3.583333},
                    "11.5": {"footing_design": 7.0, "wf": 9.0, "hf": 2.0, "hcw": 2.0, "a": 4.083, "b": 1.25,
                             "x_size": 5.00, "x_spa": 14.5, "y_size": 5, "y_spa": 7.25, "c": 3.750000},
                    "12.5": {"footing_design": 9.0, "wf": 10.0, "hf": 2.0, "hcw": 2.0, "a": 4.500, "b": 1.25,
                             "x_size": 6.00, "x_spa": 16.0, "y_size": 6, "y_spa": 8.0, "c": 4.7500000},
                    "13.5": {"footing_design": 10.0, "wf": 11.25, "hf": 2.0, "hcw": 2.0, "a": 4.833, "b": 1.25,
                             "x_size": 6.0, "x_spa": 12.5, "y_size": 6, "y_spa": 6.25, "c": 4.916666}
                },
                "0": {
                    "6.5": {"L1": 7.083, "L2": 10.0, "h1": 4.0, "h2": 6.5, "WW_Conc": 3.89, "WW_Reinf": 512,
                            "WW_Foot_Conc": 6.94, "WW_Foot_Reinf": 552, "Culv_Foot_Conc": 0.47,
                            "Culv_Foot_Reinf": 25.31},
                    "7.5": {"L1": 8.50, "L2": 12.0, "h1": 4.5, "h2": 7.5, "WW_Conc": 5.34, "WW_Reinf": 667,
                            "WW_Foot_Conc": 9.13, "WW_Foot_Reinf": 684, "Culv_Foot_Conc": 0.53,
                            "Culv_Foot_Reinf": 28.77},
                    "8.5": {"L1": 9.917, "L2": 14.0, "h1": 5.0, "h2": 8.5, "WW_Conc": 7.02, "WW_Reinf": 921,
                            "WW_Foot_Conc": 11.62, "WW_Foot_Reinf": 1028, "Culv_Foot_Conc": 0.58,
                            "Culv_Foot_Reinf": 30.40},
                    "9.5": {"L1": 11.333, "L2": 16.0, "h1": 5.5, "h2": 9.5, "WW_Conc": 8.93, "WW_Reinf": 1118,
                            "WW_Foot_Conc": 14.39, "WW_Foot_Reinf": 1373, "Culv_Foot_Conc": 0.64,
                            "Culv_Foot_Reinf": 36.79},
                    "10.5": {"L1": 12.750, "L2": 18.0, "h1": 6.0, "h2": 10.5, "WW_Conc": 13.88, "WW_Reinf": 1464,
                             "WW_Foot_Conc": 21.52, "WW_Foot_Reinf": 1677, "Culv_Foot_Conc": 0.85,
                             "Culv_Foot_Reinf": 41.10},
                    "11.5": {"L1": 14.167, "L2": 20.0, "h1": 6.5, "h2": 11.5, "WW_Conc": 16.83, "WW_Reinf": 1787,
                             "WW_Foot_Conc": 26.54, "WW_Foot_Reinf": 2144, "Culv_Foot_Conc": 0.93,
                             "Culv_Foot_Reinf": 50.56},
                    "12.5": {"L1": 15.583, "L2": 22.0, "h1": 7.0, "h2": 12.5, "WW_Conc": 20.07, "WW_Reinf": 2321,
                             "WW_Foot_Conc": 32.04, "WW_Foot_Reinf": 3030, "Culv_Foot_Conc": 1.03,
                             "Culv_Foot_Reinf": 67.81},
                    "13.5": {"L1": 17.0, "L2": 24.0, "h1": 7.5, "h2": 13.5, "WW_Conc": 23.59, "WW_Reinf": 2928,
                             "WW_Foot_Conc": 38.97, "WW_Foot_Reinf": 4023, "Culv_Foot_Conc": 1.13,
                             "Culv_Foot_Reinf": 84.51}
                },
                "15": {
                    "6.5": {"L1": 8.250, "L2": 6.333, "h1": 4.0, "h2": 4.750, "WW_Conc": 3.05, "WW_Reinf": 422,
                            "WW_Foot_Conc": 5.94, "WW_Foot_Reinf": 493, "Culv_Foot_Conc": 0.47,
                            "Culv_Foot_Reinf": 25.31},
                    "7.5": {"L1": 9.917, "L2": 7.917, "h1": 4.5, "h2": 5.5, "WW_Conc": 4.05, "WW_Reinf": 582,
                            "WW_Foot_Conc": 7.95, "WW_Foot_Reinf": 631, "Culv_Foot_Conc": 0.53,
                            "Culv_Foot_Reinf": 28.77},
                    "8.5": {"L1": 11.5, "L2": 9.5, "h1": 5.0, "h2": 6.250, "WW_Conc": 5.63, "WW_Reinf": 783,
                            "WW_Foot_Conc": 10.20, "WW_Foot_Reinf": 935, "Culv_Foot_Conc": 0.58,
                            "Culv_Foot_Reinf": 30.40},
                    "9.5": {"L1": 13.167, "L2": 11.083, "h1": 5.5, "h2": 7.0, "WW_Conc": 7.22, "WW_Reinf": 960,
                            "WW_Foot_Conc": 12.76, "WW_Foot_Reinf": 1240, "Culv_Foot_Conc": 0.64,
                            "Culv_Foot_Reinf": 36.79},
                    "10.5": {"L1": 14.833, "L2": 12.667, "h1": 6.0, "h2": 7.750, "WW_Conc": 11.32, "WW_Reinf": 1245,
                             "WW_Foot_Conc": 19.23, "WW_Foot_Reinf": 1517, "Culv_Foot_Conc": 0.85,
                             "Culv_Foot_Reinf": 41.10},
                    "11.5": {"L1": 16.5, "L2": 14.250, "h1": 6.5, "h2": 8.750, "WW_Conc": 13.89, "WW_Reinf": 1535,
                             "WW_Foot_Conc": 23.91, "WW_Foot_Reinf": 1947, "Culv_Foot_Conc": 0.93,
                             "Culv_Foot_Reinf": 50.56},
                    "12.5": {"L1": 18.083, "L2": 15.833, "h1": 7.0, "h2": 9.5, "WW_Conc": 16.59, "WW_Reinf": 2020,
                             "WW_Foot_Conc": 28.96, "WW_Foot_Reinf": 2722, "Culv_Foot_Conc": 1.03,
                             "Culv_Foot_Reinf": 67.81},
                    "13.5": {"L1": 19.750, "L2": 17.5, "h1": 7.5, "h2": 10.25, "WW_Conc": 19.61, "WW_Reinf": 2587,
                             "WW_Foot_Conc": 35.52, "WW_Foot_Reinf": 3669, "Culv_Foot_Conc": 1.13,
                             "Culv_Foot_Reinf": 84.51}
                },
                "30": {
                    "6.5": {"L1": 10.0, "L2": 4.0, "h1": 4.0, "h2": 3.5, "WW_Conc": 2.83, "WW_Reinf": 407,
                            "WW_Foot_Conc": 5.71, "WW_Foot_Reinf": 468, "Culv_Foot_Conc": 0.47,
                            "Culv_Foot_Reinf": 25.31},
                    "7.5": {"L1": 12.0, "L2": 5.333, "h1": 4.5, "h2": 4.25, "WW_Conc": 3.99, "WW_Reinf": 531,
                            "WW_Foot_Conc": 7.74, "WW_Foot_Reinf": 625, "Culv_Foot_Conc": 0.53,
                            "Culv_Foot_Reinf": 28.77},
                    "8.5": {"L1": 14.0, "L2": 6.667, "h1": 5.0, "h2": 5.0, "WW_Conc": 5.35, "WW_Reinf": 772,
                            "WW_Foot_Conc": 10.05, "WW_Foot_Reinf": 922, "Culv_Foot_Conc": 0.58,
                            "Culv_Foot_Reinf": 30.40},
                    "9.5": {"L1": 16.0, "L2": 8.0, "h1": 5.5, "h2": 5.5, "WW_Conc": 6.87, "WW_Reinf": 917,
                            "WW_Foot_Conc": 12.64, "WW_Foot_Reinf": 1229, "Culv_Foot_Conc": 0.64,
                            "Culv_Foot_Reinf": 36.79},
                    "10.5": {"L1": 18.0, "L2": 9.333, "h1": 6.0, "h2": 6.25, "WW_Conc": 10.85, "WW_Reinf": 1189,
                             "WW_Foot_Conc": 19.13, "WW_Foot_Reinf": 1487, "Culv_Foot_Conc": 0.85,
                             "Culv_Foot_Reinf": 41.10},
                    "11.5": {"L1": 20.0, "L2": 10.667, "h1": 6.5, "h2": 7.0, "WW_Conc": 13.29, "WW_Reinf": 1483,
                             "WW_Foot_Conc": 23.89, "WW_Foot_Reinf": 1908, "Culv_Foot_Conc": 0.93,
                             "Culv_Foot_Reinf": 50.56},
                    "12.5": {"L1": 22.0, "L2": 12.0, "h1": 7.0, "h2": 7.5, "WW_Conc": 15.91, "WW_Reinf": 1957,
                             "WW_Foot_Conc": 29.11, "WW_Foot_Reinf": 2683, "Culv_Foot_Conc": 1.03,
                             "Culv_Foot_Reinf": 67.81},
                    "13.5": {"L1": 24.0, "L2": 13.333, "h1": 7.5, "h2": 8.25, "WW_Conc": 18.84, "WW_Reinf": 2520,
                             "WW_Foot_Conc": 35.74, "WW_Foot_Reinf": 3674, "Culv_Foot_Conc": 1.13,
                             "Culv_Foot_Reinf": 84.51}
                },
                "45": {
                    "6.5": {"L1": 13.083, "L2": 4.0, "h1": 4.0, "h2": 2.75, "WW_Conc": 3.40, "WW_Reinf": 469,
                            "WW_Foot_Conc": 6.97, "WW_Foot_Reinf": 535, "Culv_Foot_Conc": 0.47,
                            "Culv_Foot_Reinf": 25.31},
                    "7.5": {"L1": 15.750, "L2": 4.0, "h1": 4.5, "h2": 3.5, "WW_Conc": 4.51, "WW_Reinf": 590,
                            "WW_Foot_Conc": 8.82, "WW_Foot_Reinf": 676, "Culv_Foot_Conc": 0.53,
                            "Culv_Foot_Reinf": 28.77},
                    "8.5": {"L1": 18.333, "L2": 4.917, "h1": 5.0, "h2": 4.0, "WW_Conc": 5.94, "WW_Reinf": 825,
                            "WW_Foot_Conc": 11.32, "WW_Foot_Reinf": 982, "Culv_Foot_Conc": 0.58,
                            "Culv_Foot_Reinf": 30.40},
                    "9.5": {"L1": 20.917, "L2": 6.083, "h1": 5.5, "h2": 4.5, "WW_Conc": 7.63, "WW_Reinf": 983,
                            "WW_Foot_Conc": 14.26, "WW_Foot_Reinf": 1337, "Culv_Foot_Conc": 0.64,
                            "Culv_Foot_Reinf": 36.79},
                    "10.5": {"L1": 23.583, "L2": 7.250, "h1": 6.0, "h2": 5.25, "WW_Conc": 12.06, "WW_Reinf": 1325,
                             "WW_Foot_Conc": 21.66, "WW_Foot_Reinf": 1628, "Culv_Foot_Conc": 0.85,
                             "Culv_Foot_Reinf": 41.10},
                    "11.5": {"L1": 26.167, "L2": 8.417, "h1": 6.5, "h2": 5.75, "WW_Conc": 14.71, "WW_Reinf": 1622,
                             "WW_Foot_Conc": 27.05, "WW_Foot_Reinf": 2116, "Culv_Foot_Conc": 0.93,
                             "Culv_Foot_Reinf": 50.56},
                    "12.5": {"L1": 28.750, "L2": 9.583, "h1": 7.0, "h2": 6.25, "WW_Conc": 17.63, "WW_Reinf": 2157,
                             "WW_Foot_Conc": 32.96, "WW_Foot_Reinf": 2995, "Culv_Foot_Conc": 1.03,
                             "Culv_Foot_Reinf": 67.81},
                    "13.5": {"L1": 31.417, "L2": 10.75, "h1": 7.5, "h2": 6.75, "WW_Conc": 20.84, "WW_Reinf": 2772,
                             "WW_Foot_Conc": 40.55, "WW_Foot_Reinf": 4064, "Culv_Foot_Conc": 1.13,
                             "Culv_Foot_Reinf": 84.51}
                },
            },
            "C": {
                "6.5": {"footing_design": 1, "L": 10, "wf": 5.25, "hf": 1.5, "hcw": 2.5, "a": 1.417, "b": 1.00,
                        "x_size": 5.00, "x_spa": 17.5, "y_size": 5, "y_spa": 17.5, "c": 2.416666, "WW_Conc": 4.82,
                        "WW_Reinf": 528, "WW_Foot_Conc": 8.62, "WW_Foot_Reinf": 587, "Culv_Foot_Conc": 0.49,
                        "Culv_Foot_Reinf": 27.84},
                "7.5": {"footing_design": 1, "L": 12, "wf": 5.75, "hf": 1.5, "hcw": 2.5, "a": 2.0, "b": 1.00,
                        "x_size": 5.00, "x_spa": 12.0, "y_size": 5, "y_spa": 12.0, "c": 2.416666, "WW_Conc": 6.67,
                        "WW_Reinf": 749, "WW_Foot_Conc": 11.00, "WW_Foot_Reinf": 695, "Culv_Foot_Conc": 0.55,
                        "Culv_Foot_Reinf": 29.04},
                "8.5": {"footing_design": 1, "L": 14, "wf": 6.25, "hf": 1.5, "hcw": 2.5, "a": 2.583, "b": 1.00,
                        "x_size": 5.00, "x_spa": 17.5, "y_size": 5, "y_spa": 8.75, "c": 3.5, "WW_Conc": 8.82,
                        "WW_Reinf": 1012, "WW_Foot_Conc": 13.62, "WW_Foot_Reinf": 823, "Culv_Foot_Conc": 0.59,
                        "Culv_Foot_Reinf": 30.15},
                "9.5": {"footing_design": 3, "L": 16, "wf": 7.0, "hf": 1.5, "hcw": 2.5, "a": 2.917, "b": 1.00,
                        "x_size": 5.00, "x_spa": 17.5, "y_size": 5, "y_spa": 8.75, "c": 3.667, "WW_Conc": 11.26,
                        "WW_Reinf": 1261, "WW_Foot_Conc": 16.89, "WW_Foot_Reinf": 1448, "Culv_Foot_Conc": 0.64,
                        "Culv_Foot_Reinf": 36.68},
                "10.5": {"footing_design": 3, "L": 18, "wf": 8.0, "hf": 2.0, "hcw": 2.0, "a": 3.667, "b": 1.25,
                         "x_size": 5.00, "x_spa": 18.0, "y_size": 5, "y_spa": 9.0, "c": 3.917, "WW_Conc": 17.50,
                         "WW_Reinf": 1485, "WW_Foot_Conc": 25.34, "WW_Foot_Reinf": 1803, "Culv_Foot_Conc": 0.85,
                         "Culv_Foot_Reinf": 40.93},
                "11.5": {"footing_design": 7, "L": 20, "wf": 9.0, "hf": 2.0, "hcw": 2.0, "a": 3.833, "b": 1.25,
                         "x_size": 6.00, "x_spa": 18.0, "y_size": 6, "y_spa": 9.0, "c": 4.5, "WW_Conc": 21.30,
                         "WW_Reinf": 2201, "WW_Foot_Conc": 31.12, "WW_Foot_Reinf": 2250, "Culv_Foot_Conc": 0.92,
                         "Culv_Foot_Reinf": 46.94},
                "12.5": {"footing_design": 9, "L": 22, "wf": 9.75, "hf": 2.0, "hcw": 2.0, "a": 4.250, "b": 1.25,
                         "x_size": 6.00, "x_spa": 16.0, "y_size": 6, "y_spa": 8.0, "c": 5.167, "WW_Conc": 25.47,
                         "WW_Reinf": 2775, "WW_Foot_Conc": 36.67, "WW_Foot_Reinf": 3378, "Culv_Foot_Conc": 1.00,
                         "Culv_Foot_Reinf": 66.64},
                "13.5": {"footing_design": 9, "L": 24, "wf": 10.5, "hf": 2.0, "hcw": 2.0, "a": 4.667, "b": 1.25,
                         "x_size": 6.00, "x_spa": 13.0, "y_size": 6, "y_spa": 6.5, "c": 5.333, "WW_Conc": 30.0,
                         "WW_Reinf": 3454, "WW_Foot_Conc": 42.67, "WW_Foot_Reinf": 3789, "Culv_Foot_Conc": 1.06,
                         "Culv_Foot_Reinf": 69.56}
            }
        }
        self.wall_thickness = 0

        if self.span <= 8:
            self.wall_thickness = 8
        elif self.span <= 10:
            self.wall_thickness = 10
        else:
            self.wall_thickness = 12


import os
from pathlib import Path


# Create a class object to hold functions and values
class MicrostationPidginScript:
    def __init__(self):
        """
        Defines the attributes of the class, for this class the primary thing we'll be building is a set of
        instructions for the script to execute.
        """
        self.text = ''
        self.set_level()
        self.set_color()
        self.set_style()
        self.set_weight()

    def create_script_file(self, file_name='test1.txt'):
        """
        Creates the Script file to actually be run in MicroStation family of products

        :param script_name:(str) The location the script file will be saved to, relative to present working python directory
        :returns: None, opens and saves file to disk
        """
        with open(f'scripts/{file_name}', 'w') as f:
            f.write(self.text)

        print(f"Script file:\n\t@{Path(os.getcwd() + '/scripts/' + file_name)}")

    def print_script_as_command(self):
        self.text = self.text.replace('\n', ';')
        print(self.text)

    def set_level(self, level=1):
        """
        Sets the current level the object is working with

        :param level:(int) the level you want to set active
        :returns: None, updates self.text string within object for writing to file later
        """
        self.text += f'LV={level}\n'

    def set_color(self, color=1):
        """
        Sets the current color the object is working with

        :param color:(int) the level you want to set active
        :returns: None, updates self.text string within object for writing to file later
        """
        self.text += f'CO={color}\n'

    def set_style(self, style=1):
        """
        Sets the current Line Style the object is working with

        :param style:(int) the style you want to set active
        :returns: None, updates self.text string within object for writing to file later
        """
        self.text += f'LC={style}\n'

    def set_weight(self, weight=1):
        """
        Sets the current Line weight the object is working with

        :param weight:(int) the weight you want to set active
        :returns: None, updates self.text string within object for writing to file later
        """
        self.text += f'WT={weight}\n'

    def place_circle_radius(self, radius=10, location=None):
        """
        Places a circle of a specified radius, in a specified location

        :param radius:(int) The radius of the circle to place
        :param location:(str) The location to place the circle
        :returns: None, updates self.text string within object for writing to file later
        """
        if location == None:
            self.text += f'E,Place Circle Radius;T,{radius};M,Placed Circle Radius = {radius};%d;null\n'
        else:
            self.text += f'E,Place Circle Radius;T,{radius};M,Placed Circle Radius = {radius};{location};null\n'

    def print_message(self, location='left', style='status', message='Message Default'):
        """
        Displays a message to the user in various ways depending on values

        :param location:(str) left/right - The side of the bar to display the message on
        :param stype:(str) prompt/status - The type of message to display
        :param message:(str) The message to display
        :returns: None, updates self.text string within object for writing to file later
        """
        if location.lower() == 'left' and style.lower() == 'prompt':
            self.text += f'M,CF {message}\n'
        elif location.lower() == 'left' and style.lower() == 'status':
            self.text += f'M,ER {message}\n'
        elif location.lower() == 'right' and style.lower() == 'prompt':
            self.text += f'M,PR {message}\n'
        elif location.lower() == 'right' and style.lower() == 'status':
            self.text += f'M,ST {message}\n'
        else:
            print(f"ERROR print_message({location}, {style}, {message}) combination resulted in error, check docs")

    def create_sheet_model(self, model_type='design', name='Untitled Sheet', description=''):
        """
        Adds the create sheet model dialog to the script

        :param model_type:(str) design/sheet/drawing - The type of model to create
        :param name:(str) The name of the model
        :param description:(str) Description of the model
        :returns: None, updates self.text string within object for writing to file later
        """
        self.text += f'model create sheet \"{name}\" \"{description}\"\n'

    def insert_cell(self, default_cell="A-1-b"):
        """
        Inserts a "insert cell" dialogue into the script

        :param default_cell:(str) The name of the Cell to insert into the drawing, any cell name in the library can be used
        :returns: None, updates self.text string within object for writing to file later
        """
        self.text += f"ac={default_cell}\nplace cell interactive absolute;/d\n"

    def insert_border(self, default_border="BORDER_3N"):
        """
        helper function of the insert_cell function, that defaults to the "BORDER_3N" cell

        :param default_border:(str) The name of the border Cell to insert into the drawing, any cell name in the library can be used
        :returns: None, updates self.text string within object for writing to file later
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
        self.text = ''


ohio_counties_abv = {
    "ADA": "Adams",
    "ALL": "Allen",
    "ASD": "Ashland",
    "ATB": "Ashtabula",
    "ATH": "Athens",
    "AUG": "Auglaize",
    "BEL": "Belmont",
    "BRO": "Brown",
    "BUT": "Butler",
    "CAR": "Carroll",
    "CHP": "Champaign",
    "CLA": "Clark",
    "CLE": "Clermont",
    "CLI": "Clinton",
    "COL": "Columbiana",
    "COS": "Coshocton",
    "CRA": "Crawford",
    "CUY": "Cuyahoga",
    "DAR": "Darke",
    "DEF": "Defiance",
    "DEL": "Delaware",
    "ERI": "Erie",
    "FAI": "Fairfield",
    "FAY": "Fayette",
    "FRA": "Franklin",
    "FUL": "Fulton",
    "GAL": "Gallia",
    "GEA": "Geauga",
    "GRE": "Greene",
    "GUE": "Guernsey",
    "HAM": "Hamilton",
    "HAN": "Hancock",
    "HAR": "Hardin",
    "HAS": "Harrison",
    "HEN": "Henry",
    "HIG": "Highland",
    "HOC": "Hocking",
    "HOL": "Holmes",
    "HUR": "Huron",
    "JAC": "Jackson",
    "JEF": "Jefferson",
    "KNO": "Knox",
    "LAK": "Lake",
    "LAW": "Lawrence",
    "LIC": "Licking",
    "LOG": "Logan",
    "LOR": "Lorain",
    "LUC": "Lucas",
    "MAD": "Madison",
    "MAH": "Mahoning",
    "MAR": "Marion",
    "MED": "Medina",
    "MEG": "Meigs",
    "MER": "Mercer",
    "MIA": "Miami",
    "MOE": "Monroe",
    "MOT": "Montgomery",
    "MRG": "Morgan",
    "MRW": "Morrow",
    "MUS": "Muskingum",
    "NOB": "Noble",
    "OTT": "Ottawa",
    "PAU": "Paulding",
    "PER": "Perry",
    "PIC": "Pickaway",
    "PIK": "Pike",
    "POR": "Portage",
    "PRE": "Preble",
    "PUT": "Putnam",
    "RIC": "Richland",
    "ROS": "Ross",
    "SAN": "Sandusky",
    "SCI": "Scioto",
    "SEN": "Seneca",
    "SHE": "Shelby",
    "STA": "Stark",
    "SUM": "Summit",
    "TRU": "Trumbull",
    "TUS": "Tuscarawas",
    "UNI": "Union",
    "VAN": "Van Wert",
    "VIN": "Vinton",
    "WAR": "Warren",
    "WAS": "Washington",
    "WAY": "Wayne",
    "WIL": "Williams",
    "WOO": "Wood",
    "WYA": "Wyandot"
}

factors_for_design_feature = {
    "Lane_Width_Rural": ["Function Classification", "Traffic Data", "Terrain", "Design Speed"],
    "Lane_Width_Urban": ["Function Classification", "Local"],
    "Shoulder_Width_Type_Rural": ["Function Classification", "Traffic Data"],
    "Shoulder_Width_Type_Urban": ["Function Classification", "Local"],
    "Guardrail_Offset": ["Function Classification", "Traffic Data"],
    "Degree_of_Curvature ": ["Local", "Design Speed"],
    "Grades": ["Function Classification", "Terrain", "Local", "Design Speed"],
    "Bridge_Clearances": ["Function Classification", "Traffic Data"],
    "Stopping_Sight_Distance": ["Design Speed"],
    "Passing_Intersection_Sight_Distances": ["Design Speed"],
    "Decision_Sight_Distance": ["Design Speed"],
    "Superelevation": ["Local", "Design Speed"],
    "Curve_Widening": ["Design Speed"],
    "Design_Speed_Rural": ["Function Classification", "Traffic Data", "Terrain"],
    "Design_Speed_Urban": ["Function Classification", "Local"],
    "Vertical_Alignment": ["Function Classification", "Terrain", "Local", "Design Speed"],
    "Horizontal_Alignment": ["Local", "Design Speed"]
}

design_feature_criteria = {
    "Lane_Width": {"Sections": ["301.1.2", "303.1"], "Figures": ["301-2", "301-4", "303-1"]},
    "Shoulder_Width": {"Sections": ["301.2.3", "303.1"], "Figures": ["301-3", "301-4", "303-1"]},
    "Design_Loading_Structural_Capacity": {"Sections": ["302.1"], "Figures": ["BDM"]},
    "Horizontal_Curve_Radius": {"Sections": ["202.3"], "Figures": ["202-2"]},
    "Maximum_Grade": {"Sections": ["203.2"], "Figures": ["203-1"]},
    "Stopping_Sight_Distance": {"Sections": ["201.2"], "Figures": ["201-1", "203-3", "203-4"]},
    "Pavement_Cross_Slope": {"Sections": ["301.1.5"], "Figures": [""]},
    "Superelevation": {"Sections": ["202.4.1", "202.4.3"], "Figures": ["202-3", "202-7", "202-8", "202-9", "202-10"]},
    "Vertical_Clearance": {"Sections": ["302.1"], "Figures": ["302-1", "302-2", "302-3"]},
}

