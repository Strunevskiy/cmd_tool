import logging

import pymysql

from project.src.utils.file import PropertyUtil


class DataSource(object):
    _log = logging.getLogger()

    _path_to_config_file = "./config/db.properties"
    _config_section = "CONFIG"

    def __init__(self):
        self._connection = None
        self._conf_property = PropertyUtil().get_entries(self._path_to_config_file, self._config_section)

    def get_connection(self):
        if self._connection is None:
            config = {entity[0]: entity[1] for entity in self._conf_property}
            try:
                self._connection = pymysql.connect(host=config.get("host"), port=int(config.get("port")),
                                                   user=config.get("user"), passwd=config.get("passwd"),
                                                   database=config.get("database"), db=config.get("store"))
            except Exception as e:
                self._log.error("{}".format(e))
                self.close()
            else:
                return self._connection
        else:
            return self._connection

    def close(self):
        self._connection.close()

    def commit(self):
        if self._connection is not None:
            self._connection.commit()
        else:
            self._log.error("commit was not done because connection is None")
