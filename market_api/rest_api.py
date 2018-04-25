import http.client
import json


class RestApi:
    @staticmethod
    def publicApiCall(baseEndPoint, apiPoint, methodName, http_timeout):
        conn = http.client.HTTPSConnection(baseEndPoint, timeout=http_timeout)
        conn.request('GET', apiPoint + methodName)
        response = conn.getresponse().read().decode()
        conn.close()
        return json.loads(response)
