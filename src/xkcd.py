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
    xkcd_plot(x,[y1,y2])
 
def xkcd_plot (x,ys,jiggleScale=25.0,xmin=-5,xmax=5,ymin=-5,ymax=5,ylim_min=0,ylim_max=10,xticks=[[4.75,4.75]],plotname="xkcd.png"): 


    # Add the jiggles
    scale = jiggleScale
    for y in ys: 
        y += rand_func() * scale
        y += rand_func() * scale
 
    # Set up a figure
    fig = Figure()
    canvas = fc(fig)
 
# Plot the data
    ax = fig.add_subplot(1, 1, 1)
    colors = ['c','r','g','b','y']
    
    for i  in range(len(ys)): 
        # lay down a white line first to create overlap effect
        ax.plot(x[xmax:xmin], ys[i][ymax:ymin], 'white', lw=7)
        ax.plot(x[xmax:xmin], ys[i][ymax:ymin], colors[i], lw=2)

    ax.set_ylim(ylim_min, ylim_max)
 
    # Poor man's x-axis. There's probably a better way of doing this.
    xaxis = [0.0] * 257
    xaxis += rand_func() * jiggleScale/2.5
    ax.plot(x[3:-3], xaxis[3:-3], 'k', lw=2)
    ax.arrow(8.75, xaxis[-3], 0.1, 0, fc='k', head_width=0.2, head_length=0.15)
 
    # Poor man's x-ticks
    for x in xticks: 
        x = [4.75, 4.75]
        yaxis = [-0.1, 0.1]
        ax.plot(x, yaxis, 'k', lw=1.5)
 
    # XKCD font. This won't work on your machine. Install the font
    # and change the path to the place where you installed it.
    #prop = fm.FontProperties(fname='/Users/damon/Library/Fonts/Humor-Sans.ttf')
    ax.text(4.5, -0.5, 'PEAK', size=11)
 
   # Turn off decoration
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_frame_on(False)
 
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
