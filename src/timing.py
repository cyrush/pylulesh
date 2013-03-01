import numpy as np
import pylab
import timeit
import json

import mesh
import kernel1_pure
import kernel1_numpy
import kernel1_numpy_2
import kernel1_numba
import kernel1_numba_2
import kernel1_opencl

import kernel2_pure
import kernel2_numpy
import kernel2_numba

from xkcd import *


def run_ocl_test(m,tag,kname,kernel,plat_id,res):
    kernel.element_volume(m,plat_id)
    print np.sum(m.element_vars["v"])
    edge = m.element_dims[0]
    t_sum = 0
    for i in range(5):
        t_sum += kernel.element_volume(m,plat_id)
    t_res = t_sum / 5.0
    res[tag][edge] = t_res

def run_test(m,tag,kname,kernel,res):
    #wt = WallTimer("%s_%s_%d" % (kname,tag,edge))
    #wt.start()
    kernel.element_volume(m)
    print np.sum(m.element_vars["v"])
    #wt.stop()
    #t_res = wt.get_elapsed()
    #print kernel
    edge = m.element_dims[0]
    msetup  = "import pylulesh\n"
    msetup += 'm = pylulesh.Mesh.default([%d,%d,%d],'  % (m.element_dims[0],m.element_dims[1],m.element_dims[2])
    msetup += 'float_type="%s",int_type="%s")\n' % (m.float_type,m.int_type)
    msetup += 'import pylulesh.kernel1_%s as kernel\n' % tag
    t = timeit.Timer("kernel.element_volume(m)",msetup)
    t_res = t.timeit(5) / 5.0
    res[tag][edge] = t_res

def run_test2(m,tag,kname,kernel,res):
    #wt = WallTimer("%s_%s_%d" % (kname,tag,edge))
    #wt.start()
    kernel.Kernel2(m)
    print np.sum(m.element_vars["v"])
    #wt.stop()
    #t_res = wt.get_elapsed()
    #print kernel
    edge = m.element_dims[0]
    msetup  = "import pylulesh\n"
    msetup += 'm = pylulesh.Mesh.default([%d,%d,%d],'  % (m.element_dims[0],m.element_dims[1],m.element_dims[2])
    msetup += 'float_type="%s",int_type="%s")\n' % (m.float_type,m.int_type)
    msetup += 'import pylulesh.kernel2_%s as kernel\n' % tag
    t = timeit.Timer("kernel.Kernel2(m)",msetup)
    t_res = t.timeit(5) / 5.0
    res[tag][edge] = t_res

class WallTimer(object):
    def __init__(self,tag):
        self.tag = tag
    def start(self):
        from time import time
        self.__start = time()
    def stop(self):
        from time import time
        self.__end   = time()
    def get_elapsed(self):
        return self.__end - self.__start
    def __str__(self):
        return "%s %s (s)" % (self.tag,repr(self.get_elapsed()))

def plot_results(res,ofile):
    xs = res["xs"]
    xs.sort()
    #fig = pylab.figure()
    #ax = fig.add_subplot(1, 1, 1)
    ys = []
    for k in res.keys():
        if k == "xs":
            continue
        r    = np.zeros(shape=(len(xs),),dtype=np.float64) 
        r[:] =[ res[k][x] for x in xs ]
        ys.append(r)
        #ax.plot(xs, ys,label=k)
    #handles, labels = ax.get_legend_handles_labels()
    #ax.legend(handles, labels)
    #fig.savefig(ofile)
    print xs,ys
    fig = xkcd_plot(xs,ys)
    fig.savefig(ofile)
    return fig

def run_kernel1():
    res = {"pure":{},"numpy":{},"numpy_2":{},"numba":{},"numba_2":{},"ocl_p_0":{},"xs":[2,8,16]}
    for edge in res["xs"]:
        m_pure  = mesh.Mesh.default([edge,edge,edge],
                                     float_type="double",
                                     int_type="int")
        m_numpy = mesh.Mesh.default([edge,edge,edge])
        m_numba = mesh.Mesh.default([edge,edge,edge])
        m_ocl   = mesh.Mesh.default([edge,edge,edge])
        run_test(m_pure,"pure","k1",kernel1_pure,res)
        run_test(m_numpy,"numpy","k1",kernel1_numpy,res)
        run_test(m_numpy,"numpy_2","k1",kernel1_numpy_2,res)
        run_test(m_numba,"numba","k1",kernel1_numba,res)
        run_test(m_numba,"numba_2","k1",kernel1_numba_2,res)
        run_ocl_test(m_ocl,"ocl_p_0","k1",kernel1_opencl,0,res)
        json.dump(res,open("k1_timing_results.json","w"))
    return plot_results(res,"k1_timing_results.png")

def run_kernel2():
    res = {"pure":{},"numpy":{},"numba":{},"xs":[2,8,16]}
    for edge in res["xs"]:
        m_pure  = mesh.Mesh.default([edge,edge,edge],
                                     float_type="double",
                                     int_type="int")
        m_numpy = mesh.Mesh.default([edge,edge,edge])
        m_numba = mesh.Mesh.default([edge,edge,edge])
        run_test2(m_pure,"pure","k2",kernel2_pure,res)
        run_test2(m_numpy,"numpy","k2",kernel2_numpy,res)
        run_test2(m_numba,"numba","k2",kernel2_numba,res)
        json.dump(res,open("k2_timing_results.json","w"))
    return plot_results(res,"k2_timing_results.png")
