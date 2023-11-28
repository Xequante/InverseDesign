"""
Class which stores all the details of the Inverse Design
"""


from typing import List, Union
from src.parameters import ParameterManager
from src.inputs.transmission import Transmission
from src.inputs.reflectance import Reflectance
from src.inputs.material import Material
from src.inputs.parameter import Parameter


class InverseDesign:

    def __init__(self,
                 transmission=Transmission.STANDARD,
                 reflectance=Reflectance.STANDARD,
                 materials: List[Material] = None):

        # Type of transmission and reflection which we will be considering
        self.transmission: Transmission = Transmission.STANDARD
        self.reflectance: Reflectance = Reflectance.STANDARD

        # Library of materials
        self.materials = materials
        if self.materials is None:
            self.materials = []

        # Parameter manager for the design
        self._parameters = ParameterManager()

    def set_transmission(self, transmission: Transmission):
        self.transmission = transmission

    def set_reflectance(self, reflectance: Transmission):
        self.reflectance = reflectance

    def add_material(self, m: Union[Material, List[Material]]):
        pass

    def add_parameter(self, p: Parameter):
        self._parameters.add_parameter(p)
