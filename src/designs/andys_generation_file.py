# code to generate test examples for the CNN networks
# Parallel calls to TMM code
# -->saves the entire file in memory while processing: generation of ~500k structures on 16GB RAM is OK
# arl92@case.edu 2021-01-22
# please refer to copyright

# include these files in the same folder
import TMM_numba as tmm
import BB_metals as bb
import LD_metals as ld
import dielectric_materials as di

# required modules to run generator
import numpy as np
import tables
import matplotlib.pyplot as plt
import datetime

date = datetime.datetime.now()
from joblib import Parallel, delayed
import multiprocessing
from tqdm import tqdm_notebook as tqdm

# import materials
wave = np.linspace(450, 950, 200) * 1E-9
ag = bb.nk_material('Ag', wave)
au = bb.nk_material('Au', wave)
ni = bb.nk_material('Ni', wave)
al2o3 = di.nk_material('al2o3', wave)
tio2 = di.nk_material('tio2', wave)
ito = di.nk_material('ito', wave)
gl = di.nk_Cauchy_Urbach(wave, 1.55,
                         0.005)  # glass model for substrate (based on 2-parameter cauchy fit of slides in lab)
void = np.ones(wave.size)  # vacuum

materials = np.array([ag, al2o3, ito, ni, tio2])

#########################################################################################
# System Parameters - What range of parameters are you searching?

num_mat = 5  # number of material choices in each layer (max is number of elements in materials)
num_lay = 5  # number of total layers in each system
ang = np.array(
    [25., 45., 65.])  # angles to calculate for each system [deg from normal]
min_thick = 1E-9  # minimum layer thickness [in m]
max_thick = 60E-9  # maximum layer thickness [in m]
n_super = void  # material to be used for superstrate
n_subst = gl  # material to be used for substrate

# parameters for generating random data set
np.random.seed(35447)  # Seed the RNG for reproducability
set_length = 200000  # Number of samples in data file (warning: make sure you have enough RAM!)
###########################################################################################
l = np.ones(num_lay).astype('double')
ranges = np.array([min_thick, max_thick])

# write a general discription of the dataset including parameters
# saved as a txt file in the same folder, makes usage easier
comments = 'Materials: Ag,Al2O3,ITO,Ni,TiO2. trange 1-60nm. Return [ang,mats,l, Rp, Rs, Tp, Ts, Ellipsometric] 25-45-65'
# this filename is where the data will be saved
froot = 'data_rte+ni_gen' + str(l.size) + 'lay' + str(num_mat) + 'mat_' + str(
    set_length) + 'n_v-tma_' + date.strftime("%Y") + date.strftime(
    "%m") + date.strftime("%d")
coms = open(froot + '_comments.txt', "w")
coms.write(comments)
coms.close()


################### GENERATION SCRIPT #######################

def generate_fcn(wave, n_subst, n_super, materials, num_mat, ranges, ang, l):
    n = np.zeros((l.size, wave.size), dtype=complex)
    psi = np.zeros(wave.size * ang.size)
    delta = np.zeros(wave.size * ang.size)
    rp = np.zeros(wave.size * ang.size)
    rs = np.zeros(wave.size * ang.size)
    tp = np.zeros(wave.size * ang.size)
    ts = np.zeros(wave.size * ang.size)
    m = np.zeros((num_mat * l.size))

    # create a random structure within the parameter space
    for el in range(0, l.size):
        # choose a random material from library
        mat = np.random.randint(low=0, high=num_mat)
        # do not allow subsequent layers to be the same material
        if el > 0:
            while mold == mat:
                mat = np.random.randint(low=0, high=num_mat)
        mold = mat
        # assign material to layer
        n[el, :] = materials[mat, :]
        m[mat + num_mat * el] = 1

        # choose layer thickness
        l[el] = np.random.uniform(low=ranges[0], high=ranges[1])

    # calculate output for all angles (flattened arrays)
    # set up to return reflectance, transmittance, and ellipsometric data for all structures
    for j in range(0, ang.size):
        for i in range(0, wave.size):
            (psi[i + wave.size * j], delta[i + wave.size * j]) = tmm.ellips(
                ang[j], wave[i], n[:, i], l, n_super[i], n_subst[i])
            rp[i + wave.size * j] = tmm.reflect_amp(1, ang[j], wave[i],
                                                    n[:, i], l, n_super[i],
                                                    n_subst[i])
            rs[i + wave.size * j] = tmm.reflect_amp(0, ang[j], wave[i],
                                                    n[:, i], l, n_super[i],
                                                    n_subst[i])
            tp[i + wave.size * j] = tmm.trans_amp(1, ang[j], wave[i], n[:, i],
                                                  l, n_super[i], n_subst[i])
            ts[i + wave.size * j] = tmm.trans_amp(0, ang[j], wave[i], n[:, i],
                                                  l, n_super[i], n_subst[i])
    data_save = np.concatenate((ang, m, l, rp, rs, tp, tp, psi, delta),
                               axis=None)
    data_save = np.reshape(data_save, (1, data_save.size))
    return data_save


print('Generating Parallel Pool...\n')
cores = multiprocessing.cpu_count()
print('Parallel: %d Found Cores.\n' % (cores))
print('Generating Data...\n')
results = Parallel(n_jobs=cores)(
    delayed(generate_fcn)(wave, n_subst, n_super, materials, num_mat, ranges,
                          ang, l) for g in tqdm(range(set_length)))
try:
    filename = froot + '.h5'
    print('Opening File: %s\n' % (filename))
    f = tables.open_file(filename, mode='w')
    atom = tables.Float64Atom()
    wid = len(results[0][0])
    shape = (0, wid)
    array_c = f.create_earray(f.root, 'data', atom, shape)
    print('Saving Data...\n')
    for i in range(set_length):
        array_c.append(np.reshape(results[i], (1, wid)))
    print('Closing File: %s\n' % (filename))
    f.close()
    print('Completed!')
    del results
except:
    f.close()
    print('Error in datasave!')
