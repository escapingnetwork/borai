"""Tests  for etl.utils.preprocesser"""

import pytest

from  etl.utils.preprocesser import transform_date, chop


def test_transform_date():
    test_date = "31/1/1991"

    assert transform_date(test_date) == "1991-01-31"

def test_chop_length():
    pass

def test_chop_type():
    pass
