import io
import os
import yaml
import logging

log = logging.getLogger(__name__)

CONFIG = None


class MissingData(Exception): pass


class Config(object):
    def __init__(self, config):
        self.username = config.get('username')
        self.password = config.get('password')
        self.base_url = config.get('base_url')
        self.flexget_token = config.get('flexget_token')


def load_config(base_path, config_file):
    config_file = os.path.join(base_path, config_file)
    log.debug('starting to parse config file %s', config_file)
    with io.open(config_file) as file:
        raw_config = yaml.load(file)
    validate_config(raw_config)
    global CONFIG
    log.debug('config file valid, continuing')
    CONFIG = Config(raw_config)


def get_config():
    return CONFIG


def validate_config(config):
    if not config.get('base_url'):
        raise MissingData('Missing base_url value in config file')
    if not (config.get('username') and config.get('password')) and not config.get('flexget_token'):
        raise MissingData('Missing credentials in config file')
