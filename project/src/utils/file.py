import configparser
import logging
from string import Template


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


class FileUtil(object):

    @staticmethod
    def read_to_string(path_to_file):
        file_content = ""
        try:
            with open(path_to_file) as file:
                file_content = file.read()
        except FileNotFoundError as e:
            logging.error("File was not found using file path {}. %s".format(path_to_file), e)
            return file_content
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
