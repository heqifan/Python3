#!/bin/bash

export netCDF4_DIR=$PREFIX
export HDF5_DIR=$PREFIX

${PYTHON} -m pip install --no-deps --ignore-installed .
