#initial
geo_em_flnm        = "geo_em.d01.nc"
wrfinput_flnm      = "wrfinput_d01"
ds1 = xr.open_dataset(wrfinput_flnm)


lat = ds1.XLAT[0,:,1].data
lon = ds1.XLONG[0,1,:].data

f2 = '/Run/data_download/GLDAS_NOAH025_3H.A20220101.0000.021.nc4'
ds2 = xr.open_dataset(f2)
ds2 = ds2.interp(lat = lat,lon = lon,method='nearest')

S = ds2.SWdown_f_tavg.data[0,...]
L = ds2.LWdown_f_tavg.data[0,...]
R1 = ds2.Rainf_tavg.data[0,...]
R2 = ds2.Snowf_tavg.data[0,...]
R = R1+R2
T = ds2.Tair_f_inst.data[0,...]
Q = ds2.Qair_f_inst.data[0,...]
P = ds2.Psurf_f_inst.data[0,...]
U = ds2.Wind_f_inst.data[0,...]
V = ds2.Wind_f_inst.data[0,...]
WEASD = ds2.SWE_inst.data[0,...]
CANWAT = ds2.CanopInt_inst.data[0,...]
SKINTEMP = ds2.AvgSurfT_inst.data[0,...]
SMOIS_1 = ds2.SoilMoi0_10cm_inst.data[0,...]*1e-3/0.1
SMOIS_2 = ds2.SoilMoi10_40cm_inst.data[0,...]*1e-3/0.3
SMOIS_3 = ds2.SoilMoi40_100cm_inst.data[0,...]*1e-3/0.6
SMOIS_4 = ds2.SoilMoi100_200cm_inst.data[0,...]*1e-3/1.0
STEMP_1 = ds2.SoilTMP0_10cm_inst.data[0,...]
STEMP_2 = ds2.SoilTMP10_40cm_inst.data[0,...]
STEMP_3 = ds2.SoilTMP40_100cm_inst.data[0,...]
STEMP_4 = ds2.SoilTMP100_200cm_inst.data[0,...]
VEGFRA = ds1.VEGFRA.data[0,...]

WEASD[np.isnan(WEASD)]=0
S[S<0.]=0.
WEASD[WEASD<0.]=0.
CANWAT[CANWAT<0.]=0.
SMOIS_1[SMOIS_1>0.45]=0.45
SMOIS_2[SMOIS_2>0.45]=0.45
SMOIS_3[SMOIS_3>0.45]=0.45
SMOIS_4[SMOIS_4>0.45]=0.45

p1 = xr.Dataset(data_vars={
'Times':(['Time'], np.array([b'2022-01-01_01:00:00'], dtype='|S19') ),
'T2D': (['Time', 'south_north', 'west_east'], T[np.newaxis,...]),
'Q2D': (['Time', 'south_north', 'west_east'], Q[np.newaxis,...]),
'U2D': (['Time', 'south_north', 'west_east'], U[np.newaxis,...]),
'V2D': (['Time', 'south_north', 'west_east'], np.zeros(U.shape)[np.newaxis,...]),
'PSFC': (['Time', 'south_north', 'west_east'], P[np.newaxis,...]),
'RAINRATE': (['Time', 'south_north', 'west_east'], R[np.newaxis,...]),
'SWDOWN': (['Time', 'south_north', 'west_east'], S[np.newaxis,...]),
'LWDOWN': (['Time', 'south_north', 'west_east'],L[np.newaxis,...]),

'SMOIS_1': (['Time', 'south_north', 'west_east'], SMOIS_1[np.newaxis,...]),
'SMOIS_2': (['Time', 'south_north', 'west_east'], SMOIS_2[np.newaxis,...]),
'SMOIS_3': (['Time', 'south_north', 'west_east'], SMOIS_3[np.newaxis,...]),
'SMOIS_4': (['Time', 'south_north', 'west_east'], SMOIS_4[np.newaxis,...]),
'STEMP_1': (['Time', 'south_north', 'west_east'], STEMP_1[np.newaxis,...]),
'STEMP_2': (['Time', 'south_north', 'west_east'], STEMP_2[np.newaxis,...]),
'STEMP_3': (['Time', 'south_north', 'west_east'], STEMP_3[np.newaxis,...]),
'STEMP_4': (['Time', 'south_north', 'west_east'], STEMP_4[np.newaxis,...]),

'WEASD': (['Time', 'south_north', 'west_east'], WEASD[np.newaxis,...]),
'CANWAT': (['Time', 'south_north', 'west_east'], CANWAT[np.newaxis,...]),
'SKINTEMP': (['Time', 'south_north', 'west_east'], SKINTEMP[np.newaxis,...]),

'VEGFRA': (['Time', 'south_north', 'west_east'], ds1.VEGFRA.data),
'GVFMIN': (['Time', 'south_north', 'west_east'], ds1.SHDMIN.data),
'GVFMAX': (['Time', 'south_north', 'west_east'], ds1.SHDMAX.data),
'LAI': (['Time', 'south_north', 'west_east'], ds1.LAI.data),
},
)

p1 = p1.assign_attrs(TITLE="OUTPUT FROM CONSOLIDATE_GRIB v20150518",missing_value=-1.e+36,_FillValue=-1.e+36,\
                     DX=30000.0,DY=30000.0,\
                        TRUELAT1=40.0,TRUELAT2=-999.9,LA1=35.0,LO1=115.0,STAND_LON=-999.9,\
                          MAP_PROJ=3.,MMINLU='MODIFIED_IGBP_MODIS_NOAH')

p1.to_netcdf('/HRLDAS-v3.6/Run/indir/2010010100.LDASIN_DOMAIN1')
