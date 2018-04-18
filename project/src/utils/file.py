import configparser
import csv
import logging
from string import Template


class PropertyUtil(object):
    _log = logging.getLogger()

    def __init__(self):
        self._config = configparser.ConfigParser()

    def get_entries(self, file_name, section):
        entries = {()}
        try:
            self._config.read(file_name)
            entries = self._config.items(section)
        except Exception as e:
            self._log.exception(e)
            return entries
        else:
            return entries


class FileUtil(object):

    @staticmethod
    def read_to_string(path_to_file):
        try:
            with open(path_to_file) as file:
                file_content = file.read()
        except FileNotFoundError as e:
            raise e
        else:
            return file_content

    @staticmethod
    def write(path_to_file, src=None, *args):
        try:
            with open(path_to_file, "w+") as file_to_write:
                if src is not None:
                    file_to_write.write(src)
                for line in args:
                    file_to_write.writelines(line)
        except Exception as e:
            raise e


class TemplateUtil(object):

    @staticmethod
    def process_template(path_to_template, tmp_data: {}):
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
