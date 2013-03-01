import sys, os

import timeit
import json

python_setup = """
import os
def run_python(dim):
    os.system("env PYTHONPATH=$PWD/src python ./pypy-tests/target_test_kernel2.py %s" %dim)
"""

pypy_setup = """
import os
def run_pypy(dim):
    os.system("./pypy-tests/target_test_kernel2-c %s" %dim)
"""

results = {}
testname = 'python_kernel2'
res = {}
for dim in sys.argv[1:]:
    t = timeit.Timer("run_python(%s)"%dim, python_setup)
    res[int(dim)] = t.timeit(5)/5.0
results[testname] = res

testname = 'pypy_kernel2'
res = {}
for dim in sys.argv[1:]:
    t = timeit.Timer("run_pypy(%s)"%dim, pypy_setup)
    res[int(dim)] = t.timeit(5)/5.0
results[testname] = res

print results
json.dump(results, open("pypy_kernel2_timing_results.json", "w"))
