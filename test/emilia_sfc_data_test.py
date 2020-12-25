"""Tests sfc_data module
"""
import unittest
from datetime import datetime

from emilia_romagna.emilia_sfc_data import extract_variable


class SfcDataTest(unittest.TestCase):

    date = datetime(2018, 2, 12)
    data_dir = 'example_data/emilia-romagna/sfc_observations/'
    data_file = data_dir + 'meteo-2018-02.json'
    metadata_file = data_dir + 'metadata_sfc_emilia.json'
    bad_file = data_dir + 'meteo-2018-03.json'

    def test_extract_variable_badfile(self):
        with self.assertRaises(FileNotFoundError):
            extract_variable(self.bad_file, self.metadata_file, self.date,
                             'B12101')

    def test_extract_variable_badmetadata(self):
        with self.assertRaises(FileNotFoundError):
            extract_variable(self.data_file, self.bad_file, self.date,
                             'B12101')

    def test_extract_variable(self):
        data = extract_variable(self.data_file, self.metadata_file, self.date,
                                'B12101')
        self.assertEqual(data[0]['date'], '2018-02-12T00:00:00Z')
        self.assertEqual(data[0]['id'], 'Piacenza urbana')
        self.assertEqual(data[0]['xcoord'], 553515.377911354)
