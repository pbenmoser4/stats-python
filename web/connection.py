""" Generic connection objects """

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
    # def __init__(self, base_uri, path, userAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'):
    #     super(Connection, self).__init__()
    #     self.base_uri = base_uri
    #     self.path = path
    #     self.userAgent = userAgent
    #     self.headers = {'User-Agent': userAgent}

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

    def __genericRequest(self, type = "GET", _data = {}, _headers = {}):
        """
        A generic request to a web resource

        @param {string} type - The type of request being created
        @param {dictionary} _data - the data to be added to the request, if applicable
        @param {dictionary} _headers - the headers to be added to the request, if necessary
        """

        # merge the headers into the already existing self.headers
        # TODO make sure that _headers is a dictionary object
        newHeaders = {**self.headers, **_headers}

        s = Session()

        # Creating the request object
        req = Request(type, self.address, data = _data, headers = newHeaders)
        preppedRequest = req.prepare()

        # preppedRequest.body = "Some string value"

        resonse = s.send(preppedRequest)

        return response

    def get():
        pass

    def __testConnection(self, type, _data, _headers):
        """
        Test the connection of self.address with self.headers

        @param {string} type - type of request, e.g. GET, POST, PUT, DELETE
        @param {dictionary} _data - data to be sent with request
        @param {dictionary} _headers - additional headers to send with request

        @return {int} statusCode - the status code of the request
        """
        pass

class URLFormatError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == "__main__":
    try:
        c = Connection("something")
        print(c.scheme)
        print(c.location)
        print(c.path)
        print(c.url)
    except URLFormatError as err:
        print("an error has ocurred:", err.value)
