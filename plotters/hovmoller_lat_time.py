import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import netCDF4
import os
import imageio.v3 as iio

# Define file paths and load datasets
filepath = '/home/yasin-b/Dokumente/GitHub/PLASIM-Climate-Data-Analysis-Platform/'

Data_Monthly = {'280': netCDF4.Dataset(filepath + 'Data/Out_monthly_last70yrs_280.nc'),
                '350': netCDF4.Dataset(filepath + 'Data/Out_monthly_last70yrs_350.nc'),
                '450': netCDF4.Dataset(filepath + 'Data/Out_monthly_last70yrs_450.nc'),
                '650': netCDF4.Dataset(filepath + 'Data/Out_monthly_last70yrs_650.nc'),
                '850': netCDF4.Dataset(filepath + 'Data/Out_monthly_last70yrs_850.nc'),
                '1150': netCDF4.Dataset(filepath + 'Data/Out_monthly_last70yrs_1150.nc')}

Data_Daily = {'280': netCDF4.Dataset(filepath + 'Data/Out_daily_last10yrs_280.nc'),
              '350': netCDF4.Dataset(filepath + 'Data/Out_daily_last10yrs_350.nc'),
              '450': netCDF4.Dataset(filepath + 'Data/Out_daily_last10yrs_450.nc'),
              '650': netCDF4.Dataset(filepath + 'Data/Out_daily_last10yrs_650.nc'),
              '850': netCDF4.Dataset(filepath + 'Data/Out_daily_last10yrs_850.nc'),
              '1150': netCDF4.Dataset(filepath + 'Data/Out_daily_last10yrs_1150.nc')}

os.makedirs('plots', exist_ok=True)
for var in list(Data_Monthly['280'].variables.keys()):
    os.makedirs(f'{filepath}/plots/{var}/hov', exist_ok=True)

def zonal_mean(nc_data, var_name, last_timepoints):
    return np.ma.average(nc_data.variables[var_name][-last_timepoints:], axis=2)

def lat_time(nc_data, var_name, last_timepoints, vmin, vmax, co2_level):
    data = zonal_mean(nc_data, var_name, last_timepoints)
    lat = nc_data.variables['lat'][:]

    fig, ax = plt.subplots(figsize=(10, 5))
    levels = np.linspace(vmin, vmax, 100) if vmax > vmin else np.linspace(vmin - 1e-12, vmax + 1e-12, 100)
    mesh = ax.contourf(np.arange(data.shape[0]), lat, data.T,
                       levels=levels,
                       cmap='viridis',
                       extend='both')
    plt.xlabel('Time Step')
    plt.ylabel('Latitude')
    plt.title(f'Hovmöller Diagram: {var_name} (Zonal Mean) at {co2_level} ppm CO₂')
    fig.colorbar(mesh, ax=ax, label=var_name)
    plt.savefig(f'{filepath}plots/{var_name}/hov/{var_name}_{co2_level}_hov.png', dpi=150, bbox_inches='tight')
    print(f'Saved: {var_name}_{co2_level}_hov.png')
    plt.close(fig)

def lat_time_all():
    for var in list(Data_Monthly['280'].variables.keys()):
        if var not in ['lat', 'lon', 'time', 'ta', 'ua', 'va', 'hus', 'wap', 'spd','lev']:
            filenames = []

            all_means = []
            for co2_level in ['280', '350', '450', '650', '850', '1150']:
                zonal_mean_data = zonal_mean(Data_Daily[co2_level], var, 3600)
                all_means.append(zonal_mean_data)
            vmin = np.ma.min([np.ma.min(s) for s in all_means])
            vmax = np.ma.max([np.ma.max(s) for s in all_means])
            
            # Plot with consistent scale
            for co2_level in ['280', '350', '450', '650', '850', '1150']:
                lat_time(Data_Daily[co2_level], var, 3600, vmin, vmax, co2_level)
                filenames.append(f'{filepath}plots/{var}/hov/{var}_{co2_level}_hov.png')
                iio.imwrite(f'{filepath}plots/{var}/hov/animation_{var}_hov.webp', [iio.imread(filename) for filename in filenames], duration=200, quality=95)
            print(f'Saved: animation_{var}_hov.webp ')
    print('Done!')