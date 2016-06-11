import pytest
from web.connection import Connection, URLFormatError

def test_something():
    assert "" == ""

def test_init_valid_url():
    connection = Connection("https://www.w3.org")
    assert connection.scheme == "https"
    assert connection.location == "www.w3.org"
    assert connection.url = "https://www.w3.org"

def test_init_no_scheme():
    with pytest.raises(URLFormatError) as errinfo:
        connection = Connection("www.w3.org")
    assert 'no scheme specified' in str(errinfo.value)

def test_init_no_location():
    with pytest.raises(URLFormatError) as errinfo:
        connection = Connection("https://")
    assert 'no location specified' in str(errinfo.value)

def test_init_path_parsing():
    connection = Connection("https://www.w3.org/some/path")
    assert connection.path == "/some/path"
