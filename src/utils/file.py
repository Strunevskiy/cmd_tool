"""This is util module. It holds util classes that helps to interact with different types of files."""
import logging
from string import Template

from future.moves import configparser

logger = logging.getLogger()


class PropertyUtil(object):
    """It reads data from a cfg file.

    Attributes:
        __config (configparser): an object holding configparser.
    """

    def __init__(self):
        self.__config = configparser.ConfigParser()

    def get_entries(self, path_to_config, section):
        """It makes the bill from provided order object.

        Args:
            path_to_config (str): path to cnf file.
            section (str): section from which data should be read.

        Returns:
            dict: key-value data from cnf files from specified section.

        Raises:
            Exception: if data from file can not be read due to incorrect file path or specified section.
        """
        entries = {()}
        try:
            self.__config.read(path_to_config)
            entries = self.__config.items(section)
        except Exception as e:
            logger.exception(e)
            return entries
        else:
            return entries


class FileUtil(object):
    """It reads and writes data from/to file.

    """

    @staticmethod
    def read_to_string(path_to_file):
        """It reads data from file.

        Args:
            path_to_file (str): path to file to read from.

        Returns:
            str: content of file.
        """
        with open(path_to_file) as file:
            return file.read()

    @staticmethod
    def write(path_to_file, *args):
        """It writes data to file.

        Args:
            path_to_file (str): path to file to write to.
            args (*args): number of data that should be written to file.
        """
        with open(path_to_file, "w+") as file_to_write:
            for line in args:
                file_to_write.writelines(line)


class TemplateUtil(object):
    """It works with simple substitute template engine.
    """

    @staticmethod
    def process(path_to_template, data):
        """It returns result of merging data with template.

        Args:
            path_to_template (str): path to file to write to.
            data (dict): data that should be merged with template variables.

        Returns:
           str: string representing template populated by data.
        """
        src = FileUtil.read_to_string(path_to_template)
        template = Template(src)
        return template.substitute(data)
