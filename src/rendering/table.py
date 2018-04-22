import logging


def get_whitespaces(whitespace_number):
    whitespace = ""
    for i in range(whitespace_number):
        whitespace += " "
    return whitespace


class ALIGNMENT:
    def __init__(self):
        pass

    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"


class Alignment(object):

    def __init__(self, alignment_columns={}, default_alignment=ALIGNMENT.LEFT):
        self._alignment_columns = alignment_columns
        self._default_alignment = default_alignment

    def make(self, column_index, item, max_len, table_rep):
        alignment_type = self._get_alignment_type(column_index)
        if alignment_type == ALIGNMENT.LEFT:
            item_len = len(item)
            whitespace_number = max_len - item_len
            return table_rep + item + get_whitespaces(whitespace_number)
        else:
            raise NotImplementedError

    def _get_alignment_type(self, column_index):
        alignment_column = self._alignment_columns.get(column_index)
        if alignment_column is not None:
            return alignment_column
        else:
            return self._default_alignment


class Padding(object):

    def __init__(self, padding_columns, default_padding=2):
        self._padding_columns = padding_columns
        self._default_padding = default_padding

    def add_padding(self, column_index, table):
        return table + get_whitespaces(self._get_padding(column_index))

    def _get_padding(self, column_index):
        padding_column = self._padding_columns.get(column_index)
        if padding_column is not None:
            return padding_column
        else:
            return self._default_padding


class ResizableTable(object):
    _log = logging.getLogger()

    def __init__(self, padding_left, padding_right, alignment, header, body=[], footer=[], col_sep="|"):
        self._padding_left = padding_left
        self._padding_right = padding_right
        self._alignment = alignment
        self._header = header
        self._body = body
        self._footer = footer
        self._col_sep = col_sep

    def print_table(self):
        table = self._form_table()
        if not self._is_table(table):
            raise ValueError("Number of header columns does not match up with number of body columns.")

        max_len_in_columns = self._get_max_len_in_columns(table)
        table_rep = ""
        for row_index, row in enumerate(table):
            for column_index, item in enumerate(row):
                table_rep = self._add_column_separator(column_index, table_rep)
                table_rep = self._padding_left.add_padding(column_index, table_rep)
                table_rep = self._alignment.make(column_index, item, max_len_in_columns[column_index], table_rep)
                table_rep = self._padding_right.add_padding(column_index, table_rep)
            table_rep = table_rep + "\n"
        return table_rep

    def _get_max_len_in_columns(self, table):
        max_len_content_cols = []
        for col in zip(*table):
            col_items_len = [len(col_item) for col_item in col]
            longest_content = max(col_items_len)
            max_len_content_cols.append(longest_content)
        return max_len_content_cols

    def _add_column_separator(self, column_index, table_rep):
        if column_index != 0:
            return table_rep + self._col_sep
        else:
            return table_rep

    def _is_table(self, table):
        rows_size = {len(row) for row in table}
        return len(rows_size) == 1

    def _form_table(self):
        table = [self._header]
        if len(self._body) != 0:
            table.extend(self._body)
        if len(self._footer) != 0:
            table.append(self._footer)
        return table
