#forcing
import xarray

f1 = '/mnt/data/wrf/WPS-4.2/geo_em.d01.nc'
ds1 = xr.open_dataset(f1)
lat = ds1.XLAT_M[0,:,1].data
lon = ds1.XLONG_M[0,1,:].data

f2 = '/hrldas-release-3.8/HRLDAS/HRLDAS_forcing/run/examples/GLDAS/raw/GLDAS_NOAH025_3H.2.1ːGLDAS_NOAH025_3H.A20230101.0000.021.nc4'
ds2 = xr.open_dataset(f2)
ds2 = ds2.interp(lat = lat,lon = lon,method='nearest')
S = ds2.Swnet_tavg.data[0,...]
L = ds2.Lwnet_tavg.data[0,...]
R = ds2.Rainf_tavg.data[0,...]
T = ds2.Tair_f_inst.data[0,...]
Q = ds2.Qair_f_inst.data[0,...]
P = ds2.Psurf_f_inst.data[0,...]
U = ds2.Wind_f_inst.data[0,...]
V = ds2.Wind_f_inst.data[0,...]


p1 = xr.Dataset(data_vars={
'T2D': (['Time', 'south_north', 'west_east'], T[np.newaxis,...]),
'Q2D': (['Time', 'south_north', 'west_east'], Q[np.newaxis,...]),
'U2D': (['Time', 'south_north', 'west_east'], U[np.newaxis,...]),
'V2D': (['Time', 'south_north', 'west_east'], V[np.newaxis,...]),
'PSFC': (['Time', 'south_north', 'west_east'], P[np.newaxis,...]),
'RAINRATE': (['Time', 'south_north', 'west_east'], R[np.newaxis,...]),
'SWDOWN': (['Time', 'south_north', 'west_east'], S[np.newaxis,...]),
'LWDOWN': (['Time', 'south_north', 'west_east'], L[np.newaxis,...]),
}, 
attrs=dict(WEST_EAST_GRID_DIMENSION=121.,SOUTH_NORTH_GRID_DIMENSION=131.)
)

p1.T2D.attrs['units'] = 'K'
p1.Q2D.attrs['units'] = 'kg/kg'
p1.U2D.attrs['units'] = 'm/s'
p1.V2D.attrs['units'] = 'm/s'
p1.PSFC.attrs['units'] = 'Pa'
p1.LWDOWN.attrs['units'] = 'W/m^2'
p1.SWDOWN.attrs['units'] = 'W/m^2'
p1.RAINRATE.attrs['units'] = 'kg/m^2/s'

p1.T2D.attrs['_FillValue'] = -1.e+36
p1.Q2D.attrs['_FillValue'] = -1.e+36
p1.U2D.attrs['_FillValue'] = -1.e+36
p1.V2D.attrs['_FillValue'] = -1.e+36
p1.PSFC.attrs['_FillValue'] = -1.e+36
p1.LWDOWN.attrs['_FillValue'] = -1.e+36
p1.SWDOWN.attrs['_FillValue'] = -1.e+36
p1.RAINRATE.attrs['_FillValue'] = -1.e+36

p1 = p1.assign_attrs(TITLE="OUTPUT FROM CONSOLIDATE_GRIB v20150518",missing_value=-1.e+36,_FillValue=-1.e+36,\
                     DX=30000.0,DY=30000.0,\
                        TRUELAT1=40.0,TRUELAT2=-999.9,LA1=14.5265045,LO1=94.04115,STAND_LON=-999.9,\
                          MAP_PROJ=3.,MMINLU='MODIFIED_IGBP_MODIS_NOAH')

p1.to_netcdf('/hrldas-release-3.8/HRLDAS/HRLDAS_forcing/run/examples/GLDAS/2023010110.LDASIN_DOMAIN1')
