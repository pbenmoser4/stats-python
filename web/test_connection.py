import pytest
from requests import Request, Session, Response
from web.connection import Connection, URLFormatError

def test_init_valid_url():
    connection = Connection("https://www.w3.org")
    assert connection.scheme == "https"
    assert connection.location == "www.w3.org"
    assert connection.url == "https://www.w3.org"

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

"""
Testing _genericRequest method

Generic request testing should deal with requests to properly formatted endpoints,
because only properly formatted URLs can be used to initialize a Connection object.
Properly formatted URLs are defined as having (1) a scheme, and (2) a location.

We should be testing the following:
1. Non-dicitonary headers raise an Exception
2. Non-dictionary data raises an Exception
3. If a path is passed in, it must be a string
4. Properly formatted requests return a response object
"""

def test_generic_request_headers():
    connection = Connection("https://www.w3.org")

    response = connection._genericRequest(_headers = {'some': 'header'})
    assert connection.tempHeaders['some'] == 'header'

    with pytest.raises(Exception) as errinfo:
        response = connection._genericRequest(_headers = 'something')
    assert '_header argument is not a dictionary' in str(errinfo.value)

def test_generic_request_data():
    connection = Connection("https://www.w3.org")

    response = connection._genericRequest(_data = {'some' : 'data'})
    assert connection.tempData['some'] == 'data'

    with pytest.raises(Exception) as errinfo:
        response = connection._genericRequest(_data = 'bad data')
    assert '_data argument is not a dictionary' in str(errinfo.value)

def test_generic_request_path():
    connection = Connection("https://www.w3.org")

    response = connection._genericRequest(_path = '/standards/')
    assert response.url == "https://www.w3.org/standards/"

    with pytest.raises(Exception) as errinfo:
        response = connection._genericRequest(_path = {'some' : 'path'})
    assert '_path must be a string value' in str(errinfo.value)

def test_generic_request_response():
    # Testing that the data returned from a generic request is a requests.Response object
    connection = Connection("https://www.w3.org")
    response = connection._genericRequest()
    assert isinstance(response, Response)

"""
Testing get method

We've already tested validating data, headers, and path, so now we just have to test that the GET request is being processed correctly. We can use httpbin.org for this.
"""

def test_get_request():
    fullConnection = Connection("http://www.httpbin.org/get")
    fullResponse = fullConnection.get()
    assert fullResponse.url == "http://www.httpbin.org/get"

    connection = Connection("http://www.httpbin.org")
    response = connection.get("/get")
    assert response.url == "http://www.httpbin.org/get"
