"""
 file: notebook_utils.py
 author: Cyrus Harrison <cyrush@llnl.gov>
 created: 2/28/2013
 description:
    rebuild and reload the pylulesh module within an ipython notebook.

"""

import sys
import os
import subprocess
import cStringIO

import pylulesh

from os.path import join as pjoin

from IPython.lib.deepreload import reload as dreload

from IPython.core.display import Image 

def render(m,v,fname="test.png"):
    m.save()
    db = m.output_base() + ".xmf"
    os.system("visit -nowin -cli -s vrender.py %s %s %s" % (db,v,fname))
    return Image(filename=fname)

def rebuild():
    cwd = os.getcwd()
    setup_path = os.path.abspath(pjoin(os.path.split(__file__)[0],".."))
    os.chdir(setup_path)
    subprocess.call(sys.executable  + " setup.py build",shell=True)
    subprocess.call(sys.executable  + " setup.py install",shell=True)
    os.chdir(cwd)
    # mute std out for the dreload call
    capture = cStringIO.StringIO()
    orig_stdout = sys.stdout
    sys.stdout = capture
    dreload(pylulesh)
    sys.stdout = orig_stdout
