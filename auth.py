import time
import base64
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA

import logging
log = logging.getLogger(__name__)

ENCODING = 'utf-8'

def encode_str_to_base64(s):
    """
    :param s:
    :type s: str
    :return: base64 as string
    """
    return base64.b64encode(s.encode(ENCODING)).decode(ENCODING)


def build_auth(config):
    # Server reports back GMT time, but it seems to work without adjusting
    # local time from Sweden.
    timestamp = str(round(time.time() * 1000))
    encoded_username = encode_str_to_base64(config.username)
    encoded_timestamp = encode_str_to_base64(timestamp)
    encoded_password = encode_str_to_base64(config.password)
    session_key = encoded_username + ':' + encoded_password + ':' + \
                  encoded_timestamp
    with open('NEXTAPI_TEST_public.pem', 'r') as next_pub_key:
        rsa_key = RSA.import_key(next_pub_key.read())
    cipher_rsa = PKCS1_v1_5.new(rsa_key)
    encrypted_hash = cipher_rsa.encrypt(session_key.encode(ENCODING))
    hash = base64.b64encode(encrypted_hash).decode(ENCODING)
    return hash

def build_basic_auth(session_key):
    """
    From the nExt docs for logout:
    The session_id should be sent as both username and password.
    
    From wikipedia:
    The Authorization field is constructed as follows:

    The username and password are combined with a single colon.
    The resulting string is encoded into an octet sequence.
    The resulting string is encoded using a variant of Base64.
    The authorization method and a space i.e. "Basic " is then put before the 
    encoded string.

    :param session_key: 
    :return: basic auth value string 
    """
    basic_auth_user_pass_str = session_key + ':' + session_key
    basic_auth_base64 = encode_str_to_base64(basic_auth_user_pass_str)
    return 'Basic ' + basic_auth_base64