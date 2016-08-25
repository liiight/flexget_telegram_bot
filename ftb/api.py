import requests


class FlexgetRequest(object):
    FLEXGET_BASE_URL = 'http://liiight.dlinkddns.com:7171/api/'
    FLEXGET_TOKEN = 'fed21b92a06a69b15fab1b534a94e8c638f010f5da3f4232c0fa4f20'

    def _request(self, method, endpoint, **params):
        url = FlexgetRequest.FLEXGET_BASE_URL + endpoint
        headers = {'Authorization': 'Token {}'.format(FlexgetRequest.FLEXGET_TOKEN)}
        data = params.pop('data', None)

        result = requests.request(method, url, params=params, headers=headers, json=data)
        result.raise_for_status()
        result = result.json()

        if result.get('errors'):
            raise LookupError('Error processing request on tvdb: %s' % result.get('errors'))

        return result

    def get(self, endpoint, **params):
        return self._request('get', endpoint, **params)

    def post(self, endpoint, **params):
        return self._request('post', endpoint, **params)

    def put(self, endpoint, **params):
        return self._request('put', endpoint, **params)

    def delete(self, endpoint, **params):
        return self._request('delete', endpoint, **params)
