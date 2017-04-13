import configparser

from exceptions import ConfigurationNotFound

import logging
log = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = 'conf.ini'
DEFAULT_CONFIG_NAME = 'CONFIG'
DEFAULT_CONFIG = {DEFAULT_CONFIG_NAME:
                      {'username':'username',
                       'password':'password',
                       'service':'NEXTAPI',
                       'url':'api.test.nordnet.se',
                       'api_version':'2'
                       }
                  }


class Config():
    def __init__(self):
        self.parser = configparser.ConfigParser()
    def _set_field(self, field):
        try:
            setattr(self, field, self.parser[DEFAULT_CONFIG_NAME][field])
        except KeyError:
            log.error('Could not parse %s from config', field)
            raise

    def load(self, path=None):
        """
        Loads configuration from a file on the supplied path. If path is not 
        supplied, the default location will be tried first.
        :param path: 
        :return: 
        """
        if path is None:
            files_read = self.parser.read(DEFAULT_CONFIG_PATH)
            if not files_read:
                # if default config is not present then write it.
                self.parser.read_dict(DEFAULT_CONFIG)
                with open(DEFAULT_CONFIG_PATH, 'w') as configfile:
                    self.parser.write(configfile)
        else:
            files_read = self.parser.read(path)
            if not files_read:
                # if config on expected location is not present, throw error.
                error_message = 'Could not find exception at %s'
                log.error(error_message, path)
                raise ConfigurationNotFound(error_message % path)
        self._set_field('username')
        self._set_field('password')
        self._set_field('service')
        self._set_field('url')
        self._set_field('api_version')
