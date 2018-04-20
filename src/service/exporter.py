import abc
import logging

import six
from src.utils.table import Padding, ResizableTable, Alignment


@six.add_metaclass(abc.ABCMeta)
class Exporter:

    @abc.abstractmethod
    def export(self, data, total_sales, total_values):
        pass


class ConsoleExporter(Exporter):
    _log = logging.getLogger()

    _header_first_col = "Seller name"
    _header_second_col = "Number of sales"
    _header_third_col = "Total Values ($)"
    _footer_first_column = "Total:"

    def export(self, data, total_sales, total_values):
        header = [self._header_first_col, self._header_second_col, self._header_third_col]
        footer = [self._footer_first_column, str(total_sales), str(total_values)]

        padding_left = Padding({0: 0, 1: 5, 2: 5})
        padding_right = Padding({0: 5, 1: 5, 2: 5})
        table = ResizableTable(data, header, footer, padding_left, padding_right, Alignment())
        printed_table = table.print_table()
        print(printed_table)


class CSVExporter(Exporter):
    def __init__(self):
        pass

    def export(self, data, total_sales, total_values):
        raise NotImplementedError()
