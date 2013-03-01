import numpy as np
from numba import autojit, double, jit, int32

@autojit
def triple_product(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    return (x1)*((y2)*(z3) - (z2)*(y3)) + (x2)*((z1)*(y3) - (y1)*(z3)) + (x3)*((y1)*(z2) - (z1)*(y2))

@autojit
def calc_elem_volume(x,y,z):  
        twelveth = (1.0)/(12.0);
        dx61 = x[6] - x[1];
        dy61 = y[6] - y[1];
        dz61 = z[6] - z[1];

        dx70 = x[7] - x[0];
        dy70 = y[7] - y[0];
        dz70 = z[7] - z[0];

        dx63 = x[6] - x[3];
        dy63 = y[6] - y[3];
        dz63 = z[6] - z[3];

        dx20 = x[2] - x[0];
        dy20 = y[2] - y[0];
        dz20 = z[2] - z[0];

        dx50 = x[5] - x[0];
        dy50 = y[5] - y[0];
        dz50 = z[5] - z[0];

        dx64 = x[6] - x[4];
        dy64 = y[6] - y[4];
        dz64 = z[6] - z[4];

        dx31 = x[3] - x[1];
        dy31 = y[3] - y[1];
        dz31 = z[3] - z[1];

        dx72 = x[7] - x[2];
        dy72 = y[7] - y[2];
        dz72 = z[7] - z[2];

        dx43 = x[4] - x[3];
        dy43 = y[4] - y[3];
        dz43 = z[4] - z[3];

        dx57 = x[5] - x[7];
        dy57 = y[5] - y[7];
        dz57 = z[5] - z[7];

        dx14 = x[1] - x[4];
        dy14 = y[1] - y[4];
        dz14 = z[1] - z[4];

        dx25 = x[2] - x[5];
        dy25 = y[2] - y[5];
        dz25 = z[2] - z[5];

        vol_a = triple_product(dx31 + dx72, dx63, dx20,
                               dy31 + dy72, dy63, dy20,
                               dz31 + dz72, dz63, dz20)
        vol_b = triple_product(dx43 + dx57, dx64, dx70,
                               dy43 + dy57, dy64, dy70,
                               dz43 + dz57, dz64, dz70) 
        vol_c = triple_product(dx14 + dx25, dx61, dx50,
                               dy14 + dy25, dy61, dy50,
                               dz14 + dz25, dz61, dz50);
        volume = (vol_a + vol_b + vol_c) * twelveth;
        return volume

@autojit
def element_volume_jit(x,y,z,conn,x_loc,y_loc,z_loc,v):
    for i in range(v.shape[0]):
        for j in range(8):
            x_loc[j] =  x[conn[i,j]]
            y_loc[j] =  y[conn[i,j]]
            z_loc[j] =  z[conn[i,j]]
        v[i] = calc_elem_volume(x_loc,y_loc,z_loc)

def element_volume_py(x,y,z,conn,x_loc,y_loc,z_loc,v):
    for i in range(len(v)):
        for j in range(8):
            x_loc[j] =  x[conn[i*8 + j]]
            y_loc[j] =  y[conn[i*8 + j]]
            z_loc[j] =  z[conn[i*8 + j]]
        v[i] = calc_elem_volume(x_loc,y_loc,z_loc)

def element_volume_driver_numpy(mesh):
    x_ele = np.zeros(shape=(8,),dtype=np.float64)
    y_ele = np.zeros(shape=(8,),dtype=np.float64)
    z_ele = np.zeros(shape=(8,),dtype=np.float64)
    element_volume(mesh.x,mesh.y,mesh.z,mesh.conn,
                         x_ele,y_ele,z_ele,mesh.element_vars["v"])

def element_volume_driver_py(mesh):
    x_ele = [0]*8
    y_ele = [0]*8
    z_ele = [0]*8
    element_volume(mesh.x,mesh.y,mesh.z,mesh.conn,
                         x_ele,y_ele,z_ele,mesh.element_vars["v"])

element_volume     = element_volume_jit

triple_product_jit = triple_product
triple_product_py  = triple_product.py_func

calc_elem_volume_jit = calc_elem_volume
calc_elem_volume_py = calc_elem_volume.py_func

def setupNumba():
    globals()['triple_product'] = triple_product_jit
    globals()['calc_elem_volume'] = calc_elem_volume_jit
    globals()['element_volume'] = element_volume_jit

def setupPy():
    globals()['triple_product'] = triple_product_py
    globals()['calc_elem_volume'] = calc_elem_volume_py
    globals()['element_volume'] = element_volume_py

#setupPy()
