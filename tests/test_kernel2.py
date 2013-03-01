"""
 file: test_kernel2.py
 author: Peter Robinson
 created: 2/28/2013
 description:
    unittest test cases for pylulesh.Mesh.

"""

import unittest
import os
import glob

from os.path import join as pjoin

from pylulesh import *

import numpy as np

def check_remove(fname):
    if os.path.isfile(fname):
        os.remove(fname)

def prep_output_dir():
    odir = pjoin("tests","_output")
    if not os.path.isdir(odir):
        os.mkdir(odir)
    # clean out existing files
    for f in glob.glob(pjoin(odir,"*")):
        os.remove(f)

from time import time

class TestMesh(unittest.TestCase):
    def setUp(self):
        pass
    def test_kernel_2(self):
        m = Mesh.default([5,5,5],obase="kernel2_%04d")
        # put values in the dxx, dyy, dzz fields to make something happen
        m.element_vars["dxx"][:]= np.random.random_sample(m.num_elements).reshape((m.num_elements,1))
        m.element_vars["dyy"][:]= np.random.random_sample(m.num_elements).reshape((m.num_elements,1))
        m.element_vars["dzz"][:]= np.random.random_sample(m.num_elements).reshape((m.num_elements,1))
        t0  = time()
        kernel2_numpy.Kernel2(m)
        t1 = time()        
        kernel2_numba.Kernel2(m)
        t2 = time()
        kernel2_numba.Kernel2(m)
        t3 = time()
        print 'numpy time', t1 - t0        
        print 'autojit with compile ', t2 - t1
        print 'autojit post compile ', t3 - t2
        m.save()

if __name__ == '__main__':
    unittest.main()

