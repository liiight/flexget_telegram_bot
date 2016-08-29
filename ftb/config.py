import io
import os
import yaml

config = {}


class MissingData(Exception): pass


def load_config(base_path, config_file):
    config_file = os.path.join(base_path, config_file)
    with io.open(config_file) as file:
        raw_config = yaml.load(file)
    validate_config(raw_config)
    global config
    config = raw_config


def validate_config(config):
    if not config.get('base_url'):
        raise MissingData('Missing base_url value in config file')
    if not (config.get('username') and config.get('password')) and not config.get('token'):
        raise MissingData('Missing credentials in config file')
