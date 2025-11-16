#!/usr/bin/env bash

/root/envs/py312/bin/python run.py --repeat=5
/root/envs/py312/bin/python run.py --use-preinstalled-lxml --repeat=5
/root/envs/py313/bin/python run.py --repeat=5
/root/envs/py313/bin/python run.py --use-preinstalled-lxml --repeat=5
/root/envs/py314/bin/python run.py --repeat=5
/root/envs/py314/bin/python run.py --use-preinstalled-lxml --repeat=5
/root/envs/py314t/bin/python run.py --repeat=5

