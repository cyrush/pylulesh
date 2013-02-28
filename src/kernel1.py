import numpy as np
from numba import autojit, double, jit, int32

def triple_product(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    return (x1)*((y2)*(z3) - (z2)*(y3)) + (x2)*((z1)*(y3) - (y1)*(z3)) + (x3)*((y1)*(z2) - (z1)*(y2))

def calc_elem_volume(x0,x1,x2,x3,x4,x5,x6,x7,
                     y0,y1,y2,y3,y4,y5,y6,y7,    
                     z0,z1,z2,z3,z4,z5,z6,z7):  
    twelveth = (1.0)/(12.0);
    dx61 = x6 - x1;
    dy61 = y6 - y1;
    dz61 = z6 - z1;

    dx70 = x7 - x0;
    dy70 = y7 - y0;
    dz70 = z7 - z0;

    dx63 = x6 - x3;
    dy63 = y6 - y3;
    dz63 = z6 - z3;

    dx20 = x2 - x0;
    dy20 = y2 - y0;
    dz20 = z2 - z0;

    dx50 = x5 - x0;
    dy50 = y5 - y0;
    dz50 = z5 - z0;

    dx64 = x6 - x4;
    dy64 = y6 - y4;
    dz64 = z6 - z4;

    dx31 = x3 - x1;
    dy31 = y3 - y1;
    dz31 = z3 - z1;

    dx72 = x7 - x2;
    dy72 = y7 - y2;
    dz72 = z7 - z2;

    dx43 = x4 - x3;
    dy43 = y4 - y3;
    dz43 = z4 - z3;

    dx57 = x5 - x7;
    dy57 = y5 - y7;
    dz57 = z5 - z7;

    dx14 = x1 - x4;
    dy14 = y1 - y4;
    dz14 = z1 - z4;

    dx25 = x2 - x5;
    dy25 = y2 - y5;
    dz25 = z2 - z5;

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
def calc_elem_volume_numpy(x,y,z):  
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


def element_volume(mesh):
    v = mesh.element_vars["v"]
    vals = [0.0] * 24
    for i in xrange(mesh.num_elements):
        idx  = 0
        for j in xrange(8):
            vals[idx] = mesh.x[mesh.conn[i,j]]
            idx +=1
        for j in xrange(8):
            vals[idx] = mesh.y[mesh.conn[i,j]]
            idx +=1
        for j in xrange(8):
            vals[idx] = mesh.z[mesh.conn[i,j]]
            idx +=1
        v[i] = calc_elem_volume(*vals)

@autojit
def element_volume_numba(x,y,z,conn,x_loc,y_loc,z_loc,v):
    for i in range(v.shape[0]):
        for j in range(8):
            x_loc[j] =  x[conn[i,j]]
            y_loc[j] =  y[conn[i,j]]
            z_loc[j] =  z[conn[i,j]]
    v[i] = calc_elem_volume_numpy(x_loc,y_loc,z_loc)

def element_volume_driver(mesh):
    x_ele = np.zeros(shape=(8,),dtype=np.float64)
    y_ele = np.zeros(shape=(8,),dtype=np.float64)
    z_ele = np.zeros(shape=(8,),dtype=np.float64)
    element_volume_numba(mesh.x,mesh.y,mesh.z,mesh.conn,
                         x_ele,y_ele,z_ele,mesh.element_vars["v"])


# element_volume_driver_dumba = jit(double[:,:],double[:,:],double[:,:],
#                                   int32[:,:],
#                                   double[:,:],double[:,:],double[:,:],double[:,:])(element_volume_driver)
# 
# calc_elem_volume_numpy_numba = jit(double[:,:],double[:,:],double[:,:],double)

def element_volume(mesh):
    v = mesh.element_vars["v"]
    x_ele = np.zeros(shape=(8,),dtype=np.float64)
    y_ele = np.zeros(shape=(8,),dtype=np.float64)
    z_ele = np.zeros(shape=(8,),dtype=np.float64)
    for i in xrange(mesh.num_elements):
        for j in xrange(8):
            x_ele[j] =  mesh.x[mesh.conn[i,j]]
            y_ele[j] =  mesh.y[mesh.conn[i,j]]
            z_ele[j] =  mesh.z[mesh.conn[i,j]]
    v[i] = calc_elem_volume_numpy(x_ele,y_ele,z_ele)

