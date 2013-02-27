pylulesh
========

Getting Started
---------------

Install all third party libs (python,llvm,hdf5):
<pre>
source bootstrap-env.sh
</pre>

This will leave the newly built python in your path. 

(Running this command in the future will skip the install steps and make sure the proper python is in your path.)

Run tests to double check the env setup:
<pre>
python setup.py test --filter=test_env
</pre>


IPython Notebook Example
---------------
To launch the example notebook in a web browser, run the following:
<pre>
cd notebooks
./launch.sh
</pre>
