import requests
import logging
from ftb.config import parsed_config

log = logging.getLogger('flexget_api')


class FlexgetRequest(object):
    FLEXGET_BASE_URL = parsed_config.get('base_url')
    FLEXGET_TOKEN = parsed_config.get('token')

    def _request(self, method, endpoint, **kwargs):
        url = FlexgetRequest.FLEXGET_BASE_URL + endpoint
        if not FlexgetRequest.FLEXGET_TOKEN:
            FlexgetRequest.FLEXGET_TOKEN = get_token(parsed_config.get('username'), parsed_config.get('password'))
        data = kwargs.pop('data', None)
        params = kwargs.pop('params', None)
        headers = kwargs.pop('headers', {})
        headers.setdefault('Authorization', 'Token {}'.format(FlexgetRequest.FLEXGET_TOKEN))

        log.debug('received request for %s', url)
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
    def verify_connection(cls):
        response = cls().get('/server/version/')
        return response.get('flexget_version') is not None


def get_token(username, password, base_url=None):
    if not base_url:
        base_url = parsed_config.get('base_url')
    login_url = base_url + '/auth/login/?remember=true'
    data = {'username': username, 'password': password}
    session = requests.session()
    response = session.post(login_url, json=data)
    response.raise_for_status()

    token_url = base_url + '/user/token/'
    token = session.get(token_url)
    token.raise_for_status()
    return token.json().get('token')
