import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import netCDF4
import os
import imageio as iio

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
    os.makedirs(f'{filepath}/plots/{var}/gm', exist_ok=True)

""""
def plot_global_map(nc_data, var_name, time_index=-1, cmap='coolwarm'):
    data = nc_data.variables[var_name][time_index]
    lons = nc_data.variables['lon'][:]
    lats = nc_data.variables['lat'][:]
    
    fig = plt.figure(figsize=(12, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    ax.gridlines(draw_labels=True)

    mesh = ax.contourf(lons, lats, data, 60, transform=ccrs.PlateCarree(),
                       levels=np.linspace(190, 310, part),
                       cmap=cmap)
    plt.colorbar(mesh, orientation='horizontal', label=f'{var_name}')
    plt.title(f'Global Map: {var_name} at time index {time_index}')
    plt.show()
"""


def plot_global_map_mean(nc_data, var_name, cmap='coolwarm'):
    data = nc_data.variables[var_name][:].mean(axis=0)  # Mean over all time steps
    lons = nc_data.variables['lon'][:]
    lats = nc_data.variables['lat'][:]
    
    fig = plt.figure(figsize=(12, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    ax.gridlines(draw_labels=True)

    mesh = ax.contourf(lons, lats, data, 60, transform=ccrs.PlateCarree(),
                       levels=np.linspace(-230, 0, 100),
                       cmap=cmap)
    plt.colorbar(mesh, orientation='horizontal', label=f'{var_name}')
    plt.title(f'Global Map: {var_name} mean over all time steps')
    # plt.show()


def plot_global_map_mean(nc_data, var_name, co2_level, last_timepoints, vmin, vmax):
    data = nc_data.variables[var_name][:].mean(axis=0)
    lons = nc_data.variables['lon'][:]
    lats = nc_data.variables['lat'][:]

    fig = plt.figure(figsize=(12, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    ax.gridlines(draw_labels=True)
    
    mesh = ax.contourf(lons, lats, std_data, 60, transform=ccrs.PlateCarree(), 
                       levels=np.linspace(vmin, vmax, 100),
                       cmap='coolwarm', extend='both')
    plt.colorbar(mesh, orientation='horizontal', label=f'{var_name}')
    plt.title(f'Global Map: {var_name} mean over all time steps')
    plt.savefig(f'{filepath}plots/{var_name}/gm/{var_name}_{co2_level}_gm_map.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    #plt.show()
    print(f'Saved: {var_name}_{co2_level}_gm_map.png')

print('Generating Global maps...')

for var in list(Data_Monthly['280'].variables.keys()):
    if var not in ['lat', 'lon', 'time', 'ta', 'ua', 'va', 'hus', 'wap', 'spd','lev']:
        filenames = []
        # Calculate global min/max across all CO2 levels
        all_stds = []
        for co2_level in ['280', '350', '450', '650', '850', '1150']:
            std_data = np.ma.std(Data_Daily[co2_level].variables[var][-36000:], axis=0)
            all_stds.append(std_data)
        vmin = np.ma.min([np.ma.min(s) for s in all_stds])
        vmax = np.ma.max([np.ma.max(s) for s in all_stds])
        
        # Plot with consistent scale
        for co2_level in ['280', '350', '450', '650', '850', '1150']:
            plot_global_map_mean(Data_Daily[co2_level], var, co2_level, 36000, vmin, vmax)
            #filenames.append(f'{filepath}plots/{var}/gm/{var}_{co2_level}_gm_map.png')
            #iio.imwrite(f'{filepath}plots/{var}/gm/animation_{var}_gm_map.webp', [iio.imread(filename) for filename in filenames], duration=200, quality=95)
        #print(f'Saved: animation_{var}_gm_map.webp ')
print('Done!')