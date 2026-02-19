import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import netCDF4
import os

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

os.makedirs('pictures', exist_ok=True)
for var in list(Data_Monthly['280'].variables.keys()):
    os.makedirs(f'{filepath}/pictures/{var}/std', exist_ok=True)

# Variability - Standard Deviation Map

def plot_std_map(nc_data, var_name, co2_level, last_timepoints):
    data = nc_data.variables[var_name][-last_timepoints:]  # (time, lat, lon)
    std_data = np.ma.std(data, axis=0)

    lons = nc_data.variables['lon'][:]
    lats = nc_data.variables['lat'][:]

    fig = plt.figure(figsize=(12, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    mesh = ax.contourf(lons, lats, std_data, 60, transform=ccrs.PlateCarree(), 
                       levels=np.linspace(0, 30, 100),
                       cmap='plasma')
    plt.colorbar(mesh, orientation='horizontal', label='Standard Deviation')
    plt.title(f'{var_name} Variability (STD) at {co2_level} ppm CO₂')
    plt.savefig(f'{filepath}pictures/{var_name}/std/{var_name}_{co2_level}_std_map.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved: {var_name}_{co2_level}_std_map.png')

print('Generating STD maps...')
for var in list(Data_Monthly['280'].variables.keys()):
    if var not in ['lat', 'lon', 'time', 'ta', 'ua', 'va', 'hus', 'wap', 'spd','lev']:
        for co2_level in ['280', '350', '450', '650', '850', '1150']:
            plot_std_map(Data_Daily[co2_level], var, co2_level, 36000)
print('Done!')
