try:
    import pyopencl as cl
    import numpy as np
except:
    pass

def element_volume(mesh, plat_id):
    #plat_id = 0
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
    queue = cl.CommandQueue(ctx, properties=cl.command_queue_properties.PROFILING_ENABLE)
    mf = cl.mem_flags

    v = mesh.element_vars["v"]
    x_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=mesh.x)
    y_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=mesh.y)
    z_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=mesh.z)
    conn_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=mesh.conn)
    dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, v.nbytes)
    
    prg = cl.Program(ctx, """
    #pragma OPENCL EXTENSION cl_khr_fp64: enable

    double triple_product(double x0, double y0, double z0,
    double x1, double y1, double z1, double x2, double y2, double z2)
    {
    return x0*(y1*z2-z1*y2) + x1*(z0*y2-y0*z2) + x2*(y0*z1-z0*y1);
    }
    
    __kernel void kernel1(__global const double *x,
    __global const double *y, __global const double *z,
    __global const int *conn, __global double *dest)
    {
    int id = get_global_id(0);
    int i = 8 * id;
    
    int c0 = conn[i  ], c1 = conn[i+1], c2 = conn[i+2], c3 = conn[i+3];
    int c4 = conn[i+4], c5 = conn[i+5], c6 = conn[i+6], c7 = conn[i+7];
    
    double x0 = x[c0], y0 = y[c0], z0 = z[c0];
    double x1 = x[c1], y1 = y[c1], z1 = z[c1];
    double x2 = x[c2], y2 = y[c2], z2 = z[c2];
    double x3 = x[c3], y3 = y[c3], z3 = z[c3];
    double x4 = x[c4], y4 = y[c4], z4 = z[c4];
    double x5 = x[c5], y5 = y[c5], z5 = z[c5];
    double x6 = x[c6], y6 = y[c6], z6 = z[c6];
    double x7 = x[c7], y7 = y[c7], z7 = z[c7];
    
    double dx61 = x6 - x1;
    double dy61 = y6 - y1;
    double dz61 = z6 - z1;
    
    double dx70 = x7 - x0;
    double dy70 = y7 - y0;
    double dz70 = z7 - z0;
    
    double dx63 = x6 - x3;
    double dy63 = y6 - y3;
    double dz63 = z6 - z3;
    
    double dx20 = x2 - x0;
    double dy20 = y2 - y0;
    double dz20 = z2 - z0;
    
    double dx50 = x5 - x0;
    double dy50 = y5 - y0;
    double dz50 = z5 - z0;
    
    double dx64 = x6 - x4;
    double dy64 = y6 - y4;
    double dz64 = z6 - z4;
    
    double dx31 = x3 - x1;
    double dy31 = y3 - y1;
    double dz31 = z3 - z1;
    
    double dx72 = x7 - x2;
    double dy72 = y7 - y2;
    double dz72 = z7 - z2;
    
    double dx43 = x4 - x3;
    double dy43 = y4 - y3;
    double dz43 = z4 - z3;
    
    double dx57 = x5 - x7;
    double dy57 = y5 - y7;
    double dz57 = z5 - z7;
    
    double dx14 = x1 - x4;
    double dy14 = y1 - y4;
    double dz14 = z1 - z4;
    
    double dx25 = x2 - x5;
    double dy25 = y2 - y5;
    double dz25 = z2 - z5;
    
    dest[id] =
    (triple_product(
    dx31 + dx72, dx63, dx20,
    dy31 + dy72, dy63, dy20,
    dz31 + dz72, dz63, dz20) +
    triple_product(
    dx43 + dx57, dx64, dx70,
    dy43 + dy57, dy64, dy70,
    dz43 + dz57, dz64, dz70) +
    triple_product(
    dx14 + dx25, dx61, dx50,
    dy14 + dy25, dy61, dy50,
    dz14 + dz25, dz61, dz50)) / 12.0;
    }
    """).build()
    
    e0 = prg.kernel1(queue, v.shape, None, x_buf, y_buf, z_buf, conn_buf, dest_buf)
    e0.wait()
    
    e1 = cl.enqueue_copy(queue, v, dest_buf)
    e1.wait()
    
    return 1e-9 * ((e0.profile.end - e0.profile.start) +
                   (e1.profile.end - e1.profile.start))
