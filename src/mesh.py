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
                 nodal_vars   = None,
                 obase = "pylul_%04d",
                 cycle = 0):
        self.element_dims = element_dims
        self.nodal_dims   = [element_dims[i]+1 for i in range(3)]
        self.num_elements = element_dims[0] * element_dims[1] * element_dims[2]
        self.num_nodes    = self.nodal_dims[0] * self.nodal_dims[1] * self.nodal_dims[2]
        self.xyz   = alloc_ndarray([self.num_nodes,3],np.float64)
        self.conn  = alloc_ndarray([self.num_elements,8],np.int32)
        self.obase = obase
        self.cycle = cycle
        self.element_vars = dict_type()
        self.nodal_vars   = dict_type()
        if not element_vars is None:
            for ev in element_vars:
                self.add_element_var(ev)
        if not nodal_vars is None:
            for nv in nodal_vars:
                self.add_nodal_var(nv)
    def add_element_var(self,name,ncomps=1):
        self.element_vars[name] = alloc_ndarray([self.num_elements,ncomps],np.float64)
    def add_nodal_var(self,name,ncomps=1):
        self.nodal_vars[name]   = alloc_ndarray([self.num_nodes,ncomps],np.float64)
    def __repr__(self):
        return str(self)
    def __str__(self):
        res = ["Mesh:",
               " element_dims = %s" % str(self.element_dims),
               " nodal_dims   = %s" % str(self.nodal_dims),
               " num_elements = %d"   % self.num_elements,
               " num_nodes    = %d"   % self.num_nodes,
               " obase        = %s" % str(self.obase),
               " cycle        = %d" % self.cycle,
               " output_base  = %s" % str(self.output_base()),
               " element_vars = %s" % str(self.element_vars.keys()),
               " nodal_vars   = %s" % str(self.nodal_vars.keys())]
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
                 nodal_vars = ["xd","yd","zd",
                               "xdd","ydd","zdd",
                               "fx","fy","fz",
                                "mass"])
        return m

