import requests
from ftb.bot import config


class FlexgetRequest(object):
    FLEXGET_BASE_URL = config.get('base_url')
    FLEXGET_TOKEN = config.get('token') or get_token(FLEXGET_BASE_URL, config.get('username'), config.get('password'))

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

    @classmethod
    def verify_connection(cls, token, base_url):
        response = cls().get('/server/version/')
        return response.get('flexget_version') is not None


def get_token(base_url, username, password):
    login_url = base_url + '/auth/login/?remember=true'
    data = {'username': username, 'password': password}
    session = requests.session()
    response = session.post(login_url, json=data)
    response.raise_for_status()

    token_url = base_url + '/user/token/'
    token = session.get(token_url)
    token.raise_for_status()
    return token.json().get('token')
