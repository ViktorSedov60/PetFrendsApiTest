import pytest
from conftest import *


def test_get_api_key(get_api_keys):
    # result = get_api_keys()
    assert 'key' in get_api_keys