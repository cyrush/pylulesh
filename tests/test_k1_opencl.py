"""
 file: test_env.py
 author: Cyrus Harrison <cyrush@llnl.gov>
 created: 2/16/2013
 description:
    unittest test cases for pylulesh deps.
"""

import unittest
from pylulesh import *

class TestEnv(unittest.TestCase):
    def setUp(self):
        pass
    def test_pyopencl(self):
        mesh = Mesh.default(obase="kernel1_ocl_%04d")
        kernel1_opencl.element_volume(mesh)
        mesh.save()
        
if __name__ == '__main__':
    unittest.main()
