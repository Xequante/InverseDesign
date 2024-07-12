"""
Class which stores all the details of the Inverse Design
"""


from typing import List, Union
from numpy.random import randint, uniform
from src.designs.thin_film_stack import ThinFilmLayer, ThinFilmStack
from src.managers.parameters import ParameterManager
from src.inputs.transmission import Transmission
from src.inputs.reflectance import Reflectance
from src.inputs.materials.material import Material
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
        if isinstance(m, list):
            self.materials += m
        else:
            self.materials.append(m)

    def remove_material(self, m: Union[Material, List[Material]]):
        if isinstance(m, list):
            for material in m:
                while material in self.materials:
                    self.materials.remove(material)
        else:
            self.materials.remove(m)

    def add_parameter(self, p: Parameter):
        self._parameters.add_parameter(p)

    def generate_designs(self, n: int = 1) -> List[ThinFilmStack]:
        """
        Creates random thin film stacks that meets the parameters
        :return: List[ThinFilmStack]
        """

        # Generate n stacks then return the list
        stacks: List[ThinFilmStack] = []
        for i in range(n):
            stacks.append(self.generate_design())
        return stacks

    def generate_design(self) -> ThinFilmStack:
        """
        Creates a random thin film stack that meets the parameters
        :return: ThinFilmStack
        """

        # Decide on a number of layers
        num_layers = randint(self._parameters.layer_lb,
                             self._parameters.layer_ub + 1)

        # Create a think film with this number of layers
        layers = []
        for i in range(num_layers):

            # Choose a thickness
            thickness = uniform(self._parameters.thickness_lb,
                                self._parameters.thickness_ub)

            # Choose a material (may be some restrictions on this
            material = self.materials[randint(len(self.materials))]

            # Create the layer and add it
            layers.append(ThinFilmLayer(thickness, material))

        # Generate the thin film stack from this list of layers
        return ThinFilmStack(layers)
