import io
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import IO, Iterator

import pandas


def get_empty_main_table() -> pandas.DataFrame:
    cols = [
        ("CorrelationID", str),
        ("NumberOfTrades", int),
        ("Limit", int),
        ("TradeID", str),
        ("Value", int),
    ]

    column_names, _ = zip(*cols)

    return pandas.read_csv(io.StringIO(""), names=column_names, dtype=dict(cols))


@dataclass
class Trade:
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
        return cls(Value=trade.text, **trade.attrib)


def read_xml(stream: IO[str]) -> Iterator[Trade]:
    tree = ET.parse(stream)
    root = tree.getroot()
    trades = root.findall("./Trade")

    for trade in trades:
        yield Trade.from_xml(trade)


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
    return pandas.DataFrame(summary_table, columns=["NumberOfTrades", "State"])
