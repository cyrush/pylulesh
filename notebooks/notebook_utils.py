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

def visit_bin_path():
    for path in os.environ["PATH"].split(":"):
        v_bin =pjoin(path,"visit").strip()
        if os.path.isfile(v_bin):
            return v_bin

def visit_module_path(ver):
    v_bin = visit_bin_path()
    if v_bin is None:
        return None
    ver_root = os.path.abspath(pjoin(os.path.split(v_bin)[0],"..",ver))
    arch =  None
    for test_arch  in ["linux-x86_64","darwin-x86_64"]:
        if os.path.isdir(pjoin(ver_root,test_arch)):
            arch = test_arch
    if arch is None:
        return None
    arch_root = pjoin(ver_root,arch)
    py_root   = pjoin(arch_root,"lib","site-packages")
    return py_root

def load_visit_module(ver):
    mod_path = visit_module_path(ver)
    if mod_path is None:
        print "[Error: Could not find VisIt %s - make `visit' is in your path.]" % ver
        return
    sys.path.insert(0,mod_path)
    import visit
    visit.AddArgument("-nowin")
    visit.AddArgument("-v %s" % ver)
    # squash non-sense in VisIt 2.5.2
    capture = cStringIO.StringIO()
    orig_stdout = sys.stdout
    sys.stdout = capture
    visit.Launch()
    sys.stdout = orig_stdout


