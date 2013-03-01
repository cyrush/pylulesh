import numpy as np
from numba import autojit, double, jit, int32

nd1type = double[:]
nd2type = int32[:,:]

@jit(argtypes=(nd1type,nd1type,nd1type,nd2type,
               nd1type,nd1type,nd1type,nd1type))
def element_volume_numba(x,y,z,conn,x_loc,y_loc,z_loc,v):
    for i in range(v.shape[0]):
        for j in range(8):
            x_loc[j] =  x[conn[i,j]]
            y_loc[j] =  y[conn[i,j]]
            z_loc[j] =  z[conn[i,j]]
        v[i]   = ((((x_loc[3] - x_loc[1]) + (x_loc[7] - x_loc[2]))*(((x_loc[6] - x_loc[3]))*(z_loc[2] - z_loc[0]) - (y_loc[2] - y_loc[0])*(z_loc[6] - z_loc[3])) + (y_loc[3] - y_loc[1] + y_loc[7] - y_loc[2])*((x_loc[2] - x_loc[0])*(z_loc[6] - z_loc[3]) - ((x_loc[6] - x_loc[3]))*(z_loc[2] - z_loc[0])) + (z_loc[3] - z_loc[1] + z_loc[7] - z_loc[2])*(((x_loc[6] - x_loc[3]))*(y_loc[2] - y_loc[0]) - (x_loc[2] - x_loc[0])*(y_loc[6] - y_loc[3]))) +
        ((x_loc[4] - x_loc[3] + x_loc[5] - x_loc[7])*((y_loc[6] - y_loc[4])*(z_loc[7] - z_loc[0]) - (y_loc[7] - y_loc[0])*(z_loc[6] - z_loc[4])) + (y_loc[4] - y_loc[3] + y_loc[5] - y_loc[7])*((x_loc[2] - x_loc[0])*(z_loc[6] - z_loc[4]) - (x_loc[6] - x_loc[4])*(z_loc[7] - z_loc[0])) + 
                   (z_loc[4] - z_loc[3] + z_loc[5] - z_loc[7])*((x_loc[6] - x_loc[4])*(y_loc[7] - y_loc[0] ) - (x_loc[7] - x_loc[0])*(y_loc[6] - y_loc[4]))) + 
        ((x_loc[1] - x_loc[4] + x_loc[2] - x_loc[5])*((y_loc[6] - y_loc[1])*(z_loc[5] - z_loc[0]) - (y_loc[5] - y_loc[0])*(z_loc[6] - z_loc[1])) + 
                   (y_loc[1] - y_loc[4] + y_loc[2] - y_loc[5])*((x_loc[5] - x_loc[0])*(z_loc[6] - z_loc[1]) - (x_loc[6] - x_loc[1])*(z_loc[5] - z_loc[0])) +
                   (z_loc[1] - z_loc[4] + z_loc[2] - z_loc[5])*((x_loc[6] - x_loc[1])*(y_loc[5] - y_loc[0]) - (x_loc[5] - x_loc[0])*(y_loc[6] - y_loc[1])))) / 12.0


def element_volume(mesh):
    x_ele = np.zeros(shape=(8,),dtype=np.float64)
    y_ele = np.zeros(shape=(8,),dtype=np.float64)
    z_ele = np.zeros(shape=(8,),dtype=np.float64)
    element_volume_numba(mesh.x,mesh.y,mesh.z,mesh.conn,
                         x_ele,y_ele,z_ele,mesh.element_vars["v"])

