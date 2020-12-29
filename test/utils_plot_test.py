"""Tests utils_plot module
"""
import unittest
from os import remove
from os.path import exists
from datetime import datetime
from utils_plot import plot_ros


class UtilsPlotTest(unittest.TestCase):

    ros_file = 'out/emilia_romagna/ros_20180212_1400.tif'
    dem_file = 'example_data/emilia_romagna/explanatory/dem_emilia_1km.tif'
    date = datetime(2018, 2, 12, 14)
    config = {'plt_title': 'Emilia-Romagna - Precipitation phase - {date}',
              'plt_dem_file': dem_file,
              'plt_region_shp': 'example_data/emilia_romagna/explanatory/'
                                'region_shp/emilia_limiti_25832.shp',
              'plt_out_file': 'out/emilia_romagna/ros_{date}.png',
              'plt_data_institution': 'Radar and station data: ARPAE-SIMC'}

    def test_plot_ros_without_config(self):
        plot_ros(self.ros_file, self.date)
        self.assertTrue(exists('/tmp/ros_20180212_1400.png'))
        remove('/tmp/ros_20180212_1400.png')

    def test_plot_ros_with_config(self):
        if exists('out/emilia_romagna/ros_20180212_1400.png'):
            remove('out/emilia_romagna/ros_20180212_1400.png')
        plot_ros(self.ros_file, self.date, self.config)
        self.assertTrue(exists('out/emilia_romagna/ros_20180212_1400.png'))
