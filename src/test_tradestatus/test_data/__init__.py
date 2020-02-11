from typing import IO

import pkg_resources


def get_test_data_stream(filename: str) -> IO[bytes]:
    return pkg_resources.resource_stream("test_tradestatus.test_data", filename)
