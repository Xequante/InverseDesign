import numpy as np
import os
from struct import pack, unpack
from nptyping import NDArray
from typing import Union, List
from scipy.special import wofz
from src.inputs.materials.material import Material, MaterialType


class BBMetal(Material):

    def __init__(self,
                 name: str = '',
                 f: Union[None, NDArray] = None,
                 g: Union[None, NDArray] = None,
                 w: Union[None, NDArray] = None,
                 s: Union[None, NDArray] = None,
                 wp: float = 0.):

        # Run the super class method
        super().__init__(name=name, classification=MaterialType.BB)

        # Store relevant parameters
        self.f: Union[None, NDArray] = f
        self.g: Union[None, NDArray] = g
        self.w: Union[None, NDArray] = w
        self.s: Union[None, NDArray] = s
        self.wp: float = wp

        # Check to make sure the stored data is compatible
        if not self._compatibility():
            raise SyntaxError('Arrays of different sizes cannot be used when '
                              'defining a material')

    def __eq__(self, other):
        if not super.__eq__(self, other):
            return False
        if self.f != other.f or self.g != other.g:
            return False
        if self.w != other.w or self.s != other.s:
            return False
        if self.wp != other.wp:
            return False
        return True

    def _none_entries(self) -> bool:
        if self.f is None or self.g is None:
            return True
        if self.w is None or self.s is None:
            return True
        return False

    def _compatibility(self) -> bool:
        """
        Ensures that the stored parameters f,g,w,s have the same length.
        Ignores anything stored as 'None'

        :return: bool
        """

        # Initial variable to store the length of anything that is not 'None'
        data_length = -1

        # Cycle through all the parameters
        stored_data = [self.f, self.g, self.w, self.s]
        for data in stored_data:
            if data is not None:
                if data_length < 0:
                    data_length = len(data)
                elif len(data) != data_length:
                    return False
        return True

    def eps_material(self, wavelengths, numosc: int = 5):
        """
        Returns the complex dialectric function for a given wavelength

        :param wavelengths:
        :param numosc:
        :return:
        """

        # Photon energy in eV
        pen = np.divide(1239.84193E-9, wavelengths)

        # Ensure numosc is >= 1
        if numosc <= 0:
            numosc = 1

        # Free electron eps
        eps_free = 1 - np.divide(
            np.power(np.sqrt(self.f[0]) * self.wp, 2),
            np.multiply(pen, pen + 1j * self.g[0]))

        # Bound electron eps
        eps_bound = 0 + 1j * 0
        for i in range(np.min([len(self.f) - 1, numosc])):
            a = np.sqrt(
                np.power(pen, 2) + np.multiply(1j * self.g[i + 1], pen))
            b = np.divide(
                1j * np.sqrt(np.pi) * self.f[i + 1] * self.wp * self.wp,
                np.multiply(2 * np.sqrt(2) * self.s[i + 1], a))
            c = wofz(np.divide(
                np.subtract(a, self.w[i + 1]),
                np.sqrt(2) * self.s[i + 1]))
            d = wofz(np.divide(
                a + self.w[i + 1],
                np.sqrt(2) * self.s[i + 1]))
            eps_bound += np.multiply(b, c + d)

        # complex dielectric function
        return eps_free + eps_bound

    def index_of_refraction(self, wavelengths):
        eps = self.eps_material(wavelengths)
        return np.sqrt(eps)

    def save_bb_metal(self,
                      directory='resources/materials/bb_metals',
                      filename: Union[None, str] = None,
                      overwrite=False):

        # Ensure that there are no None entries and all data is compatible
        if not self._compatibility():
            raise SyntaxError('Cannot save incompatible data')
        if self._none_entries():
            raise SyntaxError('Cannot save incomplete material object')

        # Compile all the data into a singular list
        bb_metal_data: List[float] = list(self.f)
        bb_metal_data += list(self.g) + list(self.w) + list(self.s)
        bb_metal_data.append(self.wp)

        # Create the filename that this will be saved to
        if filename is None:
            filename = os.path.join(directory, f'{self.name}_bb_metal')

        # Open the file
        if overwrite:
            output_file = open(filename, 'wb')
        else:
            try:
                output_file = open(filename, 'xb')
            except FileExistsError:
                raise FileExistsError(
                    f'Cannot save material to {filename} '
                    f'without overwriting existing file')

        # Obtain relevent lengths
        name_length = len(self.name)
        num_doubles = len(self.f)
        packed_data = pack(
            f'II{name_length}s{4 * num_doubles + 1}d',
            name_length, num_doubles,
            self.name.encode('utf-8'), *bb_metal_data
        )

        # Write the packed data to the file then close it
        output_file.write(packed_data)
        output_file.close()


def load_bb_metal(filename):
    with open(filename, 'rb') as binary_file:

        # Read the length of the string
        name_length = unpack('I', binary_file.read(4))[0]

        # Read the length of the arrays
        array_length = unpack('I', binary_file.read(4))[0]

        # Return the read cursor to 0, and read the entire file
        binary_file.seek(0)
        unpacked_data = unpack(f'II{name_length}s{4 * array_length + 1}d',
                               binary_file.read())

    # Extract the name of the material and the data being stored.
    material_name = unpacked_data[2]
    stored_data = list(unpacked_data[3:])

    # Organize the extracted data
    wp = stored_data.pop()
    f = stored_data[0: array_length]
    g = stored_data[array_length: (2 * array_length)]
    w = stored_data[2 * array_length: (3 * array_length)]
    s = stored_data[3 * array_length: (4 * array_length)]

    # Generate a material name if not given
    if material_name is None:
        file_tag = filename.split('/')[-1]
        if file_tag[-9:] == '_bb_metal':
            material_name = file_tag[:-9]
        else:
            raise SyntaxError('Name of material unspecified')

    # Create and return the bb_metal
    return BBMetal(
        name=material_name.decode('utf-8'),
        f=np.array(f), g=np.array(g), w=np.array(w), s=np.array(s), wp=wp
    )
