import numpy as np
from matplotlib import rcParams
rcParams['text.usetex'] = False
from matplotlib.backends.backend_agg import FigureCanvasAgg as fc
from matplotlib.figure import Figure
import matplotlib.font_manager as fm
 
# Function to draw a random function. Yo dawg...
def rand_func():
    # Some random Fourier coefficients
    coeffs = 0.0 + 1j * np.random.random(129)
 
    for i in range(len(coeffs)):
        if i == 0:
            coeffs[i] = 0.0
        elif i == (len(coeffs) / 2) + 1:
            coeffs[i] = 0.0
        else:
            # Make those bad boys decay. Fo' regularity, yo.
            coeffs[i] /= float(i) ** 1
 
    f = np.fft.irfft(coeffs, 256)
    return np.append(f, f[0])
 

def xkcd_plot_sample():
    # Make some data
    x = np.linspace(1.0, 9.0, num=257, endpoint=True)
    y1 = 1.5 + 10.0 * (np.sin(x) * np.sin(x) / np.sqrt(x)) * np.exp(-0.5 * (x - 5.0) * (x - 5.0))
    y2 = 3.0 + 10.0 * (np.sin(x) * np.sin(x) / np.sqrt(x)) * np.exp(-0.5 * (x - 7.0) * (x - 7.0))
    xkcd_plot(x,[y1,y2],xmin=5,xmax=-5,ymin=5,ymax=-5)
 
def xkcd_plot (x,ys,jiggleScale=5,xmin=0,xmax=-1,ymin=0,ymax=-1,ylim_min=1e-5,ylim_max=10,xticks=[[4.75,4.75]],plotname="xkcd.png",useLabels=False): 
    xticks = []
    for xt in x: 
#        print 'tick locations' ,xt
        xticks.append([xt,xt])
    nx = np.linspace(x[0], x[-1], num=257, endpoint=True)
    #xmin = 0# x[0] - x[0] * .1
    #xmax = x[-1] + x[-1] * .1
    maxofys = np.max(ys)
    ylim_max = maxofys*1.1
    # Add the jiggles
    scale = jiggleScale
    yn = []
    newscale = 0; 

    for y in ys: 
        newscale = np.max([newscale,scale*np.max(y)])

    scale = newscale

    for y in ys: 
        yy = np.interp(nx,x,y)
        yy += rand_func() * scale 
        yn.append(yy)

    ys = yn
    x  = nx
    # Set up a figure
    fig = Figure()
    canvas = fc(fig)
 
# Plot the data
    ax = fig.add_subplot(1, 1, 1)
    colors = ['c','r','g','b','y']
    verticaloffset = .003
    for i  in range(len(ys)): 
        # lay down a white line first to create overlap effect
#        ax.plot(x[xmin:xmax], ys[i][ymin:ymax], 'white', lw=7)
        ax.plot(x[xmin:xmax], ys[i][ymin:ymax]+verticaloffset, colors[i%len(colors)], lw=2)


    
    ax.set_xlim(x[0]*.9,x[-1]*1.2)
    # Poor man's x-axis. There's probably a better way of doing this.
#    xaxis = nx
    xaxis = [ylim_min] * 257
    xaxis += rand_func() * scale/2.5-(ylim_max-ylim_min)*.02
#    print "axis endpoints", x[0], x[-1], xaxis[0], xaxis[-1]
    xxaxis = ((x[0:-1]-x[0]-2)*1.1+(x[0]+1.5)*1.1)




    ax.set_ylim(np.min(xaxis)*4, ylim_max*1.1)
 
    # Poor man's x-ticks
#    for x in xticks: 
#        yaxis = [-0.001, 0.001]
#        ax.plot(x, yaxis, 'k', lw=1.5)

#    ax.set_yscale('log')
#    ax.set_xscale('log')
    # XKCD font. This won't work on your machine. Install the font
    # and change the path to the place where you installed it.
    #prop = fm.FontProperties(fname='/Users/damon/Library/Fonts/Humor-Sans.ttf')
#    ax.text(4.5, -0.5, 'PEAK', size=11)
    
   # Turn off decoration
    if not useLabels:
        ax.plot(xxaxis, xaxis[0:-1], 'k', lw=2)
        ax.arrow(xxaxis[-1], xaxis[-2], 0.1, 0, fc='k', width=(ylim_max-ylim_min)*.001,head_width= (ylim_max-ylim_min)*.03, head_length=.2)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_frame_on(False)

    return fig
 
# Turn off all clipping
    def noclip(ax): 
        "Turn off all clipping in axes ax; call immediately before drawing" 
        ax.set_clip_on(False) 
        artists = [] 
        artists.extend(ax.collections) 
        artists.extend(ax.patches) 
        artists.extend(ax.lines) 
        artists.extend(ax.texts) 
        artists.extend(ax.artists) 
        for a in artists: 
            a.set_clip_on(False) 
    noclip(ax)
 
# Save
    fig.savefig(plotname)

xkcd_plot_sample()
