import io
import os
import yaml
import logging

log = logging.getLogger(__name__)

config = {}


class MissingData(Exception): pass


def load_config(base_path, config_file):
    config_file = os.path.join(base_path, config_file)
    log.debug('starting to parse config file %s', config_file)
    with io.open(config_file) as file:
        raw_config = yaml.load(file)
    validate_config(raw_config)
    global config
    log.debug('config file valid, continuing')
    config = raw_config


def validate_config(config):
    if not config.get('base_url'):
        raise MissingData('Missing base_url value in config file')
    if not (config.get('username') and config.get('password')) and not config.get('token'):
        raise MissingData('Missing credentials in config file')
