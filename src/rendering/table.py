"""This module contains classes that are in charge of rendering a table with a customized view."""


def get_whitespaces(whitespace_number):
    """It generates str with specified numbers of whitespace.

       Args:
           whitespace_number (int): whitespace numbers.

       Returns:
           str: string with numbers of whitespace specified in argument
    """
    whitespace = ""
    for i in range(whitespace_number):
        whitespace += " "
    return whitespace


class ALIGNMENT:
    """It is a container of alignment type.
    """
    def __init__(self):
        pass

    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"


class Alignment(object):
    """It adds alignment for content in each column.

    There are three types of alignment: left, right, center.

    Attributes:
        __alignment_columns (dict): a dict representing columns numbers and its alignment respectively.
        __default_alignment (ALIGNMENT): alignment that is applied if alignment in alignment_columns are not specified.
    """

    def __init__(self, alignment_columns={}, default_alignment=ALIGNMENT.LEFT):
        self.__alignment_columns = alignment_columns
        self.__default_alignment = default_alignment

    def make(self, column_index, item, max_len, table_rep):
        """It adds content of table to column with alignment.

        Args:
            column_index (int): index column for alignment.
            item (str): content of column.
            max_len (int): max len of content in the column.
            table_rep (str): processed table representation so far.

        Return:
            str: table_rep plus content of the column with alignment
        """
        alignment_type = self.__get_alignment_type(column_index)
        if alignment_type == ALIGNMENT.LEFT:
            item_len = len(item)
            whitespace_number = max_len - item_len
            return table_rep + item + get_whitespaces(whitespace_number)
        else:
            raise NotImplementedError

    def __get_alignment_type(self, column_index):
        alignment_column = self.__alignment_columns.get(column_index)
        if alignment_column is not None:
            return alignment_column
        else:
            return self.__default_alignment


class Padding(object):
    """It adds padding margin for content in each cell.

    Attributes:
        __padding_columns (dict): an dict representing columns numbers and its padding respectively.
        __default_padding (int): number of whitespace in padding margin if padding_columns are not specified.
    """

    def __init__(self, padding_columns, default_padding=2):
        self.__padding_columns = padding_columns
        self.__default_padding = default_padding

    def add_padding(self, column_index, table_rep):
        """It adds content of table to column with alignment.

        Args:
            column_index (int): index column for padding.
            table_rep (str): processed table representation so far.

        Returns:
            str: table_rep plus content of the column with alignment
        """
        return table_rep + get_whitespaces(self.__get_padding(column_index))

    def __get_padding(self, column_index):
        padding_column = self.__padding_columns.get(column_index)
        if padding_column is not None:
            return padding_column
        else:
            return self.__default_padding


class ResizableTable(object):
    """It builds a table whose view can be customized.

    Attributes:
        __padding_left (Padding): an object representing padding margin for columns from left side.
        __padding_right (Padding): an object representing padding margin for columns from right side.
        __alignment (ALIGNMENT): an object representing alignment of content for columns. There are three strategies: left, right, center.
        __header (list): an array of str representing names of columns
        __body (list): an array of str representing content of table
        __footer (list): an array of str representing last row in table
        __col_sep (list): a string representing a symbol for separating columns in table.
    """

    def __init__(self, padding_left, padding_right, alignment, header, body=[], footer=[], col_sep="|"):
        self.__padding_left = padding_left
        self.__padding_right = padding_right
        self.__alignment = alignment
        self.__header = header
        self.__body = body
        self.__footer = footer
        self.__col_sep = col_sep

    def get_table(self):
        """ It creates a string that represents a table built based on data provided in constructor.

            Returns:
                table (str): The string representing a table

            Raises:
                ValueError: if table data, namely header, body and footer are not the same size.
        """
        table = self.__form_table()
        if not self.__is_table(table):
            raise ValueError("Header, body and footer are not the same size.")

        max_len_in_columns = self.__get_max_len_in_columns(table)
        table_rep = ""
        for row_index, row in enumerate(table):
            for column_index, item in enumerate(row):
                table_rep = self.__add_column_separator(column_index, table_rep)
                table_rep = self.__padding_left.add_padding(column_index, table_rep)
                table_rep = self.__alignment.make(column_index, item, max_len_in_columns[column_index], table_rep)
                table_rep = self.__padding_right.add_padding(column_index, table_rep)
            table_rep = table_rep + "\n"
        return table_rep

    def __get_max_len_in_columns(self, table):
        max_len_content_cols = []
        for col in zip(*table):
            col_items_len = [len(col_item) for col_item in col]
            longest_content = max(col_items_len)
            max_len_content_cols.append(longest_content)
        return max_len_content_cols

    def __add_column_separator(self, column_index, table_rep):
        if column_index != 0:
            return table_rep + self.__col_sep
        else:
            return table_rep

    def __is_table(self, table):
        rows_size = {len(row) for row in table}
        return len(rows_size) == 1

    def __form_table(self):
        table = [self.__header]
        if len(self.__body) != 0:
            table.extend(self.__body)
        if len(self.__footer) != 0:
            table.append(self.__footer)
        return table
