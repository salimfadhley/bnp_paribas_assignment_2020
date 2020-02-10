import numpy as np
import pandas
from bnp_test.main import get_empty_main_table


def test_get_blank_table():
    assert len(get_empty_main_table()) == 0


def test_column_types():
    df: pandas.DataFrame = get_empty_main_table()
    column_types = dict(zip(df.columns, df.dtypes))
    assert column_types["Limit"] == np.int64
    assert column_types["NumberOfTrades"] == np.int64
    assert column_types["Value"] == np.int64
