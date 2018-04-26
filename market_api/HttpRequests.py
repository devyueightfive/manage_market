import http.client
import json


class RestRequests:
    """Contains basic HTTP REST requests."""

    @staticmethod
    def publicRequest(toURIEndpoint: str, withApiPoint: str, withMethodName: str, withTimeLimit: int):
        """Represent public request to URI = "https://[fromURIEndpoint]/[withApiPoint]/[withMethodName]"
        (like 'api.binance.com/api/v1/trades') as Python object.
        The function returns JSON-like response from URI API as list and dictionary."""
        connectionWithURIEndpoint = http.client.HTTPSConnection(toURIEndpoint, timeout=withTimeLimit)
        connectionWithURIEndpoint.request('GET', '/' + withApiPoint + '/' + withMethodName)
        responseFromAPI = connectionWithURIEndpoint.getresponse().read().decode()
        connectionWithURIEndpoint.close()
        return json.loads(responseFromAPI)
