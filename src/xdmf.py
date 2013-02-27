"""
 file: xdmf.py
 author: Cyrus Harrison <cyrush@llnl.gov>
 created: 2/26/2013
 description:
    Xdmf output for pylulesh.Mesh

"""

import h5py
import numpy as np


def ident(n):
    return "".join(["    " for i in range(n)])

def xdmf_data_item(ofile,mesh,data,name,inline):
    if inline:
        xdmf_inline_data_item(ofile,data,name)
    else:
        xdmf_hdf5_data_item(ofile,mesh,data,name)
    
def xdmf_inline_data_item(ofile,data,name):
    pass

def xdmf_hdf5_data_item(ofile,mesh,data,name):
    ditem = '<DataItem '
    if data.shape[1] == 1:
        ditem += ' Dimensions="%d %d" ' % data.shape
    else:
        ditem += 'Dimensions="%d" ' % data.shape[0]
    if data.dtype == np.float64:
        ditem += ' NumberType="Float" Precision="8" '
    elif data.dtype == np.float32:
        ditem += ' NumberType="Float" Precision="4" '
    else:
        ditem += ' NumberType="Int" '
    ditem += 'Format="HDF">'
    ofile.write(ditem)
    ofile.write(" %s.h5/%s " % (mesh.output_base(), name))
    ofile.write('</DataItem>\n')

def xdmf_mixed_topo(ofile,mesh,inline):
    ofile.write(ident(2) + '<Geometry Type="XYZ">\n')
    ofile.write(ident(3))
    xdmf_data_item(ofile,mesh,mesh.xyz,"xyz",inline)
    ofile.write(ident(2) + '</Geometry>\n')
    ofile.write(ident(2) + '<Topology Type="Mixed" NumberOfElements="%d" >\n' % mesh.num_elements)
    ofile.write(ident(3))
    xdmf_data_item(ofile,mesh,mesh.conn, "conn",inline)
    ofile.write(ident(2) + '</Topology>\n')

def write_xdmf_root(mesh,inline):
    ofile = open(mesh.output_base() + ".xmf","w")
    hdr = ['<?xml version="1.0" ?>',
           '<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd">',
           '<Xdmf>',
           ident(1) + '<Domain>',
           ident(2) + '<Grid Name="Mixed">',
           ident(2) + '<Information Name="Description">',
           ident(3) + 'Xdmf unstructured grid.',
           ident(2) + '</Information>\n']
    ofile.write("\n".join(hdr))
    xdmf_mixed_topo(ofile,mesh,inline)
    for k,v in mesh.element_vars.items():
        ofile.write(ident(2) + '<Attribute Name="%s" AttributeType="Scalar" Center="Cell">\n' % k)
        ofile.write(ident(3))
        xdmf_data_item(ofile,mesh,v,k,inline)
        ofile.write(ident(2) + '</Attribute>\n')
    for k,v in mesh.nodal_vars.items():
        ofile.write(ident(2) + '<Attribute Name="%s" AttributeType="Scalar" Center="Node">\n' % k)
        ofile.write(ident(3))
        xdmf_data_item(ofile,mesh,v,k,inline)
        ofile.write(ident(2) + '</Attribute>\n')
    ftr = [ ident(2) + '</Grid>',
            ident(1) + '</Domain>',
            '</Xdmf>\n']
    ofile.write("\n".join(ftr))
    ofile.close()

def write_xdmf_h5(mesh):
    h5_out = h5py.File(mesh.output_base() + '.h5', 'w')
    h5_out["xyz"]   = mesh.xyz
    h5_out["conn"]  = mesh.conn
    for k,v in mesh.element_vars.items():
        h5_out[k] = v
    for k,v in mesh.nodal_vars.items():
        h5_out[k] = v
    h5_out.close()


def write_xdmf(mesh,inline):
    write_xdmf_root(mesh,inline)
    if not inline:
        write_xdmf_h5(mesh)



