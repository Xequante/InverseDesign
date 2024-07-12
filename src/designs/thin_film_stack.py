"""
Object to store the design of a thin film stack
"""


from typing import List
from src.inputs.material import Material
import numpy as np
from numpy import pi


class ThinFilmLayer:

    def __init__(self, thickness: float, material: Material):
        self.thickness: float = thickness
        self.material: Material = material


class ThinFilmStack:

    def __init__(self, layers):
        self.layers: List[ThinFilmLayer] = layers

    def __len__(self):
        return len(self.layers)

    def characterize_stack(self, wavelengths=None, theta=None,
                           wl_min=400e-9, wl_max=800e-9, wl_n=100,
                           theta_min=0, theta_max=pi/2, theta_n=100):

        # Create linspace for values of wavelength and theta we are testing
        if wavelengths is None:
            wavelengths = np.linspace(wl_min, wl_max, wl_n)
        if theta is None:
            theta = np.linspace(theta_min, theta_max, theta_n)

        # Create meshgrids
        wl_mesh, theta_mesh = np.meshgrid(wavelengths, theta)

        # Compute the transmission for each wl and theta
