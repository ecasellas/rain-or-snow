import json
from datetime import datetime

from pypros.pros import PyPros
from utils_interpolation import apply_mica

from emilia_stations_data import dict_to_file, extract_variable
from emilia_radar_data import create_composite


if __name__ == '__main__':

    print('Step 1/9 : Loading configuration file')
    with open('emilia_romagna/emilia_config.json', 'r') as f:
        config = json.load(f)
        f.close()

    date = datetime(2018, 2, 12, 14)
    date_str = datetime.strftime(date, '%Y%m%d_%H%M')

    print('Step 2/9 : Getting air temperature data')
    ta_data = extract_variable(config['data_file'], config['metadata_file'],
                               date, 'B12101')
    print('Step 3/9 : Interpolating air temperature data')
    ta_field = apply_mica(dict_to_file('example_data/emilia_romagna/'
                          'stations/ta_data.json', ta_data), config)
    ta_field.save_file('out/emilia_romagna/ta_' + date_str + '.tif')

    print('Step 4/9 : Getting dew point temperature data')
    td_data = extract_variable(config['data_file'], config['metadata_file'],
                               date, 'td')
    print('Step 5/9 : Interpolating dew point temperature data')
    td_field = apply_mica(dict_to_file('example_data/emilia_romagna/'
                          'stations/td_data.json', td_data), config)
    td_field.save_file('out/emilia_romagna/td_' + date_str + '.tif')

    print('Step 6/9 : Getting radar field')
    radar_date = datetime.strftime(date, '%Y%m%d%H%M%S')
    radar_files = [config['radar_dir'] + 'itgat_' + radar_date + '.h5',
                   config['radar_dir'] + 'itspc_' + radar_date + '.h5']

    print('Step 7/9 : Creating radar composite')
    radar_composite = create_composite(radar_files, config)

    print('Step 8/9 : Calculating precipitation phase')
    ros = PyPros(['out/emilia_romagna/ta_' + date_str + '.tif',
                  'out/emilia_romagna/td_' + date_str + '.tif'],
                 method='ks',
                 data_format={'vars_files': ['tair', 'tdew', 'dem']})

    print('Step 9/9 : Applying reflectivity mask')
    ros.save_file(ros.refl_mask(radar_composite),
                  'out/emilia_romagna/ros_' + date_str + '.tif')

    print('OK.')
