"""
 file: mesh.py
 author: Cyrus Harrison <cyrush@llnl.gov>
 created: 2/26/2013
 description:
    LULESH Mesh

"""

import numpy as np
import xdmf

# if we have 2.7, use an OrderedDict instead of a standard dict
dict_type = dict
try:
    from collections import OrderedDict
    dict_type = OrderedDict
except:
    pass

# we can use this as an entry point to select python lists or numpy arrays
def alloc_ndarray(shape,dtype):
    if isinstance(dtype,str):
        if dtype == "double":
            return [0.0] * (shape[0]*shape[1])
        else:
            return [0] * (shape[0]*shape[1])
    else:
        return np.zeros(shape=shape,dtype=dtype)

class Mesh(object):
    """
    Main mesh class.
    """
    def __init__(self,
                 element_dims,
                 element_vars = None,
                 node_vars   = None,
                 obase = "pylul_%04d",
                 cycle = 0):
        self.element_dims = element_dims
        self.node_dims    = [element_dims[i]+1 for i in range(3)]
        self.num_elements = element_dims[0] * element_dims[1] * element_dims[2]
        self.num_nodes    = self.node_dims[0] * self.node_dims[1] * self.node_dims[2]
        self.xyz   = alloc_ndarray([self.num_nodes,3],np.float64)
        self.conn  = alloc_ndarray([self.num_elements,8],np.int32)
        self.obase = obase
        self.cycle = cycle
        self.element_vars = dict_type()
        self.node_vars   = dict_type()
        self.__init_topo()
        if not element_vars is None:
            for ev in element_vars:
                self.add_element_var(ev)
        if not node_vars is None:
            for nv in node_vars:
                self.add_node_var(nv)
    def add_element_var(self,name,ncomps=1):
        self.element_vars[name] = alloc_ndarray([self.num_elements,ncomps],np.float64)
    def add_node_var(self,name,ncomps=1):
        self.node_vars[name]   = alloc_ndarray([self.num_nodes,ncomps],np.float64)
    def __init_topo(self):
        tz = 0.0
        ty = 0.0
        tx = 0.0
        nidx = 0
        nodes_x, nodes_y, nodes_z  = self.node_dims
        elems_x, elems_y, elems_z  = self.element_dims
        for k in xrange(nodes_z):
            tz =  (1.125 * float(k)) / float(elems_z)
            for j in xrange(nodes_y):
                ty = (1.125 * float(j)) / float(elems_y)
                for i in xrange(nodes_x):
                    tx = (1.125 * float(i)) / float(elems_x)
                    self.xyz[nidx,0] = tx
                    self.xyz[nidx,1] = ty
                    self.xyz[nidx,2] = tz
                    nidx+=1
        nidx = 0
        zidx = 0
        for k in xrange(elems_z):
            for j in xrange(elems_y):
                for i in xrange(elems_x):
                    self.conn[zidx,0] = nidx
                    self.conn[zidx,1] = nidx                     + 1
                    self.conn[zidx,2] = nidx                     +  nodes_x + 1
                    self.conn[zidx,3] = nidx                     +  nodes_x
                    self.conn[zidx,4] = nidx + nodes_x * nodes_y
                    self.conn[zidx,5] = nidx + nodes_x * nodes_y + 1
                    self.conn[zidx,6] = nidx + nodes_x * nodes_y + nodes_z +  1
                    self.conn[zidx,7] = nidx + nodes_x * nodes_y + nodes_z
                    zidx+=1
                    nidx+=1
                nidx+=1
            nidx+= nodes_x
    def __repr__(self):
        return str(self)
    def __str__(self):
        res = ["Mesh:",
               " element_dims = %s" % str(self.element_dims),
               " node_dims    = %s" % str(self.node_dims),
               " num_elements = %d"   % self.num_elements,
               " num_nodes    = %d"   % self.num_nodes,
               " obase        = %s" % str(self.obase),
               " cycle        = %d" % self.cycle,
               " output_base  = %s" % str(self.output_base()),
               " element_vars = %s" % str(self.element_vars.keys()),
               " node_vars   = %s" % str(self.node_vars.keys())]
        return "\n".join(res)
    def output_base(self):
        return self.obase % self.cycle
    def output_fname(self,ext):
        return (self.obase + ".%s") % (self.cycle,ext)
    def save(self,inline=False):
        xdmf.write_xdmf(self,inline)
    @classmethod
    def default(cls,element_dims = None,obase="pylul_%04d"):
        if element_dims is None:
            element_dims = [45,45,45]
        m = Mesh(element_dims,
                 obase = obase,
                 element_vars = ["p","e","q","v",
                                 "vdov","delv","volo",
                                 "arealg",
                                 "dxx","dyy","dzz",
                                 "ql","qq"],
                 node_vars = ["xd","yd","zd",
                              "xdd","ydd","zdd",
                              "fx","fy","fz",
                              "mass"])
        return m

