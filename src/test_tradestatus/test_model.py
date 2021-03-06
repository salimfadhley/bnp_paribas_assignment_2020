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
    """Verify that we can read the XML and accurately retrieve a sequence of objects which represent trades.
    """
    result = list(read_xml(get_test_data_stream("input.xml")))
    assert len(result) == 5
    first_result = result[0]

    assert first_result.CorrelationID == "234"
    assert first_result.NumberOfTrades == "3"
    assert first_result.Limit == "1000"
    assert first_result.TradeID == "654"
    assert first_result.Value == "100"


def test_get_dataframe_from_xml():
    """Verify that we can gerate a dataframe from the XML elements.
    """
    data = read_xml(get_test_data_stream("input.xml"))
    table = get_populated_table(data)
    assert len(table) == 5
    assert len(table.Limit.unique()) == 2


def test_calculate_summary_table():
    """Verify that we calculate a summary table from the trades table.
    """
    table = get_populated_table(read_xml(get_test_data_stream("input.xml")))
    summary_table = calculate_summary_table(table)
    assert len(summary_table) == 3


def test_get_blank_table():
    """Verify that we can generate an empty trades table.
    """
    assert len(get_empty_main_table()) == 0


def test_column_types():
    """Verify that the trades table has appropriate column types.
    """
    df: pandas.DataFrame = get_empty_main_table()
    column_types = dict(zip(df.columns, df.dtypes))
    assert column_types["Limit"] in [np.int64, np.dtype('int32')]
    assert column_types["NumberOfTrades"] in [np.int64, np.dtype('int32')]
    assert column_types["Value"] in [np.int64, np.dtype('int32')]
