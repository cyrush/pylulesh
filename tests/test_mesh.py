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
        prep_output_dir()
    def test_mesh_default(self):
        m = Mesh.default()
        print m
    def test_mesh_xdmf(self):
        m = Mesh.default(obase=pjoin("tests","_output","pylul_%04d"))
        h5_file  = m.output_fname(ext="h5")
        xmf_file = m.output_fname(ext="xmf")
        m.save()
        self.assertTrue(os.path.isfile(h5_file))
        self.assertTrue(os.path.isfile(xmf_file))


if __name__ == '__main__':
    unittest.main()

