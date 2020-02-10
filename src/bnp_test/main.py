import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import IO, Iterator

import pandas


@dataclass
class Trade:
    correlation_id: str
    number_of_trades: int
    limit: int
    trade_id: str
    value: int

    @classmethod
    def from_xml(cls, trade: ET.Element) -> "Trade":
        return cls(
            correlation_id=trade.attrib["CorrelationId"],
            number_of_trades=int(trade.attrib["NumberOfTrades"]),
            limit=int(trade.attrib["Limit"]),
            trade_id=trade.attrib["TradeID"],
            value=int(trade.text),
        )


def read_xml(stream: IO[str]) -> Iterator[Trade]:
    tree = ET.parse(stream)
    root = tree.getroot()
    trades = root.findall("./Trade")

    for trade in trades:
        yield Trade.from_xml(trade)
