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
import kernel2_pure
from pypymesh import *

import numpy as np

def test_kernel_2(dim):
    element_dims = [dim,dim,dim]
    obase="kernel2_%04d"
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
    kernel2_pure.Kernel2(m)
    v = m.element_vars["v"]
    vol = 0.0
    for i in xrange(len(v)):
        vol += v[i]
    print 'total volume =', vol

def entry_point(argv):
    test_kernel_2(int(argv[1]))
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)
