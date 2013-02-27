"""
 file: test_mesh.py
 author: Cyrus Harrison <cyrush@llnl.gov>
 created: 2/26/2013
 description:
    unittest test cases for pylulesh.Mesh.

"""

import unittest
import os
import shutil

from os.path import join as pjoin

from pylulesh import *

import numpy as np

def check_remove(fname):
    if os.path.isfile(fname):
        os.remove(fname)

def prep_output_dir():
    odir = pjoin("tests","_output")
    if os.path.isdir(odir):
        shutil.rmtree(odir)
    os.mkdir(odir)


class TestMesh(unittest.TestCase):
    def setUp(self):
        pass
    def test_mesh_01_default(self):
        #prep_output_dir()
        m = Mesh.default()
        print m
    def test_mesh_02_xdmf_hdf5(self):
        m = Mesh.default([3,3,3],obase=pjoin("tests","_output","pylul_%04d_hdf5"))
        h5_file  = m.output_fname(ext="h5")
        xmf_file = m.output_fname(ext="xmf")
        m.save()
        self.assertTrue(os.path.isfile(h5_file))
        self.assertTrue(os.path.isfile(xmf_file))
    def test_mesh_03_xdmf_inline(self):
        m = Mesh([3,3,3],obase=pjoin("tests","_output","pylul_%04d_inline"))
        m.add_element_var("element_var")
        m.add_nodal_var("node_var")
        m.element_vars["element_var"][:]   = np.arange(27).reshape((27,1))
        m.nodal_vars["node_var"][:] = np.arange(64).reshape((64,1))
        xmf_file = m.output_fname(ext="xmf")
        m.save(inline=True)
        self.assertTrue(os.path.isfile(xmf_file))


if __name__ == '__main__':
    unittest.main()

