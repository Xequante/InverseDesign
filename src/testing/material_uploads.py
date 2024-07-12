import numpy as np
import os
from src.inputs.materials.bb_metals import BBMetal, load_bb_metal
from src.inputs.materials.ld_metals import LDMetal, load_ld_metal


def load_all_materials():
    upload_bb_materials()
    upload_ld_materials()


def upload_bb_materials(directory='resources/materials/bb_metals'):

    Ag = {
        'f': np.array([0.821, 0.050, 0.133, 0.051, 0.467, 4.000]),
        'g': np.array([0.049, 0.189, 0.067, 0.019, 0.117, 0.052]),
        'w': np.array([0, 2.025, 5.185, 4.343, 9.809, 18.56]),
        's': np.array([0, 1.894, 0.665, 0.189, 1.170, 0.516]),
        'wp': 9.01
    }

    Au = {
        'f': np.array([0.770, 0.054, 0.050, 0.312, 0.719, 1.648]),
        'g': np.array([0.050, 0.074, 0.035, 0.083, 0.125, 0.179]),
        'w': np.array([0, 0.218, 2.885, 4.069, 6.137, 27.97]),
        's': np.array([0, 0.742, 0.349, 0.830, 1.246, 1.795]),
        'wp': 9.03
    }

    Cu = {
        'f': np.array([0.562, 0.076, 0.081, 0.324, 0.726]),
        'g': np.array([0.030, 0.056, 0.047, 0.113, 0.172]),
        'w': np.array([0, 0.416, 2.849, 4.819, 8.136]),
        's': np.array([0, 0.562, 0.469, 1.131, 1.719]),
        'wp': 10.83
    }

    Al = {
        'f': np.array([0.526, 0.213, 0.060, 0.182, 0.014]),
        'g': np.array([0.047, 0.312, 0.315, 1.587, 2.145]),
        'w': np.array([0, 0.163, 1.561, 1.827, 4.495]),
        's': np.array([0, 0.013, 0.042, 0.256, 1.735]),
        'wp': 14.98
    }

    Be = {
        'f': np.array([0.081, 0.066, 0.067, 0.346, 0.311]),
        'g': np.array([0.035, 2.956, 3.962, 2.398, 3.904]),
        'w': np.array([0, 0.131, 0.469, 2.827, 4.318]),
        's': np.array([0, 0.277, 3.167, 1.446, 0.893]),
        'wp': 18.51
    }

    Cr = {
        'f': np.array([0.154, 0.338, 0.261, 0.817, 0.105]),
        'g': np.array([0.048, 4.256, 3.957, 2.218, 6.983]),
        'w': np.array([0, 0.281, 0.584, 1.919, 6.997]),
        's': np.array([0, 0.115, 0.252, 0.225, 4.903]),
        'wp': 10.75
    }

    Ni = {
        'f': np.array([0.083, 0.357, 0.039, 0.127, 0.654]),
        'g': np.array([0.022, 2.820, 0.120, 1.822, 6.637]),
        'w': np.array([0, 0.317, 1.059, 4.583, 8.825]),
        's': np.array([0, 0.606, 1.454, 0.379, 0.510]),
        'wp': 15.92
    }

    Pd = {
        'f': np.array([0.330, 0.769, 0.093, 0.309, 0.409]),
        'g': np.array([0.009, 2.343, 0.497, 2.022, 0.119]),
        'w': np.array([0, 0.066, 0.502, 2.432, 5.987]),
        's': np.array([0, 0.694, 0.027, 1.167, 1.331]),
        'wp': 9.72
    }

    Pt = {
        'f': np.array([0.333, 0.186, 0.665, 0.551, 2.214]),
        'g': np.array([0.080, 0.498, 1.851, 2.604, 2.891]),
        'w': np.array([0, 0.782, 1.317, 3.189, 8.236]),
        's': np.array([0, 0.031, 0.096, 0.766, 1.146]),
        'wp': 9.59
    }

    Ti = {
        'f': np.array([0.126, 0.427, 0.218, 0.513, 0.0002]),
        'g': np.array([0.067, 1.877, 0.100, 0.615, 4.109]),
        'w': np.array([0, 1.459, 2.661, 0.805, 19.86]),
        's': np.array([0, 0.463, 0.506, 0.799, 2.854]),
        'wp': 7.29
    }

    W = {
        'f': np.array([0.197, 0.006, 0.022, 0.136, 2.648]),
        'g': np.array([0.057, 3.689, 0.227, 1.433, 4.555]),
        'w': np.array([0, 0.481, 0.985, 1.962, 5.442]),
        's': np.array([0, 3.754, 0.059, 0.273, 1.912]),
        'wp': 13.22
    }

    mats = {
        'Ag': Ag,
        'Au': Au,
        'Cu': Cu,
        'Al': Al,
        'Be': Be,
        'Cr': Cr,
        'Ni': Ni,
        'Pd': Pd,
        'Pt': Pt,
        'Ti': Ti,
        'W': W
    }

    # Generate the materials
    materials = []
    for key, val in mats.items():
        new_metal = BBMetal(
            name=key, **val
        )
        new_metal.save_bb_metal(overwrite=True)
        materials.append(new_metal)

    # Load the materials
    for filename in os.listdir(directory):
        file_directory = os.path.join(directory, filename)
        metal = load_bb_metal(file_directory)

        # Iterate through all metals and see which one has a matching name
        for stored_metal in materials:
            if stored_metal.name == metal.name:
                checks = [stored_metal.f - metal.f, stored_metal.g - metal.g,
                          stored_metal.w - metal.w, stored_metal.s - metal.s]
                for i, check in enumerate(checks):
                    if all(v == 0 for v in check):
                        print(f'Check {i + 1} passed for {metal.name}')
                    else:
                        print(f'Check {i + 1} failed for {metal.name}')
                if stored_metal.wp == metal.wp:
                    print(f'Check {5} passed for {metal.name}')
                else:
                    print(f'Check {5} failed for {metal.name}')

        # Provide a blank line
        print('')


def upload_ld_materials(directory='resources/materials/ld_metals'):
    Ag = {
        'f': np.array([0.845, 0.065, 0.124, 0.011, 0.840, 5.646]),
        'g': np.array([0.048, 3.886, 0.452, 0.065, 0.916, 2.419]),
        'w': np.array([0, 0.816, 4.481, 8.185, 9.083, 20.29]),
        'wp': 9.01
    }

    Au = {
        'f': np.array([0.760, 0.024, 0.010, 0.071, 0.601, 4.384]),
        'g': np.array([0.053, 0.241, 0.345, 0.870, 2.494, 2.214]),
        'w': np.array([0, 0.415, 0.830, 2.969, 4.304, 13.32]),
        'wp': 9.03
    }

    Cu = {
        'f': np.array([0.575, 0.061, 0.104, 0.723, 0.638]),
        'g': np.array([0.030, 0.378, 1.056, 3.213, 4.305]),
        'w': np.array([0, 0.291, 2.597, 5.300, 11.18]),
        'wp': 10.83
    }

    Al = {
        'f': np.array([0.532, 0.227, 0.050, 0.166, 0.030]),
        'g': np.array([0.047, 0.333, 0.312, 1.351, 3.382]),
        'w': np.array([0, 0.162, 1.544, 1.808, 3.473]),
        'wp': 14.98
    }

    Be = {
        'f': np.array([0.084, 0.031, 0.140, 0.530, 0.130]),
        'g': np.array([0.035, 1.664, 3.395, 4.454, 1.802]),
        'w': np.array([0, 0.100, 1.032, 3.183, 4.604]),
        'wp': 18.51
    }

    Cr = {
        'f': np.array([0.168, 0.151, 0.150, 1.149, 0.825]),
        'g': np.array([0.047, 3.175, 1.305, 2.676, 1.335]),
        'w': np.array([0, 0.121, 0.543, 1.970, 8.775]),
        'wp': 10.75
    }

    Ni = {
        'f': np.array([0.096, 0.100, 0.135, 0.106, 0.729]),
        'g': np.array([0.048, 4.511, 1.334, 2.178, 6.292]),
        'w': np.array([0, 0.174, 0.582, 1.597, 6.089]),
        'wp': 15.92
    }

    Pd = {
        'f': np.array([0.330, 0.649, 0.121, 0.638, 0.453]),
        'g': np.array([0.008, 2.950, 0.555, 4.621, 3.236]),
        'w': np.array([0, 0.336, 0.501, 1.659, 1.715]),
        'wp': 9.72
    }

    Pt = {
        'f': np.array([0.333, 0.191, 0.659, 0.547, 3.576]),
        'g': np.array([0.080, 0.517, 1.838, 3.668, 8.517]),
        'w': np.array([0, 0.780, 1.314, 3.141, 9.249]),
        'wp': 9.59
    }

    Ti = {
        'f': np.array([0.148, 0.899, 0.393, 0.187, 0.001]),
        'g': np.array([0.082, 2.276, 2.518, 1.663, 1.762]),
        'w': np.array([0, 0.777, 1.545, 2.509, 19.43]),
        'wp': 7.29
    }

    W = {
        'f': np.array([0.206, 0.054, 0.166, 0.706, 2.590]),
        'g': np.array([0.064, 0.530, 1.281, 3.332, 5.836]),
        'w': np.array([0, 1.004, 1.917, 3.580, 7.498]),
        'wp': 13.22
    }

    mats = {
        'Ag': Ag,
        'Au': Au,
        'Cu': Cu,
        'Al': Al,
        'Be': Be,
        'Cr': Cr,
        'Ni': Ni,
        'Pd': Pd,
        'Pt': Pt,
        'Ti': Ti,
        'W': W
    }

    # Generate the materials
    materials = []
    for key, val in mats.items():
        new_metal = LDMetal(
            name=key, **val
        )
        new_metal.save_ld_metal(overwrite=True)
        materials.append(new_metal)

    # Load the materials
    for filename in os.listdir(directory):
        file_directory = os.path.join(directory, filename)
        metal = load_ld_metal(file_directory)

        # Iterate through all metals and see which one has a matching name
        for stored_metal in materials:
            if stored_metal.name == metal.name:
                checks = [stored_metal.f - metal.f,
                          stored_metal.g - metal.g,
                          stored_metal.w - metal.w]
                for i, check in enumerate(checks):
                    if all(v == 0 for v in check):
                        print(f'Check {i + 1} passed for {metal.name}')
                    else:
                        print(f'Check {i + 1} failed for {metal.name}')
                if stored_metal.wp == metal.wp:
                    print(f'Check {len(checks) + 1} passed for {metal.name}')
                else:
                    print(f'Check {len(checks) + 1} failed for {metal.name}')

        # Provide a blank line
        print('')
