"""
Class to store parameters for an inverse design project
"""

from typing import List
from inputs.parameter import Parameter


class ParameterManager:

    def __init__(self):
        self.parameters: List[Parameter] = []

    def add_parameter(self, p: Parameter):
        self.parameters.append(p)
