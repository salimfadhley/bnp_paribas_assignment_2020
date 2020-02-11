import numpy as np
import pandas
from test_tradestatus.test_data import get_test_data_stream
from tradestatus.model import (
    calculate_summary_table,
    get_empty_main_table,
    get_populated_table,
    read_xml,
)


def test_read_xml_0():
    result = list(read_xml(get_test_data_stream("input.xml")))
    assert len(result) == 5
    first_result = result[0]

    assert first_result.CorrelationID == "234"
    assert first_result.NumberOfTrades == "3"
    assert first_result.Limit == "1000"
    assert first_result.TradeID == "654"
    assert first_result.Value == "100"


def test_get_dataframe_from_xml():
    data = read_xml(get_test_data_stream("input.xml"))
    table = get_populated_table(data)
    assert len(table) == 5
    assert len(table.Limit.unique()) == 2


def test_calculate_summary_table():
    table = get_populated_table(read_xml(get_test_data_stream("input.xml")))
    summary_table = calculate_summary_table(table)
    assert len(summary_table) == 3


def test_get_blank_table():
    assert len(get_empty_main_table()) == 0


def test_column_types():
    df: pandas.DataFrame = get_empty_main_table()
    column_types = dict(zip(df.columns, df.dtypes))
    assert column_types["Limit"] == np.int64
    assert column_types["NumberOfTrades"] == np.int64
    assert column_types["Value"] == np.int64
