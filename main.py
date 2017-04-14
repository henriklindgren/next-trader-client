from client import NextClient
from config import NextConfig

if __name__ == '__main__':
    config = NextConfig()
    config.load()
    client = NextClient(username=config.username, password=config.password,
                        url=config.url, service=config.service,
                        api_version=config.api_version)
    client.login()
    client.logout()
