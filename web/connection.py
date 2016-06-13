""" Generic connection objects """

import json
from requests import Request, Session
from urllib.parse import urlparse

class Connection(object):
    """
    docstring for Connection

    Things that the Connection should be able to do:
    - Establish a connection to a web resource
    - Test a connection to a web resource
    - make calls to a web resource
        - GET, PUT, POST, DELETE
    - Secure a connection to a web resource
    - Set the user agent for a request

    """

    def __init__(self, url, userAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'):
        super(Connection, self).__init__()

        # We want to test to make sure that there is both a scheme and a location
        parsedUrl = urlparse(url)

        if parsedUrl.scheme:
            self.scheme = parsedUrl.scheme
        else:
            raise URLFormatError('no scheme specified')

        if parsedUrl.netloc:
            self.location = parsedUrl.netloc
        else:
            raise URLFormatError('no location specified')

        # There doesn't have to be a path
        self.path = parsedUrl.path
        self.url = url

        self.userAgent = userAgent
        self.headers = {'User-Agent': userAgent}

        self.tempHeaders = {}
        self.tempData = {}

    def _genericRequest(self, type = "GET", _data = {}, _headers = {}, _path = ''):
        """
        A generic request to a web resource

        @param {string} type - The type of request being created
        @param {dictionary} _data - the data to be added to the request, if applicable
        @param {dictionary} _headers - the headers to be added to the request, if necessary
        @param {string} _path - Optional path argument, which whill replace self.path

        @return {response} response - a Requests response object
        """

        # Check to make sure the headers are a dict
        if isinstance(_headers, dict):
            # merge the headers into the already existing self.headers
            newHeaders = {**self.headers, **_headers}
            self.tempHeaders = newHeaders
        else: raise Exception('_header argument is not a dictionary')

        # Check to make sure the data passed in is formatted as a dict
        if isinstance(_data, dict):
            self.tempData = _data
        else: raise Exception('_data argument is not a dictionary')

        # Check to make sure the passed in path is a string
        # TODO make this more secure
        if _path:
            if isinstance(_path, str):
                self.path = _path
            else: raise Exception('_path must be a string value')

        s = Session()

        # Creating the request object
        #TODO make this more secure, make sure the path is valid
        fullUrl = self.scheme + '://' + self.location + self.path
        req = Request(type, fullUrl, data = _data, headers = newHeaders)
        preppedRequest = req.prepare()

        # preppedRequest.body = "Some string value"

        response = s.send(preppedRequest)

        return response

    def head(self, _path = '', _headers = {}):
        try:
            return self._genericRequest(type = "HEAD", _path = _path, _headers = _headers)
        except Exception:
            print('Head request failed')

    def get(self,  _path = '', _headers = {}):
        try:
            return self._genericRequest(type = "GET", _headers = _headers, _path = _path)
        except Exception:
            print('Get request failed')

    def put(self, _path = '', _headers = {}, _data = {}):
        pass

    def __clearTempData(self):
        self.tempData = {}
        self.tempHeaders = {}

class URLFormatError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)








if __name__ == "__main__":
    try:
        c = Connection("https://www.w3.org")
        print(c.scheme)
        print(c.location)
        print(c.path)
        print(c.url)
        # response = c._genericRequest(_path = '/standards/')
        # print(response.url)
        # print(response.headers)
        response = c.get('/standards/')
        print(response.url)
        print(response.headers)
    except URLFormatError as err:
        print("an error has ocurred:", err.value)
