from branca import Branca
import os

def get_branca():
    secret_key = os.getenv('BRANCA_KEY').encode('utf-8').hex()
    return Branca(key=secret_key)

def encode_branca(data: str) -> str:
    branca = get_branca()
    return branca.encode(data)

def decode_branca(token: str) -> str:
    branca = get_branca()
    return branca.decode(token)