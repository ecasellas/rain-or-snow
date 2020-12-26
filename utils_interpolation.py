from pymica.pymica import PyMica


def apply_mica(data_file, config):
    field = PyMica(data_file=data_file,
                   variables_file=config['variables_files'],
                   data_format=config['data_format'],
                   residuals_int=config['residuals_int'])

    return field
