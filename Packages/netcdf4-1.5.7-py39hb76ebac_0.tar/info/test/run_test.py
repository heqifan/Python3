#  tests for netcdf4-1.5.7-py39hb76ebac_0 (this is a generated file);
print('===== testing package: netcdf4-1.5.7-py39hb76ebac_0 =====');
print('running run_test.py');
#  --- run_test.py (begin) ---
import netCDF4

# libnetcdf needs to be able to write a cookie file to $TEMP so set it to $PREFIX
import os
os.environ['TEMP'] = os.environ['PREFIX']

# OPeNDAP.
url = 'http://geoport-dev.whoi.edu/thredds/dodsC/estofs/atlantic'
with netCDF4.Dataset(url) as nc:
    # Compiled with cython.
    assert nc.filepath() == url


url = 'http://geoport.whoi.edu/thredds/dodsC/usgs/vault0/models/tides/vdatum_gulf_of_maine/adcirc54_38_orig.nc'

with netCDF4.Dataset(url) as nc:
    nc['tidenames'][:]
#  --- run_test.py (end) ---

print('===== netcdf4-1.5.7-py39hb76ebac_0 OK =====');
print("import: 'netCDF4'")
import netCDF4

print("import: 'cftime'")
import cftime

