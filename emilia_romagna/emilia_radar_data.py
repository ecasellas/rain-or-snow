from os import remove
from os.path import exists

import numpy as np
from osgeo import gdal


def create_composite(radar_files, config):
    options = gdal.WarpOptions(dstSRS=config['radar_proj'],
                               dstNodata=config['radar_nodata'],
                               outputBounds=config['radar_bounds'],
                               xRes=config['radar_res'],
                               yRes=config['radar_res'])
    composite_array = []
    for radar_file in radar_files:
        if exists(radar_file) is False:
            raise FileNotFoundError('{} is not found.'.format(radar_file))
        f = radar_file[:-4] + '_ext.tif'
        gdal.Warp(f, radar_file, options=options)
        radar_array = gdal.Open(f).ReadAsArray().astype(float)
        radar_array[radar_array == 255] = np.nan
        composite_array.append(radar_array * config['radar_gain']
                               + config['radar_offset'])
        remove(f)

    composite_array = np.nanmax(composite_array, axis=0)

    return composite_array
