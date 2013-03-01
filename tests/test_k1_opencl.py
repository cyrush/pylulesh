"""
 file: test_env.py
 author: Cyrus Harrison <cyrush@llnl.gov>
 created: 2/16/2013
 description:
    unittest test cases for pylulesh deps.
"""

import unittest
from pylulesh import *
using_pyocl = False
try:
    import pyopencl
    using_pyocl = True
except:
    pass


class TestEnv(unittest.TestCase):
    def setUp(self):
        pass
    def test_pyopencl(self):
        if using_pyocl:
            mesh = Mesh.default(obase="kernel1_ocl_%04d")
            tmg0 = kernel1_opencl.element_volume(mesh, 0)
            tmg1 = kernel1_opencl.element_volume(mesh, 1)
            mesh.save()

            print "Execution time0: %g sec" % tmg0
            print "Execution time1: %g sec" % tmg1
        
if __name__ == '__main__':
    unittest.main()
