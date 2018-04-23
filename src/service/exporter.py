"""This module contains classes that implements interface exporter."""

import abc
import logging

import six
from src.rendering.table import Padding, ResizableTable, Alignment

logger = logging.getLogger()


@six.add_metaclass(abc.ABCMeta)
class Exporter:

    @abc.abstractmethod
    def export(self, data, total_sales, total_values):
        pass


class ConsoleExporter(Exporter):
    """It exports sales figures in console.
    """
    HEADER_FIRST_COL = "Seller name"
    HEADER_SECOND_COL = "Number of sales"
    HEADER_THIRD_COL = "Total Values ($)"
    FOOTER_FIRST_COLUMN = "Total:"

    def export(self, data, total_sales, total_values):
        """It exports sales figures in console in table format.

        Args:
            data (list): list of sales figures done by all salesman.
            total_sales (int): numbers of sales.
            total_values (Decimal): values of total sales.
        """
        header = [self.HEADER_FIRST_COL, self.HEADER_SECOND_COL, self.HEADER_THIRD_COL]
        footer = [self.FOOTER_FIRST_COLUMN, str(total_sales), str(total_values)]

        padding_left = Padding({0: 0, 1: 5, 2: 5})
        padding_right = Padding({0: 5, 1: 5, 2: 5})
        table = ResizableTable(padding_left, padding_right, Alignment(), header, data, footer)
        printed_table = table.get_table()
        print(printed_table)


class CSVExporter(Exporter):
    """It exports sales figures in CSV.
    """

    def export(self, data, total_sales, total_values):
        """It exports sales figures in CSV.

        Args:
            data (list): list of sales figures done by all salesman.
            total_sales (int): numbers of sales.
            total_values (Decimal): values of total sales.

        Raises:
            NotImplementedError: if method is invoked. The method has not bee implemented yet.
        """
        raise NotImplementedError()
