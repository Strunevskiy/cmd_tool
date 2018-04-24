import csv
import logging
from string import Template

from future.moves import configparser

logger = logging.getLogger()


class PropertyUtil(object):

    def __init__(self):
        self.__config = configparser.ConfigParser()

    def get_entries(self, file_name, section):
        entries = {()}
        try:
            self.__config.read(file_name)
            entries = self.__config.items(section)
        except Exception as e:
            logger.exception(e)
            return entries
        else:
            return entries


class FileUtil(object):

    @staticmethod
    def read_to_string(path_to_file):
        try:
            with open(path_to_file) as file:
                file_content = file.read()
        except Exception as e:
            raise e
        else:
            return file_content

    @staticmethod
    def write(path_to_file, *args):
        try:
            with open(path_to_file, "w+") as file_to_write:
                for line in args:
                    file_to_write.writelines(line)
        except Exception as e:
            raise e


class TemplateUtil(object):

    @staticmethod
    def process(path_to_template, tmp_data):
        src = FileUtil.read_to_string(path_to_template)
        template = Template(src)
        return template.substitute(tmp_data)


class CSVUtil(object):

    @staticmethod
    def write(path_to_csv_file, header, data, delimiter=','):
        try:
            with open(path_to_csv_file, "w+") as file_to_write:
                csv_writer = csv.writer(file_to_write, fildenames=header, delimiter=delimiter)
                csv_writer.writeheader()
                for line in data:
                    csv_writer.writerow(line)
        except Exception as e:
            raise e
