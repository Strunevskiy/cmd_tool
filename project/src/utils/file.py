import configparser
import logging


class PropertyUtil(object):

    _log = logging.getLogger()

    def __init__(self):
        self._config = configparser.ConfigParser()

    def get_entries(self, file_name, section):
        self._config.read(file_name)

        entries = {()}
        try:
            entries = self._config.items(section)
        except Exception as e:
            self._log.error("Entries from property file were not extracted. %s", e)
            return entries
        else:
            return entries
