"""Tests sfc_data module
"""
import unittest
from datetime import datetime
from emilia_romagna.emilia_radar_data import create_composite


class RadarDataTest(unittest.TestCase):

    date = datetime(2018, 2, 12, 14)
    data_dir = 'example_data/emilia_romagna/radar/'
    radar_files = [data_dir + 'itspc_20180212140000.h5',
                   data_dir + 'itgat_20180212140000.h5']
    config = {"radar_gain": 0.313725490196078,
              "radar_offset": -20,
              "radar_bounds": [489000, 4817000, 837000, 5047000],
              "radar_res": 1000,
              "radar_proj": "EPSG:25832",
              "radar_nodata": 255}

    def test_create_composite_badfile(self):
        with self.assertRaises(FileNotFoundError):
            create_composite([self.data_dir + 'not_found.tif'], self.config)

    def test_create_composite(self):
        composite = create_composite(self.radar_files, self.config)

        self.assertAlmostEqual(composite[40, 40], -20.00, 2)
        self.assertAlmostEqual(composite[115, 209], 34.27, 2)
        self.assertAlmostEqual(composite[144, 48], -20.00, 2)
        self.assertAlmostEqual(composite[5, 255], 8.86, 2)
