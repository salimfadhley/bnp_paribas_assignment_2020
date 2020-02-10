import pandas as pd
from bnp_test.main import (
    calculate_summary_table,
    get_empty_main_table,
    get_populated_table,
    read_xml,
)
from test_bnp_test.test_data import get_test_data_stream


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

    print("\n\n\n")
    print(summary_table)
    print("\n\n")
