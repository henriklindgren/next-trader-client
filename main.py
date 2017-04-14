from auth import build_auth, build_basic_auth
from config import NextConfig
from next_trader.next_trader import DefaultApi


def swagger(config):
    api = DefaultApi()
    auth = build_auth(config)
    # content type hack because of how swagger generates json-defaults for POST.
    api.api_client.default_headers = \
        {'Content-Type':'application/x-www-form-urlencoded'}
    login = api.login(auth=auth, service=config.service)
    print(repr(login))
    api.api_client.default_headers = {}
    basic_auth = build_basic_auth(login.session_key)
    login_status = api.logout(authorization=basic_auth)
    print(repr(login_status))

if __name__ == '__main__':
    config = NextConfig()
    config.load()
    swagger(config)

