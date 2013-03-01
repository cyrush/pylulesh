"""
 file: test_mesh.py
 author: Cyrus Harrison <cyrush@llnl.gov>
 created: 2/26/2013
 description:
    unittest test cases for pylulesh.Mesh.

"""

import os
import glob
import sys

from os.path import join as pjoin
import kernel1
from kernel1 import setupPy
from pypymesh import *

import numpy as np

setupPy()

def test_kernel_1(dim):
    element_dims = [dim,dim,dim]
    obase="kernel1_%04d"
    m = Mesh(element_dims,
             obase = obase,
             float_type="double",
             int_type="int",
             element_vars = ["p","e","q","v",
                             "vdov","delv","volo",
                             "arealg",
                             "dxx","dyy","dzz",
                             "ql","qq"],
             node_vars = ["xd","yd","zd",
                          "xdd","ydd","zdd",
                          "fx","fy","fz",
                          "mass"])
    kernel1.element_volume_driver_py(m)
    v = m.element_vars["v"]
    vol = 0.0
    for i in xrange(len(v)):
        vol += v[i]
    print 'total volume =', vol

def entry_point(argv):
    test_kernel_1(int(argv[1]))
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)
