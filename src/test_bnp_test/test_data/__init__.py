from typing import io

import pkg_resources


def get_test_data_stream(filename: str) -> io.TextIO:
    return pkg_resources.resource_stream("test_bnp_test.test_data", filename)
