from typing import io

import pkg_resources


def get_test_data_stream(filename: str) -> io.BinaryIO:
    return pkg_resources.resource_stream("test_tradestatus.test_data", filename)
