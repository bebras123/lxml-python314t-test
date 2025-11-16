#!/usr/bin/env bash
cd lxml

/root/envs/py312/bin/python setup.py build --with-cython
/root/envs/py313/bin/python setup.py build --with-cython
/root/envs/py314/bin/python setup.py build --with-cython
/root/envs/py314t/bin/python setup.py build --with-cython

