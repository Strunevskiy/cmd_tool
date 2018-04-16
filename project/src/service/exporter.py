import abc
import logging
from decimal import Decimal

from project.src.utils.table import ResizableTable, Padding, Alignment


class Exporter(abc.ABC):

    @abc.abstractmethod
    def export(self, records):
        pass


class ConsoleExporter(Exporter):
    _log = logging.getLogger()

    _header_first_col = "Seller name"
    _header_second_col = "Number of sales"
    _header_third_col = "Total Values ($)"
    _footer_first_column = "Total:"

    def export(self, records):
        total_sales = 0
        total_values = 0.0000
        body = []
        for record in records:
            sales_number = record.get_sales_number()
            sales_value = record.get_sales_value()
            total_sales += sales_number
            total_values = Decimal(total_values) + Decimal(sales_value)
            body.append([record.get_fullname(), str(sales_number), str(sales_value)])
        header = [self._header_first_col, self._header_second_col, self._header_third_col]
        footer = [self._footer_first_column, str(total_sales), str(total_values)]

        padding_left = Padding({0: 0, 1: 5, 2: 5})
        padding_right = Padding({0: 5, 1: 5, 2: 5})
        table = ResizableTable(body, header, footer, padding_left, padding_right, Alignment())
        printed_table = table.print_table()
        print(printed_table)


class CSVExporter(Exporter):

    def export(self, records):
        pass
