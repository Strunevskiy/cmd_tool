"""Tests for dao db."""
import pytest


@pytest.mark.dao
class TestOrderDao(object):

    def test_bad_id_order(self):
        assert 1 == 1

    def test_bad_order(self):
        pass
