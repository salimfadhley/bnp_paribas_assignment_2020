import io
import logging
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Iterator, TextIO

import pandas

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_empty_main_table() -> pandas.DataFrame:
    cols = [
        ("CorrelationID", str),
        ("NumberOfTrades", int),
        ("Limit", int),
        ("TradeID", str),
        ("Value", int),
    ]

    column_names, _ = zip(*cols)
    # This is an odd-looking hack, but actually the quickest way to get an empty data-frame with
    # correctly typed columns.
    return pandas.read_csv(io.StringIO(""), names=column_names, dtype=dict(cols))


@dataclass
class Trade:
    # Represents a single loaded trade.
    CorrelationID: str
    NumberOfTrades: str
    Limit: str
    TradeID: str
    Value: str

    def asdict(self):
        return {
            "CorrelationID": self.CorrelationID,
            "NumberOfTrades": int(self.NumberOfTrades),
            "Limit": int(self.Limit),
            "TradeID": self.TradeID,
            "Value": int(self.Value),
        }

    @classmethod
    def from_xml(cls, trade: ET.Element) -> "Trade":
        result = cls(Value=trade.text or "0", **trade.attrib)
        return result


def read_xml(stream: TextIO) -> Iterator[Trade]:
    tree = ET.parse(stream)
    root = tree.getroot()
    trades = root.findall("./Trade")

    for trade in trades:
        yield Trade.from_xml(trade)

    log.info(f"Loaded {len(trades)} trade records.")


def get_populated_table(data: Iterator[Trade]) -> pandas.DataFrame:
    table = get_empty_main_table()
    for trade in data:
        table = table.append(trade.asdict(), ignore_index=True)
    return table


def states_function(row):
    if row["NumberOfTrades"] < row["ExpectedNumberOfTrades"]:
        return "Pending"

    if row["Value"] > row["Limit"]:
        return "Rejected"

    return "Accepted"


def calculate_summary_table(trades_table: pandas.DataFrame) -> pandas.DataFrame:
    summary_table = trades_table.groupby("CorrelationID").agg(
        {"NumberOfTrades": "count", "Value": "sum", "Limit": "max"}
    )
    summary_table["ExpectedNumberOfTrades"] = trades_table.groupby("CorrelationID").agg(
        {"NumberOfTrades": "max"}
    )
    summary_table["State"] = pandas.Series(
        data=summary_table.apply(states_function, axis=1), dtype=str
    )
    return pandas.DataFrame(
        summary_table, columns=["ExpectedNumberOfTrades", "State"]
    ).rename(columns={"ExpectedNumberOfTrades": "NumberOfTrades"})


def run_trade_summary(input_file: TextIO, output_file: TextIO):
    summary = calculate_summary_table(get_populated_table(read_xml(input_file)))
    summary.to_csv(output_file, header=True)
