"""
Object to store the design of a thin film stack
"""


from typing import List
from src.inputs.material import Material


class ThinFilmLayer:

    def __init__(self, thickness: float, material: Material):
        self.thickness: float = thickness
        self.material: Material = material


class ThinFilmStack:

    def __init__(self, layers):
        self.layers: List[ThinFilmLayer] = layers
