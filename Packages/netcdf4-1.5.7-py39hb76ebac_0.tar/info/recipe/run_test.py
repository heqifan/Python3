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
