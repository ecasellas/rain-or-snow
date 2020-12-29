from datetime import datetime

import geopandas as gp
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal


def get_tif_array(tif_path):
    """Gets x and y coordinate arrays and data array from a
    .tif file.

    Args:
        tif_path (str): Path to a .tif file.

    Returns:
        tuple: (X coordinate, Y coordinate, data)
    """
    ds = gdal.Open(tif_path)
    data = ds.ReadAsArray()
    gt = ds.GetGeoTransform()

    xres = gt[1]
    yres = gt[5]

    xmin = gt[0] + xres * 0.5
    xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
    ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
    ymax = gt[3] - yres * 0.5

    xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

    return xx, yy, data


def plot_ros(ros_file, date, config_plot=None):
    """Generate a figure of a rain or snow field.

    Args:
        ros_file (str): Path to a .tif file including a ros field.
        date (datetime): Date of the data.
        config_plot (dict, optional): Parameters of the plot. Defaults to None.
    """
    if config_plot is not None:
        config = config_plot
    else:
        config = {}

    cmap = plt.cm.colors.ListedColormap(['#f9c3c6', '#f49d9e', '#e47070',
                                         '#e65050', '#c83c3c', '#c5fcbb',
                                         '#b3f8a9', '#78f573', '#50ee4e',
                                         '#3ade3e', '#b5f3fc', '#95cff6',
                                         '#4dafff', '#3c93f1', '#2881ed',
                                         '#2881ed'])

    cmap_ra = plt.cm.colors.ListedColormap(['#f9c3c6', '#f49d9e', '#e47070',
                                            '#e65050', '#c83c3c'])
    cmap_sl = plt.cm.colors.ListedColormap(['#c5fcbb', '#b3f8a9', '#78f573',
                                            '#50ee4e', '#3ade3e'])
    cmap_sn = plt.cm.colors.ListedColormap(['#b5f3fc', '#95cff6', '#4dafff',
                                            '#3c93f1', '#2881ed'])

    ros_x, ros_y, ros = get_tif_array(ros_file)
    ros[ros < 1] = np.nan
    levels = np.arange(1, 17, 1) - 0.5
    norm = plt.cm.colors.BoundaryNorm(levels, ncolors=15, clip=False)

    fig, ax = plt.subplots()

    if 'plt_dem_file' in config.keys():
        dem_x, dem_y, dem = get_tif_array(config['plt_dem_file'])
        ax.contourf(dem_x, dem_y, dem.T, cmap=plt.cm.get_cmap('Greys'),
                    alpha=0.7)

    ax.pcolormesh(ros_x, ros_y, ros.T, cmap=cmap, norm=norm, rasterized=True,
                  shading='auto')

    cbaxes = fig.add_axes([0.92, 0.60, 0.02, 0.18])
    cbaxes.tick_params(axis='both', which='both', labelsize=6)
    cb_ra = mpl.colorbar.ColorbarBase(cbaxes, cmap=cmap_ra)

    cbaxes = fig.add_axes([0.92, 0.40, 0.02, 0.18])
    cbaxes.tick_params(axis='both', which='both', labelsize=6)
    cb_sl = mpl.colorbar.ColorbarBase(cbaxes, cmap=cmap_sl)

    cbaxes = fig.add_axes([0.92, 0.20, 0.02, 0.18])
    cbaxes.tick_params(axis='both', which='both', labelsize=6)
    cb_sn = mpl.colorbar.ColorbarBase(cbaxes, cmap=cmap_sn)

    cb_ra.set_ticks(np.arange(0.2, 1, 0.2))
    cb_sl.set_ticks(np.arange(0.2, 1, 0.2))
    cb_sn.set_ticks(np.arange(0.2, 1, 0.2))
    cb_ra.set_ticklabels(['5', '10', '15', '25'])
    cb_sl.set_ticklabels(['5', '10', '15', '25'])
    cb_sn.set_ticklabels(['5', '10', '15', '25'])

    cb_ra.ax.set_ylabel('Rain (dBZ)', va='center', labelpad=10, size=6)
    cb_sl.ax.set_ylabel('Sleet (dBZ)', va='center', labelpad=10, size=6)
    cb_sn.ax.set_ylabel('Snow (dBZ)', va='center', labelpad=10, size=6)

    if 'plt_region_shp' in config.keys():
        region = gp.read_file(config['plt_region_shp'])
        region.plot(ax=ax, facecolor='None', edgecolor='black', linewidth=0.8)

    if 'plt_bounds' in config.keys():
        b = config['plt_bounds']
        ax.set_xlim(b[0], b[2])
        ax.set_ylim(b[1], b[3])

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    if 'plt_title' in config.keys():
        ax.set_title(config['plt_title']
                     .format(date=datetime.strftime(date,
                                                    '%Y-%m-%d %H:%M UTC')),
                     size=6, loc='left')
    date_str = datetime.strftime(date, '%Y%m%d_%H%M')

    plt.figtext(0.80, 0.16, '@enricasellas', ha='left', fontsize=6,
                color='black', alpha=0.8)

    if 'plt_data_institution' in config.keys():
        plt.figtext(0.13, 0.16, config['plt_data_institution'],
                    fontsize=6)

    if 'plt_out_file' in config.keys():
        plt.savefig(config['plt_out_file'].format(date=date_str),
                    bbox_inches='tight', dpi=300)
    else:
        plt.savefig('/tmp/ros_{}.png'.format(date_str),
                    bbox_inches='tight', dpi=300)
    plt.close('all')
