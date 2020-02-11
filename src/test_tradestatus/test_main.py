from io import StringIO

from test_tradestatus.test_data import get_test_data_stream
from tradestatus.model import run_trade_summary


def test_main_command():
    """This test validates the behaviuor of the command-line tool.

    Given a standard input, it should produce exactly the expected output.
    """
    input_stream = get_test_data_stream("input.xml")
    output_stream: StringIO = StringIO()
    expected_data: str = get_test_data_stream("output.csv").read().decode("utf-8")

    run_trade_summary(input_stream, output_stream)

    assert expected_data == output_stream.getvalue()
