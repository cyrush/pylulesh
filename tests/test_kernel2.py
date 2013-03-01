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

class TestMesh(unittest.TestCase):
    def setUp(self):
        pass
    def test_kernel_2(self):
        m = Mesh.default(obase="kernel2_%04d")
        # put values in the dxx, dyy, dzz fields to make something happen
        m.element_vars["dxx"]= np.random.random_sample(m.num_elements)
        m.element_vars["dyy"]= np.random.random_sample(m.num_elements)
        m.element_vars["dzz"]= np.random.random_sample(m.num_elements)
        kernel2.Kernel2(m)
        m.save()

if __name__ == '__main__':
    unittest.main()

