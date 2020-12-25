"""Script to deal with meteorological surface observations from ARPAE storico
json data files.
"""
import json
from datetime import datetime
from os.path import exists


def extract_variable(data_file, metadata_file, date, variable):
    """Gets specific instantaneous variable from ARPAE storico json data files.

    Args:
        data_file (json): File from ARPAE storico GoogleDrive.
        metadata_file (json): File including ARPAE stations metadata.
        date (datetime): Date and time of data to extract.
        variable (str): Variable to extract:
                           B12101 - air temperature
    """
    if exists(data_file) is False:
        raise FileNotFoundError('{} file is not found.'.format(data_file))
    if exists(metadata_file) is False:
        raise FileNotFoundError('{} file is not found.'.format(metadata_file))
    with open(metadata_file, 'r') as f:
        m_d = json.load(f)
        f.close()
    data = []
    with open(data_file, 'r') as f:
        for line in f:
            a = json.loads(line)
            if a['date'] == datetime.strftime(date, '%Y-%m-%dT%H:%M:%SZ'):
                for d in a['data']:
                    if 'timerange' in d.keys() and 'level' in d.keys():
                        if d['timerange'][0] == 254 and d['level'][1] == 2000:
                            if variable in d['vars'].keys():
                                value = d['vars'][variable]['v']
                                if value is not None:
                                    if variable == 'B12101':
                                        value = round(value - 273.16, 2)
                                    nome = a['data'][00]['vars']['B01019']['v']
                                    if nome in m_d.keys():
                                        data.append(
                                            {'id': nome,
                                             'date': a['date'],
                                             'xcoord': m_d[nome]['xcoord'],
                                             'ycoord': m_d[nome]['xcoord'],
                                             'altitude': m_d[nome]['altitude'],
                                             'dcoast': m_d[nome]['altitude'],
                                             'var': value})
    return data
