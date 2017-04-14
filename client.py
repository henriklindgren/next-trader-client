import time
import base64
import json
import requests
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA

from config import SERVICE

import logging
log = logging.getLogger(__name__)

AUTH = 'auth'

class NextClient():
    def __init__(self, username, password, url, service, api_version):
        self.username = username
        self.password = password
        self.url = 'https://' + url
        self.service = service
        self.api_version = api_version
        self.headers = {"Accept": "application/json"}
        self.time_of_last_communication = None
        """Keeps track of when we talked to the server the last time for 
        timeout purposes"""

    def build_timestamp(self, t):
        timestamp = int(round(t * 1000))
        timestamp = str(timestamp)
        return timestamp

    def is_next_up(self):
        try:
            r = requests.get(self.url + '/next/' + self.api_version + '/',
                             headers=self.headers)
            return r.status_code == 200
        except Exception:
            return False

    def encode_str_to_base64(self, s):
        """
        :param s:
        :type s: str
        :return: base64 as string
        """
        encoding = 'utf-8'
        return base64.b64encode(s.encode(encoding)).decode(encoding)

    def login(self, logout=False):
        """
        :param logout: if True then logging out. 
        """
        timestamp = self.build_timestamp(time.time())
        encoded_username = self.encode_str_to_base64(self.username)
        encoded_timestamp = self.encode_str_to_base64(timestamp)
        encoded_password = self.encode_str_to_base64(self.password)
        session_key = encoded_username + ':' + encoded_password + ':' + \
                      encoded_timestamp
        with open('NEXTAPI_TEST_public.pem', 'r') as next_pub_key:
            rsa_key = RSA.import_key(next_pub_key.read())
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        encrypted_hash = cipher_rsa.encrypt(session_key.encode('utf-8'))
        hash = base64.b64encode(encrypted_hash)

        data = {SERVICE: self.service, AUTH: hash}
        if logout:
            r = requests.delete(self.url + '/next/' + self.api_version + '/' +
                                'login', data=data, headers=self.headers)
        else:
            r = requests.post(self.url + '/next/' + self.api_version + '/' +
                              'login', data=data, headers=self.headers)
        print(r.status_code, r.text)
        if r.status_code == 200:
            j = json.loads(r.text)
            print(json.dumps(j))
        elif r.status_code == 401:
            j = json.loads(r.text)
            raise Exception(j['code'] + ':'+ j['message'])
        else:
            raise Exception('login/logout failed')

    def logout(self):
        self.login(logout=True)
