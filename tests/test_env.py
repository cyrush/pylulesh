"""
 file: test_env.py
 author: Cyrus Harrison <cyrush@llnl.gov>
 created: 2/16/2013
 description:
    unittest test cases for pylulesh deps.

"""

import unittest
import os


def sum2d(arr):
    m, n = arr.shape
    result = 0.0
    for i in range(m):
        for j in range(n):
            result += arr[i,j]
    return result


class TestEnv(unittest.TestCase):
    def setUp(self):
        pass
    def test_matplotlib(self):
        import numpy as np
        import pylab
        if os.path.isfile("mpl_test.png"):
            os.remove("mpl_test.png")
        fig = pylab.figure()
        x = np.linspace(0,2*np.pi,100)
        y = 2*np.sin(x)
        ax = fig.add_subplot(1,1,1)
        ax.plot(x,y)
        pylab.savefig("mpl_test.png")
        self.assertTrue(os.path.isfile("mpl_test.png"))
        if os.path.isfile("mpl_test.png"):
            os.remove("mpl_test.png")
    def test_h5py(self):
        # write an array to hdf5 file
        # read it back using another hdf5 handle.
        import numpy as np
        import h5py
        if os.path.isfile("test.hdf5"):
            os.remove("test.hdf5")
        wr_vals = np.ones(shape=(10,1),dtype=np.float64)
        wr_vals[5] = 11
        f_out = h5py.File('test.hdf5', 'w')
        f_out["data"] = wr_vals
        f_out.close()
        f_in  = h5py.File('test.hdf5', 'r')
        rd_vals = f_in["data"].value
        if os.path.isfile("test.hdf5"):
            os.remove("test.hdf5")
        self.assertEqual(np.sum(wr_vals - rd_vals),0.0)
    def test_numba(self):
        # jit & run a python function using numba
        import numpy as np
        from numba import double, jit
        vals = np.ones(shape=(10,10),dtype=np.float64)
        numba_sum2d = jit(double[:,:](double[:,:]))(sum2d)
        r = numba_sum2d(vals)
        self.assertEqual(r,100.0)
    def test_pyopencl(self):
        # test simple pyopencl kernel 
        # on this first dev in the first platform
        import pyopencl as cl
        import numpy as np
        import numpy.linalg as la
        a = np.ones(shape=(1,1),dtype=np.float64)
        b = np.ones(shape=(1,1),dtype=np.float64)
        plat_id = 0
        dev_id  = 0
        platform = cl.get_platforms()[plat_id]
        device = platform.get_devices()[dev_id]
        cinfo  = "OpenCL Context Info\n"
        cinfo += " Using platform id = %d\n" % plat_id
        cinfo += "  Platform name: %s\n" % platform.name
        cinfo += "  Platform profile: %s\n" % platform.profile
        cinfo += "  Platform vendor: %s\n" % platform.vendor
        cinfo += "  Platform version: %s\n" % platform.version
        cinfo += " Using device id = %d\n" % dev_id
        cinfo += "  Device name: %s\n" % device.name
        cinfo += "  Device type: %s\n" % cl.device_type.to_string(device.type)
        cinfo += "  Device memory: %s\n" % device.global_mem_size
        cinfo += "  Device max clock speed: %s MHz\n" % device.max_clock_frequency
        cinfo += "  Device compute units: %s\n" % device.max_compute_units
        print cinfo
        ctx   = cl.Context([device])
        queue = cl.CommandQueue(ctx)
        mf = cl.mem_flags
        a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
        b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
        dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, b.nbytes)
        prg = cl.Program(ctx, """
            __kernel void sum(__global const double *a,
            __global const double *b, __global double *c)
            {
              int gid = get_global_id(0);
              c[gid] = a[gid] + b[gid];
            }
            """).build()
        prg.sum(queue, a.shape, None, a_buf, b_buf, dest_buf)
        pyocl_res = np.empty_like(a)
        cl.enqueue_copy(queue, pyocl_res, dest_buf)
        rtest = (pyocl_res  - (a+b))
        self.assertTrue(rtest < 1e-8)


if __name__ == '__main__':
    unittest.main()

