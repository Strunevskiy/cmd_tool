import logging

import pymysql

from src.utils.file import PropertyUtil

logger = logging.getLogger()

path_to_config_file = "./../config/db.cfg"
live_section = "CONFIG_LIVE"


class DataSource(object):

    def __init__(self, config_section=live_section):
        self.__connection = None
        self.__section = config_section
        self.__conf_property = PropertyUtil().get_entries(path_to_config_file, self.__section)

    def get_connection(self):
        if self.__connection is None:
            config = {entity[0]: entity[1] for entity in self.__conf_property}
            try:
                self.__connection = pymysql.connect(host=config.get("host"), port=int(config.get("port")),
                                                    user=config.get("user"), passwd=config.get("passwd"),
                                                    database=config.get("database"), db=config.get("store"),
                                                    cursorclass=pymysql.cursors.DictCursor)
            except Exception as e:
                raise e
            else:
                return self.__connection
        else:
            return self.__connection

    def close(self):
        self.__connection.close()
        self.__connection = None

    def commit(self):
        if self.__connection is not None:
            self.__connection.commit()
        else:
            self.__log.error("commit was not done because connection is None")
