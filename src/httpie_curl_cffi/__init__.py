from httpie.plugins import TransportPlugin
from requests.adapters import HTTPAdapter
from curl_cffi import requests as curl_requests

__version__ = "1.0.0a1"
__author__ = 'Xie Yanbo'
__licence__ = 'MIT'


class CurlCffiAdapter(HTTPAdapter):
    def send(self, request, **kwargs):
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

    def get_adapter(self):
        return CurlCffiAdapter()
