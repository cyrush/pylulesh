import numpy as np
import pylab
import timeit

import mesh
import kernel1_pure
import kernel1_numpy
import kernel1_numba



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
    fig = pylab.figure()
    ax = fig.add_subplot(1, 1, 1)
    for k in res.keys():
        if k == "xs":
            continue
        ys = [ res[k][x] for x in xs ]
        ax.plot(xs, ys,label=k)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    fig.savefig(ofile)
    return fig

def run_kernel1():
    res = {"pure":{},"numpy":{},"numba":{},"xs":[2,8,16,32]}
    for edge in res["xs"]:
        m_pure  = mesh.Mesh.default([edge,edge,edge],
                                     float_type="double",
                                     int_type="int")
        m_numpy = mesh.Mesh.default([edge,edge,edge])
        m_numba = mesh.Mesh.default([edge,edge,edge])
        run_test(m_pure,"pure","k1",kernel1_pure,res)
        run_test(m_numpy,"numpy","k1",kernel1_numpy,res)
        run_test(m_numba,"numba","k1",kernel1_numba,res)
    return plot_results(res,"k1_timing_results.png")