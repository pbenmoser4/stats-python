import json
from web.connection import Connection

if __name__ == "__main__":
    connection = Connection('http://www.httpbin.org')

    # print(connection.location)
    # print(connection.url)
    # print(connection.path)
    response = connection.get()
    # print(dir(response))
    print(response.text)
    print(response.headers)
    print(response.status_code)
    print(response.reason)
