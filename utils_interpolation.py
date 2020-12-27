import numpy as np
from osgeo import gdal, ogr, osr
from pymica.pymica import PyMica
from os.path import basename


def apply_mica(data_file, config):
    """Calculates interpolation applying MICA system. More information
    on MICA and the required parameters at github.com/meteocat/pymica.

    Args:
        data_file (str): Path to file including data to interpolate.
        config (dict): Configuration dict including MICA required
                       parameters.

    Returns:
        Class: pymica class (.result for interpolated field)
    """
    field = PyMica(data_file=data_file,
                   variables_file=config['variables_files'],
                   data_format=config['data_format'],
                   residuals_int=config['residuals_int'])

    return field


def get_dcoast_array(dem_file, coast_line):
    """Calculates distance to coast array from a DEM file (.tif)
    and a coast line (.shp).

    Args:
        dem_file (str): Path to a .tif DEM file.
        coast_line (str): Path to a .shp file including a coast line.

    Returns:
        numpy.array: Distance to coast array.
    """
    dem = gdal.Open(dem_file)
    geotransform = dem.GetGeoTransform()
    x_size = dem.RasterXSize
    y_size = dem.RasterYSize
    proj = osr.SpatialReference(wkt=dem.GetProjection())

    d_s = ogr.Open(coast_line)
    lyr = d_s.GetLayerByName(basename(coast_line[:-4]))

    lyr.ResetReading()

    feat = next(iter(lyr))
    geom = feat.GetGeometryRef()

    proj_shp = geom.GetSpatialReference()

    transf = osr.CoordinateTransformation(proj, proj_shp)

    out_array = np.ones([y_size, x_size])

    for i in range(x_size):
        for j in range(y_size):
            xcoord = i * geotransform[1] + geotransform[0]
            ycoord = j * geotransform[5] + geotransform[3]
            transf_point = transf.TransformPoint(xcoord, ycoord)

            point = ogr.Geometry(ogr.wkbPoint)
            point.SetPoint_2D(0, transf_point[0], transf_point[1])

            dist = point.Distance(geom)

            out_array[j, i] = calculate_dcoast(dist)

    return out_array


def calculate_dcoast(dist):
    """Calculates distance to coast based on an exponential function. The
    influence of the sea decreases exponentially from the coast line to
    inland.

    Args:
        dist (float): Distance from a point to the coast line in metres.

    Returns:
        float: A value around 0 for point close to the sea and 1 from
                km inland.
    """
    return 1 - np.exp(-3 * dist / 100000)


def get_tif_from_array(file_path, data, geotransform, EPSG):
    """Reads an array and returns a .tif file.

    Args:
        file_path (str): Path where the .tif file will be saved.
        data (array): Data to be saved.
        geotransform (array): GeoTransform for the .tif file.
        EPSG (int): EPSG projection.

    Returns:
        str: Path of the saved .tif file.
    """
    driver = gdal.GetDriverByName('GTiff')
    ds_out = driver.Create(file_path, data.shape[1], data.shape[0], 1,
                           gdal.GDT_Float32)
    ds_out.GetRasterBand(1).WriteArray(data)
    ds_out.GetRasterBand(1).SetNoDataValue(-9999)
    ds_out.SetGeoTransform(geotransform)
    projection = osr.SpatialReference()
    projection.ImportFromEPSG(25832)
    ds_out.SetProjection(projection.ExportToWkt())

    ds_out = None

    return file_path
