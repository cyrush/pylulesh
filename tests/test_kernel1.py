"""
 file: test_mesh.py
 author: Cyrus Harrison <cyrush@llnl.gov>
 created: 2/26/2013
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
    def test_kernel1_01_pure(self):
        m = Mesh.default([5,5,5],float_type="double",int_type="int",obase="kernel1_pure_%04d")
        kernel1_pure.element_volume(m)
        #m.save() # no save for pure python mesh
    def test_kernel1_02_numpy(self):
        m = Mesh.default([5,5,5],obase="kernel1_numpy_%04d")
        kernel1_numpy.element_volume(m)
        m.save()
    def test_kernel1_03_numba(self):
        m = Mesh.default([5,5,5],obase="kernel1_numba_%04d")
        kernel1_numba_2.element_volume(m)
        m.save()



if __name__ == '__main__':
    unittest.main()

