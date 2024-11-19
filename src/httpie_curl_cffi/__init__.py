from httpie.plugins import TransportPlugin
from requests.adapters import HTTPAdapter
from curl_cffi import requests as curl_requests

__version__ = "1.0.0a0"
__author__ = 'Xie Yanbo'
__licence__ = 'MIT'


class CurlCffiAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        print('!!! curl cffi adapter')
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        print('!!! curl cffi send ...')
        # Convert requests.Request to curl_cffi.Request
        method = request.method
        url = request.url
        headers = dict(request.headers)
        data = request.body

        # Use curl_cffi to make the request
        response = curl_requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            impersonate='chrome',
            **kwargs
        )

        # Convert curl_cffi.Response to requests.Response
        response.connection = self
        return response


class CurlCffiTransportPlugin(TransportPlugin):
    name = 'curl_cffi transport'
    prefix = 'https://'  # Handle both http and https

    def init__(self, *args, **kwargs):
        print('!!! curl cffi plugin init')
        super().__init__(*args, **kwargs)

    def get_adapter(self):
        print('!!! curl cffi get_adapter')
        return CurlCffiAdapter()
