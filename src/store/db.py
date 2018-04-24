import logging

import pymysql

from src.utils.file import PropertyUtil

logger = logging.getLogger()

path_to_config_file = "./../config/db.cfg"
live_section = "CONFIG_LIVE"


class DataSource(object):
    """It performs different operations over DB connection object.

    It initializes the connection and returns it.
    Apart from that it has responsibilities for closing connection and committing changes to DB.

    Attributes:
        __connection (Connection): connection to DB.
        __config_section (str): section of DB config
        __conf_property (dict): configuration data for creating DB connection
    """

    def __init__(self, config_section=live_section):
        self.__connection = None
        self.__config_section = config_section
        self.__conf_property = PropertyUtil().get_entries(path_to_config_file, self.__config_section)

    def get_connection(self):
        """It makes lazy initialization of DB connection and returns it.

        Returns:
            Connection: initialized connection to DB.

        Raises:
            Exception: if connect to DB can not be done mostly due to provided configuration data.
        """
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
        """It closes DB connection.
        """
        self.__connection.close()
        self.__connection = None

    def commit(self):
        """It commits changes to DB.
        """
        if self.__connection is not None:
            self.__connection.commit()
        else:
            self.__log.error("commit was not done because connection is None")
