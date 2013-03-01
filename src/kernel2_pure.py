"""
 file: mesh.py
 author: Peter Robinson
 created: 2/28/2013
 description:
    LULESH Kernel2 
"""

# This code fragment is from IntegrateStressForElems (and child routines)
#from pylulesh import mesh

def SumElemFaceNormal(pfx,pfy,pfz,
                      i0,i1,i2,i3,
                      x0,  y0,  z0,
                      x1,  y1,  z1,
                      x2,  y2,  z2,
                      x3,  y3,  z3) : 
    
    bisectX0 = 0.5 * (x3 + x2 - x1 - x0);
    bisectY0 = 0.5 * (y3 + y2 - y1 - y0);
    bisectZ0 = 0.5 * (z3 + z2 - z1 - z0);
    bisectX1 = 0.5 * (x2 + x1 - x3 - x0);
    bisectY1 = 0.5 * (y2 + y1 - y3 - y0);
    bisectZ1 = 0.5 * (z2 + z1 - z3 - z0);

    areaX = 0.25 * (bisectY0 * bisectZ1 - bisectZ0 * bisectY1);
    areaY = 0.25 * (bisectZ0 * bisectX1 - bisectX0 * bisectZ1);
    areaZ = 0.25 * (bisectX0 * bisectY1 - bisectY0 * bisectX1);


    pfx[i0] += areaX;
    pfx[i1] += areaX;
    pfx[i2] += areaX;
    pfx[i3] += areaX;
    
    pfy[i0] += areaY;
    pfy[i1] += areaY;
    pfy[i2] += areaY;
    pfy[i3] += areaY;

    pfz[i0] += areaZ;
    pfz[i1] += areaZ;
    pfz[i2] += areaZ;
    pfz[i3] += areaZ;


# B should be 2 dim array, second of dim 8

def SumElemStressesToNodeForces(B, 
                                stress_xx,
                                stress_yy,
                                stress_zz,
                                fx,fy,fz) :
    pfx0 = B[0][0]
    pfx1 = B[0][1]
    pfx2 = B[0][2]
    pfx3 = B[0][3] 

    pfx4 = B[0][4] 
    pfx5 = B[0][5] 
    pfx6 = B[0][6] 
    pfx7 = B[0][7] 
    
    pfy0 = B[1][0] 
    pfy1 = B[1][1] 
    pfy2 = B[1][2] 
    pfy3 = B[1][3] 
    pfy4 = B[1][4] 
    pfy5 = B[1][5] 
    pfy6 = B[1][6]
    pfy7 = B[1][7] 
    
    pfz0 = B[2][0] 
    pfz1 = B[2][1] 
    pfz2 = B[2][2] 
    pfz3 = B[2][3] 
    pfz4 = B[2][4] 
    pfz5 = B[2][5] 
    pfz6 = B[2][6] 
    pfz7 = B[2][7] 
    
    fx[0] = -( stress_xx * pfx0 )
    fx[1] = -( stress_xx * pfx1 )
    fx[2] = -( stress_xx * pfx2 )
    fx[3] = -( stress_xx * pfx3 )
    fx[4] = -( stress_xx * pfx4 )
    fx[5] = -( stress_xx * pfx5 )
    fx[6] = -( stress_xx * pfx6 )
    fx[7] = -( stress_xx * pfx7 )
    

    fy[0] = -( stress_yy * pfy0  )
    fy[1] = -( stress_yy * pfy1  )
    fy[2] = -( stress_yy * pfy2  )
    fy[3] = -( stress_yy * pfy3  )
    fy[4] = -( stress_yy * pfy4  )
    fy[5] = -( stress_yy * pfy5  )
    fy[6] = -( stress_yy * pfy6  )
    fy[7] = -( stress_yy * pfy7  )

    fz[0] = -( stress_zz * pfz0 )
    fz[1] = -( stress_zz * pfz1 )
    fz[2] = -( stress_zz * pfz2 )
    fz[3] = -( stress_zz * pfz3 )
    fz[4] = -( stress_zz * pfz4 )
    fz[5] = -( stress_zz * pfz5 )
    fz[6] = -( stress_zz * pfz6 )
    fz[7] = -( stress_zz * pfz7 )



def  CalcElemNodeNormals( pfx, pfy, pfz, x , y, z): 

    for i in range(8): 
        pfx[i] = 0.0
        pfy[i] = 0.0
        pfz[i] = 0.0
   
    # evaluate face one: nodes 0, 1, 2, 3  
    SumElemFaceNormal(pfx,pfy,pfz,
                      0,1,2,3,
                      x[0], y[0], z[0], x[1], y[1], z[1],
                      x[2], y[2], z[2], x[3], y[3], z[3])


   # evaluate face two: nodes 0, 4, 5, 1 
    SumElemFaceNormal(pfx,pfy,pfz,
                      0,4,5,1,
                      x[0], y[0], z[0], x[4], y[4], z[4],
                      x[5], y[5], z[5], x[1], y[1], z[1])


   # evaluate face three: nodes 1, 5, 6, 2 
    SumElemFaceNormal(pfx,pfy,pfz,
                      1,5,6,2,
                      x[1], y[1], z[1], x[5], y[5], z[5],
                      x[6], y[6], z[6], x[2], y[2], z[2])

   #evaluate face four: nodes 2, 6, 7, 3 
    SumElemFaceNormal(pfx,pfy,pfz,
                      2,6,7,3,
                      x[2], y[2], z[2], x[6], y[6], z[6],
                      x[7], y[7], z[7], x[3], y[3], z[3])

   #evaluate face five: nodes 3, 7, 4, 0 
    SumElemFaceNormal(pfx,pfy,pfz,
                      3,7,4,0,
                      x[3], y[3], z[3], x[7], y[7], z[7],
                      x[4], y[4], z[4], x[0], y[0], z[0])

   # evaluate face six: nodes 4, 7, 6, 5 
    SumElemFaceNormal(pfx,pfy,pfz,
                      4,7,6,5,
                      x[4], y[4], z[4], x[7], y[7], z[7],
                      x[6], y[6], z[6], x[5], y[5], z[5])


def Kernel2(mesh): 
#def kernel2(Index_t numElem, const Index_t * const *elemsToNodesConnectivity,
#            x,  y, z,
#            fx, fy, fz,
#            sigxx, sigyy, sigzz ):
    numElem = mesh.num_elements
    elemsToNodesConnectivity = mesh.conn
    x = mesh.x
    y = mesh.y
    z = mesh.z
    fx = mesh.node_vars['fx']
    fy = mesh.node_vars['fy']
    fz = mesh.node_vars['fz']
    # not sure about this, shouldn't matter for performance
    sigxx =  mesh.element_vars['dxx']
    sigyy =  mesh.element_vars['dyy']
    sigzz =  mesh.element_vars['dzz']

    B = [[0.0]*8]*3
    x_local = [0.0]*8
    y_local = [0.0]*8
    z_local = [0.0]*8
    fx_local = [0.0]*8
    fy_local = [0.0]*8
    fz_local = [0.0]*8

    
    # loop over all elements
    for k in range(numElem): 

        #get nodal coordinates from global arrays and copy into local arrays.
        for lnode in range(8): 
            gnode = int(elemsToNodesConnectivity[k*8 + lnode])
            x_local[lnode] = x[gnode];
            y_local[lnode] = y[gnode];
            z_local[lnode] = z[gnode];

    # NOTE REMOVAL OF SHAPE DERIVATIVE CALL THAT WAS HERE! 

        CalcElemNodeNormals( B[0] , B[1], B[2], x_local, y_local, z_local );





        SumElemStressesToNodeForces( B, sigxx[k], sigyy[k], sigzz[k],

                                         fx_local, fy_local, fz_local ) ;




    # copy nodal force contributions to global force arrray.

        for lnode in range(8):
            gnode = int(elemsToNodesConnectivity[k*8 + lnode])

            fx[gnode] += fx_local[lnode];
            fy[gnode] += fy_local[lnode];
            fz[gnode] += fz_local[lnode];


