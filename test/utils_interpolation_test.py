"""Tests utils_interpolation module
"""
import unittest
from os import remove
from os.path import exists

import utils_interpolation
from numpy import ones


class UtilsInterpolationTest(unittest.TestCase):

    data_dir = 'example_data/emilia_romagna/explanatory/'
    coast_line = data_dir + 'coast_line_shp/coast_line_25832.shp'
    dem_file = data_dir + 'dem_emilia_1km.tif'

    def test_calculate_dcoast(self):
        self.assertAlmostEqual(utils_interpolation.calculate_dcoast(1000),
                               0.029, 2)
        self.assertAlmostEqual(utils_interpolation.calculate_dcoast(10000),
                               0.259, 2)
        self.assertAlmostEqual(utils_interpolation.calculate_dcoast(100000),
                               0.950, 2)

    def test_get_dcoast_array(self):
        dcoast = utils_interpolation.get_dcoast_array(self.dem_file,
                                                      self.coast_line)

        self.assertAlmostEqual(dcoast[10, 10], 0.999, 2)
        self.assertAlmostEqual(dcoast[210, 210], 0.944, 2)
        self.assertAlmostEqual(dcoast[60, 300], 0.582, 2)
        self.assertAlmostEqual(dcoast[120, 120], 0.988, 2)

    def test_get_tif_from_array(self):
        test_file = 'test/save_file_test.tif'
        data = ones((10, 10))
        utils_interpolation.get_tif_from_array(test_file,
                                               data,
                                               [10, 1, 0, 0, 0, 1],
                                               25832)
        self.assertTrue(exists(test_file))

        remove(test_file)
