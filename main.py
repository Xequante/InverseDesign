from numpy.random import seed
from src.testing.material_uploads import load_all_materials


def main():
    seed(35447)  # Seed the RNG for reproducability
    load_all_materials()
    print('Hello World')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
