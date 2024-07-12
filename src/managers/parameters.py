"""
Class to store parameters for an inverse design project
"""


from typing import List
from src.inputs.parameter import Parameter


class ParameterManager:

    def __init__(self):
        self.parameters: List[Parameter] = []

        # Upper and lower bounds on the number of layers
        self.layer_lb: int = 0
        self.layer_ub: int = 0

        # Upper and lower bounds on the thickness of each layer
        self.thickness_lb: float = 0
        self.thickness_ub: float = 0

    def add_parameter(self, p: Parameter):
        self.parameters.append(p)
