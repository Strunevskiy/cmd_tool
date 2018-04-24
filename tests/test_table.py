import pytest

from src.rendering.table import Alignment, get_whitespaces, ALIGNMENT


@pytest.mark.table
def test_get_whitespaces_method():
    exp_whitespace_str = "  "
    act_whitespace_str = get_whitespaces(2)
    assert exp_whitespace_str == act_whitespace_str


@pytest.mark.table
class TestAlignment(object):

    @pytest.mark.parametrize("alignment",
                             [Alignment(), Alignment(default_alignment=ALIGNMENT.LEFT), Alignment({1: ALIGNMENT.LEFT})])
    def test_def_left_alignment(self, alignment):
        column, content, column_max_len, table = self.__generate_test_data()
        act_alignment = alignment.make(column_index=column, item=content, max_len=column_max_len, table_rep=table)
        exp_alignment = table + content + get_whitespaces(column_max_len - len(content))
        assert exp_alignment == act_alignment

    @pytest.mark.parametrize("alignment",
                             [Alignment(default_alignment=ALIGNMENT.RIGHT), Alignment({1: ALIGNMENT.RIGHT})])
    def test_not_implemented_right_alignment(self, alignment):
        with pytest.raises(NotImplementedError):
            column, content, column_max_len, table = self.__generate_test_data()
            alignment.make(column_index=column, item=content, max_len=column_max_len, table_rep=table)

    @pytest.mark.parametrize("alignment",
                             [Alignment(default_alignment=ALIGNMENT.CENTER), Alignment({1: ALIGNMENT.CENTER})])
    def test_not_implemented_center_alignment(self, alignment):
        with pytest.raises(NotImplementedError):
            column, content, column_max_len, table = self.__generate_test_data()
            alignment.make(column_index=column, item=content, max_len=column_max_len, table_rep=table)

    @staticmethod
    def __generate_test_data():
        column = 1
        content = "content of column"
        column_max_len = len(content) * 2
        table = "_table_"
        return [column, content, column_max_len, table]
