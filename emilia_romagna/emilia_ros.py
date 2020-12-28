import json
from datetime import datetime

from pypros.ros_methods import calculate_koistinen_saltikoff
from utils_interpolation import apply_mica

from emilia_stations_data import dict_to_file, extract_variable


if __name__ == '__main__':

    print('Step 1/ : Loading configuration file')
    with open('emilia_romagna/emilia_config.json', 'r') as f:
        config = json.load(f)
        f.close()

    date = datetime(2018, 2, 12, 14)

    print('Step 2/ : Getting air temperature data')
    ta_data = extract_variable(config['data_file'], config['metadata_file'],
                               date, 'B12101')
    print('Step 3/ : Interpolating air temperature data')
    ta_field = apply_mica(dict_to_file('example_data/emilia_romagna/'
                          'stations/ta_data.json', ta_data), config)

    print('Step 4/ : Getting dew point temperature data')
    td_data = extract_variable(config['data_file'], config['metadata_file'],
                               date, 'td')
    print('Step 5/ : Interpolating dew point temperature data')
    td_field = apply_mica(dict_to_file('example_data/emilia_romagna/'
                          'stations/td_data.json', td_data), config)

    print('Step 6/ : Calculating precipitation phase')
    ros = calculate_koistinen_saltikoff(ta_field.result, td_field.result)
