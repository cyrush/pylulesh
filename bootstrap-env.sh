#!/bin/bash
#
# bootstrap-env.sh
#
# Takes you from zero to a Python env for pylulesh dev.
#
#

export PY_VERSION="2.7.3"

function info
{
    echo "$@"
}

function warn
{
    info "WARNING: $@"
}

function error
{
    info "ERROR: $@"
    if [ x"${BASH_SOURCE[0]}" == x"$0" ] ; then
        exit 1
    else
        kill -SIGINT $$
    fi
}

function check
{
    if [[ $1 != 0 ]] ; then
        error " !Last step failed!"
    fi
}

function download
{
    if [[ -e $2 ]] ; then
        info "Found: $2 <Skipping download>"
        return 0
    fi
    info "NOT Found: $2 <Downloading from $1>"
    WGET_TEST=$(which wget)
    if [[ $WGET_TEST == "" ]] ; then
        curl -ksfLO $1/$2
    else
        wget $1/$2
    fi
}

function set_install_path
{
    export START_DIR=`pwd`
    export BUILD_DIR=$1/_build
    export LOGS_DIR=$BUILD_DIR/logs
    export PY_ROOT=$1/python
    export PY_PREFIX=$PY_ROOT/$PY_VERSION
    export PY_EXE=$PY_PREFIX/bin/python
    export PIP_EXE=$PY_PREFIX/bin/pip
    export LLVM_PREFIX=$1/llvm
    export HDF5_PREFIX=$1/hdf5
}

function check_python_install
{
    if [[ -e $1/python/$PY_VERSION/bin/python ]] ; then
        return 0
    else
        return 1
    fi
}

function check_llvm_install
{
    if [[ -e $1/llvm/lib/libLLVMCore.a ]] ; then
        return 0
    else
        return 1
    fi
}

function check_hdf5_install
{
    if [[ -e $1/hdf5/lib ]] ; then
        return 0
    else
        return 1
    fi
}

function check_pyopencl_install
{
    $PY_EXE <<END
import sys
try:
    import pyopencl
except:
    sys.exit(-1)
sys.exit(0)
END
    return $?
}


function bootstrap_python
{
    mkdir $BUILD_DIR
    mkdir $PY_ROOT
    mkdir $PY_PREFIX
    mkdir $LOGS_DIR

    info "================================="
    info "Bootstraping Python $PY_VERSION"
    info "================================="
    info "[Target Prefix: $PY_PREFIX]"
    cd $BUILD_DIR
    download http://www.python.org/ftp/python/$PY_VERSION Python-$PY_VERSION.tgz
    rm -rf Python-$PY_VERSION
    info "[Inflating: Python-$PY_VERSION.tgz]"
    tar -xzf Python-$PY_VERSION.tgz
    cd Python-$PY_VERSION
    info "[Configuring Python]"
    ./configure --prefix=$PY_PREFIX &> ../logs/python_configure.txt
    check $?
    info "[Building Python]"
    make -j 4 &> ../logs/python_build.txt
    check $?
    info "[Installing Python]"
    make install &> ../logs/python_install.txt
    check $?

    cd $START_DIR
}

function bootstrap_modules
{
    # bootstrap pip
    info "================================="
    info "Bootstraping base modules"
    info "================================="
    cd $BUILD_DIR
    download http://pypi.python.org/packages/source/d/distribute distribute-0.6.30.tar.gz
    rm -rf distribute-0.6.30
    info "[Inflating: distribute-0.6.30.tar.gz]"
    tar -xzf distribute-0.6.30.tar.gz
    cd distribute-0.6.30
    info "[Building distribute]"
    $PY_EXE setup.py build  &> ../logs/distribute_build.txt
    check $?
    info "[Installing distribute]"
    $PY_EXE setup.py install &> ../logs/distribute_install.txt
    check $?

    cd $BUILD_DIR
    download http://pypi.python.org/packages/source/p/pip pip-1.2.1.tar.gz
    rm -rf pip-1.2.1
    info "[Inflating: pip-1.2.1.tar.gz]"
    tar -xzf pip-1.2.1.tar.gz
    cd pip-1.2.1
    info "[Building pip]"
    $PY_EXE setup.py build &> ../logs/pip_build.txt
    check $?
    info "[Installing pip]"
    $PY_EXE setup.py install &> ../logs/pip_install.txt
    check $?

    cd $START_DIR
}


function build_llvm
{
    info "================================="
    info "Setting up LLVM 3.2"
    info "================================="
    info "[Target Prefix: $LLVM_PREFIX]"
    cd $BUILD_DIR
    download http://llvm.org/releases/3.2/ llvm-3.2.src.tar.gz
    rm -rf llvm-3.2.src
    info "[Inflating: llvm-3.2.src.tar.gz]"
    tar -xzf llvm-3.2.src.tar.gz
    cd llvm-3.2.src
    info "[Configuring LLVM]"
    export REQUIRES_RTTI=1
    ./configure --enable-optimized --enable-pic --prefix=$LLVM_PREFIX &> ../logs/llvm_configure.txt
    check $?
    info "[Building LLVM]]"
    make -j 4 &> ../logs/llvm_build.txt
    check $?
    info "[Installing LLVM]]"
    make install &> ../logs/llvm_install.txt
    check $?
    cd $START_DIR
}

function build_hdf5
{
    info "================================="
    info "Setting up HDF5 1.8.7"
    info "================================="
    info "[Target Prefix: $HDF5_PREFIX]"
    cd $BUILD_DIR
    download http://www.hdfgroup.org/ftp/HDF5/prev-releases/hdf5-1.8.7/src/ hdf5-1.8.7.tar.gz
    rm -rf hdf5-1.8.7
    info "[Inflating: hdf5-1.8.7.tar.gz]"
    tar -xzf hdf5-1.8.7.tar.gz
    cd hdf5-1.8.7
    info "[Configuring HDF5]"
    ./configure --prefix=$HDF5_PREFIX &> ../logs/hdf5_configure.txt
    #--disable-shared \
    #--enable-static \
    check $?
    info "[Building HDF5]]"
    make -j 4 &> ../logs/hdf5_build.txt
    check $?
    info "[Installing HDF5]]"
    make install &> ../logs/hdf5_install.txt
    check $?
    cd $START_DIR
}


function build_pyopencl
{
    info "================================="
    info "Setting up pyopencl"
    info "================================="
    cd $BUILD_DIR
    rm -rf pyopencl
    git clone https://github.com/inducer/pyopencl
    cd pyopencl
    git submodule init
    git submodule update

    if [[ -e /opt/cudatoolkit-5.0/ ]] ; then
        module load cudatoolkit/5.0
    fi

    if [ -z "$CUDA_INCLUDES" ] ; then
        ./configure.py
    else
        ./configure.py --cl-inc-dir=$CUDA_INCLUDES
    fi
    make
    make install
    cd $START_DIR
}

function build_python_modules
{
    $PIP_EXE install readline
    # numpy and cython
    $PIP_EXE install numpy
    $PIP_EXE install cython
    # matplot lib & ipython
    $PIP_EXE install matplotlib
    $PIP_EXE install ipython
    # llvm & numba
    export LLVM_CONFIG_PATH=$LLVM_PREFIX/bin/llvm-config
    $PIP_EXE install git+https://github.com/llvmpy/llvmpy.git#egg=llvmpy
    $PIP_EXE install git+https://github.com/numba/Meta.git#egg=Meta
    $PIP_EXE install git+https://github.com/numba/numba.git#egg=numba
    $PIP_EXE install nose
    # h5py
    export HDF5_DIR=$HDF5_PREFIX
    $PIP_EXE install h5py
    # pyopencl
    $PIP_EXE install py
    $PIP_EXE install pytest
    $PIP_EXE install pytools
    $PIP_EXE install decorator
    $PIP_EXE install mako
    check_pyopencl_install
    if [[ $? == 0 ]] ; then
        info "[Found: pyopencl <Skipping build>]"
    else
        build_pyopencl
    fi
}


function main
{
    # Possible Feature: Check for DEST passed as $1, use `pwd` as fallback
    DEST=`pwd`/libs/
    mkdir -p $DEST
    set_install_path $DEST
    check_python_install $DEST
    if [[ $? == 0 ]] ; then
        info "[Found: Python $PY_VERSION @ $DEST/$PY_VERSION/bin/python <Skipping build>]"
    else
        bootstrap_python
        bootstrap_modules
    fi
    # Only add to PATH if `which python` isn't our Python
    PY_CURRENT=`which python`
    if [[ "$PY_CURRENT" != "$PY_PREFIX/bin/python" ]] ; then
        export PATH=$PY_PREFIX/bin:$PATH
    fi


    check_llvm_install $DEST
    if [[ $? == 0 ]] ; then
        info "[Found: LLVM @ $LLVM_PREFIX <Skipping build>]"
    else
        build_llvm
    fi

    check_hdf5_install $DEST
    if [[ $? == 0 ]] ; then
        info "[Found: HDF5 @ $HDF5_PREFIX <Skipping build>]"
    else
        build_hdf5
    fi

    build_python_modules

    info "[Active Python:" `which python` "]"
}

main