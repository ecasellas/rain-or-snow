"""Tests sfc_data module
"""
import unittest
from datetime import datetime

from emilia_romagna.emilia_sfc_data import extract_variable


class SfcDataTest(unittest.TestCase):

    date = datetime(2018, 2, 12)
    data_dir = 'example_data/emilia_romagna/sfc_observations/'
    data_file = data_dir + 'meteo-2018-02.json'
    metadata_file = data_dir + 'metadata_emilia.json'
    bad_file = data_dir + 'meteo-2018-03.json'

    def test_extract_variable_badfile(self):
        with self.assertRaises(FileNotFoundError):
            extract_variable(self.bad_file, self.metadata_file, self.date,
                             'B12101')

    def test_extract_variable_badmetadata(self):
        with self.assertRaises(FileNotFoundError):
            extract_variable(self.data_file, self.bad_file, self.date,
                             'B12101')

    def test_extract_variable_ta(self):
        data = extract_variable(self.data_file, self.metadata_file, self.date,
                                'B12101')
        self.assertEqual(data[0]['date'], '2018-02-12T00:00:00Z')
        self.assertEqual(data[0]['id'], 'Piacenza urbana')
        self.assertEqual(data[0]['lon'], 9.679647000000001)
        self.assertEqual(data[0]['lat'], 45.054924)
        self.assertEqual(data[0]['altitude'], 71.0)
        self.assertEqual(data[0]['dcoast'], 0.997882485170756)
        self.assertEqual(data[0]['var'], 5.89)

    def test_extract_variable_rh(self):
        data = extract_variable(self.data_file, self.metadata_file, self.date,
                                'B13003')
        self.assertEqual(data[0]['date'], '2018-02-12T00:00:00Z')
        self.assertEqual(data[0]['id'], 'Piacenza urbana')
        self.assertEqual(data[0]['lon'], 9.679647000000001)
        self.assertEqual(data[0]['lat'], 45.054924)
        self.assertEqual(data[0]['altitude'], 71.0)
        self.assertEqual(data[0]['dcoast'], 0.997882485170756)
        self.assertEqual(data[0]['var'], 68)

    def test_extract_variable_td(self):
        data = extract_variable(self.data_file, self.metadata_file, self.date,
                                'td')
        self.assertEqual(data[0]['date'], '2018-02-12T00:00:00Z')
        self.assertEqual(data[0]['id'], 'Piacenza urbana')
        self.assertEqual(data[0]['lon'], 9.679647000000001)
        self.assertEqual(data[0]['lat'], 45.054924)
        self.assertEqual(data[0]['altitude'], 71.0)
        self.assertEqual(data[0]['dcoast'], 0.997882485170756)
        self.assertEqual(data[0]['var'], 0.48137906228268296)
