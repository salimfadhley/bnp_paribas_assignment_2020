from bnp_test.main import read_xml
from test_bnp_test.test_data import get_test_data_stream


def test_read_xml_0():
    result = list(read_xml(get_test_data_stream("input.xml")))
    assert len(result) == 5
    first_result = result[0]

    assert first_result.correlation_id == "234"
    assert first_result.number_of_trades == 3
    assert first_result.limit == 1000
    assert first_result.trade_id == "654"
    assert first_result.value == 100
