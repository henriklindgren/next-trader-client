from auth import build_auth
from config import NextConfig
from next_trader.next_trader import DefaultApi, ApiClient

def print_me(s):
    print(s)

def swagger(config):
    api = DefaultApi(api_client=ApiClient(
        header_name='Content-Type',
        header_value='application/x-www-form-urlencoded'))
    auth = build_auth(config)
    api.login(auth=auth, service=config.service, callback=print_me)
    # api.logout() # throws error, might be because of content type quick fix.

if __name__ == '__main__':
    config = NextConfig()
    config.load()
    swagger(config)

