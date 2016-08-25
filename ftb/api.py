import requests


class FlexgetRequest(object):
    FLEXGET_BASE_URL = 'http://liiight.dlinkddns.com:7171/api/'
    FLEXGET_TOKEN = 'fed21b92a06a69b15fab1b534a94e8c638f010f5da3f4232c0fa4f20'

    def __init__(self, token, base_url):
        self.flexget_token = token
        self.base_url = base_url

    def _request(self, method, endpoint, **params):
        url = FlexgetRequest.FLEXGET_BASE_URL + endpoint
        headers = {'Authorization': 'Token {}'.format(FlexgetRequest.FLEXGET_TOKEN)}
        data = params.pop('data', None)

        result = requests.request(method, url, params=params, headers=headers, json=data)
        result.raise_for_status()
        result = result.json()

        return result

    def get(self, endpoint, **params):
        return self._request('get', endpoint, **params)

    def post(self, endpoint, **params):
        return self._request('post', endpoint, **params)

    def put(self, endpoint, **params):
        return self._request('put', endpoint, **params)

    def delete(self, endpoint, **params):
        return self._request('delete', endpoint, **params)

    @staticmethod
    def get_token(base_url, username, password):
        login_url = base_url + '/auth/login/?remember=true'
        data = {'username': username, 'password': password}
        session = requests.session()
        response = session.get(login_url, json=data)
        response.raise_for_status()

        token_url = base_url + '/user/token/'
        token = session.get(token_url)
        token.raise_for_status()
        return token.json().get('token')

    @classmethod
    def verify_connection(cls, token, base_url):
        api = cls(token, base_url)
        response = api.get('/server/version/')
        return response.get('flexget_version') is not None
