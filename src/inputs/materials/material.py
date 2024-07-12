"""
Class to define the specifications of a material
"""


from enum import Enum
from abc import ABC, abstractmethod


class MaterialType(Enum):
    DIALECTRIC = 0
    LD = 1
    BB = 2


class Material(ABC):

    def __init__(self,
                 name: str = '',
                 classification: MaterialType = MaterialType.DIALECTRIC):

        self.name = name
        self.classification = MaterialType

    def __eq__(self, other):
        if not isinstance(other, Material):
            return False
        if self.name != other.name:
            return False
        if self.classification != other.classification:
            return False
        return True

    @abstractmethod
    def index_of_refraction(self, wavelengths):
        pass
