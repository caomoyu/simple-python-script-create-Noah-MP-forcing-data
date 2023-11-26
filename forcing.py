#forcing
import glob
import os
path = glob.glob('/data_download/GLDAS_NOAH025_3H.A2022*')
path_new = sorted(path, key = os.path.getctime)
for i in path_new:
    
    if os.path.exists('/HRLDAS-v3.6/Run/indir/'+i[80:88]+i[89:91]+'.LDASIN_DOMAIN1'):
        pass
    else:
        ds2 = xr.open_dataset(i)
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


        p1 = xr.Dataset(data_vars={
        'Times':(['Time'], np.array([b'2022-01-01_01:00:00'], dtype='|S19') ),
        'T2D': (['Time', 'south_north', 'west_east'], T[np.newaxis,...]),
        'Q2D': (['Time', 'south_north', 'west_east'], Q[np.newaxis,...]),
        'U2D': (['Time', 'south_north', 'west_east'], U[np.newaxis,...]),
        'V2D': (['Time', 'south_north', 'west_east'], np.zeros(U.shape)[np.newaxis,...]),
        'PSFC': (['Time', 'south_north', 'west_east'], P[np.newaxis,...]),
        'RAINRATE': (['Time', 'south_north', 'west_east'], R[np.newaxis,...]),
        'SWDOWN': (['Time', 'south_north', 'west_east'], S[np.newaxis,...]),
        'LWDOWN': (['Time', 'south_north', 'west_east'],L[np.newaxis,...])
        },
        )

        p1 = p1.assign_attrs(TITLE="OUTPUT FROM CONSOLIDATE_GRIB v20150518",missing_value=-1.e+36,_FillValue=-1.e+36,\
                            DX=30000.0,DY=30000.0,\
                                TRUELAT1=40.0,TRUELAT2=-999.9,LA1=35.0,LO1=115.0,STAND_LON=-999.9,\
                                MAP_PROJ=3.,MMINLU='MODIFIED_IGBP_MODIS_NOAH')
        p1.to_netcdf('/HRLDAS-v3.6/Run/indir/'+'2020'+i[84:88]+i[89:91]+'.LDASIN_DOMAIN1')



